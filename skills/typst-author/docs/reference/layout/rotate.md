# Rotate

# rotate

Rotates content without affecting layout.

Rotates an element by a given angle. The layout will act as if the element was not rotated unless you specify `reflow: true`.

## Example

```typst
#stack(
  dir: ltr,
  spacing: 1fr,
  ..range(16)
    .map(i => rotate(24deg * i)[X]),
)
```

```typst
#rotate(
  angle,
  origin: alignment,
  reflow: bool,
  body
) -> content
```

## Parameters

- angle:
  - description: The amount of rotation. ```typst #rotate(-1.571rad)[Space!] ```
  - type: angle
  - default: 0deg
- origin:
  - description: The origin of the rotation. If, for instance, you wanted the bottom left corner of the rotated element to stay aligned with the baseline, you would set it to `bottom + left` instead. ```typst #set text(spacing: 8pt) #let square = square.with(width: 8pt) #box(square()) #box(rotate(30deg, origin: center, square())) #box(rotate(30deg, origin: top + left, square())) #box(rotate(30deg, origin: bottom + right, square())) ```
  - type: alignment
  - default: center + horizon
- reflow:
  - description: Whether the rotation impacts the layout. If set to `false`, the rotated content will retain the bounding box of the original content. If set to `true`, the bounding box will take the rotation of the content into account and adjust the layout accordingly. ```typst Hello #rotate(90deg, reflow: true)[World]! ```
  - type: bool
  - default: false
- body:
  - description: The content to rotate.
  - type: content
  - default: None


