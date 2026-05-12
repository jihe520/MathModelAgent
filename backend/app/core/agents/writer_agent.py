"""写作手 Agent 模块，负责基于建模结果撰写学术论文。"""

from app.core.agents.agent import Agent
from app.core.llm.llm import LLM
from app.core.prompts import get_writer_prompt
from app.schemas.enums import CompTemplate, FormatOutPut
from app.tools.openalex_scholar import OpenAlexScholar
from app.utils.log_util import logger
from app.services.redis_manager import redis_manager
from app.schemas.response import SystemMessage, WriterMessage
import json
from app.core.functions import writer_tools
from icecream import ic  # type: ignore[import-unresolved]
from app.schemas.A2A import WriterResponse

# 写作手默认最大重试次数
DEFAULT_WRITER_MAX_RETRIES = 3


# TODO: 并行 parallel
# TODO: 获取当前文件下的文件
# TODO: 引用cites tool


class WriterAgent(Agent):
    """写作手 Agent，基于建模和代码执行结果撰写竞赛论文。"""
    def __init__(
        self,
        task_id: str,
        model: LLM,
        max_chat_turns: int | None = None,  # 最大对话轮次，None表示无限制
        comp_template: CompTemplate = CompTemplate.CHINA,
        format_output: FormatOutPut = FormatOutPut.Markdown,
        scholar: OpenAlexScholar | None = None,
        max_memory: int = 25,  # 添加最大记忆轮次
        max_retries: int = DEFAULT_WRITER_MAX_RETRIES,
    ) -> None:
        super().__init__(task_id, model, max_chat_turns, max_memory)
        self.format_out_put = format_output
        self.comp_template = comp_template
        self.scholar = scholar
        self.is_first_run = True
        self.system_prompt = get_writer_prompt(format_output)
        self.available_images: list[str] = []
        self.max_retries = max_retries

    async def run(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        prompt: str,
        available_images: list[str] | None = None,
        sub_title: str | None = None,
    ) -> WriterResponse:
        """执行写作任务，支持有限重试和软降级。

        Args:
            prompt: 写作提示。
            available_images: 可用的图片相对路径列表。
            sub_title: 子任务标题。

        Returns:
            WriterResponse 对象，最终失败时包含错误信息。
        """
        logger.info(f"subtitle是:{sub_title}")

        if self.is_first_run:
            self.is_first_run = False
            await self.append_chat_history(
                {"role": "system", "content": self.system_prompt}
            )

        if available_images:
            self.available_images = available_images
            image_lines = "\n".join(
                [f"- ![{img}]({img})" for img in available_images]
            )
            image_prompt = (
                f"\n\n【必须插入的图片列表】\n"
                f"以下图片是代码手生成的，你必须在论文相关段落后用 Markdown 格式逐一插入：\n"
                f"{image_lines}\n"
                f"插入格式为独占一行的 ![描述](文件名)，每张图片后需配3行以上的分析解读。\n"
            )
            logger.info(f"image_prompt是:{image_prompt}")
            prompt = prompt + image_prompt

        logger.info(f"{self.__class__.__name__}:开始:执行对话")
        self.current_chat_turns += 1

        await self.append_chat_history({"role": "user", "content": prompt})

        last_error: str = ""
        for attempt in range(self.max_retries + 1):
            try:
                # 获取历史消息用于本次对话
                response = await self.model.chat(
                    history=self.chat_history,
                    tools=writer_tools,
                    tool_choice="auto",
                    agent_name=self.__class__.__name__,
                    sub_title=sub_title,
                )

                footnotes = []
                response_content: str = ""

                if (
                    hasattr(response.choices[0].message, "tool_calls")
                    and response.choices[0].message.tool_calls
                ):
                    logger.info("检测到工具调用")
                    tool_call = response.choices[0].message.tool_calls[0]
                    tool_id = tool_call.id
                    if tool_call.function.name == "search_papers":
                        logger.info("调用工具: search_papers")
                        await redis_manager.publish_message(
                            self.task_id,
                            SystemMessage(content=f"写作手调用{tool_call.function.name}工具"),
                        )

                        query = json.loads(tool_call.function.arguments)["query"]

                        await redis_manager.publish_message(
                            self.task_id,
                            WriterMessage(
                                content=query,
                            ),
                        )

                        # 更新对话历史 - 添加助手的响应
                        await self.append_chat_history(response.choices[0].message.model_dump())
                        ic(response.choices[0].message.model_dump())

                        assert self.scholar is not None, "scholar 未初始化"
                        papers = await self.scholar.search_papers(query)

                        # TODO: pass to frontend
                        papers_str = self.scholar.papers_to_str(papers)
                        logger.info(f"搜索文献结果\n{papers_str}")
                        await self.append_chat_history(
                            {
                                "role": "tool",
                                "content": papers_str,
                                "tool_call_id": tool_id,
                                "name": "search_papers",
                            }
                        )
                        next_response = await self.model.chat(
                            history=self.chat_history,
                            tools=writer_tools,
                            tool_choice="auto",
                            agent_name=self.__class__.__name__,
                            sub_title=sub_title,
                        )
                        response_content = next_response.choices[0].message.content
                else:
                    response_content = response.choices[0].message.content
                self.chat_history.append({"role": "assistant", "content": response_content})
                logger.info(f"{self.__class__.__name__}:完成:执行对话")
                return WriterResponse(response_content=response_content, footnotes=footnotes)

            except Exception as e:
                last_error = str(e)
                logger.warning(
                    f"WriterAgent 执行失败 (尝试 {attempt + 1}/{self.max_retries + 1}): {last_error}"
                )
                if attempt < self.max_retries:
                    await redis_manager.publish_message(
                        self.task_id,
                        SystemMessage(
                            content=f"写作手执行出错，正在重试({attempt + 1}/{self.max_retries})...",
                            type="warning",
                        ),
                    )

        # 所有重试均失败，软降级返回错误信息
        error_msg = f"写作手超过最大重试次数({self.max_retries})，最后错误: {last_error}"
        logger.error(error_msg)
        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content=error_msg, type="error"),
        )
        return WriterResponse(response_content=error_msg, footnotes=[])

    async def summarize(self) -> str:
        """总结对话内容，生成任务执行摘要。"""
        try:
            await self.append_chat_history(
                {"role": "user", "content": "请简单总结以上完成什么任务取得什么结果:"}
            )
            # 获取历史消息用于本次对话
            response = await self.model.chat(
                history=self.chat_history, agent_name=self.__class__.__name__
            )
            await self.append_chat_history(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"总结生成失败: {str(e)}")
            # 返回一个基础总结，避免完全失败
            return "由于网络原因无法生成详细总结，但已完成主要任务处理。"
