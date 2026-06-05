#set document(title: "[Paper Title]", author: ())

#let roman = ("Times New Roman", "Times", "New Computer Modern")
#let mono = ("Courier New", "Menlo", "Monaco")

#let year = "2026"
#let team-number = "[Team Number]"
#let problem-chosen = "[A/B/C]"

#let header-line(ltext: [], rtext: []) = [
  #grid(
    columns: (1fr, 1fr),
    align: (left, right),
    text(size: 10pt, style: "italic")[#ltext],
    text(size: 10pt, style: "italic")[#rtext],
  )
  #line(length: 100%, stroke: 0.6pt)
]

#let front-page() = {
  set page(
    paper: "a4",
    margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
    numbering: none,
    header: none,
    footer: none,
  )
}
#let numbered-page(header-left: [], header-right: []) = {
  set page(
    paper: "a4",
    margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
    numbering: "1",
    header: header-line(ltext: header-left, rtext: header-right),
    footer: align(center)[#context counter(page).display()],
  )
}

#set text(font: roman, size: 12pt, lang: "en")
#set par(first-line-indent: 2em, justify: true, leading: 0.95em, spacing: 0.5em)
#set enum(numbering: "1.", spacing: 0.35em)
#show figure.caption: it => text(size: 11pt, weight: "bold")[#it]

#let sec(body) = block(width: 100%, above: 1.55em, below: 1.25em)[
  #align(center)[#text(size: 16pt, weight: "bold")[#body]]
]
#let subsec(body) = block(above: 1.25em, below: 0.7em)[
  #text(size: 13pt, weight: "bold")[#body]
]
#let problem-row(label, body) = block(above: 0.36em, below: 0.36em)[
  #h(2em)#strong[#label:] #body
]
#let toc-entry(title, page, indent: 0pt, strong: false) = {
  grid(
    columns: (auto, 1fr, auto),
    column-gutter: 0.45em,
    inset: (left: indent),
    text(weight: if strong { "bold" } else { "regular" })[#title],
    box(width: 1fr, baseline: 0.78em)[
      #line(length: 100%, stroke: (
        paint: black,
        thickness: 0.55pt,
        dash: "dotted",
      ))
    ],
    text(weight: if strong { "bold" } else { "regular" })[#page],
  )
  v(0.42em)
}
#let three-line-table(columns, body) = table(
  columns: columns,
  align: center,
  inset: (x: 10pt, y: 6pt),
  stroke: (_, y) => if y == 0 {
    (top: 1.4pt, bottom: 0.75pt)
  } else if y == 3 {
    (bottom: 1.4pt)
  } else { none },
  ..body,
)
#let model-table() = align(center)[
  #table(
    columns: (auto, auto, auto),
    align: center,
    inset: (x: 10pt, y: 6pt),
    stroke: (_, y) => if y == 0 {
      (top: 1.4pt, bottom: 0.75pt)
    } else if y == 3 {
      (bottom: 1.4pt)
    } else { none },
    [#strong[Model]], [#strong[Train $R^2$]], [#strong[Test $R^2$]],
    [Linear Regression], [0.852], [0.834],
    [Ridge Regression], [0.861], [0.847],
    [Random Forest], [0.921], [0.896],
  )
]
#let sensitivity-table() = align(center)[
  #table(
    columns: (auto, auto, auto),
    align: center,
    inset: (x: 10pt, y: 6pt),
    stroke: (_, y) => if y == 0 {
      (top: 1.4pt, bottom: 0.75pt)
    } else if y == 3 {
      (bottom: 1.4pt)
    } else { none },
    [#strong[Parameter Change]],
    [#strong[$R^2$ Change]],
    [#strong[Sensitivity]],

    [$lambda + 20%$], [-1.2%], [Low],
    [$lambda - 20%$], [+0.8%], [Low],
    [Tree depth +2], [+0.3%], [Very Low],
  )
]

#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
  numbering: none,
  header: none,
  footer: none,
)
#align(center)[#text(size: 24pt, weight: "bold")[#year APMCM Control Sheet]]
#v(1.0em)
#set par(first-line-indent: 2em, justify: true, leading: 0.9em, spacing: 0.35em)
#strong[Each team member must sign the statement below:]

(Failure to obtain signatures from each team member will result in disqualification of the entire team.)

Each of us hereby testifies that our team abided by all of the contest's rules and did not consult with anyone who was not on this team in developing the enclosed solution paper. Our submission and all rights to its publication become the property of APMCM. APMCM may use, edit, excerpt, and publish this submission for promotional use or any other purpose, including placing it online, distributing it electronically or otherwise, without compensation of any kind. APMCM reserves the right to use in materials relating to this contest, the names of the team members, their advisor(s), and their affiliations, without further notification, permission, or compensation. Team members assert that All images, figures, photographs, tables, and drawings in their submission were either created by the team or else, if reproduced from another source, the submission cites a specific reference for each at its location in the submission. All direct quotations in the submission are enclosed in quotation marks or otherwise identified as such, with a specific reference cited for each at its location in the submission.

#set par(first-line-indent: 0pt, justify: true, leading: 0.8em, spacing: 0.28em)
#v(0.6em)
#let under-value(value, width) = box(width: width)[
  #align(center)[#value]
  #line(length: 100%)
]
#let field(label, value, width: 8.2cm) = block(above: 0.25em)[
  #align(center)[#label #under-value(value, width)]
]
#field([Problem chosen is (A or B):], [#problem-chosen])
#field([Team control number is (team number):], [#team-number])
#field([School (Please fill in the full name):], [[School Name]])
#grid(
  columns: (auto, auto, 1fr),
  column-gutter: 0.35em,
  row-gutter: 0.28em,
  align: (left, right, left),
  [Member name (Handwriting signature):], [1.], under-value([Member A], 7.4cm),

  [], [2.], under-value([Member B], 7.4cm),

  [], [3.], under-value([Member C], 7.4cm),
)
#block(
  above: 0.5em,
)[Team adviser name:#under-value([], 10.2cm)]

(Please check the above content carefully, #strong[fill in English], and will not be allowed to make any changes after submission. Such as fill in error, the thesis may be canceled qualification awards.)

#align(right)[Date:#under-value([], 4.5cm)]

#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
  numbering: "1",
  header: none,
  footer: align(center)[#context counter(page).display()],
)
#counter(page).update(2)
#pagebreak()
#set par(
  first-line-indent: 2em,
  justify: true,
  leading: 0.95em,
  spacing: 0.45em,
)
#line(length: 100%, stroke: 0.65pt)
#v(1.35em)
#align(center)[
  #table(
    columns: (auto, auto),
    stroke: 0.45pt,
    inset: (x: 9pt, y: 5pt),
    align: left,
    [Team Number:], [#team-number],
    [Problem Chosen:], [#problem-chosen],
  )
]
#v(1.0em)
#line(length: 100%, stroke: 2pt)
#v(1.15em)
#align(center)[#text(size: 14pt)[#year APMCM summary sheet]]
#v(1.1em)
[Summary: problem overview + methods for each sub-problem + key numerical results + conclusions, 300-500 words]
#v(0.8em)
#text(size: 15pt, weight: "bold")[Keywords:] #h(0.4em)#text(
  "[Keyword1]; [Keyword2]; [Keyword3]",
)

#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
  numbering: "1",
  header: header-line(ltext: [CONTENTS], rtext: [CONTENTS]),
  footer: align(center)[#context counter(page).display()],
)
#pagebreak()
#align(center)[#text(size: 17pt, weight: "bold")[Contents]]
#v(1.1em)
#toc-entry([1. Introduction], [4], strong: true)
#toc-entry([1.1 Background], [4], indent: 1.7em)
#toc-entry([1.2 Problem Statement], [4], indent: 1.7em)
#toc-entry([1.3 Our Approach], [4], indent: 1.7em)
#toc-entry([2. Assumptions and Justifications], [4], strong: true)
#toc-entry([3. Model Design and Methodology], [4], strong: true)
#toc-entry([3.1 Prediction Model], [4], indent: 1.7em)
#toc-entry([3.2 Optimization Objective], [4], indent: 1.7em)
#toc-entry([3.3 Ensemble Strategy], [4], indent: 1.7em)
#toc-entry([4. Solution and Results], [5], strong: true)
#toc-entry([4.1 Problem 1], [5], indent: 1.7em)
#toc-entry([4.2 Problem 2], [5], indent: 1.7em)
#toc-entry([4.3 Problem 3], [5], indent: 1.7em)
#toc-entry([5. Sensitivity Analysis], [5], strong: true)
#toc-entry([6. Strengths and Weaknesses], [6], strong: true)
#toc-entry([6.1 Strengths], [6], indent: 1.7em)
#toc-entry([6.2 Weaknesses], [6], indent: 1.7em)
#toc-entry([7. Conclusions], [6], strong: true)
#toc-entry([8. References], [6], strong: true)
#toc-entry([A. Appendix Core Code], [6], strong: true)

#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
  numbering: "1",
  header: header-line(
    rtext: [3 #h(1em) MODEL DESIGN #h(0.35em) AND METHODOLOGY],
  ),
  footer: align(center)[#context counter(page).display()],
)
#pagebreak()
#sec[ I. #h(0.45em) Introduction]
#subsec[1.1 #h(0.45em) Background]
Mathematical modeling translates real-world problems into mathematical language. This paper addresses a data-driven optimization problem using both classical and modern computational techniques.
#v(0.55em)

#subsec[1.2 #h(0.45em) Problem Statement]
#problem-row[Problem 1][Develop a predictive model with good generalization capability.]
#problem-row[Problem 2][Improve the model by considering multiple influencing factors.]
#problem-row[Problem 3][Design optimal strategies under practical constraints.]
#v(0.55em)

#set par(first-line-indent: 2em, justify: true, leading: 0.95em, spacing: 0.5em)
#subsec[1.3 #h(0.45em) Our Approach]
We employ a multi-model comparison strategy ensuring both interpretability and accuracy.
#v(0.65em)

#sec[II. #h(0.45em) Assumptions and Justifications]
To simplify the real-world problem, we make the following assumptions:

#set enum(numbering: "1.", spacing: 0.35em)
+ The provided data is accurate and free from systematic measurement errors.
+ Interaction effects between different factors are negligible.
+ The system remains in a steady state over the short term.
+ All variables are continuous and differentiable.
+ Missing values can be handled through imputation techniques.
#v(0.55em)

#sec[III. #h(0.45em) Model Design and Methodology]
#subsec[3.1 #h(0.45em) Prediction Model]
#v(0.4em)
#align(
  center,
)[$hat(y) = f(x; theta) = sum_(i=1)^n theta_i phi_i (x)$ #h(7em) (1)]
#v(0.5em)

#subsec[3.2 #h(0.45em) Optimization Objective]
#v(0.4em)
#align(
  center,
)[$cal(L)(theta) = 1 / N sum_(i=1)^N (y_i - hat(y)_i)^2 + lambda R(theta)$ #h(5em) (2)]
#v(0.5em)

#subsec[3.3 #h(0.45em) Ensemble Strategy]
Random Forest with $n = 100$ estimators and max_depth=10 for robust prediction.

#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
  numbering: "1",
  header: header-line(rtext: [5 #h(1em) SENSITIVITY ANALYSIS]),
  footer: align(center)[#context counter(page).display()],
)
#pagebreak()
#sec[IV. #h(0.45em) Solution and Results]
#subsec[4.1 #h(0.45em) Problem 1]
#h(2em)Multiple models were compared:
#v(0.9em)

#align(center)[#text(
  size: 13pt,
  weight: "bold",
)[Table 1 #h(1em) Model Performance Comparison]]
#v(0.35em)
#model-table()
#v(1.0em)

#h(2em)Random Forest achieves the best $R^2$ of 0.896 on the test set.
#v(0.75em)

#subsec[4.2 #h(0.45em) Problem 2]
#h(2em)LASSO-based feature selection identifies 8 key features. The optimized model achieves $R^2 = 0.923$ with 15% RMSE reduction.
#v(0.85em)

#subsec[4.3 #h(0.45em) Problem 3]
#h(2em)A genetic algorithm (population size 200, 100 generations) solves the constrained optimization, converging to a stable solution efficiently.
#v(0.95em)

#sec[V. #h(0.45em) Sensitivity Analysis]
#h(2em)Parameter perturbation ($plus.minus 20%$) on key parameters shows maximum $R^2$ variation of only 1.5%, confirming strong model robustness.
#v(0.85em)

#align(center)[#text(
  size: 13pt,
  weight: "bold",
)[Table 2 #h(1em) Sensitivity Analysis]]
#v(0.35em)
#sensitivity-table()

#set page(
  paper: "a4",
  margin: (top: 25.4mm, bottom: 25.4mm, left: 31.8mm, right: 31.8mm),
  numbering: "1",
  header: header-line(rtext: [A #h(1em) CORE CODE]),
  footer: align(center)[#context counter(page).display()],
)
#pagebreak()
#sec[VI. #h(0.45em) Strengths and Weaknesses]
#subsec[6.1 #h(0.45em) Strengths]
+ Solid theoretical foundations with rigorous derivations.
+ Multi-model comparison ensures optimal selection.
+ High accuracy ($R^2 = 0.923$) with good interpretability.
+ Computationally efficient for large-scale applications.

#subsec[6.2 #h(0.45em) Weaknesses]
+ Assumes data stationarity; may not hold for rapidly changing systems.
+ Does not capture temporal dynamics explicitly.

#sec[VII. #h(0.45em) Conclusions]
Our main contributions:

+ Developed a robust prediction framework achieving $R^2 = 0.923$.
+ Implemented effective feature selection for identifying key factors.
+ Designed an optimization algorithm for constrained problems.
+ Validated robustness through comprehensive sensitivity analysis.

The framework achieves high accuracy while maintaining interpretability, and can be extended to various real-world applications.

#sec[VIII. #h(0.45em) References]
#sec[I. #h(0.45em) Core Code]
#block(
  width: 100%,
  fill: rgb("#f6f6f6"),
  stroke: (
    top: (paint: rgb("#cfcfcf"), thickness: 1pt),
    bottom: (paint: rgb("#cfcfcf"), thickness: 1pt),
  ),
  inset: 0pt,
)[
  #set text(font: mono, size: 8.2pt)
  ```python
  import numpy as np
  import pandas as pd
  from sklearn.model_selection import train_test_split
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.metrics import r2_score

  data = pd.read_csv('data.csv')
  X = data.drop('target', axis=1)
  y = data['target']
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42
  )

  model = RandomForestRegressor(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)
  print(f'R2: {r2_score(y_test, model.predict(X_test)):.4f}')
  ```
]
