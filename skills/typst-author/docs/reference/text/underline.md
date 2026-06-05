# Underline

# underline

Underlines text.

## Example

```typst
This is #underline[important].
```

```typst
#underline(
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
  - description: How to [stroke](/docs/reference/visualize/stroke/) the line. If set to `auto`, takes on the text\'s color and a thickness defined in the current font. ```typst Take #underline(  stroke: 1.5pt + red,  offset: 2pt,  [care], ) ```
  - type: auto | length | color | gradient | stroke | tiling | dictionary
  - default: auto
- offset:
  - description: The position of the line relative to the baseline, read from the font tables if `auto`. ```typst #underline(offset: 5pt)[  The Tale Of A Faraway Line I ] ```
  - type: auto | length
  - default: auto
- extent:
  - description: The amount by which to extend the line beyond (or within if negative) the content. ```typst #align(center,  underline(extent: 2pt)[Chapter 1] ) ```
  - type: length
  - default: 0pt
- evade:
  - description: Whether the line skips sections in which it would collide with the glyphs. ```typst This #underline(evade: true)[is great]. This #underline(evade: false)[is less great]. ```
  - type: bool
  - default: true
- background:
  - description: Whether the line is placed behind the content it underlines. ```typst #set underline(stroke: (thickness: 1em, paint: maroon, cap: "round")) #underline(background: true)[This is stylized.] \\ #underline(background: false)[This is partially hidden.] ```
  - type: bool
  - default: false
- body:
  - description: The content to underline.
  - type: content
  - default: None


