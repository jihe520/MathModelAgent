import requests
import json
from typing import List, Dict, Any


class OpenAlexScholar:
    def __init__(self, email: str = None):
        """Initialize OpenAlex client.

        Args:
            email: Optional email for better API service
        """
        self.base_url = "https://api.openalex.org"
        self.email = email

    def _get_request_url(self, endpoint: str) -> str:
        """Construct request URL with email parameter if provided."""
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

    def search_papers(
        self, query: str, limit: int = 10, author: str = None, year: int = None
    ) -> List[Dict[str, Any]]:
        """Search for papers using OpenAlex API.

        Args:
            query: Search query string
            limit: Maximum number of results to return
            author: Filter by author name
            year: Filter by publication year

        Returns:
            List of papers with their details
        """
        # 构建基础 URL
        base_url = self._get_request_url("works")

        # 设置请求参数，根据API支持的字段进行选择
        params = {
            "search": query,
            "per_page": limit,
            "select": "id,title,display_name,authorships,cited_by_count,doi,publication_year,biblio,abstract_inverted_index",
        }

        # Add filters for author and year
        filters = []
        if author:
            filters.append(f"authorships.author.display_name:{author}")
        if year:
            filters.append(f"publication_year:{year}")

        if filters:
            params["filter"] = ",".join(filters)

        # 添加邮箱参数到请求URL
        if self.email:
            params["mailto"] = self.email

        # 设置请求头，包含User-Agent和邮箱信息
        headers = {
            "User-Agent": f"OpenAlexScholar/1.0 (mailto:{self.email})"
            if self.email
            else "OpenAlexScholar/1.0"
        }

        # 让 requests 处理参数编码和 URL 构建
        try:
            print(f"请求 URL: {base_url} 参数: {params}")
            response = requests.get(base_url, params=params, headers=headers)
            print(f"响应状态: {response.status_code}")

            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP 错误: {e}")
            if response.status_code == 403:
                print(
                    "提示: 403错误通常意味着您需要提供有效的邮箱地址或者遵循礼貌池（polite pool）规则"
                )
            if hasattr(response, "text"):
                print(f"响应内容: {response.text}")
            raise
        except Exception as e:
            print(f"请求出错: {e}")
            raise

        papers = []
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

        return papers

    def _format_citation(self, work: Dict[str, Any], style: str = "apa") -> str:
        """Format citation in a specified style."""
        if style.lower() == "apa":
            return self._format_apa(work)
        else:
            # Default to a simple format
            return self._format_simple(work)

    def _format_simple(self, work: Dict[str, Any]) -> str:
        """Formats citation in a simple, readable format."""
        authors = [
            authorship.get("author", {}).get("display_name")
            for authorship in work.get("authorships", [])
            if authorship.get("author")
        ]
        authors_str = ", ".join(authors) if authors else "N.A."
        title = work.get("display_name") or work.get("title", "No Title")
        year = work.get("publication_year", "N.D.")
        return f"{authors_str} ({year}). {title}."

    def _format_apa(self, work: Dict[str, Any]) -> str:
        """Formats citation in APA style."""
        authors = [
            authorship.get("author", {}).get("display_name")
            for authorship in work.get("authorships", [])
            if authorship.get("author")
        ]

        authors_str = ""
        if len(authors) == 1:
            authors_str = authors[0]
        elif len(authors) > 1:
            authors_str = ", ".join(authors[:-1]) + f" & {authors[-1]}"

        year = work.get("publication_year", "n.d.")
        title = work.get("display_name") or work.get("title", "No Title")

        # This is a simplified APA format. A full implementation would need more details
        # like journal name, volume, issue, pages, etc.
        citation = f"{authors_str} ({year}). *{title}*."

        doi = work.get("doi")
        if doi:
            citation += f" https://doi.org/{doi}"

        return citation


if __name__ == "__main__":
    # Example usage
    scholar = OpenAlexScholar(email="xxx@xxx.com")  # 请替换为您的真实邮箱
    try:
        papers = scholar.search_papers("machine learning")
        for paper in papers:
            print("\n" + "=" * 80)
            print(f"标题: {paper['title']}")
            print(f"\n摘要: {paper['abstract']}")
            print("\n作者:")
            for author in paper["authors"]:
                print(f"- {author['name']}")
                if author["institution"]:
                    print(f"  所属机构: {author['institution']}")
            print(f"\n引用次数: {paper['citations_count']}")
            print(f"发表年份: {paper['publication_year']}")
            print(f"\n引用格式:\n{paper['citation_format']}")
            print("=" * 80)
    except Exception as e:
        print(f"发生错误: {e}")
        print("请检查您的网络连接或API访问权限。")
