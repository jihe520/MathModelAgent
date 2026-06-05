# Strikethrough

# strike

Strikes through text.

## Example

```typst
This is #strike[not] relevant.
```

```typst
#strike(
  stroke: auto | length | color | gradient | stroke | tiling | dictionary,
  offset: auto | length,
  extent: length,
  background: bool,
  body
) -> content
```

## Parameters

- stroke:
  - description: How to [stroke](/docs/reference/visualize/stroke/) the line. If set to `auto`, takes on the text\'s color and a thickness defined in the current font. _Note:_ Please don\'t use this for real redaction as you can still copy paste the text. ```typst This is #strike(stroke: 1.5pt + red)[very stricken through]. \\ This is #strike(stroke: 10pt)[redacted]. ```
  - type: auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- offset:
  - description: The position of the line relative to the baseline. Read from the font tables if `auto`. This is useful if you are unhappy with the offset your font provides. ```typst #set text(font: "Inria Serif") This is #strike(offset: auto)[low-ish]. \\ This is #strike(offset: -3.5pt)[on-top]. ```
  - type: auto | length
  - default: auto
- extent:
  - description: The amount by which to extend the line beyond (or within if negative) the content. ```typst This #strike(extent: -2pt)[skips] parts of the word. This #strike(extent: 2pt)[extends] beyond the word. ```
  - type: length
  - default: 0pt
- background:
  - description: Whether the line is placed behind the content. ```typst #set strike(stroke: red) #strike(background: true)[This is behind.] \\ #strike(background: false)[This is in front.] ```
  - type: bool
  - default: false
- body:
  - description: The content to strike through.
  - type: content
  - default: None


