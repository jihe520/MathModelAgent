#set document(title: "[Paper Title]", author: ())

#let serif-font = ("Times New Roman", "Times", "New Computer Modern")
#let sans-font = ("Arial", "Helvetica")
#let code-font = ("Courier New", "Courier", "DejaVu Sans Mono")

#set page(
  paper: "a4",
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
  numbering: none,
)
#set text(font: serif-font, size: 12pt, lang: "en")
#set par(
  first-line-indent: 1.5em,
  justify: true,
  leading: 0.64em,
  spacing: 0.5em,
)
#set enum(numbering: "1.", spacing: 0.52em)
#set heading(numbering: "1.1")
#set math.equation(numbering: "(1)")

#show heading.where(level: 1): it => block(above: 1.0em, below: 0.75em)[
  #text(size: 22pt, weight: "bold")[#it]
]
#show heading.where(level: 2): it => block(above: 0.75em, below: 0.62em)[
  #text(size: 18pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.55em, below: 0.38em)[
  #text(size: 12pt, weight: "bold")[#it]
]
#show raw.where(block: true): it => block(width: 100%)[
  #line(length: 100%, stroke: 0.6pt)
  #text(font: code-font, size: 9pt)[#it]
  #line(length: 100%, stroke: 0.6pt)
]

#let summary-text = [Summary: problem overview + methods for each sub-problem + key numerical results + conclusions, 300-500 words]
#let keywords = [[Keyword1]; [Keyword2]; [Keyword3]]

#let summary-sheet() = {
  v(-0.45in)
  grid(
    columns: (1fr, 1fr, 1fr),
    align: center + top,
    [
      #text(weight: "bold")[Problem Chosen] \
      #v(0.25em)
      #text(size: 28pt, weight: "bold")[A]
    ],
    [
      #text(weight: "bold")[2026] \
      #text(weight: "bold")[MCM/ICM] \
      #text(weight: "bold")[Summary Sheet]
    ],
    [
      #text(weight: "bold")[Team Control Number] \
      #v(0.25em)
      #text(size: 28pt, weight: "bold")[0000]
    ],
  )
  v(0.7em)
  line(length: 100%, stroke: 0.8pt)
  v(1.45em)
  align(center)[#text(weight: "bold")[Summary]]
  v(1.6em)
  [#summary-text]
  v(0.45em)
  block[
    #set par(first-line-indent: 0pt)
    #text(weight: "bold")[Keywords:] #keywords
  ]
  pagebreak()
}

#let title-page() = {
  v(0.45in)
  align(center)[#text(size: 24pt)[[Paper Title]]]
  v(1.0in)
  align(center)[#text(size: 15pt)[June 3, 2026]]
  v(0.75in)
  align(center)[#text(weight: "bold")[Summary]]
  v(1.25em)
  [#summary-text]
  v(0.45em)
  block[
    #set par(first-line-indent: 0pt)
    #text(weight: "bold")[Keywords:] #keywords
  ]
  pagebreak()
}

#let mcm-header = context [
  #grid(
    columns: (1fr, 1fr),
    align: (left, right),
    text(font: ("Courier New", "Courier"), size: 11pt)[Team \# 0000],
    text(
      font: ("Courier New", "Courier"),
      size: 11pt,
    )[Page #counter(page).display() of 4],
  )
  #line(length: 100%, stroke: 0.4pt)
]

#let toc-line(level, title, page) = {
  let indent = if level == 1 { 0pt } else { 28pt }
  let weight = if level == 1 { "bold" } else { "regular" }
  block(above: if level == 1 { 1.05em } else { 0.55em })[
    #grid(
      columns: (auto, auto, 1fr, auto),
      column-gutter: 0.55em,
      inset: (left: indent),
      text(weight: weight)[#title.at(0)],
      text(weight: weight)[#title.at(1)],
      box(height: 1em, width: 100%)[#v(0.72em)#line(length: 100%, stroke: (
          dash: "dotted",
          thickness: 0.65pt,
        ))],
      text(weight: weight)[#page],
    )
  ]
}

#let contents-page() = {
  align(center)[#text(font: sans-font, size: 20pt, weight: "bold")[Contents]]
  v(1.6em)
  toc-line(1, ([1], [Introduction]), [2])
  toc-line(2, ([1.1], [Background]), [2])
  toc-line(2, ([1.2], [Problem Statement]), [2])
  toc-line(2, ([1.3], [Our Approach]), [2])
  toc-line(1, ([2], [Assumptions and Justifications]), [2])
  toc-line(1, ([3], [Model Design and Methodology]), [2])
  toc-line(2, ([3.1], [Prediction Model]), [2])
  toc-line(2, ([3.2], [Optimization Objective]), [2])
  toc-line(2, ([3.3], [Ensemble Strategy]), [2])
  toc-line(1, ([4], [Solution and Results]), [3])
  toc-line(2, ([4.1], [Problem 1]), [3])
  toc-line(2, ([4.2], [Problem 2]), [3])
  toc-line(2, ([4.3], [Problem 3]), [3])
  toc-line(1, ([5], [Sensitivity Analysis]), [3])
  toc-line(1, ([6], [Strengths and Weaknesses]), [3])
  toc-line(2, ([6.1], [Strengths]), [3])
  toc-line(2, ([6.2], [Weaknesses]), [3])
  toc-line(1, ([7], [Conclusions]), [4])
  toc-line(1, ([], [Appendices]), [4])
  toc-line(1, ([Appendix A], [Core Code]), [4])
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
        #align(center)[#text(font: sans-font, size: 10.5pt, weight: "bold")[#caption]]
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

#summary-sheet()
#title-page()

#counter(page).update(1)
#set page(
  paper: "a4",
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
  numbering: none,
  header: mcm-header,
)

#contents-page()

#include "sections/1_introduction.typ"
#include "sections/2_assumptions.typ"
#include "sections/3_model_design.typ"
#pagebreak()
#include "sections/4_solution.typ"
#include "sections/5_sensitivity.typ"
#include "sections/6_strengths_weaknesses.typ"
#pagebreak()
#include "sections/7_conclusions.typ"

#heading(numbering: none, outlined: true)[References]
#v(0.8em)
#text(size: 30pt, weight: "bold")[Appendices]
#v(1.0em)
#block[
  #set par(first-line-indent: 0pt)
  #text(size: 22pt, weight: "bold")[Appendix A #h(1.2em) Core Code]
]
#include "sections/A_code.typ"
