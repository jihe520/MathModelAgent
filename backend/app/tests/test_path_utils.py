"""Regression tests for task and file path validation."""

import tempfile
import unittest
from pathlib import Path

from app.utils.path_utils import (
    ensure_safe_path_component,
    ensure_safe_task_id,
    resolve_path_within,
)


class TestPathUtils(unittest.TestCase):
    """Verify that user-controlled path components cannot escape their base."""

    def test_safe_task_id_is_preserved(self):
        self.assertEqual(
            ensure_safe_task_id("20260721-120000-deadbeef"),
            "20260721-120000-deadbeef",
        )

    def test_task_id_path_traversal_is_rejected(self):
        invalid_task_ids = [
            "../task",
            "../../..",
            "/tmp/task",
            r"..\task",
            "",
        ]

        for task_id in invalid_task_ids:
            with self.subTest(task_id=task_id):
                with self.assertRaises(ValueError):
                    ensure_safe_task_id(task_id)

    def test_cross_platform_unsafe_components_are_rejected(self):
        invalid_components = [
            "../outside.csv",
            "folder/data.csv",
            r"..\outside.csv",
            r"C:\temp\data.csv",
            "C:data.csv",
            "/tmp/data.csv",
            ".",
            "..",
            "data\n.csv",
            "",
        ]

        for component in invalid_components:
            with self.subTest(component=component):
                with self.assertRaises(ValueError):
                    ensure_safe_path_component(component, "文件名")

    def test_valid_filename_resolves_inside_base_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir).resolve()
            resolved_path = resolve_path_within(base_dir, "数据 01.csv")

            self.assertEqual(resolved_path, base_dir / "数据 01.csv")
            self.assertEqual(resolved_path.parent, base_dir)

    def test_symlink_escape_is_rejected(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            tempfile.TemporaryDirectory() as outside_dir,
        ):
            outside_file = Path(outside_dir) / "outside.csv"
            outside_file.write_text("sensitive", encoding="utf-8")
            symlink_path = Path(temp_dir) / "data.csv"

            try:
                symlink_path.symlink_to(outside_file)
            except OSError as exc:
                self.skipTest(f"symlink creation is unavailable: {exc}")

            with self.assertRaises(ValueError):
                resolve_path_within(temp_dir, "data.csv")


if __name__ == "__main__":
    unittest.main()
