"""通用工具函数模块，提供任务 ID 生成、文件操作和文档转换等功能。"""

import os
import datetime
import hashlib
import tomllib
from app.schemas.enums import CompTemplate
from app.utils.log_util import logger
import re
import pypandoc  # type: ignore[import-unresolved]
from app.config.setting import settings

TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def create_task_id() -> str:
    """生成基于时间戳和随机哈希的唯一任务 ID。"""
    # 生成时间戳和随机hash
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    random_hash = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8]
    return f"{timestamp}-{random_hash}"


def ensure_safe_task_id(task_id: str) -> str:
    """验证任务 ID 的合法性，防止路径遍历攻击。

    Args:
        task_id: 待验证的任务 ID。

    Returns:
        验证通过的任务 ID。

    Raises:
        ValueError: 任务 ID 不合法时抛出。
    """
    normalized = (task_id or "").strip()
    if not normalized or not TASK_ID_PATTERN.fullmatch(normalized):
        raise ValueError("非法 task_id")
    return normalized


def create_work_dir(task_id: str) -> str:
    """为指定任务创建工作目录。

    Args:
        task_id: 任务 ID。

    Returns:
        工作目录路径。
    """
    # 设置主工作目录和子目录
    work_dir = os.path.join("project", "work_dir", task_id)

    try:
        # 创建目录，如果目录已存在也不会报错
        os.makedirs(work_dir, exist_ok=True)
        return work_dir
    except Exception as e:
        # 捕获并记录创建目录时的异常
        logger.error(f"创建工作目录失败: {str(e)}")
        raise


def get_work_dir(task_id: str) -> str:
    """获取指定任务的工作目录路径。

    Args:
        task_id: 任务 ID。

    Returns:
        工作目录路径。

    Raises:
        FileNotFoundError: 工作目录不存在时抛出。
    """
    work_dir = os.path.join("project", "work_dir", task_id)
    if os.path.exists(work_dir):
        return work_dir
    else:
        logger.error(f"工作目录不存在: {work_dir}")
        raise FileNotFoundError(f"工作目录不存在: {work_dir}")


# TODO: 是不是应该将 Prompt 写成一个 class
def get_config_template(comp_template: CompTemplate = CompTemplate.CHINA) -> dict:
    """获取论文模板配置。

    Args:
        comp_template: 竞赛模板类型。

    Returns:
        模板配置字典。
    """
    if comp_template == CompTemplate.CHINA:
        return load_toml(os.path.join("app", "config", "md_template.toml"))
    return {}


def load_toml(path: str) -> dict:
    """加载 TOML 配置文件。

    Args:
        path: TOML 文件路径。
    """
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_markdown(path: str) -> str:
    """加载 Markdown 文件内容。

    Args:
        path: Markdown 文件路径。
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_current_files(folder_path: str, type: str = "all") -> list[str]:
    """获取指定目录下的文件列表。

    Args:
        folder_path: 目录路径。
        type: 文件类型过滤（all/md/ipynb/data/image）。
    """
    files = os.listdir(folder_path)
    if type == "all":
        return files
    elif type == "md":
        return [file for file in files if file.endswith(".md")]
    elif type == "ipynb":
        return [file for file in files if file.endswith(".ipynb")]
    elif type == "data":
        return [
            file for file in files if file.endswith(".xlsx") or file.endswith(".csv")
        ]
    elif type == "image":
        return [
            file for file in files if file.endswith(".png") or file.endswith(".jpg")
        ]
    return []


def transform_link(task_id: str, content: str):
    """将 Markdown 中的图片链接转换为静态资源 URL。

    Args:
        task_id: 任务 ID，用于构建 URL 路径。
        content: 包含图片链接的 Markdown 文本。
    """
    content = re.sub(
        r"!\[(.*?)\]\((.*?\.(?:png|jpg|jpeg|gif|bmp|webp))\)",
        lambda match: f"![{match.group(1)}]({settings.SERVER_HOST}/static/{task_id}/{match.group(2)})",
        content,
    )
    return content


def md_2_docx(task_id: str):
    """将 Markdown 论文转换为 DOCX 格式。

    Args:
        task_id: 任务 ID。
    """
    work_dir = get_work_dir(task_id)
    md_path = os.path.join(work_dir, "res.md")
    docx_path = os.path.join(work_dir, "res.docx")

    extra_args = [
        "--resource-path",
        str(work_dir),
        "--mathml",  # MathML 格式公式
        "--standalone",
    ]

    pypandoc.convert_file(
        source_file=md_path,
        to="docx",
        outputfile=docx_path,
        format="markdown+tex_math_dollars",
        extra_args=extra_args,
    )
    print(f"转换完成: {docx_path}")
    logger.info(f"转换完成: {docx_path}")


def split_footnotes(text: str) -> tuple[str, list[tuple[str, str]]]:
    """从文本中分离正文和脚注。

    Args:
        text: 包含脚注的完整文本。

    Returns:
        (正文, 脚注列表) 的元组，脚注格式为 (编号, 内容)。
    """
    main_text = re.sub(
        r"\n\[\^\d+\]:.*?(?=\n\[\^|\n\n|\Z)", "", text, flags=re.DOTALL
    ).strip()

    # 匹配脚注定义
    footnotes = re.findall(r"\[\^(\d+)\]:\s*(.+?)(?=\n\[\^|\n\n|\Z)", text, re.DOTALL)
    logger.info(f"main_text:{main_text} \n footnotes:{footnotes}")
    return main_text, footnotes
