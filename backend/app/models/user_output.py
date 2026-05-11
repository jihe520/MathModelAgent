"""用户输出管理模块，负责论文结果的拼接、引用处理和保存。"""

import os
import re
from app.utils.data_recorder import DataRecorder
from app.schemas.A2A import WriterResponse
import json
import uuid


class UserOutput:
    """管理建模任务的输出结果，处理引用编号、脚注和最终论文拼接。"""
    def __init__(
        self, work_dir: str, ques_count: int, data_recorder: DataRecorder | None = None
    ):
        self.work_dir = work_dir
        self.res: dict[str, dict] = {
            # "eda": {
            #     "response_content": "",
            #     "footnotes": "",
            # },
            # "ques1": {
            #     "response_content": "",
            #     "footnotes": "",
            # },
        }
        self.data_recorder = data_recorder
        self.cost_time = 0.0
        self.initialized = True
        self.ques_count: int = ques_count
        self.footnotes = {}
        self._init_seq()

    def _init_seq(self):
        # 动态顺序获取拼接res value，正确拼接顺序
        ques_str = [f"ques{i}" for i in range(1, self.ques_count + 1)]

        # 修改：调整章节顺序，确保符合论文结构
        self.seq = [
            "firstPage",  # 标题、摘要、关键词
            "RepeatQues",  # 一、问题重述
            "analysisQues",  # 二、问题分析
            "modelAssumption",  # 三、模型假设
            "symbol",  # 四、符号说明和数据预处理
            "eda",  # 四、数据预处理（EDA部分）
            *ques_str,  # 五、模型的建立与求解（问题1、2...）
            "sensitivity_analysis",  # 六、模型的分析与检验
            "judge",  # 七、模型的评价、改进与推广
        ]

    def set_res(self, key: str, writer_response: WriterResponse):
        """设置指定章节的写作结果。

        Args:
            key: 章节标识（如 eda、ques1）。
            writer_response: 写作手的响应对象。
        """
        self.res[key] = {
            "response_content": writer_response.response_content,
            "footnotes": writer_response.footnotes,
        }

    def get_res(self):
        """获取所有章节的写作结果。"""
        return self.res

    def get_model_build_solve(self) -> str:
        """获取模型求解结果的摘要字符串。"""
        model_build_solve = ",".join(
            f"{key}-{value}"
            for key, value in self.res.items()
            if key.startswith("ques") and key != "ques_count"
        )

        return model_build_solve

    def replace_references_with_uuid(self, text: str) -> str:
        """将文本中的引用标记替换为 UUID，用于去重和排序。

        Args:
            text: 包含引用标记的文本。

        Returns:
            替换引用为 UUID 后的文本。
        """
        # 匹配引用内容，格式为 {[^数字]: 引用内容}
        # 修改正则表达式，匹配大括号包裹的引用格式
        references = re.findall(r"\{\[\^(\d+)\]:\s*(.*?)\}", text, re.DOTALL)

        for ref_num, ref_content in references:
            # 清理引用内容，去除末尾的空格和点号
            ref_content = ref_content.strip().rstrip(".")

            # 检查当前引用内容是否已经存在于footnotes中
            existing_uuid = None
            for uuid_key, footnote_data in self.footnotes.items():
                if footnote_data["content"] == ref_content:
                    existing_uuid = uuid_key
                    break

            if existing_uuid:
                # 如果已存在，使用现有的UUID
                text = re.sub(
                    rf"\{{\[\^{ref_num}\]:.*?\}}",
                    f"[{existing_uuid}]",
                    text,
                    flags=re.DOTALL,
                )
            else:
                # 如果不存在，创建新的UUID和footnote条目
                new_uuid = str(uuid.uuid4())
                self.footnotes[new_uuid] = {
                    "content": ref_content,
                }
                text = re.sub(
                    rf"\{{\[\^{ref_num}\]:.*?\}}",
                    f"[{new_uuid}]",
                    text,
                    flags=re.DOTALL,
                )

        return text

    def sort_text_with_footnotes(self, replace_res: dict) -> dict:
        """按章节顺序排列文本并将 UUID 替换为连续编号。

        Args:
            replace_res: 已替换 UUID 的结果字典。

        Returns:
            按顺序编号后的结果字典。
        """
        sort_res = {}
        ref_index = 1

        for seq_key in self.seq:
            text = replace_res[seq_key]["response_content"]
            # 找到[uuid]
            uuid_list = re.findall(r"\[([a-f0-9-]{36})\]", text)
            for uid in uuid_list:
                text = text.replace(f"[{uid}]", f"[^{ref_index}]")
                if self.footnotes[uid].get("number") is None:
                    self.footnotes[uid]["number"] = ref_index

                ref_index += 1
            sort_res[seq_key] = {
                "response_content": text,
            }

        return sort_res

    def append_footnotes_to_text(self, text: str) -> str:
        """在文本末尾追加参考文献列表。

        Args:
            text: 论文正文。

        Returns:
            附带参考文献的完整文本。
        """
        text += "\n\n ## 参考文献"
        # 将脚注转换为列表并按 number 排序
        sorted_footnotes = sorted(self.footnotes.items(), key=lambda x: x[1]["number"])
        for _, footnote in sorted_footnotes:
            text += f"\n\n[^{footnote['number']}]: {footnote['content']}"
        return text

    def get_result_to_save(self) -> str:
        """获取最终拼接的论文全文，包含引用处理和参考文献。"""
        replace_res = {}

        for key, value in self.res.items():
            new_text = self.replace_references_with_uuid(value["response_content"])
            replace_res[key] = {
                "response_content": new_text,
            }

        sort_res = self.sort_text_with_footnotes(replace_res)

        full_res_1 = "\n\n".join(
            [sort_res[key]["response_content"] for key in self.seq]
        )

        full_res = self.append_footnotes_to_text(full_res_1)
        return full_res

    def save_result(self):
        """将结果保存为 res.json 和 res.md 文件。"""
        with open(os.path.join(self.work_dir, "res.json"), "w", encoding="utf-8") as f:
            json.dump(self.res, f, ensure_ascii=False, indent=4)

        res_path = os.path.join(self.work_dir, "res.md")
        with open(res_path, "w", encoding="utf-8") as f:
            f.write(self.get_result_to_save())
