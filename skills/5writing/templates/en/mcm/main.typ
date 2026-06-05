#set document(title: "[Paper Title]", author: ())

#let roman = ("Times New Roman", "Times", "New Computer Modern")
#let sans = ("Arial", "Helvetica", "Helvetica Neue")
#let mono = ("Courier New", "Courier", "Menlo", "Monaco")

#let year = "2026"
#let team-number = "0000"
#let problem-chosen = "A"
#let paper-title = "[Paper Title]"
#let paper-date = "June 3, 2026"
#let summary-placeholder = "[Summary: problem overview + methods for each sub-problem + key numerical results + conclusions, 300-500 words]"
#let keywords = "[Keyword1]; [Keyword2]; [Keyword3]"
#let total-pages = "4"

#let page-header = [
  #grid(
    columns: (1fr, 1fr),
    align: (left, right),
    text(font: sans, size: 11pt)[Team \# #team-number],
    text(font: sans, size: 11pt)[
      Page #context {
        let physical = counter(page).get().first()
        [#(physical - 2)]
      } of #total-pages
    ],
  )
  #v(0.12em)
  #line(length: 100%, stroke: 0.55pt)
]

#let sheet() = [
  #set page(
    paper: "a4",
    margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
    numbering: none,
    header: none,
    footer: none,
  )
  #set text(font: roman, size: 12pt, lang: "en")
  #set par(
    first-line-indent: 0pt,
    justify: false,
    leading: 0.72em,
    spacing: 0pt,
  )

  #v(-1.8em)
  #grid(
    columns: (1fr, 0.9fr, 1.25fr),
    align: (center, center, center),
    [
      #text(size: 15pt, weight: "bold")[Problem Chosen]
      #v(0.7em)
      #text(size: 31pt, weight: "bold")[#problem-chosen]
    ],
    [
      #text(size: 15pt, weight: "bold")[#year]
      #linebreak()
      #text(size: 15pt, weight: "bold")[MCM/ICM]
      #linebreak()
      #text(size: 15pt, weight: "bold")[Summary Sheet]
    ],
    [
      #text(size: 13.5pt, weight: "bold")[Team Control Number]
      #v(0.44em)
      #text(size: 31pt, weight: "bold")[#team-number]
    ],
  )
  #v(0.43em)
  #line(length: 100%, stroke: 0.8pt)
  #v(2.4em)
  #align(center)[#text(size: 14pt, weight: "bold")[Summary]]
  #v(2.1em)
  #block(width: 100%)[#summary-placeholder]
  #v(0.75em)
  #text(weight: "bold")[Keywords:] #keywords
]

#let title-page() = [
  #set page(
    paper: "a4",
    margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
    numbering: none,
    header: none,
    footer: none,
  )
  #set text(font: roman, size: 12pt, lang: "en")
  #set par(
    first-line-indent: 0pt,
    justify: false,
    leading: 0.72em,
    spacing: 0pt,
  )

  #v(0.25em)
  #align(center)[#text(size: 24pt)[#paper-title]]
  #v(5.8em)
  #align(center)[#text(size: 15pt)[#paper-date]]
  #v(2.75em)
  #align(center)[#text(size: 14pt, weight: "bold")[Summary]]
  #v(2.1em)
  #block(width: 100%)[#summary-placeholder]
  #v(0.75em)
  #text(weight: "bold")[Keywords:] #keywords
]

#let leader() = box(width: 1fr, baseline: 0.64em)[
  #line(length: 100%, stroke: (
    paint: black,
    thickness: 0.52pt,
    dash: "dotted",
  ))
]

#let toc-entry(num, title, page, level: 1, leader-line: true) = block(
  above: if level == 1 {
    1.05em
  } else { 0.55em },
)[
  #grid(
    columns: (auto, auto, 1fr, auto),
    column-gutter: if level == 1 { 0.95em } else { 0.65em },
    inset: (left: if level == 1 { 0pt } else { 2.35em }),
    text(size: 12pt, weight: if level == 1 { "bold" } else { "regular" })[#num],
    text(size: 12pt, weight: if level == 1 { "bold" } else {
      "regular"
    })[#title],
    if leader-line { leader() } else { [] },
    text(size: 12pt, weight: if level == 1 { "bold" } else {
      "regular"
    })[#page],
  )
]

#let contents-page() = [
  #set par(
    first-line-indent: 0pt,
    justify: false,
    leading: 0.75em,
    spacing: 0pt,
  )
  #align(center)[#text(font: sans, size: 19pt, weight: "bold")[Contents]]
  #v(2.0em)
  #toc-entry([1], [Introduction], [2], leader-line: false)
  #toc-entry([1.1], [Background], [2], level: 2)
  #toc-entry([1.2], [Problem Statement], [2], level: 2)
  #toc-entry([1.3], [Our Approach], [2], level: 2)
  #toc-entry([2], [Assumptions and Justifications], [2], leader-line: false)
  #toc-entry([3], [Model Design and Methodology], [2], leader-line: false)
  #toc-entry([3.1], [Prediction Model], [2], level: 2)
  #toc-entry([3.2], [Optimization Objective], [2], level: 2)
  #toc-entry([3.3], [Ensemble Strategy], [2], level: 2)
  #toc-entry([4], [Solution and Results], [3], leader-line: false)
  #toc-entry([4.1], [Problem 1], [3], level: 2)
  #toc-entry([4.2], [Problem 2], [3], level: 2)
  #toc-entry([4.3], [Problem 3], [3], level: 2)
  #toc-entry([5], [Sensitivity Analysis], [3], leader-line: false)
  #toc-entry([6], [Strengths and Weaknesses], [3], leader-line: false)
  #toc-entry([6.1], [Strengths], [3], level: 2)
  #toc-entry([6.2], [Weaknesses], [3], level: 2)
  #toc-entry([7], [Conclusions], [4], leader-line: false)
  #toc-entry([], [Appendices], [4], leader-line: false)
  #toc-entry([Appendix A], [Core Code], [4], leader-line: false)
]

#set text(font: roman, size: 12pt, lang: "en")
#set par(first-line-indent: 2em, justify: true, leading: 0.82em, spacing: 0.5em)
#set enum(numbering: "1.", spacing: 0.9em)
#set heading(numbering: "1.1")
#set table(inset: (x: 0.7em, y: 0.26em))

#show heading.where(level: 1): it => block(above: 1.2em, below: 0.55em)[
  #text(size: 20pt, weight: "bold")[
    #counter(heading).display("1") #h(1.25em)#it.body
  ]
]
#show heading.where(level: 2): it => block(above: 0.82em, below: 0.4em)[
  #text(size: 16pt, weight: "bold")[
    #counter(heading).display("1.1") #h(1.15em)#it.body
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
  #text(font: mono, size: 9.6pt)[#it]
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
#pagebreak()
#title-page()
#pagebreak()

#set page(
  paper: "a4",
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
  numbering: "1",
  header: page-header,
  footer: none,
)
#contents-page()
#pagebreak()

#include "sections/1_introduction.typ"
#include "sections/2_assumptions.typ"
#include "sections/3_model_design.typ"
#pagebreak()
#include "sections/4_solution.typ"
#include "sections/5_sensitivity.typ"
#include "sections/6_strengths_weaknesses.typ"
#pagebreak()
#include "sections/7_conclusions.typ"

#block(above: 1.15em, below: 0.7em)[
  #text(size: 20pt, weight: "bold")[References]
]
#include "references.typ"

#block(above: 1.35em, below: 0.9em)[
  #text(size: 28pt, weight: "bold")[Appendices]
]
#block(above: 0.9em, below: 0.4em)[
  #text(size: 20pt, weight: "bold")[Appendix A #h(1.25em) Core Code]
]
#include "sections/A_code.typ"
