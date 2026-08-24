#!/usr/bin/env python3
"""Regression tests for the 7ai-disclosure validator and renderer."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from generate_ai_usage_pdf import GenerationError, compile_pdf, parse_log, render_tex
from validate_ai_usage_log import validate

FIXTURE_PATH = (
    Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "valid_multi_tool.md"
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

    def test_rendered_tex_has_four_sections_and_no_template_markers(self) -> None:
        tex_path = self.root / "supporting_materials" / "AI 工具使用详情.tex"
        render_tex(self.log_path, self.template, tex_path)
        text = tex_path.read_text(encoding="utf-8")
        self.assertNotIn("%%__", text)
        self.assertNotIn("待队员确认", text)
        self.assertIn(r"Claude Code \& MathModelAgent", text)
        self.assertIn(r"x\_1 \% 边界", text)
        self.assertIn("AI-001", text)
        self.assertIn("EX-001", text)
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

    def test_pending_confirmation_blocks_generation(self) -> None:
        pending = VALID_MULTI_TOOL_LOG.replace(
            "- 当前状态：已确认", "- 当前状态：待队员确认", 1
        )
        self.log_path.write_text(pending, encoding="utf-8")
        with self.assertRaises(GenerationError):
            render_tex(self.log_path, self.template, self.root / "out.tex")

    def test_non_contiguous_tool_ids_fail_validation(self) -> None:
        invalid = VALID_MULTI_TOOL_LOG.replace("TOOL-02", "TOOL-03")
        self.log_path.write_text(invalid, encoding="utf-8")
        errors = validate(self.log_path, "record")
        self.assertIn("工具编号必须从 1 开始连续递增", errors)

    def test_missing_compilers_fail_with_actionable_error(self) -> None:
        tex_path = self.root / "AI 工具使用详情.tex"
        tex_path.write_text("test", encoding="utf-8")
        with (
            patch("generate_ai_usage_pdf.shutil.which", return_value=None),
            self.assertRaisesRegex(GenerationError, "缺少 PDF 编译器"),
        ):
            compile_pdf(tex_path)


if __name__ == "__main__":
    unittest.main()
