# Skew

# skew

Skews content.

Skews an element in horizontal and/or vertical direction. The layout will act as if the element was not skewed unless you specify `reflow: true`.

## Example

```typst
#skew(ax: -12deg)[
  This is some fake italic text.
]
```

```typst
#skew(
  ax: angle,
  ay: angle,
  origin: alignment,
  reflow: bool,
  body
) -> content
```

## Parameters

- ax:
  - description: The horizontal skewing angle. ```typst #skew(ax: 30deg)[Skewed] ```
  - type: angle
  - default: 0deg
- ay:
  - description: The vertical skewing angle. ```typst #skew(ay: 30deg)[Skewed] ```
  - type: angle
  - default: 0deg
- origin:
  - description: The origin of the skew transformation. The origin will stay fixed during the operation. ```typst X #box(skew(ax: -30deg, origin: center + horizon)[X]) X \\ X #box(skew(ax: -30deg, origin: bottom + left)[X]) X \\ X #box(skew(ax: -30deg, origin: top + right)[X]) X ```
  - type: alignment
  - default: center + horizon
- reflow:
  - description: Whether the skew transformation impacts the layout. If set to `false`, the skewed content will retain the bounding box of the original content. If set to `true`, the bounding box will take the transformation of the content into account and adjust the layout accordingly. ```typst Hello #skew(ay: 30deg, reflow: true, "World")! ```
  - type: bool
  - default: false
- body:
  - description: The content to skew.
  - type: content
  - default: None


