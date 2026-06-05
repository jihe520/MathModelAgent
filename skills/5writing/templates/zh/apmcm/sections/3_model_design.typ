// Section 3
= 模型设计与方法

== 整体框架

整体建模包括数据预处理、模型构建和模型评估三个主要阶段。

== 核心模型

$ hat(y) = f(bold(x); theta) = sum_(i=1)^n theta_i phi_i(bold(x)) $

模型参数的优化目标是最小化正则化损失函数：

$
  cal(L)(theta) = frac(1, N) sum_(i=1)^N (y_i - hat(y)_i)^2 + lambda norm(theta)_2^2
$
