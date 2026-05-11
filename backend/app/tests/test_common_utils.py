"""通用工具函数单元测试。"""

import unittest

from app.utils.common_utils import split_footnotes


class TestCommonUtils(unittest.TestCase):
    """测试 common_utils 模块的核心函数。"""

    def test_split_footnotes(self):
        """测试脚注分离功能。"""
        text = "Example[^1]\n\n[^1]: Footnote content"
        main, notes = split_footnotes(text)
        self.assertEqual(main, "Example")
        self.assertEqual(notes, [("1", "Footnote content")])


if __name__ == "__main__":
    unittest.main()
