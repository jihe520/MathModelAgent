# Ellipse

# ellipse

An ellipse with optional content.

## Example

```typst
// Without content.
#ellipse(width: 35%, height: 30pt)

// With content.
#ellipse[
  #set align(center)
  Automatically sized \
  to fit the content.
]
```

```typst
#ellipse(
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

- width:
  - description: The ellipse\'s width, relative to its parent container.
  - type: auto | relative
  - default: auto
- height:
  - description: The ellipse\'s height, relative to its parent container.
  - type: auto | relative | fraction
  - default: auto
- fill:
  - description: How to fill the ellipse. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-fill) for more details.
  - type: none | color | gradient | tiling
  - default: none
- stroke:
  - description: How to stroke the ellipse. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-stroke) for more details.
  - type: none | auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- inset:
  - description: How much to pad the ellipse\'s content. See the [box\'s documentation](/docs/reference/layout/box/#parameters-inset) for more details.
  - type: relative | dictionary
  - default: 0 % + 5pt
- outset:
  - description: How much to expand the ellipse\'s size without affecting the layout. See the [box\'s documentation](/docs/reference/layout/box/#parameters-outset) for more details.
  - type: relative | dictionary
  - default: (:)
- body:
  - description: The content to place into the ellipse. When this is omitted, the ellipse takes on a default size of at most `45pt` by `30pt`.
  - type: none | content
  - default: none


