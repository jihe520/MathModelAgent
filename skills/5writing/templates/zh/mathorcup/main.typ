#set document(title: "[论文标题]", author: ())

#let song-font = ("SimSun", "Songti SC", "STSong", "Times New Roman")
#let hei-font = ("SimHei", "Heiti SC", "STHeiti", "SimSun", "Songti SC")
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
  numbering: none,
)
#set text(font: song-font, size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 1.2em, spacing: 0.65em)
#set enum(numbering: "1.")
#set heading(numbering: cn-heading-numbering)
#set math.equation(numbering: "(1)")

#show heading.where(level: 1): it => block(width: 100%, above: 1.25em, below: 1.05em)[
  #align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[#it]]
]
#show heading.where(level: 2): it => block(above: 0.9em, below: 0.55em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.65em, below: 0.4em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show raw.where(block: true): it => block(width: 100%)[#text(font: code-font, size: 10pt)[#it]]

#let front-page() = {
  v(1.14cm)
  align(center)[
    #table(
      columns: (5.65cm, 5.65cm),
      rows: (0.75cm, 0.75cm),
      stroke: 0.5pt,
      inset: 0pt,
      align: center + horizon,
      [队伍编号], [[队伍编号]],
      [题号], [[题号]],
    )
  ]
  v(1.05cm)
  line(length: 100%, stroke: 1.5pt)
  v(1.15cm)
  align(center)[#text(size: 14pt)[[论文标题]]]
  v(0.25em)
  align(center)[摘要]
  v(0.55em)
  align(center)[[中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论，400-600字]]
  v(1.15em)
  block[
    #set par(first-line-indent: 0pt)
    关键词： [关键词1]；[关键词2]；[关键词3]
  ]
  pagebreak()
}

#let toc-line(level, title, page) = {
  let indent = if level == 1 { 0pt } else { 22pt }
  let weight = if level == 1 { "bold" } else { "regular" }
  block(above: if level == 1 { 0.48em } else { 0.34em })[
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
  v(0.85cm)
  toc-line(1, [一、问题重述], [1])
  toc-line(2, [1.1 #h(1em) 问题背景], [1])
  toc-line(2, [1.2 #h(1em) 问题内容], [1])
  toc-line(1, [二、问题分析], [1])
  toc-line(2, [2.1 #h(1em) 问题一的分析], [1])
  toc-line(2, [2.2 #h(1em) 问题二的分析], [1])
  toc-line(2, [2.3 #h(1em) 问题三的分析], [1])
  toc-line(1, [三、模型假设], [1])
  toc-line(1, [四、符号说明], [1])
  toc-line(1, [五、问题一的模型建立与求解], [2])
  toc-line(2, [5.1 #h(1em) 数据预处理], [2])
  toc-line(2, [5.2 #h(1em) 模型建立], [2])
  toc-line(2, [5.3 #h(1em) 求解结果], [2])
  toc-line(1, [六、问题二的模型建立与求解], [2])
  toc-line(2, [6.1 #h(1em) 特征选择], [2])
  toc-line(2, [6.2 #h(1em) 模型优化], [2])
  toc-line(1, [七、问题三的模型建立与求解], [3])
  toc-line(2, [7.1 #h(1em) 优化模型], [3])
  toc-line(2, [7.2 #h(1em) 算法求解], [3])
  toc-line(2, [7.3 #h(1em) 结果], [3])
  toc-line(1, [八、模型评价与推广], [3])
  toc-line(2, [8.1 #h(1em) 模型优点], [3])
  toc-line(2, [8.2 #h(1em) 模型缺点], [3])
  toc-line(2, [8.3 #h(1em) 推广], [3])
  toc-line(1, [参考文献], [3])
  toc-line(1, [附录 1： 核心代码], [4])
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

#front-page()
#toc-page()

#set page(
  paper: "a4",
  margin: (top: 25mm, bottom: 25mm, left: 25mm, right: 25mm),
  numbering: none,
  footer: context align(center)[第 #counter(page).display() 页  共 4 页],
)
#counter(page).update(1)

#include("sections/1_restatement.typ")
#include("sections/2_analysis.typ")
#include("sections/3_assumptions.typ")
#include("sections/4_symbols.typ")
#include("sections/5_problem1.typ")
#include("sections/6_problem2.typ")
#pagebreak()
#include("sections/7_problem3.typ")
#include("sections/8_evaluation.typ")

#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[参考文献]]
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[附 #h(1em) 录]]
#pagebreak()
#include("sections/A_code.typ")
