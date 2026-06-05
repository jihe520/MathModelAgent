# Repeat

# repeat

Repeats content to the available space.

This can be useful when implementing a custom index, reference, or outline.

Space may be inserted between the instances of the body parameter, so be sure to adjust the [`justify`](/docs/reference/layout/repeat/#parameters-justify) parameter accordingly.

Errors if there are no bounds on the available space, as it would create infinite content.

## Example

```typst
Sign on the dotted line:
#box(width: 1fr, repeat[.])

#set text(10pt)
#v(8pt, weak: true)
#align(right)[
  Berlin, the 22nd of December, 2022
]
```

## Accessibility

Repeated content is automatically marked as an [artifact](/docs/reference/pdf/artifact/) and hidden from Assistive Technology (AT). Do not use this function to create content that contributes to the meaning of your document.

```typst
#repeat(
  body,
  gap: length,
  justify: bool
) -> content
```

## Parameters

- body:
  - description: The content to repeat.
  - type: content
  - default: None
- gap:
  - description: The gap between each instance of the body.
  - type: length
  - default: 0pt
- justify:
  - description: Whether to increase the gap between instances to completely fill the available space.
  - type: bool
  - default: true


