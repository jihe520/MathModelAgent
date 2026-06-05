= 问题一的模型建立与求解

== 数据预处理

采用 Z-score 标准化处理：$x' = frac(x - mu, sigma)$。

== 模型建立

采用多元线性回归作为基础模型：

$ y = theta_0 + theta_1 x_1 + theta_2 x_2 + dots.c + theta_n x_n + epsilon $ <eq-regression>

同时引入随机森林模型进行对比分析，通过集成多棵决策树提高精度和鲁棒性。

== 求解结果

随机森林的测试集 $R^2$ 达到 0.896，优于线性回归的 0.834。
