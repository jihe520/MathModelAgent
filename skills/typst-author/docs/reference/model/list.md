# Bullet List

# list

A bullet list.

Displays a sequence of items vertically, with each item introduced by a marker.

## Example

```typst
Normal list.
- Text
- Math
- Layout
- ...

Multiple lines.
- This list item spans multiple
  lines because it is indented.

Function call.
#list(
  [Foundations],
  [Calculate],
  [Construct],
  [Data Loading],
)
```

## Syntax

This functions also has dedicated syntax: Start a line with a hyphen, followed by a space to create a list item. A list item can contain multiple paragraphs and other block-level content. All content that is indented more than an item's marker becomes part of that item.

```typst
#list(
  tight: bool,
  marker: content | array | function,
  indent: length,
  body-indent: length,
  spacing: auto | length,
  children
) -> content
```

## Parameters

- tight:
  - description: Defines the default [spacing](/docs/reference/model/list/#parameters-spacing) of the list. If it is `false`, the items are spaced apart with [paragraph spacing](/docs/reference/model/par/#parameters-spacing). If it is `true`, they use [paragraph leading](/docs/reference/model/par/#parameters-leading) instead. This makes the list more compact, which can look better if the items are short. In markup mode, the value of this parameter is determined based on whether items are separated with a blank line. If items directly follow each other, this is set to `true`; if items are separated by a blank line, this is set to `false`. The markup-defined tightness cannot be overridden with set rules. ```typst - If a list has a lot of text, and  maybe other inline content, it  should not be tight anymore. - To make a list wide, simply insert  a blank line between the items. ```
  - type: bool
  - default: true
- marker:
  - description: The marker which introduces each item. Instead of plain content, you can also pass an array with multiple markers that should be used for nested lists. If the list nesting depth exceeds the number of markers, the markers are cycled. For total control, you may pass a function that maps the list\'s nesting depth (starting from `0`) to a desired marker. ```typst #set list(marker: [--]) - A more classic list - With en-dashes #set list(marker: ([•], [--])) - Top-level  - Nested  - Items - Items ```
  - type: content | array | function
  - default: ([•], [‣], [–])
- indent:
  - description: The indent of each item.
  - type: length
  - default: 0pt
- body-indent:
  - description: The spacing between the marker and the body of each item.
  - type: length
  - default: 0.5em
- spacing:
  - description: The spacing between the items of the list. If set to `auto`, uses paragraph [`leading`](/docs/reference/model/par/#parameters-leading) for tight lists and paragraph [`spacing`](/docs/reference/model/par/#parameters-spacing) for wide (non-tight) lists.
  - type: auto | length
  - default: auto
- children:
  - description: The bullet list\'s children. When using the list syntax, adjacent items are automatically collected into lists, even through constructs like for loops. ```typst #for letter in "ABC" [  - Letter #letter ] ```
  - type: content
  - default: None


## Definitions
### list.item

A bullet list item.

```typst
#list.item(
  body
) -> content
```

#### Parameters

- body:
  - description: The item\'s body.
  - type: content
  - default: None


