"""OpenAlex 学术文献搜索模块。"""

import requests
from typing import List, Dict, Any
from app.services.redis_manager import redis_manager
from app.schemas.response import ScholarMessage


class OpenAlexScholar:
    """OpenAlex 学术文献搜索客户端。"""

    def __init__(self, task_id: str, email: str | None = None, api_key: str | None = None):
        """初始化 OpenAlex 客户端。

        Args:
            task_id: 任务 ID。
            email: 可选的邮箱地址，用于获取更好的 API 服务。
            api_key: 可选的 OpenAlex API Key。
        """
        self.base_url = "https://api.openalex.org"
        self.email = email
        self.api_key = api_key
        self.task_id = task_id

    def _get_request_url(self, endpoint: str) -> str:
        """构建请求 URL。

        Args:
            endpoint: API 端点路径。
        """
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        return f"{self.base_url}/{endpoint}"

    def _get_abstract_from_index(self, abstract_inverted_index: Dict) -> str:
        """从abstract_inverted_index中重建摘要文本

        Args:
            abstract_inverted_index: OpenAlex API返回的倒排索引

        Returns:
            重建的摘要文本
        """
        if not abstract_inverted_index:
            return ""

        # 创建一个足够大的空列表来存放所有单词
        max_position = 0
        for positions in abstract_inverted_index.values():
            if positions and max(positions) > max_position:
                max_position = max(positions)

        words = [""] * (max_position + 1)

        # 在正确的位置填入单词
        for word, positions in abstract_inverted_index.items():
            for position in positions:
                words[position] = word

        # 拼接单词形成文本
        return " ".join(words).strip()

    async def search_papers(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """使用 OpenAlex API 搜索学术论文。

        Args:
            query: 搜索关键词。
            limit: 最大返回结果数。

        Returns:
            包含论文详细信息的字典列表。
        """
        # 构建基础 URL
        base_url = self._get_request_url("works")

        # 设置请求参数，根据API支持的字段进行选择
        params = {
            "search": query,
            "per_page": limit,
            "select": "id,title,display_name,authorships,cited_by_count,doi,publication_year,biblio,abstract_inverted_index",
        }

        # 添加邮箱参数到请求URL
        if self.email:
            params["mailto"] = self.email
        else:
            raise ValueError("配置OpenAlex邮箱获取访问文献权利")
        if self.api_key:
            params["api_key"] = self.api_key

        # 设置请求头，包含User-Agent和邮箱信息
        headers = {
            "User-Agent": f"OpenAlexScholar/1.0 (mailto:{self.email})"
            if self.email
            else "OpenAlexScholar/1.0"
        }

        # 让 requests 处理参数编码和 URL 构建
        response: requests.Response | None = None
        try:
            print(f"请求 URL: {base_url} 参数: {params}")
            response = requests.get(base_url, params=params, headers=headers)
            print(f"响应状态: {response.status_code}")

            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP 错误: {e}")
            if response is not None and response.status_code == 403:
                print(
                    "提示: 403错误通常意味着您需要提供有效的邮箱地址或者遵循礼貌池（polite pool）规则"
                )
            if response is not None and hasattr(response, "text"):
                print(f"响应内容: {response.text}")
            raise
        except Exception as e:
            print(f"请求出错: {e}")
            raise

        papers = []
        paper_titles = []  # 用于存储论文标题
        for work in results.get("results", []):
            # 从倒排索引中获取摘要
            abstract = self._get_abstract_from_index(
                work.get("abstract_inverted_index", {})
            )

            # 获取作者信息
            authors = []
            for authorship in work.get("authorships", []):
                author = authorship.get("author", {})
                if author:
                    author_info = {
                        "name": author.get("display_name"),
                        "position": authorship.get("author_position"),
                        "institution": authorship.get("institutions", [{}])[0].get(
                            "display_name"
                        )
                        if authorship.get("institutions")
                        else None,
                    }
                    authors.append(author_info)

            # 获取引用格式信息
            biblio = work.get("biblio", {})
            citation = {
                "volume": biblio.get("volume"),
                "issue": biblio.get("issue"),
                "first_page": biblio.get("first_page"),
                "last_page": biblio.get("last_page"),
            }

            paper = {
                "title": work.get("display_name") or work.get("title", ""),
                "abstract": abstract,
                "authors": authors,
                "citations_count": work.get("cited_by_count"),
                "doi": work.get("doi"),
                "publication_year": work.get("publication_year"),
                "citation_info": citation,
                # 构建引用格式
                "citation_format": self._format_citation(work),
            }
            papers.append(paper)
            paper_titles.append(paper["title"])  # 添加标题到列表

        await redis_manager.publish_message(
            self.task_id,
            ScholarMessage(
                input={"query": query},
                output=paper_titles,  # 只发送论文标题列表
            ),
        )

        return papers

    def papers_to_str(self, papers: List[Dict[str, Any]]) -> str:
        """将文献列表转换为可读字符串。"""
        result = ""
        for paper in papers:
            result += "\n" + "=" * 80
            result += f"\n标题: {paper['title']}"
            result += f"\n摘要: {paper['abstract']}"
            result += "\n作者:"
            for author in paper["authors"]:
                result += f"- {author['name']}"
            result += f"\n引用次数: {paper['citations_count']}"
            result += f"\n发表年份: {paper['publication_year']}"
            result += f"\n引用格式:\n{paper['citation_format']}"
            result += "=" * 80
        return result

    def _format_citation(self, work: Dict[str, Any]) -> str:
        """将论文数据格式化为引用字符串。"""
        # 获取所有作者
        authors = [
            authorship.get("author", {}).get("display_name")
            for authorship in work.get("authorships", [])
            if authorship.get("author")
        ]

        # 格式化作者列表
        if len(authors) > 3:
            authors_str = f"{authors[0]} et al."
        else:
            authors_str = ", ".join(authors)

        # 获取标题
        title = work.get("display_name") or work.get("title", "")

        # 获取年份
        year = work.get("publication_year", "")

        # 获取DOI
        doi = work.get("doi", "")

        # 构建引用格式
        citation = f"{authors_str} ({year}). {title}."
        if doi:
            citation += f" DOI: {doi}"

        return citation
