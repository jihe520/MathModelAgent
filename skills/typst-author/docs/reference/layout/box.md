# Box

# box

An inline-level container that sizes content.

All elements except inline math, text, and boxes are block-level and cannot occur inside of a [paragraph](/docs/reference/model/par/). The box function can be used to integrate such elements into a paragraph. Boxes take the size of their contents by default but can also be sized explicitly.

## Example

```typst
Refer to the docs
#box(
  height: 9pt,
  image("docs.svg")
)
for more information.
```

```typst
#box(
  width: auto | relative | fraction,
  height: auto | relative,
  baseline: relative,
  fill: none | color | gradient | tiling,
  stroke: none | length | color | gradient | stroke | tiling | dictionary,
  radius: relative | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  clip: bool,
  body
) -> content
```

## Parameters

- width:
  - description: The width of the box. Boxes can have [fractional](/docs/reference/layout/fraction/) widths, as the example below demonstrates. _Note:_ Currently, only boxes and only their widths might be fractionally sized within paragraphs. Support for fractionally sized images, shapes, and more might be added in the future. ```typst Line in #box(width: 1fr, line(length: 100%)) between. ```
  - type: auto | relative | fraction
  - default: auto
- height:
  - description: The height of the box.
  - type: auto | relative
  - default: auto
- baseline:
  - description: An amount to shift the box\'s baseline by. ```typst Image: #box(baseline: 40%, image("tiger.jpg", width: 2cm)). ```
  - type: relative
  - default: 0 % + 0pt
- fill:
  - description: The box\'s background color. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-fill) for more details.
  - type: none | color | gradient | tiling
  - default: none
- stroke:
  - description: The box\'s border color. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-stroke) for more details.
  - type: none | length | color | gradient | stroke | tiling | dictionary
  - default: (:)
- radius:
  - description: How much to round the box\'s corners. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-radius) for more details.
  - type: relative | dictionary
  - default: (:)
- inset:
  - description: How much to pad the box\'s content. This can be a single length for all sides or a dictionary of lengths for individual sides. When passing a dictionary, it can contain the following keys in order of precedence: `top`, `right`, `bottom`, `left` (controlling the respective cell sides), `x`, `y` (controlling vertical and horizontal insets), and `rest` (covers all insets not styled by other dictionary entries). All keys are optional; omitted keys will use their previously set value, or the default value if never set. [Relative lengths](/docs/reference/layout/relative/) for this parameter are relative to the box size excluding [outset](/docs/reference/layout/box/#parameters-outset). Note that relative insets and outsets are different from relative [widths](/docs/reference/layout/box/#parameters-width) and [heights](/docs/reference/layout/box/#parameters-height), which are relative to the container. _Note:_ When the box contains text, its exact size depends on the current [text edges](/docs/reference/text/text/#parameters-top-edge). ```typst #rect(inset: 0pt)[Tight] ```
  - type: relative | dictionary
  - default: (:)
- outset:
  - description: How much to expand the box\'s size without affecting the layout. This can be a single length for all sides or a dictionary of lengths for individual sides. [Relative lengths](/docs/reference/layout/relative/) for this parameter are relative to the box size excluding outset. See the documentation for [inset](/docs/reference/layout/box/#parameters-inset) above for further details. This is useful to prevent padding from affecting line layout. For a generalized version of the example below, see the documentation for the [raw text\'s block parameter](/docs/reference/text/raw/#parameters-block). ```typst An inline #box(  fill: luma(235),  inset: (x: 3pt, y: 0pt),  outset: (y: 3pt),  radius: 2pt, )[rectangle]. ```
  - type: relative | dictionary
  - default: (:)
- clip:
  - description: Whether to clip the content inside the box. Clipping is useful when the box\'s content is larger than the box itself, as any content that exceeds the box\'s bounds will be hidden. ```typst #box(  width: 50pt,  height: 50pt,  clip: true,  image("tiger.jpg", width: 100pt, height: 100pt) ) ```
  - type: bool
  - default: false
- body:
  - description: The contents of the box.
  - type: none | content
  - default: none


