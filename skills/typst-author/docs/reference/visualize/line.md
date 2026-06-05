# Line

# line

A line from one point to another.

## Example

```typst
#set page(height: 100pt)

#line(length: 100%)
#line(end: (50%, 50%))
#line(
  length: 4cm,
  stroke: 2pt + maroon,
)
```

```typst
#line(
  start: array,
  end: none | array,
  length: relative,
  angle: angle,
  stroke: length | color | gradient | stroke | tiling | dictionary
) -> content
```

## Parameters

- start:
  - description: The start point of the line. Must be an array of exactly two relative lengths.
  - type: array
  - default: (0 % + 0pt, 0 % + 0pt)
- end:
  - description: The point where the line ends.
  - type: none | array
  - default: none
- length:
  - description: The line\'s length. This is only respected if `end` is `none`.
  - type: relative
  - default: 0 % + 30pt
- angle:
  - description: The angle at which the line points away from the origin. This is only respected if `end` is `none`.
  - type: angle
  - default: 0deg
- stroke:
  - description: How to [stroke](/docs/reference/visualize/stroke/) the line. ```typst #set line(length: 100%) #stack(  spacing: 1em,  line(stroke: 2pt + red),  line(stroke: (paint: blue, thickness: 4pt, cap: "round")),  line(stroke: (paint: blue, thickness: 1pt, dash: "dashed")),  line(stroke: (paint: blue, thickness: 1pt, dash: ("dot", 2pt, 4pt, 2pt))), ) ```
  - type: length | color | gradient | stroke | tiling | dictionary
  - default: 1pt + black


