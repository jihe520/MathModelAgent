"""UserOutput、通用工具与安全函数单元测试。"""

import unittest
from app.models.user_output import UserOutput
from app.schemas.A2A import WriterResponse
from app.utils.common_utils import ensure_safe_task_id, get_work_dir
from app.routers.modeling_router import normalize_base_url


def _response(content: str) -> WriterResponse:
    return WriterResponse(response_content=content, footnotes=[])


class UserOutputReferencesTests(unittest.TestCase):
    """参考文献处理链路测试：引用解析、格式化、编号复用与章节顶格。"""

    def _filled_output(self, sections: dict[str, str]) -> UserOutput:
        output = UserOutput(work_dir=".", ques_count=1)
        for key in output.seq:
            output.set_res(key, _response(sections.get(key, f"{key} 正文。")))
        return output

    def test_citation_with_colon_is_collected(self):
        """带冒号格式 {[^1]: 引用} 应被正确收集并转为 [1]。"""
        output = self._filled_output(
            {
                "analysisQues": (
                    "抽样检验采用精确概率枚举"
                    "{[^1]: 张三. 抽样检验研究[J]. 统计, 2024.}完成方案设计。"
                )
            }
        )
        result = output.get_result_to_save()
        self.assertIn("[1] 张三. 抽样检验研究[J]. 统计, 2024", result)
        self.assertNotIn("{[^1]", result)
        self.assertIn("抽样检验采用精确概率枚举[1]完成方案设计。", result)

    def test_citation_without_colon_is_collected(self):
        """不带冒号格式 {[^1] 引用} 也应被兼容收集。"""
        output = self._filled_output(
            {
                "analysisQues": (
                    "马尔可夫递推{[^2] 李四. 递推模型分析[J]. 应用数学, 2023.}适用于该场景。"
                )
            }
        )
        result = output.get_result_to_save()
        self.assertIn("[1] 李四. 递推模型分析[J]. 应用数学, 2023", result)
        self.assertNotIn("{[^2]", result)
        self.assertIn("马尔可夫递推[1]适用于该场景。", result)

    def test_references_heading_is_flush(self):
        """参考文献标题必须顶格输出 '# 参考文献'。"""
        output = self._filled_output(
            {"ques1": "参考已有研究{[^1]: 王五. 方法综述[J]. 数学, 2022.}。"}
        )
        result = output.get_result_to_save()
        self.assertIn("\n# 参考文献", result)
        self.assertNotIn(" ## 参考文献", result)
        self.assertIn("\n\n[1] 王五. 方法综述[J]. 数学, 2022", result)

    def test_duplicate_citation_reuses_number(self):
        """同一文献跨章节重复引用时应复用编号。"""
        output = self._filled_output(
            {
                "analysisQues": "方法见文献{[^1]: 张三. 抽样检验研究[J]. 统计, 2024.}。",
                "ques1": "再次沿用该文献{[^2]: 张三. 抽样检验研究[J]. 统计, 2024}求解。",
            }
        )
        result = output.get_result_to_save()
        self.assertIn("方法见文献[1]。", result)
        self.assertIn("再次沿用该文献[1]求解。", result)
        self.assertEqual(result.count("\n\n[1] 张三"), 1)
        self.assertNotIn("\n\n[2]", result)


class SecurityAndUtilsTests(unittest.TestCase):
    """安全与工具函数测试。"""

    def test_safe_task_id_validation(self):
        """确保非法 task_id 会被安全拦截。"""
        self.assertEqual(ensure_safe_task_id("task-123_456"), "task-123_456")

        invalid_ids = ["../../etc/passwd", "..\\..\\win.ini", "task/id", "task;rm", ""]
        for invalid_id in invalid_ids:
            with self.assertRaises(ValueError):
                ensure_safe_task_id(invalid_id)

    def test_get_work_dir_rejects_path_traversal(self):
        """get_work_dir 必须拦截路径遍历尝试。"""
        with self.assertRaises(ValueError):
            get_work_dir("../../secret")

    def test_normalize_base_url(self):
        """测试 base_url 自动去除末尾端点后缀。"""
        self.assertEqual(
            normalize_base_url("https://api.deepseek.com/v1/chat/completions"),
            "https://api.deepseek.com/v1",
        )
        self.assertEqual(
            normalize_base_url("https://api.deepseek.com/v1/chat/completions/"),
            "https://api.deepseek.com/v1",
        )
        self.assertEqual(
            normalize_base_url("https://api.deepseek.com/v1/"),
            "https://api.deepseek.com/v1",
        )
        self.assertIsNone(normalize_base_url(None))
        self.assertIsNone(normalize_base_url("   "))


if __name__ == "__main__":
    unittest.main()
