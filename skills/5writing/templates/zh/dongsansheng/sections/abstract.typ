#align(center)[#text(size: 14pt, weight: "bold")[[论文题目]]]
#v(0.65em)
#align(center)[#text(size: 14pt, weight: "bold")[摘 #h(1em) 要]]

本文针对数学建模竞赛题目，建立了完整的数学模型体系。
问题一采用多元线性回归和随机森林进行对比分析，随机森林的测试集 $R^2$ 达到 0.896。
问题二采用 LASSO 回归筛选关键特征，优化后 $R^2$ 提升至 0.923。
问题三采用遗传算法求解约束优化问题，得到最优策略方案。
经敏感性分析验证，模型具有较强的鲁棒性。

#v(0.6em)
#block[
  #set par(first-line-indent: 0pt)
  #text(font: ("Heiti SC", "STHeiti", "Songti SC"), weight: "bold")[关键词：] 数据预测；随机森林；LASSO 回归；遗传算法；约束优化
]
