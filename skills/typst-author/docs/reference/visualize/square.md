# Square

# square

A square with optional content.

## Example

```typst
// Without content.
#square(size: 40pt)

// With content.
#square[
  Automatically \
  sized to fit.
]
```

```typst
#square(
  size: auto | length,
  width: auto | relative,
  height: auto | relative | fraction,
  fill: none | color | gradient | tiling,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  radius: relative | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  body
) -> content
```

## Parameters

- size:
  - description: The square\'s side length. This is mutually exclusive with `width` and `height`.
  - type: auto | length
  - default: auto
- width:
  - description: The square\'s width. This is mutually exclusive with `size` and `height`. In contrast to `size`, this can be relative to the parent container\'s width.
  - type: auto | relative
  - default: auto
- height:
  - description: The square\'s height. This is mutually exclusive with `size` and `width`. In contrast to `size`, this can be relative to the parent container\'s height.
  - type: auto | relative | fraction
  - default: auto
- fill:
  - description: How to fill the square. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-fill) for more details.
  - type: none | color | gradient | tiling
  - default: none
- stroke:
  - description: How to stroke the square. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-stroke) for more details.
  - type: none | auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- radius:
  - description: How much to round the square\'s corners. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-radius) for more details.
  - type: relative | dictionary
  - default: (:)
- inset:
  - description: How much to pad the square\'s content. See the [box\'s documentation](/docs/reference/layout/box/#parameters-inset) for more details.
  - type: relative | dictionary
  - default: 0 % + 5pt
- outset:
  - description: How much to expand the square\'s size without affecting the layout. See the [box\'s documentation](/docs/reference/layout/box/#parameters-outset) for more details.
  - type: relative | dictionary
  - default: (:)
- body:
  - description: The content to place into the square. The square expands to fit this content, keeping the 1-1 aspect ratio. When this is omitted, the square takes on a default size of at most `30pt`.
  - type: none | content
  - default: none


