#set document(title: "[论文标题]", author: ())

#let song-font = ("SimSun", "Songti SC", "STSong", "Times New Roman")
#let kai-font = ("KaiTi", "Kaiti SC", "STKaiti", "SimSun")
#let hei-font = ("Heiti SC", "STHeiti", "SimSun", "Songti SC")
#let code-font = ("Courier New", "Menlo")

#let cn-heading-numbering(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("一、", ns.at(0))
  } else if ns.len() == 2 {
    numbering("1.1", ns.at(0), ns.at(1))
  } else {
    numbering("1.1.1", ns.at(0), ns.at(1), ns.at(2))
  }
}

#set page(
  paper: "a4",
  margin: (top: 25mm, bottom: 25mm, left: 25mm, right: 25mm),
  numbering: "1",
)
#set text(font: song-font, size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 1.02em, spacing: 0.65em)
#set enum(numbering: "1.")
#set heading(numbering: cn-heading-numbering)
#set math.equation(numbering: "(1)")
#show heading.where(level: 1): it => block(width: 100%, above: 1.35em, below: 1.0em)[
  #align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[#it]]
]
#show heading.where(level: 2): it => block(above: 0.95em, below: 0.55em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.75em, below: 0.45em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show raw.where(block: true): it => block(
  inset: (x: 0.7em, y: 0.55em),
  stroke: 0.9pt + rgb("#cfcfcf"),
  fill: rgb("#f7f7f7"),
  width: 100%,
)[#text(font: code-font, size: 9pt)[#it]]

#let abstract-page() = {
  align(center)[#text(font: hei-font, size: 16pt, weight: "bold")[[论文标题]]]
  v(1.4em)
  align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[摘要]]
  v(0.8em)
  align(center)[[中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论]]
  v(0.75em)
  block[
    #set par(first-line-indent: 0pt)
    #text(font: hei-font, weight: "bold")[关键字：] [关键词1] #h(1em) [关键词2] #h(1em) [关键词3]
  ]
  pagebreak()
}

#let toc-line(level, title, page) = {
  let indent = if level == 1 { 0pt } else if level == 2 { 28pt } else { 52pt }
  let weight = if level == 1 { "bold" } else { "regular" }
  block(above: if level == 1 { 0.58em } else { 0.35em })[
    #grid(
      columns: (auto, 1fr, auto),
      column-gutter: 0.55em,
      inset: (left: indent),
      text(font: if level == 1 { hei-font } else { song-font }, weight: weight)[#title],
      box(height: 1em, width: 100%)[#v(0.72em)#line(length: 100%, stroke: (dash: "dotted", thickness: 0.7pt))],
      text(weight: weight)[#page],
    )
  ]
}

#let toc-page() = {
  align(center)[#text(font: hei-font, size: 16pt, weight: "bold")[目录]]
  v(0.9cm)
  toc-line(1, [一、问题重述], [4])
  toc-line(2, [1.1 问题背景], [4])
  toc-line(2, [1.2 问题内容], [4])
  toc-line(1, [二、问题分析], [4])
  toc-line(2, [2.1 问题一的分析], [4])
  toc-line(2, [2.2 问题二的分析], [4])
  toc-line(2, [2.3 问题三的分析], [4])
  toc-line(1, [三、模型假设], [4])
  toc-line(1, [四、符号说明], [4])
  toc-line(1, [五、问题一的模型建立与求解], [5])
  toc-line(2, [5.1 数据预处理], [5])
  toc-line(2, [5.2 模型建立], [5])
  toc-line(2, [5.3 求解结果], [5])
  toc-line(1, [六、问题二的模型建立与求解], [5])
  toc-line(2, [6.1 特征选择], [5])
  toc-line(2, [6.2 模型优化], [5])
  toc-line(1, [七、问题三的模型建立与求解], [6])
  toc-line(2, [7.1 优化模型], [6])
  toc-line(2, [7.2 算法求解], [6])
  toc-line(2, [7.3 结果], [6])
  toc-line(1, [八、敏感性分析], [6])
  toc-line(2, [8.1 参数敏感性], [6])
  toc-line(1, [九、模型评价与推广], [6])
  toc-line(2, [9.1 模型优点], [6])
  toc-line(2, [9.2 模型缺点], [6])
  toc-line(2, [9.3 推广], [6])
  toc-line(1, [参考文献], [6])
  pagebreak()
  toc-line(1, [附录 A #h(1em) 核心代码], [7])
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

#abstract-page()
#toc-page()

#include("sections/1_restatement.typ")
#include("sections/2_analysis.typ")
#include("sections/3_assumptions.typ")
#include("sections/4_symbols.typ")
#include("sections/5_problem1.typ")
#include("sections/6_problem2.typ")
#pagebreak()
#include("sections/7_problem3.typ")
#include("sections/8_sensitivity.typ")
#include("sections/9_evaluation.typ")

#pagebreak()
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[参考文献]]

#v(1.45em)
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[附录 A #h(1em) 核心代码]]
#include("sections/A_code.typ")
