#set document(title: "论文的题目（三号黑体）", author: ())

#let song-font = ("Songti SC", "STSong", "Times New Roman")
#let hei-font = ("Heiti SC", "STHeiti", "Songti SC")
#let mono-font = ("Ubuntu Mono", "Courier New")
#let red-note(body) = body
#let blue-note(body) = body
#let hei(body, size: 12pt) = text(
  font: hei-font,
  weight: "bold",
  size: size,
)[#body]
#let dots = [......]
#let cn-heading-number(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("一、", ns.at(0))
  } else {
    numbering("1.1", ..ns)
  }
}

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

#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 25mm, right: 25mm),
  numbering: none,
)
#set text(font: song-font, size: 12pt, lang: "zh")
#set par(
  first-line-indent: 2em,
  justify: true,
  leading: 0.83em,
  spacing: 0.12em,
)
#set enum(numbering: "1.", spacing: 0.18em)
#show figure.caption: it => text(size: 9pt)[#it]

#align(center)[
  #v(27mm)
  #hei([2026 第十届“数维杯”大学生], size: 25pt)\
  #hei([数学建模挑战赛论文], size: 25pt)
]

#v(14mm)
#grid(
  columns: (70pt, 1fr),
  align: (center, horizon),
  column-gutter: 18pt,
  [#hei([题 #h(1.2em) 目], size: 14pt)],
  [
    #align(center)[#hei([论文的题目（三号黑体）], size: 16pt)]
    #line(length: 100%, stroke: 1.1pt)
  ],
)

#v(14mm)
#align(center)[#hei([摘 #h(2em) 要], size: 15pt)]

#v(9mm)
#set text(size: 11.2pt)
#set par(
  first-line-indent: 2em,
  justify: true,
  leading: 1.02em,
  spacing: 0.46em,
)

[中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论]

#v(1.4em)
#par(first-line-indent: 0pt)[
  #hei([关键词：], size: 12pt)关键词1；关键词2；关键词3
]

#pagebreak()

#set page(numbering: none)
#align(center)[#v(22mm)#text(size: 18pt, font: hei-font, weight: "bold")[目录]]
#v(1.5em)
#outline(title: none, depth: 3)

#pagebreak()
#counter(page).update(1)
#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 25mm, right: 25mm),
  numbering: "1",
  header: [
    #grid(
      columns: (1fr, auto),
      align: (left, right),
      [#text(
        size: 10pt,
      )[Team \# 2024000000001 ]],
      [#text(size: 10pt)[Page #context counter(page).display() of ??]],
    )
    #line(length: 100%, stroke: 0.45pt)
  ],
  footer: align(center)[#text(size: 9pt)[#context counter(page).display()]],
)
#set text(font: song-font, size: 12pt, lang: "zh")
#set par(
  first-line-indent: (amount: 2em, all: true),
  justify: true,
  leading: 1.24em,
  spacing: 0.42em,
)
#set heading(numbering: cn-heading-number)
#set enum(numbering: "1.", spacing: 0.72em)
#show heading.where(level: 1): it => block(above: 1.35em, below: 0.82em)[
  #text(font: hei-font, size: 16pt, weight: "bold")[#it]
]
#show heading.where(level: 2): it => block(above: 1.08em, below: 0.82em)[
  #text(font: song-font, size: 15pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.92em, below: 0.62em)[
  #text(font: song-font, size: 13.5pt, weight: "bold")[#it]
]

= 问题重述
== 引言

== 要解决的具体问题

+ [问题一：问题一的重述]
+ [问题二：问题二的重述]
+ [问题三：问题三的重述]

= 问题分析

== 问题一的分析

== 问题二的分析

#dots

= 模型假设

+ 模型的假设要结合整个模型的建立作出的一个合理的假设，不能过于理想化，要尽量切合实际问题的处理来做出相应的合理的假设；
+ 模型假设二；
+ 模型假设三；

= 名词解释与符号说明

== 名词解释与说明

+ #strong[理论通行能力：]理论通行能力是指每一条车道（或每一条道路）在单位时间内能够通过的最大交通量。

#figure(
  rect(
    width: 95pt,
    height: 95pt,
    fill: gray.lighten(75%),
    stroke: gray + 0.6pt,
  )[
    #align(center + horizon)[#text(size: 10pt)[公众号图]]
  ],
  caption: [图 1，示例图片],
)

#par(first-line-indent: 2em)[
  关于插图、绘图、表格以及公式等相关资源请点击 
]

+ #strong[修正通行能力：]在具体条件下，通过修正系数对理论通行能力修正后得到的单位时间内所能通过的最大交通量。

== 主要符号与说明

#three-line-table(
  [表 1 主要符号说明],
  (55pt, 55pt, 1fr),
  ([序号], [符号], [符号说明]),
  (
    [1], [$nu$], [行车速度（km/h）],
    [2], [$t_min$], [车头最小时距（s）],
    [3], [$J_a$], [车头最小间隔（m）],
    [4], [$J_z$], [车辆平均长度（m）],
    [5], [$J_gamma$], [车辆的制动距离（m）],
    [6], [$J_max$], [司机在反应时间内车辆行驶的距离（m）],
    [7], [$A_max$], [最大交通量],
    [8], [$alpha_1$], [车道数修正系数],
    [9], [$alpha_2$], [车道宽度和侧向净宽修正系数],
    [10], [$alpha_3$], [大型车修正系数],
    [11], [$alpha_4$], [驾驶员技术水平修正系数],
    [12], [$K_j$], [阻塞密度],
    [13], [$nu_f$], [自由车速],
    [...], [...], [],
  ),
  cell-align: (center, center, left),
)

= 模型的建立与求解

数据的预处理：
1. #dots 数据全部缺失，不予考虑。
2. 对数据测试的特点，如周期等进行分析。
3. #dots 数据残缺，根据数据挖掘等理论根据 #dots 变化趋势进行补充。
4. 对数据特点（后面将会用到的特征）进行提取。用 #dots 软件聚类分析和各个不同问题的需要，采得 #dots 组采样，每组 5-8 个采样值。将采样所对应的特征值进行列表或图示。根据数据特点，对总体和个体的特点进行比较，以表格或图示方式显示。

== 问题一的分析和求解

=== 模型的建立

模型建立的内容要点如下：

模型的主要类别：

几种常见的建模目的：

建模过程常见的几个要点：

模型的基本要求：

模型选择要点：

加分项（能在规定时间内做完后还有足够时间的再考虑加分项）：

1、鼓励创新。在能解决问题的基础上，对经典模型进行改进，欣赏独树一帜、有创新性的模型，但要合理。

2、对于同一问题使用两个或以上合理模型进行求解。避免出现单纯罗列模型，又不做对比和评价的现象。

#figure(
  table(
    columns: (18pt, 18pt, 18pt, 18pt, 18pt, 18pt, 18pt, 18pt, 18pt),
    align: center,
    stroke: none,
    fill: blue.lighten(25%),
    ..range(81).map(n => [#text(fill: white, size: 6.6pt)[#str(n + 1)]])
  ),
  caption: [图 2 的标题名称],
)

参考话术：我们需要解决的问题是 #dots，题目要求是 #dots，剔除 #dots 数据后选用何种类型的模型优点进行分析。具体步骤 123 #dots

=== 模型的求解

$
  A_max &= 3600 / t_min = 3600 / (J_min / (v / 3.6)) = (1000 v) / J_min ("辆" / h) \
  J_min &= J_r + J_z + J_a
$

=== 结果

== 问题三的求解和分析 的求解和分析 的求解和分析

=== 对问题的分析

问题三要求我们 #dots。

=== 对问题的求解

#strong[模型 Ⅱ—基于负荷度负荷度分析的小区开放影响度综合评价]

（1）模型的准备

1）负荷度介绍

负荷度（V/CV/CV/C）是指在理想条件下，最大服务交通量与基本行能力之比。

2）数据处理

将道路分为主干和次，其要参数详见表 10。

#figure(
  table(
    columns: (1fr, 1fr, 1fr, 1.2fr, 1.2fr),
    align: center,
    stroke: none,
    table.hline(stroke: 0.8pt),
    [道路类型], [主干路], [支干路], [小区内宽道路], [小区内窄道路],
    table.hline(stroke: 0.5pt),
    [行车速度], [50 km/h], [40 km/h], [30 km/h], [20 km/h],
    [车道数], [4], [3], [2], [1],
    table.hline(stroke: 0.8pt),
  ),
  caption: [主次道路参数表],
)

（2）模型的建立

1）小区的分类

根据小区结构，周边道路分布形状和周边道路车道数的不同，我们将小区分别分为 4、2、3 类，小区的分类结果详见表 11。

2）计算周边各路段及交叉口的通行能力

对于周边各路段的通行能力，我们运用问题二已建立的模型进行计算。在此基础上对于交叉口的通行能力交叉口 G 我们建立公式如下：

$
  G_"交叉口" & = sum_(i=1)^n G_i \
         G_i & = sum_(j=1)^k C_j
$

其中，$C_j$ 为进口各车道的通行能力，$G_i$ 为交叉口各进口的通行能力。

3）建立影响度综合评价体系 [9][10][11]

我们采用先单项评价再综合评价的方法，其总体思路见表 12。

= 模型的评价与推广

== 模型的评价

1. 优点

（1）问题求解中辅之流程图，将建模思路完整清晰的展现出来；

（2）问题二在对理论通行能力进修复时考虑因素细致、全面，理论通行能力进修复时考虑因素细致、全面，系数准确度高；

（3）在问题三中，提出“影响度”的概念较为直观地定量给小区开放后的效果，简便有。在影响度计算上由点及面从每个路段、交叉口到整个路网，层深入具有逻辑性；

#figure(
  rect(width: 85%, height: 92pt, fill: gray.lighten(78%), stroke: gray + 0.6pt)[
    #align(center + horizon)[#text(size: 11pt)[模型评价示意图]]
  ],
  caption: [图 3 的标题名称],
)

（4）运用多种数学软件（如 MATLAB、SPSS），取长补短，使计算结果更加准确、明晰。

2. 缺点

（1）在数学软件的计算中会将小数计算结果进行保留，使得随后的或统计结果造成一定误差；

（2）问题二求解修正通行能力时多次使用了查表，操作不够简便。

== 模型的推广



1. 问题二中建立的模型在现实生活中可以作为检验数据对实测数据的准确性进行检验，帮助人们更好地测算交通数据。

2. 基于问题三建立的模型，可以根据道路实时检测数，推算新建一条道路对于当前交通状况的改善效果。

= 模型的改进

== 模型一的改进

针对问题二中的模型一，在具体求解大型车对车辆通行能力的修正系数时，我们利用交通量的测算值对照得到相应的大型车修正系数。但是，在实际操作中交通量的测定有很大的难度，如果此时交通量数据无法得到，那么我们便不能得到相应的修正系数，因此我们对模型进行改进。

由 GREENSHIELD K-V 线性模型，可得通行能力的公式：

$
  A_p = cases(
    3600 / t (1 - (3.6 l) / (V_t t)) & (V_f > 7.2 l / t),
    (250 V_f) / t & (V_f <= 7.2 l / t),
  )
$

对应的临界车辆速度：

$
  V_p = cases(
    (V_f - 3.6 l) / t & (V_f > 7.2 l / t),
    1 / 2 V_f & (V_f <= 7.2 l / t),
  )
$

由美国道路通行能力准则可得，美国将道路服务水平分为六级：A-F 级，而我国目前针对当前国情，将道路服务水平分成四级：一级相当于美国的 A、B 两级；二级相当于美国的 C 级；三级相当于美国的 D 级；四级相当于美国的 E、F 级。

== 模型二的改进

针对于问题三中的模型，在得出各个类型小区在开放后对于整个小区周边路网交通负荷影响度后，无法判别小区开放的效果是积极的还是消极的，由此我们可以采用 Bress 悖论的原理进行判别。

#pagebreak()

= 参考文献

#set par(first-line-indent: 0pt, leading: 0.65em)
[1] 作者一. 论文题目一[D]. 学科名称，年份.

[2] 作者二等. 书名[M]. 出版地：出版社，年份.

[3] 作者三. 论文题目二[D]. 学科名称，年份.

[4] 作者四. 论文题目三[J]. 期刊名称，年份.

[5] 资料名称. URL

[6] 作者五，作者六. 论文题目四[J]. 期刊名称，年份.

[7] 作者七，作者八. 论文题目五[J]. 期刊名称，年份.

[8] 标准名称[S]. 年份.

[9] 作者九等. 论文题目六[J]. 期刊名称，年份.

[10] 作者十等. 论文题目七[J]. 期刊名称，年份.

[11] 作者十一. 论文题目八[D]. 学科名称，年份.

#pagebreak()

= 附录

#set text(font: song-font, size: 11pt)
#set par(first-line-indent: 0pt, leading: 0.5em)

```matlab
v = 60;
tmin = 2.5;
Amax = 3600 / tmin;
fprintf("capacity = %.2f\n", Amax);
```

#v(1em)

```cpp
#include <iostream>
int main() {
  double before = 1200, after = 1320, capacity = 1800;
  std::cout << (after - before) / capacity << std::endl;
}
```

#pagebreak()
#set text(font: song-font, size: 12pt)
#set par(first-line-indent: 0pt)
#align(left)[#hei([数据表格], size: 16pt)]
#v(0.35em)

#table(
  columns: (40pt, 60pt, 60pt, 60pt, 60pt),
  align: center,
  stroke: 0.5pt,
  [序号], [指标一], [指标二], [指标三], [指标四],
  [1], [12.4], [8.7], [0.63], [A],
  [2], [11.9], [9.1], [0.58], [B],
  [3], [13.2], [8.4], [0.71], [C],
)
