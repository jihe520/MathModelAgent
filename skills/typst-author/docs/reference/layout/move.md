# Move

# move

Moves content without affecting layout.

The `move` function allows you to move content while the layout still 'sees' it at the original positions. Containers will still be sized as if the content was not moved.

## Example

```typst
#rect(inset: 0pt, fill: gray, move(
  dx: 4pt, dy: 6pt,
  rect(
    inset: 8pt,
    fill: white,
    stroke: black,
    [Abra cadabra]
  )
))
```

## Accessibility

Moving is transparent to Assistive Technology (AT). Your content will be read in the order it appears in the source, regardless of any visual movement. If you need to hide content from AT altogether in PDF export, consider using [`pdf.artifact`](/docs/reference/pdf/artifact/).

```typst
#move(
  dx: relative,
  dy: relative,
  body
) -> content
```

## Parameters

- dx:
  - description: The horizontal displacement of the content.
  - type: relative
  - default: 0 % + 0pt
- dy:
  - description: The vertical displacement of the content.
  - type: relative
  - default: 0 % + 0pt
- body:
  - description: The content to move.
  - type: content
  - default: None


