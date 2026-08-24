#!/usr/bin/env python3
"""Validate the structured Markdown log used by 7ai-disclosure."""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

PENDING_MARKERS = ("待队员确认", "请填写", "TODO", "PLACEHOLDER")
SECRET_PATTERNS = {
    "OpenAI 风格密钥": re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    "GitHub 令牌": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{12,}\b"),
    "Tavily 密钥": re.compile(r"\btvly-[A-Za-z0-9_-]{12,}\b"),
    "Bearer 令牌": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{12,}", re.IGNORECASE),
    "环境变量密钥": re.compile(r"\b[A-Z][A-Z0-9_]*(?:API_KEY|TOKEN|SECRET)\s*=\s*\S+"),
}

REQUIRED_HEADINGS = ("AI 工具目录", "AI 使用记录")
REQUIRED_TOOL = ("工具名称", "版本或型号")
REQUIRED_RECORD = (
    "工具编号",
    "使用环节",
    "具体使用目的",
    "是否仅用于语言润色",
    "主要提示方式",
    "使用过程说明",
    "AI 输出采纳情况",
    "对应证据文件或产物",
    "当前状态",
)
REQUIRED_HUMAN_REVIEW = ("人工修改内容", "人工核验方法与结果")
REQUIRED_EXAMPLE = ("对应记录", "代表性提示摘要", "AI 输出摘要", "队员处理")
ID_PATTERN = re.compile(
    r"^###\s+((?:TOOL-\d{2})|(?:AI-\d{3})|(?:EX-\d{3}))\s*$", re.MULTILINE
)


def parse_fields(text: str) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*-\s*([^：:]+)[：:]\s*(.*?)\s*$", line)
        if match:
            fields.setdefault(match.group(1).strip(), []).append(match.group(2).strip())
    return fields


def id_sections(text: str) -> list[tuple[str, str]]:
    matches = list(ID_PATTERN.finditer(text))
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((match.group(1), text[match.end() : end]))
    return result


def missing_fields(
    fields: dict[str, list[str]], required: tuple[str, ...]
) -> list[str]:
    return [name for name in required if name not in fields or not any(fields[name])]


def is_pending(value: str) -> bool:
    return (
        not value.strip()
        or any(marker.casefold() in value.casefold() for marker in PENDING_MARKERS)
        or bool(re.search(r"【[^】]*】", value))
    )


def expected_ids(prefix: str, count: int, width: int) -> list[str]:
    """Build the required contiguous identifiers for one entry type."""
    return [f"{prefix}-{index:0{width}d}" for index in range(1, count + 1)]


def validate(path: Path, mode: str) -> list[str]:
    if not path.is_file():
        return [f"日志不存在：{path}"]

    text = path.read_text(encoding="utf-8-sig")
    errors: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^##\s+{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
            errors.append(f"缺少二级标题：{heading}")

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"检测到疑似{label}，请删除或脱敏")

    sections = id_sections(text)
    tools = [
        (item_id, block) for item_id, block in sections if item_id.startswith("TOOL-")
    ]
    records = [
        (item_id, block) for item_id, block in sections if item_id.startswith("AI-")
    ]
    examples = [
        (item_id, block) for item_id, block in sections if item_id.startswith("EX-")
    ]
    tool_ids = [item_id for item_id, _ in tools]
    record_ids = [item_id for item_id, _ in records]
    example_ids = [item_id for item_id, _ in examples]

    if not tools:
        errors.append("至少需要一个 TOOL-xx 工具条目")
    if not records:
        errors.append("至少需要一个 AI-xxx 使用记录")
    for label, ids in (
        ("工具", tool_ids),
        ("使用记录", record_ids),
        ("典型交互", example_ids),
    ):
        if len(ids) != len(set(ids)):
            errors.append(f"{label}编号重复")
    for label, ids, prefix, width in (
        ("工具", tool_ids, "TOOL", 2),
        ("使用记录", record_ids, "AI", 3),
        ("典型交互", example_ids, "EX", 3),
    ):
        if ids and ids != expected_ids(prefix, len(ids), width):
            errors.append(f"{label}编号必须从 1 开始连续递增")

    for tool_id, block in tools:
        fields = parse_fields(block)
        for name in missing_fields(fields, REQUIRED_TOOL):
            errors.append(f"{tool_id} 缺少字段或值：{name}")

    for record_id, block in records:
        fields = parse_fields(block)
        for name in missing_fields(fields, REQUIRED_RECORD):
            errors.append(f"{record_id} 缺少字段或值：{name}")

        references = re.findall(r"TOOL-\d{2}", " ".join(fields.get("工具编号", [])))
        if not references:
            errors.append(f"{record_id} 未引用 TOOL-xx")
        for reference in references:
            if reference not in tool_ids:
                errors.append(f"{record_id} 引用了不存在的工具：{reference}")

        language_only = " ".join(fields.get("是否仅用于语言润色", []))
        if language_only and language_only not in {"是", "否", "待队员确认"}:
            errors.append(
                f"{record_id} “是否仅用于语言润色”只能是“是”“否”或“待队员确认”"
            )
        if language_only != "是":
            for name in missing_fields(fields, REQUIRED_HUMAN_REVIEW):
                errors.append(f"{record_id} 非纯语言润色，缺少字段或值：{name}")

        status = " ".join(fields.get("当前状态", []))
        if status and status not in {"已确认", "待队员确认"}:
            errors.append(f"{record_id} 当前状态只能是“已确认”或“待队员确认”")

    for example_id, block in examples:
        fields = parse_fields(block)
        for name in missing_fields(fields, REQUIRED_EXAMPLE):
            errors.append(f"{example_id} 缺少字段或值：{name}")
        references = re.findall(r"AI-\d{3}", " ".join(fields.get("对应记录", [])))
        if not references:
            errors.append(f"{example_id} 未引用 AI-xxx")
        for reference in references:
            if reference not in record_ids:
                errors.append(f"{example_id} 引用了不存在的记录：{reference}")

    if mode == "finalize":
        for field_name, values in parse_fields(text).items():
            for value in values:
                if is_pending(value):
                    errors.append(f"最终生成前仍有待确认或占位内容：{field_name}")
        for record_id, block in records:
            fields = parse_fields(block)
            if " ".join(fields.get("当前状态", [])) != "已确认":
                errors.append(f"{record_id} 尚未标记为“已确认”")

    return list(dict.fromkeys(errors))


VALID_SAMPLE = """# AI 工具使用过程记录
## AI 工具目录
### TOOL-01
- 工具名称：示例工具
- 版本或型号：示例模型 1
## AI 使用记录
### AI-001
- 工具编号：TOOL-01
- 使用环节：代码复核
- 具体使用目的：检查边界条件
- 是否仅用于语言润色：否
- 主要提示方式：提供代码和约束，请列出边界风险
- 使用过程说明：模型给出检查清单，队员逐项验证
- AI 输出采纳情况：部分采纳
- 人工修改内容：删除不适用建议并补充测试
- 人工核验方法与结果：运行边界测试，全部通过
- 对应证据文件或产物：tests/test_boundary.py
- 当前状态：已确认
## 典型交互示例（可选）
### EX-001
- 对应记录：AI-001
- 代表性提示摘要：检查边界条件
- AI 输出摘要：列出三类风险
- 队员处理：逐项测试后采纳两项
"""


def self_test() -> int:
    language_sample = VALID_SAMPLE.replace(
        "- 是否仅用于语言润色：否", "- 是否仅用于语言润色：是"
    )
    language_sample = language_sample.replace(
        "- 人工修改内容：删除不适用建议并补充测试\n", ""
    )
    language_sample = language_sample.replace(
        "- 人工核验方法与结果：运行边界测试，全部通过\n", ""
    )
    cases = [
        ("valid", VALID_SAMPLE, "finalize", False),
        ("language_only", language_sample, "finalize", False),
        (
            "pending",
            VALID_SAMPLE.replace("- 当前状态：已确认", "- 当前状态：待队员确认"),
            "finalize",
            True,
        ),
        (
            "bad_ref",
            VALID_SAMPLE.replace("- 工具编号：TOOL-01", "- 工具编号：TOOL-99"),
            "record",
            True,
        ),
        (
            "secret",
            VALID_SAMPLE + "\n- 备注：sk-abcdefghijklmnopqrstuvwxyz\n",
            "record",
            True,
        ),
        (
            "missing_review",
            VALID_SAMPLE.replace("- 人工核验方法与结果：运行边界测试，全部通过\n", ""),
            "record",
            True,
        ),
        ("non_contiguous", VALID_SAMPLE.replace("TOOL-01", "TOOL-02"), "record", True),
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        for name, content, mode, should_fail in cases:
            path = Path(tmpdir) / f"{name}.md"
            path.write_text(content, encoding="utf-8")
            failed = bool(validate(path, mode))
            if failed != should_fail:
                print(f"SELF-TEST FAIL: {name}")
                return 1
    print("SELF-TEST PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 AI 工具使用过程记录")
    parser.add_argument("path", nargs="?", type=Path, help="AI_USAGE_LOG.md 路径")
    parser.add_argument("--mode", choices=("record", "finalize"), default="finalize")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.path is None:
        parser.error("除 --self-test 外，必须提供日志路径")
    errors = validate(args.path, args.mode)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"VALIDATION FAILED: {len(errors)} error(s)")
        return 1
    print(f"VALIDATION PASS ({args.mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
