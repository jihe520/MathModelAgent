# Rectangle

# rect

A rectangle with optional content.

## Example

```typst
// Without content.
#rect(width: 35%, height: 30pt)

// With content.
#rect[
  Automatically sized \
  to fit the content.
]
```

```typst
#rect(
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

- width:
  - description: The rectangle\'s width, relative to its parent container.
  - type: auto | relative
  - default: auto
- height:
  - description: The rectangle\'s height, relative to its parent container.
  - type: auto | relative | fraction
  - default: auto
- fill:
  - description: How to fill the rectangle. When setting a fill, the default stroke disappears. To create a rectangle with both fill and stroke, you have to configure both. ```typst #rect(fill: blue) ```
  - type: none | color | gradient | tiling
  - default: none
- stroke:
  - description: How to stroke the rectangle. This can be: - `none` to disable stroking - `auto` for a stroke of `1pt + black` if and only if no fill is given. - Any kind of [stroke](/docs/reference/visualize/stroke/) - A dictionary describing the stroke for each side individually. The dictionary can contain the following keys in order of precedence:  - `top`: The top stroke.  - `right`: The right stroke.  - `bottom`: The bottom stroke.  - `left`: The left stroke.  - `x`: The horizontal stroke.  - `y`: The vertical stroke.  - `rest`: The stroke on all sides except those for which the dictionary explicitly sets a size. All keys are optional; omitted keys will use their previously set value, or the default stroke if never set. ```typst #stack(  dir: ltr,  spacing: 1fr,  rect(stroke: red),  rect(stroke: 2pt),  rect(stroke: 2pt + red), ) ```
  - type: none | auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- radius:
  - description: How much to round the rectangle\'s corners, relative to the minimum of the width and height divided by two. This can be: - A relative length for a uniform corner radius. - A dictionary: With a dictionary, the stroke for each side can be set individually. The dictionary can contain the following keys in order of precedence:  - `top-left`: The top-left corner radius.  - `top-right`: The top-right corner radius.  - `bottom-right`: The bottom-right corner radius.  - `bottom-left`: The bottom-left corner radius.  - `left`: The top-left and bottom-left corner radii.  - `top`: The top-left and top-right corner radii.  - `right`: The top-right and bottom-right corner radii.  - `bottom`: The bottom-left and bottom-right corner radii.  - `rest`: The radii for all corners except those for which the dictionary explicitly sets a size. ```typst #set rect(stroke: 4pt) #rect(  radius: (   left: 5pt,   top-right: 20pt,   bottom-right: 10pt,  ),  stroke: (   left: red,   top: yellow,   right: green,   bottom: blue,  ), ) ```
  - type: relative | dictionary
  - default: (:)
- inset:
  - description: How much to pad the rectangle\'s content. See the [box\'s documentation](/docs/reference/layout/box/#parameters-inset) for more details.
  - type: relative | dictionary
  - default: 0 % + 5pt
- outset:
  - description: How much to expand the rectangle\'s size without affecting the layout. See the [box\'s documentation](/docs/reference/layout/box/#parameters-outset) for more details.
  - type: relative | dictionary
  - default: (:)
- body:
  - description: The content to place into the rectangle. When this is omitted, the rectangle takes on a default size of at most `45pt` by `30pt`.
  - type: none | content
  - default: none


