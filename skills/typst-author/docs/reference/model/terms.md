# Term List

# terms

A list of terms and their descriptions.

Displays a sequence of terms and their descriptions vertically. When the descriptions span over multiple lines, they use hanging indent to communicate the visual hierarchy.

## Example

```typst
/ Ligature: A merged glyph.
/ Kerning: A spacing adjustment
  between two adjacent letters.
```

## Syntax

This function also has dedicated syntax: Starting a line with a slash, followed by a term, a colon and a description creates a term list item.

```typst
#terms(
  tight: bool,
  separator: content,
  indent: length,
  hanging-indent: length,
  spacing: auto | length,
  children
) -> content
```

## Parameters

- tight:
  - description: Defines the default [spacing](/docs/reference/model/terms/#parameters-spacing) of the term list. If it is `false`, the items are spaced apart with [paragraph spacing](/docs/reference/model/par/#parameters-spacing). If it is `true`, they use [paragraph leading](/docs/reference/model/par/#parameters-leading) instead. This makes the list more compact, which can look better if the items are short. In markup mode, the value of this parameter is determined based on whether items are separated with a blank line. If items directly follow each other, this is set to `true`; if items are separated by a blank line, this is set to `false`. The markup-defined tightness cannot be overridden with set rules. ```typst / Fact: If a term list has a lot  of text, and maybe other inline  content, it should not be tight  anymore. / Tip: To make it wide, simply  insert a blank line between the  items. ```
  - type: bool
  - default: true
- separator:
  - description: The separator between the item and the description. If you want to just separate them with a certain amount of space, use `h(2cm, weak: true)` as the separator and replace `2cm` with your desired amount of space. ```typst #set terms(separator: [: ]) / Colon: A nice separator symbol. ```
  - type: content
  - default: h (amount : 0.6em, weak : true)
- indent:
  - description: The indentation of each item.
  - type: length
  - default: 0pt
- hanging-indent:
  - description: The hanging indent of the description. This is in addition to the whole item\'s `indent`. ```typst #set terms(hanging-indent: 0pt) / Term: This term list does not  make use of hanging indents. ```
  - type: length
  - default: 2em
- spacing:
  - description: The spacing between the items of the term list. If set to `auto`, uses paragraph [`leading`](/docs/reference/model/par/#parameters-leading) for tight term lists and paragraph [`spacing`](/docs/reference/model/par/#parameters-spacing) for wide (non-tight) term lists.
  - type: auto | length
  - default: auto
- children:
  - description: The term list\'s children. When using the term list syntax, adjacent items are automatically collected into term lists, even through constructs like for loops. ```typst #for (year, product) in (  "1978": "TeX",  "1984": "LaTeX",  "2019": "Typst", ) [/ #product: Born in #year.] ```
  - type: content | array
  - default: None


## Definitions
### terms.item

A term list item.

```typst
#terms.item(
  term,
  description
) -> content
```

#### Parameters

- term:
  - description: The term described by the list item.
  - type: content
  - default: None
- description:
  - description: The description of the term.
  - type: content
  - default: None


