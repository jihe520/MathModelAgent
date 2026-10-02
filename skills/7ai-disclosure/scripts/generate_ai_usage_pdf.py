#!/usr/bin/env python3
"""Generate the CUMCM AI usage disclosure from a validated Markdown log."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from validate_ai_usage_log import (
    NO_HUMAN_RECORD_PHRASES,
    PENDING_MARKERS,
    SECRET_PATTERNS,
    id_sections,
    parse_fields,
    validate,
)

TEMPLATE_MARKERS = (
    "%%__TOOLS_ROWS__%%",
    "%%__PURPOSE_ROWS__%%",
    "%%__PROCESS_BLOCKS__%%",
    "%%__ADOPTION_BLOCKS__%%",
)
REQUIRED_PDF_HEADINGS = (
    "一、所用AI工具名称、版本或型号",
    "二、具体使用目的和环节",
    "三、主要提示方式与使用过程说明",
    "四、对AI输出的采纳、人工修改和核验的主要情况",
)


class GenerationError(RuntimeError):
    """Raised when a disclosure artifact cannot be generated safely."""


@dataclass(frozen=True)
class ToolEntry:
    """One AI tool declared in the usage log."""

    tool_id: str
    name: str
    version: str


@dataclass(frozen=True)
class UsageRecord:
    """One stage-level AI usage record."""

    record_id: str
    tool_ids: tuple[str, ...]
    stage: str
    purpose: str
    language_only: bool
    prompt_method: str
    process: str
    adoption: str
    iteration: str
    verification: str
    human_edit: str


@dataclass(frozen=True)
class InteractionExample:
    """One optional representative interaction example."""

    example_id: str
    record_ids: tuple[str, ...]
    prompt_summary: str
    output_summary: str
    process_result: str


@dataclass(frozen=True)
class DisclosureLog:
    """Structured data parsed from the Markdown log."""

    tools: tuple[ToolEntry, ...]
    records: tuple[UsageRecord, ...]
    examples: tuple[InteractionExample, ...]


def _field(fields: dict[str, list[str]], name: str, default: str = "") -> str:
    """Return a stable, compact value for a structured Markdown field."""
    values = [value.strip() for value in fields.get(name, []) if value.strip()]
    return "；".join(values) if values else default


def parse_log(path: Path) -> DisclosureLog:
    """Parse a validated AI usage log into structured records.

    Args:
        path: Markdown log path.

    Returns:
        Structured disclosure data.
    """
    text = path.read_text(encoding="utf-8-sig")
    tools: list[ToolEntry] = []
    records: list[UsageRecord] = []
    examples: list[InteractionExample] = []

    for item_id, block in id_sections(text):
        fields = parse_fields(block)
        if item_id.startswith("TOOL-"):
            tools.append(
                ToolEntry(
                    tool_id=item_id,
                    name=_field(fields, "工具名称"),
                    version=_field(fields, "版本或型号"),
                )
            )
        elif item_id.startswith("AI-"):
            tool_ids = tuple(
                dict.fromkeys(re.findall(r"TOOL-\d{2}", _field(fields, "工具编号")))
            )
            records.append(
                UsageRecord(
                    record_id=item_id,
                    tool_ids=tool_ids,
                    stage=_field(fields, "使用环节"),
                    purpose=_field(fields, "具体使用目的"),
                    language_only=_field(fields, "是否仅用于语言润色") == "是",
                    prompt_method=_field(fields, "主要提示方式"),
                    process=_field(fields, "使用过程说明"),
                    adoption=_field(fields, "AI 输出采纳情况"),
                    iteration=_field(fields, "迭代修正情况"),
                    verification=_field(fields, "核验方法与结果"),
                    human_edit=_field(fields, "人工修改内容"),
                )
            )
        elif item_id.startswith("EX-"):
            record_ids = tuple(
                dict.fromkeys(re.findall(r"AI-\d{3}", _field(fields, "对应记录")))
            )
            examples.append(
                InteractionExample(
                    example_id=item_id,
                    record_ids=record_ids,
                    prompt_summary=_field(fields, "代表性提示摘要"),
                    output_summary=_field(fields, "AI 输出摘要"),
                    process_result=_field(fields, "处理结果"),
                )
            )

    return DisclosureLog(tuple(tools), tuple(records), tuple(examples))


def latex_escape(value: str) -> str:
    """Escape untrusted log text for LaTeX text mode.

    Args:
        value: Plain text from the automatically summarized usage log.

    Returns:
        A single-line LaTeX-safe string.
    """
    compact = re.sub(r"\s+", " ", value).strip()
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "_": r"\_",
        "%": r"\%",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in compact)


def _tools_rows(data: DisclosureLog) -> str:
    return "\n".join(
        f"{tool.tool_id} & {latex_escape(tool.name)} & "
        f"{latex_escape(tool.version)} \\\\"
        for tool in data.tools
    )


def _purpose_rows(data: DisclosureLog) -> str:
    return "\n".join(
        f"{latex_escape('、'.join(record.tool_ids))} & "
        f"{latex_escape(record.stage)} & {latex_escape(record.purpose)} \\\\"
        for record in data.records
    )


def _process_blocks(data: DisclosureLog) -> str:
    examples_by_record: dict[str, list[InteractionExample]] = {}
    for example in data.examples:
        for record_id in example.record_ids:
            examples_by_record.setdefault(record_id, []).append(example)

    blocks: list[str] = []
    for record in data.records:
        tool_ids = "、".join(record.tool_ids)
        lines = [
            rf"\recordheading{{{record.record_id}}}{{{latex_escape(tool_ids)}}}",
            rf"\textbf{{主要提示方式：}}{latex_escape(record.prompt_method)}。",
            "",
            rf"\textbf{{使用过程：}}{latex_escape(record.process)}。",
        ]
        for example in examples_by_record.get(record.record_id, []):
            lines.extend(
                [
                    "",
                    rf"\noindent\textbf{{典型交互示例 {example.example_id}}}",
                    "",
                    rf"\textbf{{代表性提示摘要：}}{latex_escape(example.prompt_summary)}。",
                    "",
                    rf"\textbf{{AI 输出摘要：}}{latex_escape(example.output_summary)}。",
                    "",
                    rf"\textbf{{处理结果：}}{latex_escape(example.process_result)}。",
                ]
            )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _adoption_blocks(data: DisclosureLog) -> str:
    blocks: list[str] = []
    for record in data.records:
        if record.language_only:
            continue
        tool_ids = "、".join(record.tool_ids)
        lines = [
            rf"\recordheading{{{record.record_id}}}{{{latex_escape(tool_ids)}}}",
            rf"\textbf{{采纳情况：}}{latex_escape(record.adoption)}。",
        ]
        if record.human_edit:
            lines.extend(
                ["", rf"\textbf{{人工修改：}}{latex_escape(record.human_edit)}。"]
            )
        if record.iteration:
            lines.extend(
                ["", rf"\textbf{{迭代修正：}}{latex_escape(record.iteration)}。"]
            )
        if record.verification:
            lines.extend(
                ["", rf"\textbf{{核验情况：}}{latex_escape(record.verification)}。"]
            )
        blocks.append("\n".join(lines))
    if not blocks:
        return "本次记录仅涉及语言表达辅助，第四部分不作展开。"
    return "\n\n".join(blocks)


def render_tex(log_path: Path, template_path: Path, tex_path: Path) -> Path:
    """Render a final TeX source from a validated log.

    Args:
        log_path: Finalized Markdown log.
        template_path: LaTeX template containing deterministic markers.
        tex_path: Destination TeX path.

    Returns:
        The written TeX path.

    Raises:
        GenerationError: If validation or template rendering fails.
    """
    errors = validate(log_path, "finalize")
    if errors:
        raise GenerationError("日志未通过最终校验：\n- " + "\n- ".join(errors))
    if not template_path.is_file():
        raise GenerationError(f"LaTeX 模板不存在：{template_path}")

    template = template_path.read_text(encoding="utf-8-sig")
    for marker in TEMPLATE_MARKERS:
        if template.count(marker) != 1:
            raise GenerationError(f"模板标记缺失或重复：{marker}")

    data = parse_log(log_path)
    rendered = template
    replacements = {
        TEMPLATE_MARKERS[0]: _tools_rows(data),
        TEMPLATE_MARKERS[1]: _purpose_rows(data),
        TEMPLATE_MARKERS[2]: _process_blocks(data),
        TEMPLATE_MARKERS[3]: _adoption_blocks(data),
    }
    for marker, content in replacements.items():
        rendered = rendered.replace(marker, content)

    if any(marker in rendered for marker in TEMPLATE_MARKERS):
        raise GenerationError("生成后的 TeX 仍含模板标记")
    for marker in PENDING_MARKERS:
        if marker.casefold() in rendered.casefold():
            raise GenerationError(f"生成后的 TeX 仍含待确认或占位内容：{marker}")
    for phrase in NO_HUMAN_RECORD_PHRASES:
        if phrase in rendered:
            raise GenerationError(f"生成后的 TeX 含禁止的无人工记录提示：{phrase}")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(rendered):
            raise GenerationError(f"生成后的 TeX 检测到疑似{label}")

    tex_path.parent.mkdir(parents=True, exist_ok=True)
    with tex_path.open("w", encoding="utf-8", newline="\n") as output:
        output.write(rendered)
    return tex_path


def _run_compiler(command: list[str], cwd: Path) -> None:
    """Run a PDF compiler and raise a compact actionable error on failure."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise GenerationError(f"PDF 编译超时：{' '.join(command)}") from exc
    if result.returncode != 0:
        output = (result.stdout + "\n" + result.stderr).strip()
        raise GenerationError(
            f"PDF 编译失败（退出码 {result.returncode}）：\n{output[-4000:]}"
        )


def compile_pdf(tex_path: Path, compiler: str = "auto") -> Path:
    """Compile the rendered TeX using XeLaTeX or Tectonic.

    Args:
        tex_path: Rendered TeX source.
        compiler: ``auto``, ``xelatex``, or ``tectonic``.

    Returns:
        Compiled PDF path.
    """
    candidates = ("xelatex", "tectonic") if compiler == "auto" else (compiler,)
    selected = next(
        ((name, shutil.which(name)) for name in candidates if shutil.which(name)),
        None,
    )
    if selected is None:
        expected = " 或 ".join(candidates)
        raise GenerationError(f"缺少 PDF 编译器：需要 {expected}")

    name, executable = selected
    assert executable is not None
    if name == "xelatex":
        command = [
            executable,
            "-interaction=nonstopmode",
            "-halt-on-error",
            tex_path.name,
        ]
        _run_compiler(command, tex_path.parent)
        _run_compiler(command, tex_path.parent)
    else:
        _run_compiler([executable, "--keep-logs", tex_path.name], tex_path.parent)

    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        raise GenerationError(f"编译器未生成非空 PDF：{pdf_path}")
    return pdf_path


def cleanup_auxiliary_files(tex_path: Path) -> None:
    """Remove compiler by-products after a fully verified build."""
    names = [
        tex_path.with_suffix(suffix)
        for suffix in (".aux", ".log", ".out", ".toc", ".xdv")
    ]
    names.append(tex_path.with_name(f"{tex_path.stem}.synctex.gz"))
    for path in names:
        if path.is_file():
            path.unlink()


def _normalize_pdf_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def inspect_pdf(pdf_path: Path, source_tex: Path | None = None) -> list[str]:
    """Check filename, A4 pages, text layer, headings, and sensitive content.

    Some PDF parsers cannot decode CJK ToUnicode maps produced by every TeX
    engine. In that case the compiled source verifies the required headings,
    while the PDF parser still verifies that a non-empty text layer exists.
    """
    errors: list[str] = []
    if pdf_path.name != "AI 工具使用详情.pdf":
        errors.append("最终 PDF 文件名必须完全等于“AI 工具使用详情.pdf”")
    if not pdf_path.is_file() or pdf_path.stat().st_size < 1024:
        return errors + ["最终 PDF 不存在或文件过小"]
    if pdf_path.read_bytes()[:5] != b"%PDF-":
        errors.append("最终文件不是有效 PDF")

    pages: list[tuple[float, float, str]] = []
    try:
        import fitz  # type: ignore[import-unresolved]

        with fitz.open(pdf_path) as document:
            pages = [
                (float(page.rect.width), float(page.rect.height), page.get_text("text"))
                for page in document
            ]
    except ImportError:
        try:
            from pypdf import PdfReader  # type: ignore[import-unresolved]

            reader = PdfReader(str(pdf_path))
            pages = [
                (
                    float(page.mediabox.width),
                    float(page.mediabox.height),
                    page.extract_text() or "",
                )
                for page in reader.pages
            ]
        except ImportError:
            errors.append("缺少 PyMuPDF 或 pypdf，无法检查页面尺寸和文本层")
            return errors
        except Exception as exc:  # noqa: BLE001
            errors.append(f"PDF 读取失败：{exc}")
            return errors
    except Exception as exc:  # noqa: BLE001
        errors.append(f"PDF 读取失败：{exc}")
        return errors

    if not pages:
        return errors + ["最终 PDF 没有页面"]
    for index, (width, height, _) in enumerate(pages, start=1):
        if abs(width - 595.28) > 5 or abs(height - 841.89) > 5:
            errors.append(
                f"第 {index} 页不是 A4 纵向页面：{width:.1f} x {height:.1f} pt"
            )

    text = "\n".join(page_text for _, _, page_text in pages)
    normalized_pdf = _normalize_pdf_text(text)
    if not normalized_pdf:
        errors.append("最终 PDF 没有可提取文本层")
    heading_text = text
    if source_tex is not None and source_tex.is_file():
        heading_text = source_tex.read_text(encoding="utf-8-sig")
    normalized_headings = _normalize_pdf_text(heading_text)
    for heading in REQUIRED_PDF_HEADINGS:
        if heading not in normalized_headings:
            errors.append(f"最终 PDF 缺少规定部分：{heading}")
    for marker in PENDING_MARKERS:
        if marker.casefold() in text.casefold():
            errors.append(f"最终 PDF 仍含待确认或占位内容：{marker}")
    inspection_text = text
    if source_tex is not None and source_tex.is_file():
        inspection_text += "\n" + source_tex.read_text(encoding="utf-8-sig")
    for phrase in NO_HUMAN_RECORD_PHRASES:
        if phrase in inspection_text:
            errors.append(f"最终 PDF 含禁止的无人工记录提示：{phrase}")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"最终 PDF 检测到疑似{label}")
    return list(dict.fromkeys(errors))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="根据自动归纳的 AI 使用日志生成国赛 AI 工具使用详情 PDF"
    )
    parser.add_argument("log_path", type=Path, help="reports/AI_USAGE_LOG.md 路径")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("supporting_materials"),
        help="输出目录，默认 supporting_materials",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "templates"
        / "AI工具使用详情模板.tex",
    )
    parser.add_argument(
        "--compiler",
        choices=("auto", "xelatex", "tectonic"),
        default="auto",
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="只生成 TeX，不编译；仅用于自动测试",
    )
    args = parser.parse_args()

    tex_path = args.output_dir / "AI 工具使用详情.tex"
    try:
        render_tex(args.log_path, args.template, tex_path)
        print(f"TEX GENERATED: {tex_path}")
        if args.no_compile:
            return 0
        pdf_path = compile_pdf(tex_path, args.compiler)
        errors = inspect_pdf(pdf_path, tex_path)
        if errors:
            raise GenerationError("PDF 验收失败：\n- " + "\n- ".join(errors))
        cleanup_auxiliary_files(tex_path)
        print(f"PDF GENERATED AND VERIFIED: {pdf_path}")
        return 0
    except GenerationError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
