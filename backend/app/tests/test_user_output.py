"""UserOutput 的引用收集与参考文献拼接行为测试。"""

import unittest

from app.models.user_output import UserOutput
from app.schemas.A2A import WriterResponse


def _response(content: str) -> WriterResponse:
    return WriterResponse(response_content=content, footnotes=[])


class ReferencesFlowTests(unittest.TestCase):
    """参考文献链路：引用收集 → 编号 → 文末参考文献节。"""

    def _filled_output(self, sections: dict[str, str]) -> UserOutput:
        """构造覆盖 seq 全部章节 key 的 UserOutput（缺 key 拼接时 KeyError）。"""
        output = UserOutput(work_dir=".", ques_count=1)
        for key in output.seq:
            output.set_res(key, _response(sections.get(key, f"{key} 正文。")))
        return output

    def test_citation_with_colon_is_collected(self):
        """带冒号格式 {[^1]: 引用} 必须被收集为参考文献条目。"""
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

    def test_citation_without_colon_is_collected(self):
        """不带冒号的 {[^1] 引用} 写法同样收集（历史提示词格式）。"""
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

    def test_references_heading_is_flush_and_entries_are_plain(self):
        """标题必须顶格（行首空格使严格渲染器不识别为标题）；
        条目用 [n] 文本而非 [^n]: 脚注定义（不支持的渲染器会整节丢弃）。"""
        output = self._filled_output(
            {"ques1": "本文方法借鉴了已有研究{[^1]: 王五. 方法综述[J]. 数学, 2022.}。"}
        )
        result = output.get_result_to_save()

        self.assertIn("\n# 参考文献", result)
        self.assertNotIn(" ## 参考文献", result)
        self.assertIn("\n\n[1] 王五. 方法综述[J]. 数学, 2022", result)
        self.assertNotIn("[^1]:", result)
        self.assertIn("已有研究[1]。", result)

    def test_duplicate_citation_reuses_number(self):
        """同一文献多处引用去重：正文复用同一编号，列表只出现一次。"""
        output = self._filled_output(
            {
                "analysisQues": "方法见文献{[^1]: 张三. 抽样检验研究[J]. 统计, 2024.}。",
                "ques1": (
                    "再次沿用该文献{[^2]: 张三. 抽样检验研究[J]. 统计, 2024}求解。"
                ),
            }
        )
        result = output.get_result_to_save()

        self.assertIn("方法见文献[1]。", result)
        self.assertIn("再次沿用该文献[1]求解。", result)
        self.assertEqual(result.count("\n\n[1] 张三"), 1)
        self.assertNotIn("\n\n[2]", result)


if __name__ == "__main__":
    unittest.main()
