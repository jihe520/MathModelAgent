#set document(title: "[Paper Title]", author: ())

#let roman = ("New Computer Modern", "Times New Roman", "Times")
#let sans = ("Arial", "Helvetica", "Helvetica Neue")
#let mono = ("Courier New", "Courier", "Menlo", "Monaco")

#let year = "2026"
#let team-number = "0000000"
#let problem-chosen = "A"
#let paper-title = "[Paper Title]"
#let summary-placeholder = "Summary content -- THIS IS THE MOST IMPORTANT PART"
#let total-pages = "4"

#let page-header = [
  #grid(
    columns: (1fr, 1fr),
    align: (left, right),
    text(font: sans, size: 11pt)[Team \# #team-number],
    text(font: sans, size: 11pt)[
      Page #context counter(page).display() of #total-pages
    ],
  )
  #v(0.12em)
  #line(length: 100%, stroke: 0.55pt)
]

#let toc-title = align(center)[
  #text(font: sans, size: 21pt, weight: "bold")[Contents]
]

#let leader() = box(width: 1fr, baseline: 0.74em)[
  #line(length: 100%, stroke: (
    paint: black,
    thickness: 0.5pt,
    dash: "dotted",
  ))
]

#let toc-entry(title, page, level: 1) = block(above: if level == 1 {
  1.22em
} else { 0.62em })[
  #grid(
    columns: (auto, 1fr, auto),
    column-gutter: 0.55em,
    inset: (left: if level == 1 { 0pt } else { 2em }),
    text(size: 12pt, weight: if level == 1 { "bold" } else {
      "regular"
    })[#title],
    if level == 1 { [] } else { leader() },
    text(size: 12pt)[#page],
  )
]

#let sheet() = [
  #set page(
    paper: "a4",
    margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
    numbering: none,
    header: none,
    footer: none,
  )
  #set par(
    first-line-indent: 0pt,
    justify: false,
    leading: 0.72em,
    spacing: 0pt,
  )
  #v(-3.2em)
  #grid(
    columns: (1fr, 0.85fr, 1.2fr),
    align: (center, center, center),
    [
      #text(size: 15pt, weight: "bold")[Problem Chosen]
      #v(0.75em)
      #text(size: 32pt, weight: "regular")[#problem-chosen]
    ],
    [
      #text(size: 15pt, weight: "bold")[#year]
      #linebreak()
      #text(size: 15pt, weight: "bold")[MCM/ICM]
      #linebreak()
      #text(size: 15pt, weight: "bold")[Summary Sheet]
    ],
    [
      #text(size: 13pt, weight: "bold")[Team Control Number]
      #v(0.45em)
      #text(size: 32pt, weight: "regular")[#team-number]
    ],
  )
  #v(0.42em)
  #line(length: 100%, stroke: 0.8pt)
  #v(2.3em)
  #align(center)[#text(size: 24pt)[#paper-title]]
  #v(2.2em)
  #align(center)[#text(size: 14pt, weight: "bold")[Summary]]
  #v(2.0em)
  \[#summary-placeholder\]
]

#set text(font: roman, size: 12pt, lang: "en")
#set par(first-line-indent: 2em, justify: true, leading: 0.82em, spacing: 0.5em)
#set enum(numbering: "1.", spacing: 0.9em)
#set heading(numbering: "1.1")
#set table(inset: (x: 0.7em, y: 0.26em))

#show heading.where(level: 1): it => block(above: 1.45em, below: 0.95em)[
  #text(size: 20.5pt, weight: "regular")[
    #counter(heading).display("1") #h(1.25em)#it.body
  ]
]
#show heading.where(level: 2): it => block(above: 1.1em, below: 0.65em)[
  #text(size: 16.5pt, weight: "regular")[
    #counter(heading).display("1.1") #h(1.25em)#it.body
  ]
]
#show raw.where(block: true): it => block(
  width: 100%,
  stroke: (
    top: (paint: black, thickness: 0.55pt),
    bottom: (paint: black, thickness: 0.55pt),
  ),
  inset: 0pt,
  above: 0.2em,
  below: 0.2em,
)[
  #text(font: mono, size: 9.7pt)[#it]
]

#let three-line-table(caption, columns, header, body, inset: (x: 0.35em, y: 0.52em), cell-align: center) = {
  let col-count = header.len()
  let body-rows = calc.floor(body.len() / col-count)
  let bottom-y = body-rows + 1
  let styled-header = header.map(cell => strong(cell))

  block(width: 100%, breakable: false)[
    #align(center)[
      #box[
        #align(center)[#text(font: sans, size: 10.5pt, weight: "bold")[#caption]]
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

#sheet()

#set page(
  paper: "a4",
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
  numbering: "1",
  header: page-header,
  footer: none,
)
#counter(page).update(1)
#pagebreak()
#toc-title
#v(1.9em)
#toc-entry([1 #h(1em) Introduction], [2])
#toc-entry([1.1 #h(0.9em) Background], [2], level: 2)
#toc-entry([1.2 #h(0.9em) Problem Statement], [2], level: 2)
#toc-entry([1.3 #h(0.9em) Our Approach], [2], level: 2)
#toc-entry([2 #h(1em) Assumptions and Justifications], [2])
#toc-entry([3 #h(1em) Notations and Terminology], [2])
#toc-entry([4 #h(1em) Solution and Results], [2])
#toc-entry([4.1 #h(0.9em) Problem 1], [2], level: 2)
#toc-entry([4.2 #h(0.9em) Problem 2], [3], level: 2)
#toc-entry([4.3 #h(0.9em) Problem 3], [3], level: 2)
#toc-entry([5 #h(1em) Sensitivity Analysis], [3])
#toc-entry([6 #h(1em) Strengths and Weaknesses], [3])
#toc-entry([6.1 #h(0.9em) Strengths], [3], level: 2)
#toc-entry([6.2 #h(0.9em) Weaknesses], [3], level: 2)
#toc-entry([7 #h(1em) Conclusions], [4])
#toc-entry([A #h(1em) Core Code], [4])

#pagebreak()
#include "sections/1_introduction.typ"
#include "sections/2_assumptions.typ"
#include "sections/3_notations.typ"
#include "sections/4_model.typ"
#include "sections/6_sensitivity.typ"
#include "sections/7_evaluation.typ"
#pagebreak()
#include "sections/8_conclusions.typ"

#block(above: 1.15em, below: 0.7em)[
  #text(size: 20.5pt)[References]
]

#block(above: 1.15em, below: 0.7em)[
  #text(size: 20.5pt)[A #h(1.25em) Core Code]
]
#include "sections/A_code.typ"
