"""Web Search 工具模块，Agent 主动生成搜索查询并提取结构化数据证据。"""

import hashlib
import json

import httpx

from app.config.setting import settings
from app.core.llm.llm import LLM, simple_chat
from app.schemas.evidence import DataEvidence
from app.schemas.response import SystemMessage
from app.services.redis_manager import redis_manager
from app.services.state_store import state_store
from app.utils.log_util import logger

# LLM 提取结构化数据的 prompt
_EXTRACT_PROMPT = """你是一个数据提取专家。从以下网页搜索结果中提取结构化数据。

搜索查询：{query}

搜索结果：
{results}

请提取所有有价值的结构化数据，以 JSON 数组格式返回，每个元素包含：
- content: 数据描述（简洁明了）
- unit: 数据单位（如"亿元"、"万人"、"%"），无明确单位填 null
- time_range: 数据时间范围（如"2020-2024"），无明确时间填 null
- region: 数据地域范围（如"中国"、"全球"），无明确地域填 null
- original_excerpt: 原文摘录（包含具体数字的原文片段）
- source_url: 数据来源 URL
- source_title: 来源标题
- source_level: 来源级别，"official"（政府/官方）| "academic"（学术）| "media"（媒体）| "unknown"
- confidence: 数据可信度 0-1（官方>学术>媒体>未知）
- data_format: 数据格式 "table"|"timeseries"|"categorical"

只返回 JSON 数组，不要其他文字。如果没有有价值的数据，返回空数组 []。"""


class WebSearcher:
    """Web 搜索工具，调用 Tavily API 获取网页数据并用 LLM 提取结构化证据。"""

    def __init__(self, llm: LLM) -> None:
        """初始化 WebSearcher。

        Args:
            llm: 用于提取结构化数据的 LLM 实例。
        """
        self.llm = llm

    def _cache_key(self, query: str) -> str:
        """生成缓存键。"""
        return hashlib.md5(query.encode()).hexdigest()

    async def search(
        self, query: str, data_type: str = "general", max_results: int = 5
    ) -> list[DataEvidence]:
        """执行 Web 搜索并提取结构化数据证据。

        Args:
            query: 搜索查询。
            data_type: 数据类型提示（如 "statistical", "timeseries"）。
            max_results: 最大结果数。

        Returns:
            DataEvidence 列表。
        """
        if not settings.TAVILY_API_KEY:
            logger.warning("TAVILY_API_KEY 未配置，跳过 Web 搜索")
            return []

        # 查缓存
        cache_key = self._cache_key(f"{query}_{data_type}_{max_results}")
        cached = await state_store.get("search", cache_key)
        if cached is not None:
            logger.info(f"WebSearcher: 命中缓存 query={query}")
            return [DataEvidence(**item) for item in cached]

        # 发布搜索中消息
        await redis_manager.publish_message(
            self.llm.task_id,
            SystemMessage(content=f"正在搜索: {query}"),
        )

        # 调用 Tavily API
        raw_results = await self._tavily_search(query, max_results)
        if not raw_results:
            return []

        # 用 LLM 提取结构化数据
        evidence_list = await self._extract_evidence(query, raw_results)

        # 缓存结果
        if evidence_list:
            await state_store.set(
                "search",
                cache_key,
                [e.model_dump() for e in evidence_list],
                ttl=settings.SEARCH_CACHE_TTL,
            )

        # 发布搜索完成消息
        await redis_manager.publish_message(
            self.llm.task_id,
            SystemMessage(content=f"搜索完成: 找到 {len(evidence_list)} 条数据证据"),
        )

        return evidence_list

    async def _tavily_search(self, query: str, max_results: int) -> list[dict]:
        """调用 Tavily Search API。

        Args:
            query: 搜索查询。
            max_results: 最大结果数。

        Returns:
            搜索结果列表。
        """
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": settings.TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": True,
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
        except Exception as e:
            logger.error(f"Tavily API 调用失败: {e}")
            return []

    async def _extract_evidence(
        self, query: str, raw_results: list[dict]
    ) -> list[DataEvidence]:
        """用 LLM 从搜索结果中提取结构化数据证据。

        Args:
            query: 原始搜索查询。
            raw_results: Tavily API 返回的原始结果。

        Returns:
            DataEvidence 列表。
        """
        # 格式化搜索结果给 LLM
        results_text = ""
        for i, r in enumerate(raw_results, 1):
            results_text += f"\n--- 结果 {i} ---\n"
            results_text += f"标题: {r.get('title', '')}\n"
            results_text += f"URL: {r.get('url', '')}\n"
            results_text += f"内容: {r.get('content', '')[:1500]}\n"

        prompt = _EXTRACT_PROMPT.format(query=query, results=results_text)

        try:
            response_text = await simple_chat(
                self.llm,
                [{"role": "user", "content": prompt}],
            )
            # 清理 JSON
            response_text = response_text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[-1]
            if response_text.endswith("```"):
                response_text = response_text.rsplit("```", 1)[0]
            response_text = response_text.strip()

            items = json.loads(response_text)
            if not isinstance(items, list):
                return []

            evidence_list = []
            for item in items:
                try:
                    evidence_list.append(DataEvidence(**item))
                except Exception:
                    continue
            return evidence_list

        except Exception as e:
            logger.error(f"LLM 数据提取失败: {e}")
            return []
