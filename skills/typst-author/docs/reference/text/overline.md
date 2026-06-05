# Overline

# overline

Adds a line over text.

## Example

```typst
#overline[A line over text.]
```

```typst
#overline(
  stroke: auto | length | color | gradient | stroke | tiling | dictionary,
  offset: auto | length,
  extent: length,
  evade: bool,
  background: bool,
  body
) -> content
```

## Parameters

- stroke:
  - description: How to [stroke](/docs/reference/visualize/stroke/) the line. If set to `auto`, takes on the text\'s color and a thickness defined in the current font. ```typst #set text(fill: olive) #overline(  stroke: green.darken(20%),  offset: -12pt,  [The Forest Theme], ) ```
  - type: auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- offset:
  - description: The position of the line relative to the baseline. Read from the font tables if `auto`. ```typst #overline(offset: -1.2em)[  The Tale Of A Faraway Line II ] ```
  - type: auto | length
  - default: auto
- extent:
  - description: The amount by which to extend the line beyond (or within if negative) the content. ```typst #set overline(extent: 4pt) #set underline(extent: 4pt) #overline(underline[Typography Today]) ```
  - type: length
  - default: 0pt
- evade:
  - description: Whether the line skips sections in which it would collide with the glyphs. ```typst #overline(  evade: false,  offset: -7.5pt,  stroke: 1pt,  extent: 3pt,  [Temple], ) ```
  - type: bool
  - default: true
- background:
  - description: Whether the line is placed behind the content it overlines. ```typst #set overline(stroke: (thickness: 1em, paint: maroon, cap: "round")) #overline(background: true)[This is stylized.] \\ #overline(background: false)[This is partially hidden.] ```
  - type: bool
  - default: false
- body:
  - description: The content to add a line over.
  - type: content
  - default: None


