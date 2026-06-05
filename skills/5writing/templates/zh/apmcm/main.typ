#let paper-title = "[Paper Title]"
#let problem-chosen = [A/B/C]
#let team-number = [Team Number]
#let school-name = [School Name]
#let member-a = [Member A]
#let member-b = [Member B]
#let member-c = [Member C]
#let adviser-name = []
#let fill-date = []
#let current-year = str(datetime.today().year())
#let apmcm-appendix-mode = state("apmcm-appendix-mode", false)

#let apmcm-heading-numbering(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("1.", ns.at(0))
  } else if ns.len() == 2 {
    numbering("1.1", ns.at(0), ns.at(1))
  } else {
    numbering("1.1.1", ns.at(0), ns.at(1), ns.at(2))
  }
}

#let apmcm-appendix-numbering(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("A.", ns.at(0))
  } else if ns.len() == 2 {
    numbering("A.1", ns.at(0), ns.at(1))
  } else {
    numbering("A.1.1", ns.at(0), ns.at(1), ns.at(2))
  }
}

#let apmcm-header-mark() = context {
  let heads = query(selector(heading.where(level: 1)).before(here()))
  if heads.len() > 0 {
    let last = heads.at(heads.len() - 1)
    let nums = counter(heading).at(last.location())
    text(size: 10pt)[#numbering("1.", nums.at(0)) #last.body]
  } else {
    []
  }
}

#set document(title: paper-title, author: ())
#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
  header-ascent: 42%,
  footer-descent: 45%,
  header: context {
    if counter(page).get().first() > 1 {
      stack(
        spacing: 2pt,
        grid(
          columns: (1fr, 1fr),
          text(size: 10pt)[#apmcm-header-mark()],
          align(right)[#text(size: 10pt)[#apmcm-header-mark()]],
        ),
        line(length: 100%, stroke: 0.45pt),
      )
    }
  },
  footer: context {
    if counter(page).get().first() > 1 {
      align(center)[#text(size: 10pt)[#counter(page).display("1")]]
    }
  },
)
#set text(font: ("Times New Roman", "Times", "Songti SC", "STSong", "New Computer Modern"), size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 0.58em)
#set enum(numbering: "1.")
#set figure(supplement: [Figure])
#set table(stroke: 0.5pt, inset: (x: 5pt, y: 3pt))
#set heading(numbering: apmcm-heading-numbering)

#show heading.where(level: 1): it => block(width: 100%, above: 1.25em, below: 0.8em)[
  #align(center)[
    #text(size: 17pt, weight: "bold")[
      #context {
        if apmcm-appendix-mode.get() {
          it
        } else {
          [#counter(heading).display("I.")#h(0.5em)#it.body]
        }
      }
    ]
  ]
]
#show heading.where(level: 2): it => block(above: 1em, below: 0.45em)[
  #text(size: 14pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.9em, below: 0.4em)[
  #text(size: 12pt, weight: "bold", style: "italic")[#it]
]
#show figure.caption: it => text(size: 10pt, weight: "bold")[#it]

#let line-field(body, width: 100%) = box(
  width: width,
  height: 1.45em,
  inset: (left: 0.5em, bottom: 2pt),
  stroke: (bottom: 0.45pt),
)[
  #body
]

#let form-row(label, value, width: 12.8cm) = pad(left: 2em)[
  #box(width: width)[
    #grid(
      columns: (auto, 1fr),
      column-gutter: 0.8em,
      [#label],
      line-field(value),
    )
  ]
]

#let member-rows(width: 12.8cm) = pad(left: 2em)[
  #box(width: width)[
    #grid(
      columns: (auto, auto, 1fr),
      column-gutter: 0.25em,
      row-gutter: 0.14em,
      [Member name (Handwriting signature):],
      [1.],
      line-field(member-a),
      [],
      [2.],
      line-field(member-b),
      [],
      [3.],
      line-field(member-c),
    )
  ]
]

#let summary-table() = align(center)[
  #table(
    columns: (auto, 4cm),
    align: (left, left),
    [Team Number:],
    [#team-number],
    [Problem Chosen:],
    [#problem-chosen],
  )
]

#let control-sheet() = {
  set par(first-line-indent: 2em, justify: true, leading: 0.72em)
  align(center)[#text(size: 21pt, weight: "bold")[#current-year APMCM Control Sheet]]
  v(1.05em)
  block[
    #strong[Each team member must sign the statement below:]

    (Failure to obtain signatures from each team member will result in disqualification of the
    entire team.)

    Each of us hereby testifies that our team abided by all of the contest's rules and
    did not consult with anyone who was not on this team in developing the enclosed
    solution paper. Our submission and all rights to its publication become the property of
    APMCM. APMCM may use, edit, excerpt, and publish this submission for
    promotional use or any other purpose, including placing it online, distributing it
    electronically or otherwise, without compensation of any kind. APMCM reserves the
    right to use in materials relating to this contest, the names of the team members,
    their advisor(s), and their affiliations, without further notification, permission, or
    compensation. Team members assert that All images, figures, photographs, tables,
    and drawings in their submission were either created by the team or else, if
    reproduced from another source, the submission cites a specific reference for each
    at its location in the submission. All direct quotations in the submission are
    enclosed in quotation marks or otherwise identified as such, with a specific
    reference cited for each at its location in the submission.
  ]
  v(0.45em)
  form-row([Problem chosen is (A or B):], problem-chosen)
  v(0.18em)
  form-row([Team control number is (team number):], team-number)
  v(0.18em)
  form-row([School (Please fill in the full name):], school-name)
  v(0.18em)
  member-rows()
  v(0.22em)
  form-row([Team adviser name:], adviser-name)
  v(0.15em)
  [(Please check the above content carefully, #strong[fill in English], and will not be
  allowed to make any changes after submission. Such as fill in error, the thesis may
  be canceled qualification awards.)]
  v(1.05em)
  align(right)[
    #box(width: 5.8cm)[
      #grid(
        columns: (auto, 1fr),
        column-gutter: 0.3em,
        [Date:],
        line-field(fill-date),
      )
    ]
  ]
}

#let summary-sheet() = {
  pagebreak()
  v(0.4em)
  summary-table()
  v(1.35em)
  line(length: 100%, stroke: 2pt)
  v(1.35em)
  align(center)[#text(size: 12pt)[#current-year APMCM summary sheet]]
  v(1.2em)
  [\[Summary: problem overview + methods for each sub-problem + key numerical results + conclusions, 300-500 words\]]
  v(0.45em)
  [#text(size: 15pt, weight: "bold")[Keywords：] #h(0.25em) [Keyword1]; [Keyword2]; [Keyword3]]
}

#let toc-page() = {
  pagebreak()
  align(center)[#text(size: 17pt)[Contents]]
  v(1em)
  outline(title: none)
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
        #align(center)[#text(font: ("Arial", "Heiti SC", "STHeiti"), size: 10.5pt, weight: "bold")[#caption]]
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

#control-sheet()
#summary-sheet()
#toc-page()

#include("sections/1_introduction.typ")
#include("sections/2_assumptions.typ")
#include("sections/3_model_design.typ")
#include("sections/4_solution.typ")
#include("sections/5_sensitivity.typ")
#include("sections/6_strengths_weaknesses.typ")
#include("sections/7_conclusions.typ")

= References
#include("references.typ")

#apmcm-appendix-mode.update(true)
#set heading(numbering: apmcm-appendix-numbering)
#counter(heading).update(0)
= Appendix
#include("sections/A_code.typ")
