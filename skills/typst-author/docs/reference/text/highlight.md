# Highlight

# highlight

Highlights text with a background color.

## Example

```typst
This is #highlight[important].
```

```typst
#highlight(
  fill: none | color | gradient | tiling,
  stroke: none | length | color | gradient | stroke | tiling | dictionary,
  top-edge: length | str,
  bottom-edge: length | str,
  extent: length,
  radius: relative | dictionary,
  body
) -> content
```

## Parameters

- fill:
  - description: The color to highlight the text with. ```typst This is #highlight(  fill: blue )[highlighted with blue]. ```
  - type: none | color | gradient | tiling
  - default: rgb ("#fffd11a1")
- stroke:
  - description: The highlight\'s border color. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-stroke) for more details. ```typst This is a #highlight(  stroke: fuchsia )[stroked highlighting]. ```
  - type: none | length | color | gradient | stroke | tiling | dictionary
  - default: (:)
- top-edge:
  - description: The top end of the background rectangle. ```typst #set highlight(top-edge: "ascender") #highlight[a] #highlight[aib] #set highlight(top-edge: "x-height") #highlight[a] #highlight[aib] ```
  - type: length | str
  - default: "ascender"
- bottom-edge:
  - description: The bottom end of the background rectangle. ```typst #set highlight(bottom-edge: "descender") #highlight[a] #highlight[ap] #set highlight(bottom-edge: "baseline") #highlight[a] #highlight[ap] ```
  - type: length | str
  - default: "descender"
- extent:
  - description: The amount by which to extend the background to the sides beyond (or within if negative) the content. ```typst A long #highlight(extent: 4pt)[background]. ```
  - type: length
  - default: 0pt
- radius:
  - description: How much to round the highlight\'s corners. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-radius) for more details. ```typst Listen #highlight(  radius: 5pt, extent: 2pt )[carefully], it will be on the test. ```
  - type: relative | dictionary
  - default: (:)
- body:
  - description: The content that should be highlighted.
  - type: content
  - default: None


