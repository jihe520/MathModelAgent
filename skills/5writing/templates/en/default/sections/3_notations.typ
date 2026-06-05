= Notations and Terminology

Key notations used throughout this paper:

#v(0.7em)
#align(center)[
  #text(size: 10.5pt)[Table 1: Key Notations]
  #v(-0.12em)
  #table(
    columns: (3.1em, 12.1em, 3.2em),
    align: center,
    stroke: (x, y) => if y == 0 {
      (top: 0.75pt, bottom: 0.5pt)
    } else if y == 5 {
      (bottom: 0.75pt)
    } else if x > 0 {
      (left: 0.45pt)
    } else {
      none
    },
    inset: (x: 0.28em, y: 0.12em),
    [#strong[Symbol]], [#strong[Description]], [#strong[Units]],
    [$N$], [Number of samples], [--],
    [$M$], [Feature dimension], [--],
    [$theta$], [Model parameter vector], [--],
    [$R^2$], [Coefficient of determination], [--],
    [RMSE], [Root mean squared error], [--],
  )
]
