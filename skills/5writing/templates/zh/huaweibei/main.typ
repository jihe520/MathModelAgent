#set document(title: "[论文标题]", author: ())

#let song-font = ("SimSun", "Songti SC", "STSong", "Times New Roman")
#let kai-font = ("KaiTi", "Kaiti SC", "STKaiti", "SimSun")
#let hei-font = ("SimHei", "Heiti SC", "STHeiti", "SimSun")
#let code-font = ("Courier New", "Menlo")

#let heading-numbering(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("1.", ns.at(0))
  } else if ns.len() == 2 {
    numbering("1.1", ns.at(0), ns.at(1))
  } else {
    numbering("1.1.1", ns.at(0), ns.at(1), ns.at(2))
  }
}

#set page(
  paper: "a4",
  margin: (top: 30mm, bottom: 25mm, left: 22.5mm, right: 22.5mm),
  numbering: "1",
)
#set text(font: song-font, size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 1.02em, spacing: 0.65em)
#set enum(numbering: "1.")
#set heading(numbering: heading-numbering)
#set math.equation(numbering: "(1)")
#show heading.where(level: 1): it => block(above: 1.15em, below: 1.0em, width: 100%)[
  #align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[#it]]
]
#show heading.where(level: 2): it => block(above: 0.85em, below: 0.55em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.75em, below: 0.45em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show raw.where(block: true): it => block(
  inset: (x: 0.7em, y: 0.55em),
  stroke: 0.5pt + rgb("#808080"),
  fill: rgb("#f7f7f7"),
  width: 100%,
)[#text(font: code-font, size: 10pt)[#it]]

#let cover-info-table() = align(center)[
  #block(width: 15.2cm)[
    #block(width: 100%, height: 1.55cm)[
      #grid(
        columns: (4.2cm, 1fr),
        align: (left + horizon, left + horizon),
        box(height: 1.05cm)[
          #align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[学 #h(1em) 校]]
        ],
        box(height: 1.05cm)[
          #align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[[学校名称]]]
        ],
      )
      #line(length: 100%, stroke: 1.2pt)
    ]
    #block(width: 100%, height: 1.55cm)[
      #grid(
        columns: (4.2cm, 1fr),
        align: (left + horizon, left + horizon),
        box(height: 1.05cm)[
          #align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[参赛队号]]
        ],
        box(height: 1.05cm)[
          #align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[[参赛队号]]]
        ],
      )
      #line(length: 100%, stroke: 1.2pt)
    ]
    #grid(
      columns: (4.2cm, 1fr),
      align: (left + horizon, left + top),
      block(height: 3.3cm)[
        #align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[队员姓名]]
      ],
      block(width: 100%)[
        #block(width: 100%, height: 1.1cm)[
          #box(height: 0.82cm)[#align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[1. [成员 A]]]]
          #line(length: 100%, stroke: 0.55pt)
        ]
        #block(width: 100%, height: 1.1cm)[
          #box(height: 0.82cm)[#align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[2. [成员 B]]]]
          #line(length: 100%, stroke: 0.55pt)
        ]
        #block(width: 100%, height: 1.1cm)[
          #box(height: 0.82cm)[#align(left + horizon)[#text(font: hei-font, size: 20pt, weight: "bold")[3. [成员 C]]]]
          #line(length: 100%, stroke: 1.2pt)
        ]
      ],
    )
  ]
]

#let cover-page() = {
  counter(page).update(0)
  align(center)[#image("logo.pdf", width: 14.5cm)]
  v(1.35cm)
  align(center)[#image("title.pdf", width: 10.8cm)]
  v(2.35cm)
  cover-info-table()
  pagebreak()
}

#let abstract-page() = {
  counter(page).update(1)
  align(center)[#image("title.pdf", width: 10.8cm)]
  v(0.65cm)
  grid(
    columns: (4.5em, 1fr),
    align: (left + horizon, center + horizon),
    text(size: 14pt)[题 #h(1em) 目],
    block(width: 100%)[
      #align(center)[#text(font: hei-font, size: 16pt, weight: "bold")[[论文标题]]]
      #line(length: 100%, stroke: 0.5pt)
    ],
  )
  v(0.45cm)
  align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[摘 #h(2em) 要：]]
  v(0.45cm)
  [[中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论]]
  v(0.65em)
  block[
    #set par(first-line-indent: 0pt)
    #text(font: hei-font, size: 12pt, weight: "bold")[关键词：] [关键词1] #h(1em) [关键词2] #h(1em) [关键词3]
  ]
  pagebreak()
}

#let toc-line(level, title, page) = {
  let indent = if level == 1 { 0pt } else if level == 2 { 28pt } else { 52pt }
  let weight = if level == 1 { "bold" } else { "regular" }
  block(above: if level == 1 { 0.52em } else { 0.24em })[
    #grid(
      columns: (auto, 1fr, auto),
      column-gutter: 0.55em,
      inset: (left: indent),
      text(font: if level == 1 { hei-font } else { song-font }, weight: weight)[#title],
      box(height: 1em, width: 100%)[#v(0.72em)#line(length: 100%, stroke: (dash: "dotted", thickness: 0.8pt))],
      text(weight: weight)[#page],
    )
  ]
}

#let toc-page() = {
  align(center)[#text(font: hei-font, size: 16pt, weight: "bold")[目录]]
  v(1.0cm)
  toc-line(1, [1. 问题重述], [3])
  toc-line(2, [1.1 问题背景], [3])
  toc-line(2, [1.2 问题内容], [3])
  toc-line(1, [2. 问题分析], [3])
  toc-line(2, [2.1 问题一的分析], [3])
  toc-line(2, [2.2 问题二的分析], [3])
  toc-line(2, [2.3 问题三的分析], [3])
  toc-line(1, [3. 模型假设], [3])
  toc-line(1, [4. 符号说明], [3])
  toc-line(1, [5. 问题一的模型建立与求解], [4])
  toc-line(2, [5.1 数据预处理], [4])
  toc-line(2, [5.2 模型建立], [4])
  toc-line(2, [5.3 求解结果], [4])
  toc-line(1, [6. 问题二的模型建立与求解], [4])
  toc-line(2, [6.1 特征选择], [4])
  toc-line(2, [6.2 模型优化], [4])
  toc-line(1, [7. 问题三的模型建立与求解], [5])
  toc-line(2, [7.1 优化模型], [5])
  toc-line(2, [7.2 算法求解], [5])
  toc-line(2, [7.3 结果], [5])
  toc-line(1, [8. 敏感性分析], [5])
  toc-line(2, [8.1 参数敏感性], [5])
  toc-line(1, [9. 模型评价与推广], [5])
  toc-line(2, [9.1 模型优点], [5])
  toc-line(2, [9.2 模型缺点], [5])
  toc-line(2, [9.3 推广], [5])
  toc-line(1, [参考文献], [5])
  toc-line(1, [A 附录 核心代码], [6])
  pagebreak()
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

#cover-page()
#abstract-page()
#toc-page()

#include("sections/1_restatement.typ")
#include("sections/2_analysis.typ")
#include("sections/3_assumptions.typ")
#include("sections/4_symbols.typ")
#include("sections/5_problem1.typ")
#include("sections/6_problem2.typ")
#include("sections/7_problem3.typ")
#include("sections/8_sensitivity.typ")
#include("sections/9_evaluation.typ")

#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[参考文献]]

#pagebreak()
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[附录 A #h(1em) 核心代码]]
#include("sections/A_code.typ")
