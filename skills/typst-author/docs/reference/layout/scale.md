# Scale

# scale

Scales content without affecting layout.

Lets you mirror content by specifying a negative scale on a single axis.

## Example

```typst
#set align(center)
#scale(x: -100%)[This is mirrored.]
#scale(x: -100%, reflow: true)[This is mirrored.]
```

```typst
#scale(
  factor: auto | length | ratio,
  x: auto | length | ratio,
  y: auto | length | ratio,
  origin: alignment,
  reflow: bool,
  body
) -> content
```

## Parameters

- factor:
  - description: The scaling factor for both axes, as a positional argument. This is just an optional shorthand notation for setting `x` and `y` to the same value.
  - type: auto | length | ratio
  - default: 100 %
- x:
  - description: The horizontal scaling factor. The body will be mirrored horizontally if the parameter is negative.
  - type: auto | length | ratio
  - default: 100 %
- y:
  - description: The vertical scaling factor. The body will be mirrored vertically if the parameter is negative.
  - type: auto | length | ratio
  - default: 100 %
- origin:
  - description: The origin of the transformation. ```typst A#box(scale(75%)[A])A \\ B#box(scale(75%, origin: bottom + left)[B])B ```
  - type: alignment
  - default: center + horizon
- reflow:
  - description: Whether the scaling impacts the layout. If set to `false`, the scaled content will be allowed to overlap other content. If set to `true`, it will compute the new size of the scaled content and adjust the layout accordingly. ```typst Hello #scale(x: 20%, y: 40%, reflow: true)[World]! ```
  - type: bool
  - default: false
- body:
  - description: The content to scale.
  - type: content
  - default: None


