#!/usr/bin/env python3
"""Validate the structured Markdown log used by 7ai-disclosure."""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

PENDING_MARKERS = (
    "待队员确认",
    "请填写",
    "TODO",
    "PLACEHOLDER",
    "示例工具",
    "示例模型",
    "示例型号",
)
NO_HUMAN_RECORD_PHRASES = (
    "未记录到额外人工修改",
    "未记录人工修改",
    "无人工修改记录",
    "没有人工修改记录",
    "未发现人工修改",
)
SECRET_PATTERNS = {
    "OpenAI 风格密钥": re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    "GitHub 令牌": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{12,}\b"),
    "Tavily 密钥": re.compile(r"\btvly-[A-Za-z0-9_-]{12,}\b"),
    "Bearer 令牌": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{12,}", re.IGNORECASE),
    "环境变量密钥": re.compile(r"\b[A-Z][A-Z0-9_]*(?:API_KEY|TOKEN|SECRET)\s*=\s*\S+"),
}
CORE_DETAIL_PATTERNS = {
    "公式或变量表达式": re.compile(
        r"(?:\\(?:frac|sum|int|begin)\b|\$[^$\n]+\$|\b[A-Za-z]\w*_\d+\b|"
        r"\b[A-Za-z][A-Za-z0-9_]*\s*=\s*-?\d)"
    ),
    "具体数值结果": re.compile(
        r"(?:最终结果|最优值|预测值|权重|参数|误差|准确率|目标函数值)"
        r"[^。；\n]{0,16}-?\d+(?:\.\d+)?"
    ),
    "特定模型或算法名称": re.compile(
        r"(?:AHP|TOPSIS|ARIMA|LSTM|XGBoost|NSGA(?:-?II)?|"
        r"随机森林|层次分析法|熵权法|遗传算法|模拟退火|微分方程|"
        r"线性规划|整数规划)",
        re.IGNORECASE,
    ),
    "内部项目路径": re.compile(
        r"(?:^|[\s（(])(?:code|results|paper|figures|reports)[/\\][^\s，。；）)]+",
        re.IGNORECASE,
    ),
}
HUMAN_CLAIM_PATTERN = re.compile(
    r"(?:队员|手工|参赛者|团队成员|人工(?:复算|检查|核验|修改|审阅|调整|确认|验证))"
)

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
REQUIRED_REVIEW = ("迭代修正情况", "核验方法与结果")
OPTIONAL_HUMAN = ("人工修改内容", "人工修改依据")
REQUIRED_EXAMPLE = ("对应记录", "代表性提示摘要", "AI 输出摘要", "处理结果")
PUBLIC_DISCLOSURE_FIELDS = (
    "使用环节",
    "具体使用目的",
    "主要提示方式",
    "使用过程说明",
    "AI 输出采纳情况",
    "迭代修正情况",
    "核验方法与结果",
    "人工修改内容",
    "代表性提示摘要",
    "AI 输出摘要",
    "处理结果",
)
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


def validate_public_content(
    owner: str, fields: dict[str, list[str]], errors: list[str]
) -> None:
    """Reject details or claims that must not enter the public disclosure."""
    for field_name in PUBLIC_DISCLOSURE_FIELDS:
        for value in fields.get(field_name, []):
            for phrase in NO_HUMAN_RECORD_PHRASES:
                if phrase in value:
                    errors.append(
                        f"{owner} {field_name} 含禁止的无人工记录提示：{phrase}"
                    )
            if field_name not in OPTIONAL_HUMAN and HUMAN_CLAIM_PATTERN.search(value):
                errors.append(
                    f"{owner} {field_name} 将过程表述为人工行为；仅有明确会话依据时"
                    "才可使用人工修改专用字段"
                )
            for label, pattern in CORE_DETAIL_PATTERNS.items():
                if pattern.search(value):
                    errors.append(
                        f"{owner} {field_name} 含{label}，请改为不泄露核心建模过程的阶段概括"
                    )


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
        if language_only and language_only not in {"是", "否"}:
            errors.append(f"{record_id} “是否仅用于语言润色”只能是“是”或“否”")
        if language_only != "是":
            for name in missing_fields(fields, REQUIRED_REVIEW):
                errors.append(f"{record_id} 非纯语言润色，缺少字段或值：{name}")

        human_edit = " ".join(fields.get("人工修改内容", [])).strip()
        human_basis = " ".join(fields.get("人工修改依据", [])).strip()
        if bool(human_edit) != bool(human_basis):
            errors.append(
                f"{record_id} 人工修改内容与人工修改依据必须同时填写或同时省略"
            )

        status = " ".join(fields.get("当前状态", []))
        if status and status not in {"记录中", "已归纳"}:
            errors.append(f"{record_id} 当前状态只能是“记录中”或“已归纳”")
        validate_public_content(record_id, fields, errors)

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
        validate_public_content(example_id, fields, errors)

    if mode == "finalize":
        for field_name, values in parse_fields(text).items():
            for value in values:
                if is_pending(value):
                    errors.append(f"最终生成前仍有待确认或占位内容：{field_name}")
        for record_id, block in records:
            fields = parse_fields(block)
            if " ".join(fields.get("当前状态", [])) != "已归纳":
                errors.append(f"{record_id} 尚未标记为“已归纳”")

    return list(dict.fromkeys(errors))


VALID_SAMPLE = """# AI 工具使用过程记录
## AI 工具目录
### TOOL-01
- 工具名称：MathModelAgent 桌面 Agent
- 版本或型号：运行环境未提供具体版本
## AI 使用记录
### AI-001
- 工具编号：TOOL-01
- 使用环节：代码复核
- 具体使用目的：检查边界条件
- 是否仅用于语言润色：否
- 主要提示方式：提供代码和约束，请列出边界风险
- 使用过程说明：生成检查清单后与实际产物逐项对照
- AI 输出采纳情况：经文件对照后选择性纳入最终稿
- 迭代修正情况：程序运行发现的问题已修正并重新生成相关产物
- 核验方法与结果：完成代码复现、异常检查和正文结果一致性核对，检查通过
- 对应证据文件或产物：tests/test_boundary.py
- 当前状态：已归纳
## 典型交互示例（可选）
### EX-001
- 对应记录：AI-001
- 代表性提示摘要：检查边界条件
- AI 输出摘要：列出三类风险
- 处理结果：与现有产物对照后，仅保留有运行记录支持的建议
"""


def self_test() -> int:
    language_sample = VALID_SAMPLE.replace(
        "- 是否仅用于语言润色：否", "- 是否仅用于语言润色：是"
    )
    language_sample = language_sample.replace(
        "- 迭代修正情况：程序运行发现的问题已修正并重新生成相关产物\n",
        "",
    )
    language_sample = language_sample.replace(
        "- 核验方法与结果：完成代码复现、异常检查和正文结果一致性核对，检查通过\n",
        "",
    )
    cases = [
        ("valid", VALID_SAMPLE, "finalize", False),
        ("language_only", language_sample, "finalize", False),
        (
            "pending",
            VALID_SAMPLE.replace("- 当前状态：已归纳", "- 当前状态：记录中"),
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
            VALID_SAMPLE.replace(
                "- 核验方法与结果：完成代码复现、异常检查和正文结果一致性核对，检查通过\n",
                "",
            ),
            "record",
            True,
        ),
        (
            "fabricated_human_claim",
            VALID_SAMPLE.replace("完成代码复现", "队员手工复算并完成代码复现"),
            "record",
            True,
        ),
        (
            "core_detail",
            VALID_SAMPLE.replace("检查边界条件", "检查 ARIMA 参数为 0.8 的结果"),
            "record",
            True,
        ),
        (
            "no_human_record_phrase",
            VALID_SAMPLE.replace("程序运行发现的问题已修正", "未记录到额外人工修改"),
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
