= Solution and Results

== Problem 1

Multiple models were compared:

#align(center)[
  #text(size: 12pt)[Table 1: Model Performance Comparison]
  #v(-0.08em)
  #table(
    columns: (12em, 6.2em, 6.2em),
    align: center,
    stroke: (_, y) => if y == 0 {
      (top: 0.8pt, bottom: 0.5pt)
    } else if y == 3 {
      (bottom: 0.8pt)
    } else {
      none
    },
    inset: (x: 0.65em, y: 0.18em),
    [#strong[Model]], [#strong[Train $R^2$]], [#strong[Test $R^2$]],
    [Linear Regression], [0.852], [0.834],
    [Ridge Regression], [0.861], [0.847],
    [Random Forest], [0.921], [0.896],
  )
]

Random Forest achieves the best $R^2$ of 0.896 on the test set.

== Problem 2

LASSO-based feature selection identifies 8 key features. The optimized model
achieves $R^2 = 0.923$ with 15% RMSE reduction.

== Problem 3

A genetic algorithm (population size 200, 100 generations) solves the
constrained optimization, converging to a stable solution efficiently.
