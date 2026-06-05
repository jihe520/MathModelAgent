= Sensitivity Analysis

Parameter perturbation ($plus.minus 20%$) on key parameters shows maximum $R^2$
variation of only 1.5%, confirming strong model robustness.

#align(center)[#text(size: 11pt)[Table 2: Sensitivity Analysis]]
#align(center)[
  #table(
    columns: (auto, auto, auto),
    align: center,
    stroke: none,
    inset: (x: 0.75em, y: 0.28em),
    table.hline(stroke: 0.8pt),
    [#strong[Parameter Change]],
    [#strong[$R^2$ Change]],
    [#strong[Sensitivity]],
    table.hline(stroke: 0.5pt),
    [$lambda + 20%$], [$-1.2%$], [Low],
    [$lambda - 20%$], [$+0.8%$], [Low],
    [Tree depth $+2$], [$+0.3%$], [Very Low],
    table.hline(stroke: 0.8pt),
  )
]
