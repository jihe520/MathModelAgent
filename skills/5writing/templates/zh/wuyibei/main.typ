#set document(title: "[论文标题]", author: ())

#let song-font = ("SimSun", "Songti SC", "STSong", "Times New Roman")
#let hei-font = ("Heiti SC", "STHeiti", "SimSun")
#let kai-font = ("KaiTi", "Kaiti SC", "STKaiti", "SimSun")
#let code-font = ("YaHei Consolas Hybrid", "Monaco", "FiraCode Nerd Font")

#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  numbering: "1",
  footer: align(center)[#context counter(page).display()],
)
#set text(font: song-font, size: 12pt, lang: "zh")
#set par(
  first-line-indent: (amount: 2em, all: true),
  justify: true,
  leading: 0.95em,
  spacing: 0.75em,
)
#set enum(numbering: "1.", spacing: 0.78em)
#show figure.caption: it => text(size: 10pt)[#it]

#let cn-numbering(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("一、", ns.at(0))
  } else {
    numbering("1.1", ..ns)
  }
}
#set heading(numbering: cn-numbering)
#show heading.where(level: 1): it => block(
  width: 100%,
  above: 1.55em,
  below: 1.25em,
)[
  #align(center)[#text(font: hei-font, size: 15.5pt, weight: "bold")[#it]]
]
#show heading.where(level: 2): it => block(above: 1.18em, below: 0.95em)[
  #text(font: hei-font, size: 13pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.85em, below: 0.55em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]

#let bold = body => text(font: hei-font, weight: "bold", body)
#let center-title(body, size: 22pt) = align(center)[
  #text(font: hei-font, size: size, weight: "bold")[#body]
]
#let underline(width: 8cm) = box(width: width, baseline: -0.1em)[#line(
  length: 100%,
)]
#let filled-line(body, width: 8cm) = box(width: width, baseline: -0.1em)[
  #align(center)[#body]
  #line(length: 100%)
]
#let pledge-row(label, body, width: 10.6cm) = block(
  above: 0.78em,
  below: 0.34em,
)[
  #label#filled-line(body, width: width)
]
#let toc-entry(title, page, indent: 0pt, size: 12pt) = {
  grid(
    columns: (1fr, auto),
    column-gutter: 0.65em,
    align: (left, right),
    inset: 0pt,
    box(width: 100%)[#h(indent)#text(size: size)[#title]#h(0.45em)#box(
        width: 1fr,
      )[#line(length: 100%, stroke: (
        paint: black,
        thickness: 0.45pt,
        dash: "dotted",
      ))]],
    text(size: size)[#page],
  )
  v(0.62em)
}
#let appendix-title(body) = block(width: 100%, above: 0.95em, below: 0.75em)[
  #align(center)[#text(font: hei-font, size: 15pt, weight: "bold")[#body]]
]

#let three-line-table(caption, columns, header, body, inset: (x: 0.35em, y: 0.52em), cell-align: center) = {
  let col-count = header.len()
  let body-rows = calc.floor(body.len() / col-count)
  let bottom-y = body-rows + 1
  let styled-header = header.map(cell => strong(cell))

  block(width: 100%, breakable: false)[
    #align(center)[
      #box[
        #align(center)[#text(font: hei-font, size: 10.5pt, weight: "bold")[#caption]]
        #v(0.6em)
        #table(
          columns: columns,
          align: cell-align,
          stroke: none,
          inset: inset,
          table.hline(y: 0, stroke: 0.8pt),
          table.hline(y: 1, stroke: 0.5pt),
          table.hline(y: bottom-y, stroke: 0.8pt),
          ..styled-header,
          ..body,
        )
      ]
    ]
  ]
}

#counter(page).update(1)
#center-title([五一数学建模竞赛])
#v(0.72em)
#center-title([承 #h(0.95em) 诺 #h(0.95em) 书], size: 18pt)
#v(1.15em)

我们仔细阅读了五一数学建模竞赛的竞赛规则。我们完全明白，在竞赛开始后参赛队员不能以任何方式（包括电话、电子邮件、网上咨询等）与本队以外的任何人（包括指导教师）研究、讨论与赛题有关的问题。

我们知道，抄袭别人的成果是违反竞赛规则的, 如果引用别人的成果或其它公开的资料（包括网上查到的资料），必须按照规定的参考文献的表述方式在正文引用处和参考文献中明确列出。

我们郑重承诺，严格遵守竞赛规则，以保证竞赛的公正、公平性。如有违反竞赛规则的行为，我们愿意承担由此引起的一切后果。

我们授权五一数学建模竞赛组委会，可将我们的论文以任何形式进行公开展示（包括进行网上公示，在书籍、期刊和其他媒体进行正式或非正式发表等）。

#pledge-row([参赛题号（从A/B/C中选择一项填写）：], [], width: 8.1cm)
#pledge-row([参赛队号：], [], width: 12.2cm)
#pledge-row([参赛组别（研究生、本科、专科、高中）：], [], width: 7.4cm)
#pledge-row([所属学校（学校全称）：], [], width: 9.6cm)
#block(
  above: 0.7em,
  below: 0.2em,
)[参赛队员：队员1姓名：#filled-line([], width: 8.6cm)]
#block(
  above: 0.28em,
  below: 0.2em,
)[#h(4.3em)队员2姓名：#filled-line([], width: 8.6cm)]
#block(
  above: 0.28em,
  below: 0.2em,
)[#h(4.3em)队员3姓名：#filled-line([], width: 8.6cm)]
#block(
  above: 0.7em,
  below: 0.2em,
)[联系方式：Email：#underline(width: 4.1cm)#h(0.8em)联系电话：#underline(width: 4.1cm)]
#align(
  right,
)[日期：#underline(width: 1.1cm)年#underline(width: 1.1cm)月#underline(width: 1.1cm)日]
#v(0.65em)
#align(right)[#bold[（除本页外不允许出现学校及个人信息）]]

#pagebreak()
#center-title([五一数学建模竞赛])
#v(1em)
#align(center)[#image("image2.png", width: 2in)]
#v(1em)
#align(center)[#bold[题目：#filled-line([[论文标题]], width: 3.4cm)]]
#v(1em)
#block[#text(font: hei-font, weight: "bold", "关键词：") #text("[关键词1]")#h(
    0.8em,
  )#text("[关键词2]")#h(0.8em)#text("[关键词3]")#h(0.8em)#text("[关键词4]")#h(
    0.8em,
  )#text("[关键词5]")]
#v(0.55em)
#block[#bold[摘 #h(0.95em) 要：]]

[中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论。400-600字。每个子问题单独一段。]

#pagebreak()
#align(center)[#text(
  font: ("Times New Roman", "SimSun", "Songti SC"),
  size: 16pt,
  weight: "bold",
)[Contents]]
#v(1.2em)
#toc-entry([一、 问题重述], [4])
#toc-entry([1.1 问题背景], [4], indent: 2em)
#toc-entry([1.2 问题内容], [4], indent: 2em)
#toc-entry([二、 问题分析], [4])
#toc-entry([2.1 问题一分析], [4], indent: 2em)
#toc-entry([2.2 问题二分析], [4], indent: 2em)
#toc-entry([2.3 问题三分析], [4], indent: 2em)
#toc-entry([三、 模型假设], [4])
#toc-entry([四、 符号说明], [4])
#toc-entry([五、 问题一模型的建立和求解], [5])
#toc-entry([5.1 数据预处理], [5], indent: 2em)
#toc-entry([5.2 模型建立], [5], indent: 2em)
#toc-entry([5.3 求解结果], [5], indent: 2em)
#toc-entry([六、 问题二模型的建立和求解], [5])
#toc-entry([6.1 特征选择], [5], indent: 2em)
#toc-entry([6.2 模型优化], [5], indent: 2em)
#toc-entry([七、 问题三模型的建立和求解], [6])
#toc-entry([7.1 优化模型], [6], indent: 2em)
#toc-entry([7.2 算法求解], [6], indent: 2em)
#toc-entry([7.3 结果], [6], indent: 2em)
#toc-entry([八、 模型评价与推广], [6])
#toc-entry([8.1 模型优点], [6], indent: 2em)
#toc-entry([8.2 模型缺点], [6], indent: 2em)
#toc-entry([8.3 推广], [6], indent: 2em)
#toc-entry([A Appendix 文件列表], [7])
#toc-entry([B Appendix 代码], [7])
#toc-entry([C Appendix 核心代码], [7])

#pagebreak()
= 问题重述
== 问题背景
数学建模是解决实际问题的重要工具。本文研究的问题涉及多维度数据分析与优化决策。

== 问题内容
#par(
  first-line-indent: 2em,
)[#bold[问题一：] 对给定数据集进行分析和预测，要求模型具有泛化能力。]
#v(0.55em)
#par(
  first-line-indent: 2em,
)[#bold[问题二：] 考虑多因素影响，改进和优化模型，提高预测精度。]
#v(0.55em)
#par(
  first-line-indent: 2em,
)[#bold[问题三：] 结合实际约束条件，设计最优策略方案。]

= 问题分析
== 问题一的分析
问题一的关键在于特征工程和模型选择，数据中同时存在线性和非线性特征。
#v(0.55em)

== 问题二的分析
问题二涉及多变量分析和模型融合技术，需要识别主要影响因素。
#v(0.55em)

== 问题三的分析
问题三是约束优化问题，需要建立目标函数和约束条件。
#v(0.55em)

= 模型假设
为简化问题，本文做出以下基本假设：
#set enum(numbering: "1.", spacing: 0.75em)
+ 假设题目所给数据真实可靠，不存在系统性的测量误差；
+ 假设各因素之间的交互作用可以忽略不计；
+ 假设系统在短期内处于稳定状态；
+ 假设所有变量连续可微；
+ 假设缺失值为随机缺失，可采用插补方法处理。

= 符号说明
#pagebreak()
#v(-0.55cm)
#align(center)[#text(
  font: ("Times New Roman", "SimSun", "Songti SC"),
  size: 10.5pt,
)[Table 1 主要符号说明]]
#align(center)[
  #table(
    columns: (3cm, 1fr, 3cm),
    align: (center, center, center),
    stroke: (_, y) => if y == 0 {
      (top: 1.4pt, bottom: 0.75pt)
    } else if y == 5 {
      (bottom: 1.4pt)
    } else { none },
    inset: 5pt,
    [符号], [含义], [单位],
    [$N$], [样本数量], [个],
    [$M$], [特征维度], [维],
    [$X$], [特征矩阵], [—],
    [$y$], [目标变量], [—],
    [$R^2$], [决定系数], [—],
  )
]

= 问题一模型的建立和求解
== 数据预处理
采用 Z-score 标准化处理：$x' = (x - mu) / sigma$。

== 模型建立
采用多元线性回归作为基础模型：

#align(
  center,
)[$y = theta_0 + theta_1 x_1 + theta_2 x_2 + dots.c + theta_n x_n + epsilon$ #h(2em) (1)]

同时引入随机森林模型进行对比分析，通过集成多棵决策树提高精度和鲁棒性。

== 求解结果
随机森林的测试集 $R^2$ 达到 0.896，优于线性回归的 0.834。

= 问题二模型的建立和求解
== 特征选择
采用 LASSO 回归筛选关键特征：

#align(
  center,
)[$min_(theta) (1 / (2 N)) sum_(i=1)^N (y_i - theta^T x_i)^2 + lambda ||theta||_1$ #h(2em) (2)]

== 模型优化
基于筛选的关键特征建立优化预测模型，引入交叉项捕捉交互效应。优化后测试集 $R^2$ 从 0.896 提升至 0.923，RMSE 降低约 15%。

#pagebreak()
= 问题三模型的建立和求解
== 优化模型
将问题建模为约束优化问题：

#align(center)[$min f(bold(x)) = sum_(i=1)^n c_i (x_i)$ #h(2em) (3)]
#align(
  center,
)[$"s.t." quad g_j(bold(x)) <= 0, quad h_k(bold(x)) = 0$ #h(2em) (4)]

== 算法求解
采用遗传算法（种群规模 200，迭代 100 代）进行求解，算法快速收敛到稳定解。

== 结果
得到最优策略方案：$x_1 = 0.75$，$x_2 = 1.20$，$x_3 = 0.45$，$x_4 = 0.88$。

= 模型评价与推广
== 模型优点
#set enum(numbering: "1.", spacing: 0.55em)
+ 理论基础扎实，推导严谨；
+ 多模型对比确保最优性；
+ 可解释性强，计算效率高。

== 模型缺点
+ 对数据质量有一定要求；
+ 未考虑时间动态性。

== 推广
可推广至金融风控、工业生产、智能交通和能源管理等领域。

#pagebreak()
#appendix-title([Appendix A #h(0.6em) 文件列表])
#align(center)[#text(
  font: ("Times New Roman", "SimSun", "Songti SC"),
  size: 10.5pt,
)[Table 2 文件列表]]
#align(center)[
  #table(
    columns: (4cm, 1fr),
    align: (center, center),
    stroke: (_, y) => if y == 0 {
      (top: 1.4pt, bottom: 0.75pt)
    } else if y == 1 {
      (bottom: 1.4pt)
    } else { none },
    inset: 5pt,
    [文件名], [文件描述],
    [main.py], [主程序],
  )
]

#appendix-title([Appendix B #h(0.6em) 代码])
#appendix-title([Appendix C #h(0.6em) 核心代码])
#let code-line(n, body) = grid(
  columns: (1.4em, 1fr),
  column-gutter: 0.65em,
  align: (right, left),
  text(font: code-font, size: 8.8pt)[#n],
  text(font: code-font, size: 8.8pt)[#body],
)
#block(inset: 0pt, radius: 0pt)[
  #set text(font: code-font, size: 8.8pt)
  #code-line(1, [import numpy as np])
  #code-line(2, [import pandas as pd])
  #code-line(3, [from sklearn.ensemble import RandomForestRegressor])
  #code-line(4, [from sklearn.model_selection import train_test_split])
  #code-line(5, [from sklearn.metrics import r2_score])
  #code-line(6, [])
  #code-line(7, [data = pd.read_csv('data.csv')])
  #code-line(8, [X = data.drop('target', axis=1); y = data['target']])
  #code-line(9, [X_train, X_test, y_train, y_test = train_test_split(])
  #code-line(10, [X, y, test_size=0.2, random_state=42])
  #code-line(11, [)])
  #code-line(
    12,
    [model = RandomForestRegressor(n_estimators=100, random_state=42)],
  )
  #code-line(13, [model.fit(X_train, y_train)])
  #code-line(14, [print(f'R2: {r2_score(y_test, model.predict(X_test)):.4f}')])
]
