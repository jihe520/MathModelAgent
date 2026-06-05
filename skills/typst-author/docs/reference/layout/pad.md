# Padding

# pad

Adds spacing around content.

The spacing can be specified for each side individually, or for all sides at once by specifying a positional argument.

## Example

```typst
#set align(center)

#pad(x: 16pt, image("typing.jpg"))
_Typing speeds can be
 measured in words per minute._
```

```typst
#pad(
  left: relative,
  top: relative,
  right: relative,
  bottom: relative,
  x: relative,
  y: relative,
  rest: relative,
  body
) -> content
```

## Parameters

- left:
  - description: The padding at the left side.
  - type: relative
  - default: 0 % + 0pt
- top:
  - description: The padding at the top side.
  - type: relative
  - default: 0 % + 0pt
- right:
  - description: The padding at the right side.
  - type: relative
  - default: 0 % + 0pt
- bottom:
  - description: The padding at the bottom side.
  - type: relative
  - default: 0 % + 0pt
- x:
  - description: A shorthand to set `left` and `right` to the same value.
  - type: relative
  - default: 0 % + 0pt
- y:
  - description: A shorthand to set `top` and `bottom` to the same value.
  - type: relative
  - default: 0 % + 0pt
- rest:
  - description: A shorthand to set all four sides to the same value.
  - type: relative
  - default: 0 % + 0pt
- body:
  - description: The content to pad at the sides.
  - type: content
  - default: None


