#let paper_title = "[论文题目]"
#let category = "[研究生/本科生/专科生]"
#let school_name = "[学校名称]"
#let problem_id = "[A/B/C/D]"
#let member_a = "[队员1]"
#let member_b = "[队员2]"
#let member_c = "[队员3]"
#let phone_a = "[电话1]"
#let phone_b = "[电话2]"
#let phone_c = "[电话3]"
#let supervisor = "[指导教师]"

#let body-font = ("Times New Roman", "Songti SC", "STSong")
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

#set document(title: paper_title, author: ())
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  numbering: none,
)
#set text(font: body-font, size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 0.95em, spacing: 0.45em)
#set heading(numbering: cn-numbering)
#set enum(numbering: "1.")
#set table(inset: (x: 0.5em, y: 0.52em), stroke: 0.55pt)

#show heading.where(level: 1): set align(center)
#show heading.where(level: 1): set text(size: 14pt, weight: "bold")
#show heading.where(level: 1): set block(above: 1.45em, below: 0.95em)
#show heading.where(level: 2): set text(size: 12pt, weight: "bold")
#show heading.where(level: 2): set block(above: 1.15em, below: 0.65em)
#show heading.where(level: 3): set text(size: 12pt, weight: "bold")
#show heading.where(level: 3): set block(above: 0.95em, below: 0.55em)
#show figure.caption: set text(size: 10.5pt, weight: "bold")
#show raw: set text(font: ("Menlo", "Courier New", "Times New Roman"), size: 9pt)
#show raw.where(block: true): set block(fill: luma(96%), stroke: 0.55pt, inset: 0.55em, above: 0.4em, below: 0.4em)

#let strong-hei(body) = text(font: hei-font, weight: "bold", body)
#let footer-page = context align(center)[#text(size: 9pt)[#counter(page).display("1")]]
#let header-rule = line(length: 100%, stroke: 0.4pt)

#let underlined(body, width: 6.2cm) = box(width: width, inset: (bottom: 2pt), stroke: (bottom: 0.55pt))[
  #align(center)[#body]
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

#let cover-page() = {
  v(3.2cm)
  grid(
    columns: (3cm, 6.2cm),
    row-gutter: 2.7em,
    column-gutter: 0.5em,
    align: (left, center),
    [#strong-hei([论文题目：])], underlined(problem_id),
    [#strong-hei([组 #h(1.5em) 别：])], underlined(category),
  )

  v(4.35cm)
  strong-hei([参赛队员信息：])
  v(0.9em)
  table(
    columns: (3.1cm, 5.1cm, 5.1cm, 4.1cm),
    align: center,
    [], [#strong-hei([姓名])], [#strong-hei([联系电话])], [#strong-hei([指导老师])],
    [#strong-hei([参赛队员 1])], [#member_a], [#phone_a], [#supervisor],
    [#strong-hei([参赛队员 2])], [#member_b], [#phone_b], [],
    [#strong-hei([参赛队员 3])], [#member_c], [#phone_c], [],
  )

  v(3cm)
  strong-hei([参赛学校：])
  v(1em)
  align(center)[#underlined(school_name, width: 7.6cm)]
}

#cover-page()

#pagebreak()
#set page(numbering: "1", header: header-rule, footer: footer-page)
#counter(page).update(1)

#include("sections/abstract.typ")
#include("sections/1_restatement.typ")
#include("sections/2_analysis.typ")
#include("sections/3_assumptions.typ")
#include("sections/4_symbols.typ")
#include("sections/5_problem1.typ")
#include("sections/6_problem2.typ")
#include("sections/7_problem3.typ")
#include("sections/8_evaluation.typ")

#pagebreak()
#heading(level: 1, numbering: none, outlined: false)[参考文献]
#include("references.typ")
#include("sections/A_code.typ")
