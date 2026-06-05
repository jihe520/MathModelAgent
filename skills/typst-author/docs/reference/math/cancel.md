# Cancel

# math.cancel

Displays a diagonal line over a part of an equation.

This is commonly used to show the elimination of a term.

## Example

```typst
Here, we can simplify:
$ (a dot b dot cancel(x)) /
    cancel(x) $
```

```typst
#math.cancel(
  body,
  length: relative,
  inverted: bool,
  cross: bool,
  angle: auto | angle | function,
  stroke: length | color | gradient | stroke | tiling | dictionary
) -> content
```

## Parameters

- body:
  - description: The content over which the line should be placed.
  - type: content
  - default: None
- length:
  - description: The length of the line, relative to the length of the diagonal spanning the whole element being "cancelled". A value of `100%` would then have the line span precisely the element\'s diagonal. ```typst $ a + cancel(x, length: #200%)   - cancel(x, length: #200%) $ ```
  - type: relative
  - default: 100 % + 3pt
- inverted:
  - description: Whether the cancel line should be inverted (flipped along the y-axis). For the default angle setting, inverted means the cancel line points to the top left instead of top right. ```typst $ (a cancel((b + c), inverted: #true)) /   cancel(b + c, inverted: #true) $ ```
  - type: bool
  - default: false
- cross:
  - description: Whether two opposing cancel lines should be drawn, forming a cross over the element. Overrides `inverted`. ```typst $ cancel(Pi, cross: #true) $ ```
  - type: bool
  - default: false
- angle:
  - description: How much to rotate the cancel line. - If given an angle, the line is rotated by that angle clockwise with respect to the y-axis. - If `auto`, the line assumes the default angle; that is, along the rising diagonal of the content box. - If given a function `angle => angle`, the line is rotated, with respect to the y-axis, by the angle returned by that function. The function receives the default angle as its input. ```typst $ cancel(Pi)  cancel(Pi, angle: #0deg)  cancel(Pi, angle: #45deg)  cancel(Pi, angle: #90deg)  cancel(1/(1+x), angle: #(a => a + 45deg))  cancel(1/(1+x), angle: #(a => a + 90deg)) $ ```
  - type: auto | angle | function
  - default: auto
- stroke:
  - description: How to [stroke](/docs/reference/visualize/stroke/) the cancel line. ```typst $ cancel(  sum x,  stroke: #(   paint: red,   thickness: 1.5pt,   dash: "dashed",  ), ) $ ```
  - type: length | color | gradient | stroke | tiling | dictionary
  - default: 0.5pt


