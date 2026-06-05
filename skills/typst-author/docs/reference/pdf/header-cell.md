# Header Cell

# pdf.header-cell

Explicitly defines a cell as a header cell.

Header cells help users of Assistive Technology (AT) understand and navigate complex tables. When your table is correctly marked up with header cells, AT can announce the relevant header information on-demand when entering a cell.

By default, Typst will automatically mark all cells within [`table.header`](/docs/reference/model/table/#definitions-header) as header cells. They will apply to the columns below them. You can use that function's [`level`](/docs/reference/model/table/#definitions-header-level) parameter to make header cells labelled by other header cells.

The `pdf.header-cell` function allows you to indicate that a cell is a header cell in the following additional situations:

- You have a **header column** in which each cell applies to its row. In that case, you pass `"row"` as an argument to the [`scope` parameter](/docs/reference/pdf/header-cell/#parameters-scope) to indicate that the header cell applies to the row.
- You have a cell in [`table.header`](/docs/reference/model/table/#definitions-header), for example at the very start, that labels both its row and column. In that case, you pass `"both"` as an argument to the [`scope`](/docs/reference/pdf/header-cell/#parameters-scope) parameter.
- You have a header cell in a row not containing other header cells. In that case, you can use this function to mark it as a header cell.

The API of this feature is temporary. Hence, calling this function requires enabling the `a11y-extras` feature flag at the moment. In a future Typst release, this functionality may move out of the `pdf` module so that tables in other export targets can contain the same information.

```typst
#show table.cell.where(x: 0): set text(weight: "medium")
#show table.cell.where(y: 0): set text(weight: "bold")

#table(
  columns: 3,
  align: (start, end, end),

  table.header(
    // Top-left cell: Labels both the nutrient rows
    // and the serving size columns.
    pdf.header-cell(scope: "both")[Nutrient],
    [Per 100g],
    [Per Serving],
  ),

  // First column cells are row headers
  pdf.header-cell(scope: "row")[Calories],
  [250 kcal], [375 kcal],
  pdf.header-cell(scope: "row")[Protein],
  [8g], [12g],
  pdf.header-cell(scope: "row")[Fat],
  [12g], [18g],
  pdf.header-cell(scope: "row")[Carbs],
  [30g], [45g],
)
```

```typst
#pdf.header-cell(
  level: int,
  scope: str,
  cell
) -> content
```

## Parameters

- level:
  - description: The nesting level of this header cell.
  - type: int
  - default: 1
- scope:
  - description: What track of the table this header cell applies to.
  - type: str
  - default: "column"
- cell:
  - description: The table cell. This can be content or a call to [`table.cell`](/docs/reference/model/table/#definitions-cell).
  - type: content
  - default: None


