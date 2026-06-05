# Circle

# circle

A circle with optional content.

## Example

```typst
// Without content.
#circle(radius: 25pt)

// With content.
#circle[
  #set align(center + horizon)
  Automatically \
  sized to fit.
]
```

```typst
#circle(
  radius: length,
  width: auto | relative,
  height: auto | relative | fraction,
  fill: none | color | gradient | tiling,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  body
) -> content
```

## Parameters

- radius:
  - description: The circle\'s radius. This is mutually exclusive with `width` and `height`.
  - type: length
  - default: 0pt
- width:
  - description: The circle\'s width. This is mutually exclusive with `radius` and `height`. In contrast to `radius`, this can be relative to the parent container\'s width.
  - type: auto | relative
  - default: auto
- height:
  - description: The circle\'s height. This is mutually exclusive with `radius` and `width`. In contrast to `radius`, this can be relative to the parent container\'s height.
  - type: auto | relative | fraction
  - default: auto
- fill:
  - description: How to fill the circle. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-fill) for more details.
  - type: none | color | gradient | tiling
  - default: none
- stroke:
  - description: How to stroke the circle. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-stroke) for more details.
  - type: none | auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- inset:
  - description: How much to pad the circle\'s content. See the [box\'s documentation](/docs/reference/layout/box/#parameters-inset) for more details.
  - type: relative | dictionary
  - default: 0 % + 5pt
- outset:
  - description: How much to expand the circle\'s size without affecting the layout. See the [box\'s documentation](/docs/reference/layout/box/#parameters-outset) for more details.
  - type: relative | dictionary
  - default: (:)
- body:
  - description: The content to place into the circle. The circle expands to fit this content, keeping the 1-1 aspect ratio.
  - type: none | content
  - default: none


