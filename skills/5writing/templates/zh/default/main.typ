#set document(title: "[论文标题]", author: ())
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  numbering: none,
)
#set text(font: ("Songti SC", "STSong", "Times New Roman"), size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 0.78em, spacing: 0.55em)
#set heading(numbering: "1.1")
#set enum(numbering: "1.")
#show heading.where(level: 1): it => block(above: 1.8em, below: 1.0em)[#align(center)[#text(font: ("Heiti SC", "STHeiti", "Songti SC"), size: 16pt, weight: "bold")[#it]]]
#show heading.where(level: 2): it => block(above: 1.25em, below: 0.65em)[#text(font: ("Heiti SC", "STHeiti", "Songti SC"), size: 14pt, weight: "bold")[#it]]
#show heading.where(level: 3): it => block(above: 0.9em, below: 0.4em)[#text(font: ("Heiti SC", "STHeiti", "Songti SC"), size: 12pt, weight: "bold")[#it]]
#show figure.caption: it => text(size: 9pt)[#it]

#let song = (body) => text(font: ("Songti SC", "STSong"), body)
#let hei = (body) => text(font: ("Heiti SC", "STHeiti", "Songti SC"), weight: "bold", body)
#let kai = (body) => text(font: ("Kaiti SC", "STKaiti", "Songti SC"), body)
#let tight-title(body, size: 18pt) = align(center)[#text(font: ("Heiti SC", "STHeiti", "Songti SC"), size: size, weight: "bold")[#body]]
#let keywords-cn(body) = block(above: 0.65em)[
  #set par(first-line-indent: 0pt)
  #text(font: ("Heiti SC", "STHeiti", "Songti SC"), weight: "bold")[关键词：]#body
]
#let running-header = [
  #align(center)[#text(size: 10.5pt)[数学建模竞赛论文]]
  #v(-0.45em)
  #line(length: 100%, stroke: 0.45pt)
]
#let toc-page(title: [目录]) = {
  align(center)[#text(font: ("Heiti SC", "STHeiti", "Songti SC"), size: 16pt, weight: "bold")[#title]]
  v(1em)
  outline(title: none)
  pagebreak()
}
#let references-cn() = [
#heading(level: 1, numbering: none, outlined: false)[参考文献]
#set par(first-line-indent: 0pt)
#include("references.typ")
]
#let appendix-cn(file: "sections/A_code.typ") = {
  set heading(numbering: "A")
  set par(first-line-indent: 0pt, leading: 0.55em, spacing: 0pt)
  show raw: set text(size: 8.6pt)
  show raw.where(block: true): set block(above: 0.35em, below: 0pt)
  counter(heading).update(0)
  heading(level: 1)[核心代码]
  include(file)
}

#let three-line-table(caption, columns, header, body, inset: (x: 0.35em, y: 0.52em), cell-align: center) = {
  let col-count = header.len()
  let body-rows = calc.floor(body.len() / col-count)
  let bottom-y = body-rows + 1
  let styled-header = header.map(cell => strong(cell))

  block(width: 100%, breakable: false)[
    #align(center)[
      #box[
        #align(center)[#text(font: ("Heiti SC", "STHeiti", "Songti SC"), size: 10.5pt, weight: "bold")[#caption]]
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

#v(1.85cm)
#tight-title([[论文标题]], size: 22pt)

#v(2.25cm)
#align(center)[#hei([摘 #h(2em) 要])]
#v(0.6em)
[摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论]
#keywords-cn([[关键词1]；[关键词2]；[关键词3]])

#pagebreak()
#set page(
  numbering: "1",
  header: running-header,
  footer: context align(center)[#counter(page).display("1")],
)
#toc-page()

#include("sections/1_restatement.typ")
#include("sections/2_assumptions.typ")
#include("sections/3_symbols.typ")
#include("sections/4_problem1.typ")
#include("sections/5_problem2.typ")
#include("sections/6_problem3.typ")
#include("sections/7_sensitivity.typ")
#include("sections/8_evaluation.typ")

#references-cn()
#appendix-cn()
