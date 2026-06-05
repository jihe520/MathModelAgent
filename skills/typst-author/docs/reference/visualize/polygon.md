# Polygon

# polygon

A closed polygon.

The polygon is defined by its corner points and is closed automatically.

## Example

```typst
#polygon(
  fill: blue.lighten(80%),
  stroke: blue,
  (20%, 0pt),
  (60%, 0pt),
  (80%, 2cm),
  (0%,  2cm),
)
```

```typst
#polygon(
  fill: none | color | gradient | tiling,
  fill-rule: str,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  vertices
) -> content
```

## Parameters

- fill:
  - description: How to fill the polygon. When setting a fill, the default stroke disappears. To create a rectangle with both fill and stroke, you have to configure both.
  - type: none | color | gradient | tiling
  - default: none
- fill-rule:
  - description: The drawing rule used to fill the polygon. See the [curve documentation](/docs/reference/visualize/curve/#parameters-fill-rule) for an example.
  - type: str
  - default: "non - zero"
- stroke:
  - description: How to [stroke](/docs/reference/visualize/stroke/) the polygon. Can be set to `none` to disable the stroke or to `auto` for a stroke of `1pt` black if and only if no fill is given.
  - type: none | auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- vertices:
  - description: The vertices of the polygon. Each point is specified as an array of two [relative lengths](/docs/reference/layout/relative/).
  - type: array
  - default: None


## Definitions
### polygon.regular

A regular polygon, defined by its size and number of vertices.

```typst
#polygon.regular(
  fill: blue.lighten(80%),
  stroke: blue,
  size: 30pt,
  vertices: 3,
)
```

```typst
#polygon.regular(
  fill: none | color | gradient | tiling,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  size: length,
  vertices: int
) -> content
```

#### Parameters

- fill:
  - description: How to fill the polygon. See the general [polygon\'s documentation](/docs/reference/visualize/polygon/#parameters-fill) for more details.
  - type: none | color | gradient | tiling
  - default: None
- stroke:
  - description: How to stroke the polygon. See the general [polygon\'s documentation](/docs/reference/visualize/polygon/#parameters-stroke) for more details.
  - type: none | auto | length | color | gradient | stroke | tiling | dictionary
  - default: None
- size:
  - description: The diameter of the [circumcircle](https://en.wikipedia.org/wiki/Circumcircle) of the regular polygon.
  - type: length
  - default: 1em
- vertices:
  - description: The number of vertices in the polygon.
  - type: int
  - default: 3


