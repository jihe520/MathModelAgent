"""RAG 知识检索模块，从 ChromaDB 检索专业知识并产出 KnowledgeEvidence。"""

from app.config.setting import settings
from app.schemas.evidence import KnowledgeEvidence
from app.utils.log_util import logger


class KnowledgeRetriever:
    """知识检索器，支持 Dense (ChromaDB) + Metadata Filter + Rerank。"""

    def __init__(self) -> None:
        self._collection = None
        self._reranker = None
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """延迟初始化 ChromaDB 和 Reranker。"""
        if self._initialized:
            return

        try:
            import chromadb  # type: ignore[import-unresolved]

            client = chromadb.PersistentClient(path=settings.RAG_DB_PATH)
            self._collection = client.get_or_create_collection(
                name="knowledge",
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(f"ChromaDB 初始化完成，路径: {settings.RAG_DB_PATH}")
        except Exception as e:
            logger.error(f"ChromaDB 初始化失败: {e}")
            self._collection = None

        try:
            from sentence_transformers import CrossEncoder  # type: ignore[import-unresolved]

            self._reranker = CrossEncoder(settings.RAG_RERANKER_MODEL)
            logger.info(f"Reranker 加载完成: {settings.RAG_RERANKER_MODEL}")
        except Exception as e:
            logger.warning(f"Reranker 加载失败（将跳过 rerank）: {e}")
            self._reranker = None

        self._initialized = True

    async def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        source_type: str | None = None,
        method_name: str | None = None,
    ) -> list[KnowledgeEvidence]:
        """检索与查询相关的知识证据。

        Args:
            query: 检索查询。
            top_k: 返回结果数量，默认使用配置值。
            source_type: 过滤来源类型（"paper"|"textbook"|"code"|"problem"）。
            method_name: 过滤方法名（如 "TOPSIS"）。

        Returns:
            KnowledgeEvidence 列表。
        """
        await self._ensure_initialized()

        if self._collection is None:
            logger.warning("ChromaDB 未初始化，跳过知识检索")
            return []

        top_k = top_k or settings.RAG_TOP_K

        # 构建 metadata 过滤条件
        where = self._build_where_filter(source_type, method_name)

        try:
            # Dense search
            results = self._collection.query(
                query_texts=[query],
                n_results=top_k * 2,  # 多取一些用于 rerank
                where=where if where else None,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            logger.error(f"ChromaDB 查询失败: {e}")
            return []

        if not results or not results["documents"] or not results["documents"][0]:
            return []

        documents = results["documents"][0]
        metadatas: list[dict[str, object]] = (
            [dict(m) for m in results["metadatas"][0]]
            if results["metadatas"]
            else [{}] * len(documents)
        )
        distances = (
            results["distances"][0] if results["distances"] else [0.0] * len(documents)
        )

        # Rerank
        if self._reranker and len(documents) > top_k:
            documents, metadatas, distances = self._rerank(
                query, documents, metadatas, distances, top_k
            )

        # 构建 KnowledgeEvidence
        evidence_list = []
        for doc, meta, dist in zip(
            documents[:top_k], metadatas[:top_k], distances[:top_k]
        ):
            confidence = max(0.0, 1.0 - dist)  # cosine distance → confidence
            source_type_raw = meta.get("source_type", "textbook")
            source_type = source_type_raw if source_type_raw in ("paper", "textbook", "code", "problem") else "textbook"
            evidence = KnowledgeEvidence(
                content=doc,
                source_type=source_type,  # type: ignore[arg-type]
                method_name=str(meta["method_name"]) if meta.get("method_name") else None,
                source_file=str(meta["source_file"]) if meta.get("source_file") else None,
                source_url=str(meta["source_url"]) if meta.get("source_url") else None,
                source_title=str(meta["source_title"]) if meta.get("source_title") else None,
                confidence=min(1.0, confidence),
                metadata=dict(meta),
            )
            evidence_list.append(evidence)

        logger.info(f"知识检索完成: query={query}, 找到 {len(evidence_list)} 条")
        return evidence_list

    def _build_where_filter(
        self, source_type: str | None, method_name: str | None
    ) -> dict | None:
        """构建 ChromaDB metadata 过滤条件。"""
        conditions = []
        if source_type:
            # 支持逗号分隔的多值过滤
            if "," in source_type:
                types = [t.strip() for t in source_type.split(",")]
                conditions.append({"source_type": {"$in": types}})
            else:
                conditions.append({"source_type": source_type})
        if method_name:
            conditions.append({"method_name": method_name})

        if len(conditions) == 0:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return {"$and": conditions}

    def _rerank(
        self,
        query: str,
        documents: list[str],
        metadatas: list[dict[str, object]],
        distances: list[float],
        top_k: int,
    ) -> tuple[list[str], list[dict[str, object]], list[float]]:
        """使用 CrossEncoder 对检索结果重排序。"""
        pairs = [(query, doc) for doc in documents]
        scores = self._reranker.predict(pairs)  # type: ignore[union-attr]

        # 按 rerank 分数降序排列
        scored = list(zip(documents, metadatas, distances, scores))
        scored.sort(key=lambda x: x[3], reverse=True)

        reranked_docs = [x[0] for x in scored[:top_k]]
        reranked_metas = [x[1] for x in scored[:top_k]]
        # 将 rerank 分数转换为 distance（越小越好 → 越大越好）
        reranked_dists = [1.0 - float(x[3]) for x in scored[:top_k]]

        return reranked_docs, reranked_metas, reranked_dists


# 全局单例
knowledge_retriever = KnowledgeRetriever()
