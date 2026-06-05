#let paper-title = "[论文标题]"
#let team-number = "[队伍编号]"
#let problem-id = "[A/B/C]"
#let track-name = "[本科生/研究生]"
#let current-year = str(datetime.today().year())

#let body-font = ("Times New Roman", "SimSun", "NSimSun", "Songti SC", "STSong")
#let song-font = ("SimSun", "NSimSun", "Songti SC", "STSong", "Times New Roman")
#let hei-font = ("SimHei", "Heiti SC", "STHeiti", "SimSun")

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

#let line-field(body, width: 100%, height: 1.35em, body-align: center) = box(
  width: width,
  height: height,
  inset: (x: 0.25em, bottom: 1.5pt),
  stroke: (bottom: 0.55pt),
)[
  #align(body-align)[#body]
]

#let info-field(body, width: 100%) = box(
  width: width,
  height: 1em,
  inset: (x: 0.2em, bottom: 1.2pt),
  stroke: (bottom: 0.55pt),
)[#align(center)[#body]]

#let song-bold(body, size: 12pt, fill: black, stroke-width: 0.18pt) = text(
  font: song-font,
  size: size,
  weight: "regular",
  fill: fill,
  stroke: stroke-width + fill,
)[#body]

#let shadow-title(body) = {
  box(width: 100%, height: 1.18em)[
    #place(center, dx: 1pt, dy: 1pt)[
      #song-bold(body, size: 22pt, fill: luma(125), stroke-width: 0.16pt)
    ]
    #place(center)[
      #song-bold(body, size: 22pt, stroke-width: 0.16pt)
    ]
  ]
}

#let info-box() = align(center)[
  #move(dx: 2.5pt)[
    #rect(
      width: 415.5pt,
      stroke: 0.55pt,
      inset: 0pt,
    )[
      #box(width: 100%, height: 35pt)[
        #place(top + center, dy: 4pt)[
          #text(size: 10.5pt)[参赛编号: #team-number]
        ]
        #place(top + center, dy: 19pt)[
          #text(size: 10.5pt)[
            选题:
            #info-field(problem-id, width: 1.5cm)
            #h(0.35em)
            参赛赛道:
            #info-field(track-name, width: 3cm)
          ]
        ]
      ]
    ]
  ]
]

#let title-row() = align(center)[
  #move(dx: 15pt)[
    #box(width: 392pt, height: 24.5pt)[
      #place(top + left, dx: 0pt, dy: 0pt)[
        #text(font: hei-font, size: 15.75pt, weight: "bold")[题#h(1em)目]
      ]
      #place(top + left, dx: 62pt, dy: 0pt)[
        #box(width: 330pt)[
          #align(center)[#text(font: hei-font, size: 15.75pt, weight: "bold")[#paper-title]]
        ]
      ]
      #place(top + left, dx: 62pt, dy: 19.5pt)[
        #line(length: 330pt, stroke: 0.8pt)
      ]
    ]
  ]
]

#let cover-summary() = {
  set align(left)
  set par(first-line-indent: 2em, justify: true, leading: 0.7em)

  v(-12mm)
  info-box()
  v(0.45em)
  shadow-title([#current-year 年第四届长三角高校数学建模竞赛])
  v(2em)
  title-row()
  v(-0.36em)
  align(center)[
    #song-bold([摘#h(1em)要：], size: 15.75pt, stroke-width: 0.14pt)
  ]
  v(0.05em)
  block(inset: (x: 1cm))[
    [中文摘要内容：问题概述 + 每个子问题的方法和数值结果 + 结论]
  ]
}

#let toc-entry(label, title, page, indent: 0pt) = block(height: 1.82em)[
  #grid(
    columns: (1fr, 2em),
    column-gutter: 1em,
    align: (left, right),
    [#box(width: 100%, inset: (left: indent))[#label #h(0.45em)#title]],
    [#page],
  )
]

#let toc-page() = {
  pagebreak()
  align(center)[#text(font: hei-font, size: 17pt, weight: "bold")[目录]]
  v(1.55em)
  text(font: body-font, size: 12pt, weight: "bold")[
    #toc-entry([一、], [1 restatement], [3])
    #toc-entry([二、], [2 analysis], [3])
    #toc-entry([三、], [3 assumptions], [3])
    #toc-entry([四、], [4 symbols], [3])
    #toc-entry([五、], [5 problem1], [3])
    #toc-entry([六、], [6 problem2], [3])
    #toc-entry([七、], [7 problem3], [3])
    #toc-entry([八、], [8 evaluation], [4])
    #toc-entry([], [Appendices], [4])
    #toc-entry([附录 A], [A code], [4])
  ]
  pagebreak()
}

#let references-cn() = block(above: 1.1em, below: 1.2em, width: 100%)[
  #align(center)[#text(font: body-font, size: 14pt, weight: "bold")[参考文献]]
]

#let appendix-cn(file: "sections/A_code.typ") = [
#v(1.6em)
#text(font: body-font, size: 26pt, weight: "regular")[Appendices]
#v(0em)
#include(file)
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

#set document(title: "[论文标题]", author: ())
#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 25mm, right: 25mm),
  numbering: none,
  footer: none,
)
#set text(font: body-font, size: 12pt, lang: "zh")
#set par(first-line-indent: (amount: 2em, all: true), justify: true, leading: 0.9em, spacing: 0.65em)
#set heading(numbering: cn-numbering)
#set math.equation(numbering: "(1)")
#set enum(numbering: "1.")
#set figure(supplement: [图])
#set table(stroke: 0.5pt, inset: (x: 5pt, y: 3pt))

#show heading.where(level: 1): it => block(width: 100%, above: 1.4em, below: 0.85em)[
  #align(center)[#text(font: body-font, size: 14pt, weight: "bold")[#it]]
]
#show heading.where(level: 2): it => block(above: 0.9em, below: 0.55em)[
  #text(font: body-font, size: 12pt, weight: "bold")[#it]
]
#show heading.where(level: 3): it => block(above: 0.7em, below: 0.4em)[
  #text(font: body-font, size: 10.5pt, weight: "bold")[#it]
]
#show figure.caption: it => text(font: body-font, size: 10.5pt)[#it]

#cover-summary()
#toc-page()

#include("sections/1_restatement.typ")
#include("sections/2_analysis.typ")
#include("sections/3_assumptions.typ")
#include("sections/4_symbols.typ")
#include("sections/5_problem1.typ")
#include("sections/6_problem2.typ")
#include("sections/7_problem3.typ")
#include("sections/8_evaluation.typ")

#pagebreak()
#references-cn()
#appendix-cn()
