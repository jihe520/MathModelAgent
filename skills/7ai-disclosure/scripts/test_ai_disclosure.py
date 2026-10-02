#!/usr/bin/env python3
"""Regression tests for the 7ai-disclosure validator and renderer."""

from __future__ import annotations

import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

from generate_ai_usage_pdf import GenerationError, compile_pdf, parse_log, render_tex
from validate_ai_usage_log import validate

FIXTURE_PATH = (
    Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "valid_multi_tool.md"
)
TEMPLATE_LOG_PATH = (
    Path(__file__).resolve().parents[1] / "templates" / "AI_USAGE_LOG.md"
)
VALID_MULTI_TOOL_LOG = FIXTURE_PATH.read_text(encoding="utf-8")


class DisclosureGenerationTests(unittest.TestCase):
    """Verify stable mapping, safety gates, and LaTeX rendering."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.log_path = self.root / "AI_USAGE_LOG.md"
        self.log_path.write_text(VALID_MULTI_TOOL_LOG, encoding="utf-8")
        self.template = (
            Path(__file__).resolve().parents[1] / "templates" / "AI工具使用详情模板.tex"
        )

    def test_final_log_is_valid_and_ids_map_to_records(self) -> None:
        self.assertEqual(validate(self.log_path, "finalize"), [])
        data = parse_log(self.log_path)
        self.assertEqual([tool.tool_id for tool in data.tools], ["TOOL-01", "TOOL-02"])
        self.assertEqual(data.records[0].tool_ids, ("TOOL-01",))
        self.assertEqual(data.examples[0].record_ids, ("AI-001",))

    def test_initial_template_passes_record_mode_only(self) -> None:
        record_errors = validate(TEMPLATE_LOG_PATH, "record")
        final_errors = validate(TEMPLATE_LOG_PATH, "finalize")
        self.assertEqual(record_errors, [])
        self.assertTrue(any("占位内容" in error for error in final_errors))
        self.assertTrue(any("尚未标记为“已归纳”" in error for error in final_errors))

    def test_rendered_tex_has_four_sections_and_no_template_markers(self) -> None:
        tex_path = self.root / "supporting_materials" / "AI 工具使用详情.tex"
        render_tex(self.log_path, self.template, tex_path)
        text = tex_path.read_text(encoding="utf-8")
        self.assertNotIn("%%__", text)
        self.assertNotIn("待队员确认", text)
        self.assertIn("MathModelAgent 桌面 Agent", text)
        self.assertIn("运行环境未提供具体版本", text)
        self.assertIn("AI-001", text)
        self.assertIn("EX-001", text)
        self.assertIn("迭代修正：", text)
        self.assertIn("核验情况：", text)
        self.assertNotIn("人工修改：", text)
        self.assertNotIn("人工核验：", text)
        self.assertNotIn("未记录到额外人工修改", text)
        self.assertIn("一、所用 AI 工具名称、版本或型号", text)
        self.assertIn("四、对 AI 输出的采纳、人工修改和核验的主要情况", text)

    def test_language_polishing_is_excluded_from_part_four(self) -> None:
        tex_path = self.root / "AI 工具使用详情.tex"
        render_tex(self.log_path, self.template, tex_path)
        part_four = tex_path.read_text(encoding="utf-8").split(
            "四、对 AI 输出的采纳、人工修改和核验的主要情况", 1
        )[1]
        self.assertIn("AI-001", part_four)
        self.assertNotIn("AI-002", part_four)

    def test_in_progress_record_blocks_generation(self) -> None:
        pending = VALID_MULTI_TOOL_LOG.replace(
            "- 当前状态：已归纳", "- 当前状态：记录中", 1
        )
        self.log_path.write_text(pending, encoding="utf-8")
        with self.assertRaises(GenerationError):
            render_tex(self.log_path, self.template, self.root / "out.tex")

    def test_core_model_detail_is_rejected(self) -> None:
        unsafe = VALID_MULTI_TOOL_LOG.replace(
            "检查实现完整性", "检查 ARIMA 参数为 0.8 的实现完整性"
        )
        self.log_path.write_text(unsafe, encoding="utf-8")
        errors = validate(self.log_path, "finalize")
        self.assertTrue(any("核心建模过程" in error for error in errors))

    def test_optional_evidenced_human_edit_is_rendered(self) -> None:
        with_human_edit = VALID_MULTI_TOOL_LOG.replace(
            "- 对应证据文件或产物：reports/VERIFY_REPORT.md",
            "- 人工修改内容：根据明确反馈调整了章节顺序\n"
            "- 人工修改依据：当前会话中的明确修改要求\n"
            "- 对应证据文件或产物：reports/VERIFY_REPORT.md",
        )
        self.log_path.write_text(with_human_edit, encoding="utf-8")
        tex_path = self.root / "AI 工具使用详情.tex"
        render_tex(self.log_path, self.template, tex_path)
        text = tex_path.read_text(encoding="utf-8")
        self.assertIn("人工修改：", text)
        self.assertIn("根据明确反馈调整了章节顺序", text)

    def test_forbidden_no_human_record_phrase_is_rejected(self) -> None:
        unsafe = VALID_MULTI_TOOL_LOG.replace(
            "程序运行发现的问题已修正，并重新生成相关产物",
            "未记录到额外人工修改",
        )
        self.log_path.write_text(unsafe, encoding="utf-8")
        errors = validate(self.log_path, "finalize")
        self.assertTrue(any("禁止的无人工记录提示" in error for error in errors))

    def test_non_contiguous_tool_ids_fail_validation(self) -> None:
        invalid = VALID_MULTI_TOOL_LOG.replace("TOOL-02", "TOOL-03")
        self.log_path.write_text(invalid, encoding="utf-8")
        errors = validate(self.log_path, "record")
        self.assertIn("工具编号必须从 1 开始连续递增", errors)

    def test_missing_compilers_fail_with_actionable_error(self) -> None:
        tex_path = self.root / "AI 工具使用详情.tex"
        tex_path.write_text("test", encoding="utf-8")
        with ExitStack() as stack:
            stack.enter_context(
                patch("generate_ai_usage_pdf.shutil.which", return_value=None)
            )
            stack.enter_context(
                self.assertRaisesRegex(GenerationError, "缺少 PDF 编译器")
            )
            compile_pdf(tex_path)


if __name__ == "__main__":
    unittest.main()
