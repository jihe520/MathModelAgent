#set document(title: "[论文标题]", author: ())

#let song-font = ("SimSun", "Songti SC", "STSong", "Times New Roman")
#let hei-font = ("SimHei", "Heiti SC", "STHeiti", "SimSun")
#let code-font = ("Menlo", "Courier New")

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
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.66cm, right: 2.66cm),
  numbering: "1",
)
#set text(font: song-font, size: 12pt, lang: "zh")
#set par(
  first-line-indent: (amount: 2em, all: true),
  justify: true,
  leading: 0.92em,
  spacing: 1.0em,
)
#set enum(
  numbering: n => [#n、],
  indent: 2em,
  body-indent: 0pt,
  spacing: 1.0em,
  number-align: start,
)
#set math.equation(numbering: "(1)")
#set heading(numbering: cn-heading-numbering)
#show heading.where(level: 1): it => block(width: 100%, above: 1.52em, below: 1.15em)[
  #align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[#it]]
]
#show heading.where(level: 2): it => block(above: 1.18em, below: 1.18em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.9em, below: 0.75em)[
  #text(font: hei-font, size: 12pt, weight: "bold")[#it]
]
#show figure.caption: it => text(font: hei-font, size: 10.5pt, weight: "bold")[#it]
#show raw.where(block: true): it => block(
  inset: (x: 0.65em, y: 0.55em),
  stroke: none,
  width: 100%,
)[#text(font: code-font, size: 9pt)[#it]]

#let abstract-page(body, keywords) = {
  align(center)[#text(font: hei-font, size: 16pt, weight: "bold")[[论文标题]]]
  v(0.85em)
  align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[摘 #h(1em) 要]]
  v(0.55em)
  body
  v(0.65em)
  block[
    #set par(first-line-indent: 0pt)
    #text(font: hei-font, weight: "bold")[关键词：]#keywords
  ]
  pagebreak()
}

#let manual-section-title(number, title) = {
  counter(heading).step()
  block(width: 100%, above: 1.52em, below: 1.15em)[
    #align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[#number、 #title]]
  ]
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

#let symbols-table(header, body, columns: (3.6em, auto, 3.0em), cell-align: (center, left, center)) = {
  manual-section-title([四], [符号说明])
  three-line-table(
    [表 1 主要符号说明],
    columns,
    header,
    body,
    cell-align: cell-align,
  )
}

#let references-section(body) = {
  align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[参考文献]]
  v(0.65em)
  block[
    #set par(first-line-indent: 0pt, spacing: 0.65em)
    #body
  ]
}

#let appendix-code-title() = {
  v(0.8em)
  align(left)[#text(font: hei-font, size: 12pt, weight: "bold")[附录1：核心代码]]
}

#import "sections/4_symbols.typ": huashubei-symbol-header, huashubei-symbol-body

#abstract-page(
  [[中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论]],
  [[关键词1]、[关键词2]、[关键词3]],
)

#include("sections/1_restatement.typ")
#include("sections/2_analysis.typ")
#include("sections/3_assumptions.typ")
#symbols-table(huashubei-symbol-header, huashubei-symbol-body)
#include("sections/5_problem1.typ")
#include("sections/6_problem2.typ")
#include("sections/7_problem3.typ")
#include("sections/8_evaluation.typ")

#references-section(include("references.typ"))

#pagebreak()
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[附 #h(1em) 录]]
#appendix-code-title()
#include("sections/A_code.typ")
