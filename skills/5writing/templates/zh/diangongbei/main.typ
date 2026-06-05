
// Compile with: typst compile --font-path fonts main.typ main.pdf

#let paper-title = "[论文题目]"
#let team-number = "[报名序号]"
#let problem-id = "[A/B]"

#let body-font = ("Times New Roman", "Songti SC", "STSong")
#let song-font = ("Songti SC", "STSong", "Times New Roman")
#let hei-font = ("Heiti SC", "STHeiti", "Songti SC", "STSong")

#let cn-numbering(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("一、", ns.at(0))
  } else if ns.len() == 2 {
    numbering("1.1", ns.at(0), ns.at(1))
  } else {
    numbering("1.1.1", ns.at(0), ns.at(1), ns.at(2))
  }
}

#set document(title: paper-title, author: ())
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  numbering: none,
)
#set text(font: body-font, size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 0.82em, spacing: 0.35em)
#set heading(numbering: cn-numbering)
#set enum(numbering: "1.")
#set table(inset: (x: 0.75em, y: 0.35em), stroke: 0.6pt)

#show heading.where(level: 1): set align(center)
#show heading.where(level: 1): set text(size: 14pt, weight: "bold")
#show heading.where(level: 1): set block(above: 1.25em, below: 0.85em)
#show heading.where(level: 2): set text(size: 12pt, weight: "bold")
#show heading.where(level: 2): set block(above: 0.95em, below: 0.45em)
#show heading.where(level: 3): set text(size: 12pt, weight: "bold")
#show heading.where(level: 3): set block(above: 0.75em, below: 0.35em)
#show figure.caption: set text(size: 12pt)
#show raw: set text(font: ("Ubuntu Mono", "Menlo", "Courier New"), size: 9.2pt)
#show raw.where(block: true): set block(
  stroke: (top: 0.7pt, bottom: 0.7pt),
  inset: (top: 0.45em, bottom: 0.45em),
  above: 0.2em,
  below: 0.2em,
)

#let hei(body) = text(font: hei-font, weight: "bold", body)
#let title-font(body, size: 14pt) = text(font: hei-font, size: size, weight: "bold", body)
#let footer-page = context align(center)[#text(size: 9pt)[#counter(page).display("1")]]

#let cover-page() = {
  v(8.15cm)
  pad(left: 1.65cm)[#title-font([报名序号: #team-number], size: 16pt)]
  v(3.15cm)
  pad(left: 1.65cm)[#title-font([论文题目: #problem-id 题 #paper-title], size: 16pt)]
}

#let abstract-page() = {
  align(center)[#title-font(paper-title, size: 14pt)]
  v(1.2em)
  align(center)[#hei([摘 #h(1.7em) 要])]
  v(1.1em)
  [中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论]
  v(0.65em)
  block[
    #set par(first-line-indent: 0pt)
    #hei([关键词:]) [关键词1] #h(1.5em) [关键词2] #h(1.5em) [关键词3]
  ]
}

#let toc-page() = {
  align(center)[#text(font: ("Arial", "Times New Roman", "Songti SC"), size: 17pt, weight: "bold")[目录]]
  v(2.7em)
  outline(title: none)
  pagebreak()
}

#let references-cn() = {
  heading(level: 1, numbering: none, outlined: false)[参考文献]
}

#let appendices() = {
  heading(level: 1, numbering: none)[Appendices]
  align(center)[#heading(level: 2, numbering: none)[附录 A #h(1em) 核心代码]]
  include("sections/A_code.typ")
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

#pagebreak()
#set page(numbering: "1", footer: footer-page)
#counter(page).update(1)
#abstract-page()

#pagebreak()
#toc-page()

#include("sections/1_restatement.typ")
#include("sections/2_analysis.typ")
#include("sections/3_assumptions.typ")
#include("sections/4_symbols.typ")
#include("sections/5_problem1.typ")
#include("sections/6_problem2.typ")
#include("sections/7_problem3.typ")
#include("sections/8_evaluation.typ")

#references-cn()
#pagebreak()
#appendices()
