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
    "Bearer 令牌": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{12,}", re.I),
    "环境变量密钥": re.compile(r"\b[A-Z][A-Z0-9_]*(?:API_KEY|TOKEN|SECRET)\s*=\s*\S+"),
}

REQUIRED_HEADINGS = (
    "基本信息",
    "AI 工具目录",
    "分阶段使用记录",
    "典型交互示例",
    "未采纳的重要 AI 建议或结果",
    "最终确认",
)
REQUIRED_BASIC = ("竞赛名称", "赛题编号或名称", "参赛队号", "记录起止时间")
REQUIRED_TOOL = ("工具名称", "提供方", "版本或模型", "使用入口或方式", "信息来源及确认状态")
REQUIRED_RECORD = (
    "使用阶段",
    "工具编号",
    "使用目的",
    "主要提示方式或代表性提示摘要",
    "使用过程摘要",
    "AI 输出采纳情况",
    "人工修改内容",
    "人工核验方法与结果",
    "对应证据文件或产物",
    "负责确认的队员",
    "当前状态",
)
REQUIRED_FINAL = (
    "核心建模与分析由参赛队主导",
    "所有记录已逐项人工审查",
    "仍有待核实内容",
    "队员确认",
)


def parse_fields(text: str) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*-\s*([^：:]+)[：:]\s*(.*?)\s*$", line)
        if match:
            fields.setdefault(match.group(1).strip(), []).append(match.group(2).strip())
    return fields


def sections_by_id(text: str, pattern: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(pattern, text, flags=re.M))
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((match.group(1), text[match.end() : end]))
    return result


def missing_fields(fields: dict[str, list[str]], required: tuple[str, ...]) -> list[str]:
    return [name for name in required if name not in fields or not any(fields[name])]


def is_pending(value: str) -> bool:
    return not value.strip() or any(marker.casefold() in value.casefold() for marker in PENDING_MARKERS) or bool(
        re.search(r"【[^】]*】", value)
    )


def validate(path: Path, mode: str) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"日志不存在：{path}"]
    text = path.read_text(encoding="utf-8-sig")

    for name in REQUIRED_HEADINGS:
        if not re.search(rf"^##\s+{re.escape(name)}\s*$", text, flags=re.M):
            errors.append(f"缺少二级标题：{name}")

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"检测到疑似{label}，请删除或脱敏")

    fields = parse_fields(text)
    for name in missing_fields(fields, REQUIRED_BASIC):
        errors.append(f"基本信息缺少字段或值：{name}")
    for name in missing_fields(fields, REQUIRED_FINAL):
        errors.append(f"最终确认缺少字段或值：{name}")

    tools = sections_by_id(text, r"^###\s+(TOOL-\d+)\s*$")
    records = sections_by_id(text, r"^###\s+(AI-\d+)\s*$")
    tool_ids = [item_id for item_id, _ in tools]
    record_ids = [item_id for item_id, _ in records]

    if len(tool_ids) != len(set(tool_ids)):
        errors.append("AI 工具编号重复")
    if len(record_ids) != len(set(record_ids)):
        errors.append("阶段记录编号重复")
    if not tools:
        errors.append("至少需要一个 TOOL-xx 工具条目")
    if not records:
        errors.append("至少需要一个 AI-xxx 阶段记录")

    for tool_id, block in tools:
        tool_fields = parse_fields(block)
        for name in missing_fields(tool_fields, REQUIRED_TOOL):
            errors.append(f"{tool_id} 缺少字段或值：{name}")

    for record_id, block in records:
        record_fields = parse_fields(block)
        for name in missing_fields(record_fields, REQUIRED_RECORD):
            errors.append(f"{record_id} 缺少字段或值：{name}")
        refs = record_fields.get("工具编号", [])
        referenced = re.findall(r"TOOL-\d+", " ".join(refs))
        if not referenced:
            errors.append(f"{record_id} 未引用 TOOL-xx")
        for ref in referenced:
            if ref not in tool_ids:
                errors.append(f"{record_id} 引用了不存在的工具：{ref}")
        status = " ".join(record_fields.get("当前状态", []))
        if status and status not in {"已确认", "待队员确认"}:
            errors.append(f"{record_id} 当前状态只能是“已确认”或“待队员确认”")

    if mode == "finalize":
        for field_name, values in fields.items():
            for value in values:
                if is_pending(value):
                    errors.append(f"最终生成前仍有待确认或占位内容：{field_name}")
        for record_id, block in records:
            status = " ".join(parse_fields(block).get("当前状态", []))
            if status != "已确认":
                errors.append(f"{record_id} 尚未标记为“已确认”")
        final_values = {name: fields.get(name, [""])[-1].strip() for name in REQUIRED_FINAL}
        if final_values["核心建模与分析由参赛队主导"] != "是":
            errors.append("最终确认必须明确“核心建模与分析由参赛队主导：是”")
        if final_values["所有记录已逐项人工审查"] != "是":
            errors.append("最终确认必须明确“所有记录已逐项人工审查：是”")
        if final_values["仍有待核实内容"] != "否":
            errors.append("最终确认必须明确“仍有待核实内容：否”")
        if not final_values["队员确认"] or is_pending(final_values["队员确认"]):
            errors.append("缺少有效的队员确认")

    return list(dict.fromkeys(errors))


VALID_SAMPLE = """# AI 工具使用过程记录
## 基本信息
- 竞赛名称：全国大学生数学建模竞赛
- 赛题编号或名称：A 题
- 参赛队号：20260001
- 记录起止时间：2026-09-10 至 2026-09-13
## AI 工具目录
### TOOL-01
- 工具名称：示例工具
- 提供方：示例提供方
- 版本或模型：示例模型 1
- 使用入口或方式：网页端
- 信息来源及确认状态：界面显示，已确认
## 分阶段使用记录
### AI-001
- 使用阶段：代码复核
- 工具编号：TOOL-01
- 使用目的：检查边界条件
- 主要提示方式或代表性提示摘要：给出代码和约束，请列出边界风险
- 使用过程摘要：模型给出检查清单，队员逐项验证
- AI 输出采纳情况：部分采纳
- 人工修改内容：删除不适用建议并补充测试
- 人工核验方法与结果：运行边界测试，全部通过
- 对应证据文件或产物：tests/test_boundary.py
- 负责确认的队员：队员甲
- 当前状态：已确认
## 典型交互示例
### EX-001
- 对应记录：AI-001
- 代表性提示摘要：检查边界条件
- AI 结果摘要：列出三类风险
- 队员处理：逐项测试后采纳两项
## 未采纳的重要 AI 建议或结果
- 建议更换模型，经对比后未采纳
## 最终确认
- 核心建模与分析由参赛队主导：是
- 所有记录已逐项人工审查：是
- 仍有待核实内容：否
- 队员确认：队员甲、队员乙、队员丙已共同确认
"""


def self_test() -> int:
    cases = [
        ("valid", VALID_SAMPLE, "finalize", False),
        ("pending", VALID_SAMPLE.replace("队员甲、队员乙、队员丙已共同确认", "待队员确认"), "finalize", True),
        ("bad_ref", VALID_SAMPLE.replace("- 工具编号：TOOL-01", "- 工具编号：TOOL-99"), "record", True),
        ("secret", VALID_SAMPLE + "\n- 备注：sk-abcdefghijklmnopqrstuvwxyz\n", "record", True),
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
