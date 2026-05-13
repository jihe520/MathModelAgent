"""离线构建知识库脚本，扫描 data/knowledge/ 目录并构建 ChromaDB 索引。

使用方法:
    cd backend
    python scripts/build_knowledge_base.py

目录结构:
    data/knowledge/
        papers/       # 论文 PDF
        textbooks/    # 教材（Markdown/文本）
        code/         # 代码模板
        problems/     # 优秀论文方案
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


KNOWLEDGE_DIR = Path("data/knowledge")
CHROMADB_PATH = "data/chromadb"
EMBEDDING_MODEL = "BAAI/bge-m3"
CHUNK_SIZE = 500  # 字符数
CHUNK_OVERLAP = 50


def chunk_text(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """将文本按固定大小分块。

    Args:
        text: 原始文本。
        chunk_size: 每块大小（字符数）。
        overlap: 块间重叠字符数。

    Returns:
        文本块列表。
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def extract_pdf_text(pdf_path: str) -> str:
    """从 PDF 提取文本（使用 PyMuPDF）。

    Args:
        pdf_path: PDF 文件路径。

    Returns:
        提取的文本内容。
    """
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(pdf_path)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n".join(text_parts)
    except ImportError:
        print("警告: PyMuPDF 未安装，跳过 PDF 文件。请运行: pip install pymupdf")
        return ""
    except Exception as e:
        print(f"PDF 提取失败 {pdf_path}: {e}")
        return ""


def scan_knowledge_dir() -> list[dict]:
    """扫描知识库目录，收集所有待索引的文档。

    Returns:
        文档信息列表，每项包含 text, metadata。
    """
    documents = []

    if not KNOWLEDGE_DIR.exists():
        print(f"知识库目录不存在: {KNOWLEDGE_DIR}")
        print("请创建目录结构:")
        print(f"  {KNOWLEDGE_DIR}/papers/     # 论文 PDF")
        print(f"  {KNOWLEDGE_DIR}/textbooks/  # 教材")
        print(f"  {KNOWLEDGE_DIR}/code/       # 代码模板")
        print(f"  {KNOWLEDGE_DIR}/problems/   # 优秀论文方案")
        return documents

    # 映射目录名到 source_type
    dir_type_map = {
        "papers": "paper",
        "textbooks": "textbook",
        "code": "code",
        "problems": "problem",
    }

    for dir_name, source_type in dir_type_map.items():
        dir_path = KNOWLEDGE_DIR / dir_name
        if not dir_path.exists():
            continue

        for file_path in dir_path.rglob("*"):
            if file_path.is_dir():
                continue

            suffix = file_path.suffix.lower()
            text = ""

            if suffix == ".pdf":
                text = extract_pdf_text(str(file_path))
            elif suffix in (".md", ".txt", ".rst"):
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            elif suffix in (".py", ".jl", ".r"):
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            else:
                continue

            if not text.strip():
                continue

            # 尝试从文件名提取方法名
            method_name = file_path.stem.replace("_", " ").replace("-", " ")

            documents.append(
                {
                    "text": text,
                    "metadata": {
                        "source_type": source_type,
                        "source_file": str(file_path),
                        "source_title": file_path.stem,
                        "method_name": method_name,
                    },
                }
            )

    print(f"扫描完成，找到 {len(documents)} 个文档")
    return documents


def build_chromadb(documents: list[dict]) -> None:
    """构建 ChromaDB 索引。

    Args:
        documents: 文档信息列表。
    """
    try:
        import chromadb
    except ImportError:
        print("错误: chromadb 未安装。请运行: pip install chromadb")
        sys.exit(1)

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print(
            "错误: sentence-transformers 未安装。请运行: pip install sentence-transformers"
        )
        sys.exit(1)

    print(f"加载 Embedding 模型: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=CHROMADB_PATH)
    # 删除旧集合重建
    try:
        client.delete_collection("knowledge")
        print("已删除旧的 knowledge 集合")
    except Exception:
        pass

    collection = client.create_collection(
        name="knowledge",
        metadata={"hnsw:space": "cosine"},
    )

    # 分块并索引
    all_ids = []
    all_documents = []
    all_metadatas = []
    doc_idx = 0

    for doc_info in documents:
        chunks = chunk_text(doc_info["text"])
        for chunk in chunks:
            all_ids.append(f"doc_{doc_idx}")
            all_documents.append(chunk)
            all_metadatas.append(doc_info["metadata"])
            doc_idx += 1

    print(f"共 {len(all_documents)} 个文本块，开始生成 embeddings...")

    # 批量生成 embeddings
    batch_size = 64
    for i in range(0, len(all_documents), batch_size):
        batch_docs = all_documents[i : i + batch_size]
        batch_ids = all_ids[i : i + batch_size]
        batch_metas = all_metadatas[i : i + batch_size]

        embeddings = model.encode(batch_docs, show_progress_bar=False).tolist()

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=embeddings,
            metadatas=batch_metas,
        )
        progress = min(i + batch_size, len(all_documents))
        print(f"  已索引: {progress}/{len(all_documents)}")

    print(f"ChromaDB 构建完成，保存至: {CHROMADB_PATH}")
    print(f"共索引 {len(all_documents)} 个文本块，来自 {len(documents)} 个文档")


def main():
    """主入口。"""
    print("=" * 60)
    print("MathModelAgent 知识库构建工具")
    print("=" * 60)

    documents = scan_knowledge_dir()
    if not documents:
        print("没有找到可索引的文档，退出。")
        return

    build_chromadb(documents)
    print("\n构建完成！")


if __name__ == "__main__":
    main()
