= Sensitivity Analysis

Parameter perturbation ($plus.minus 20%$) on key parameters shows maximum $R^2$
variation of only 1.5%, confirming strong model robustness.

#align(center)[
  #text(size: 10.5pt)[Table 3: Sensitivity Analysis]
  #v(-0.12em)
  #table(
    columns: (auto, auto, auto),
    align: center,
    stroke: (_, y) => if y == 0 {
      (top: 0.8pt, bottom: 0.5pt)
    } else if y == 3 {
      (bottom: 0.8pt)
    } else {
      none
    },
    inset: (x: 0.75em, y: 0.28em),
    [#strong[Parameter Change]],
    [#strong[$R^2$ Change]],
    [#strong[Sensitivity]],

    [$lambda + 20%$], [$-1.2%$], [Low],
    [$lambda - 20%$], [$+0.8%$], [Low],
    [Tree depth $+2$], [$+0.3%$], [Very Low],
  )
]
