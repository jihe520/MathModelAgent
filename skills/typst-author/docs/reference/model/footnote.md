# Footnote

# footnote

A footnote.

Includes additional remarks and references on the same page with footnotes. A footnote will insert a superscript number that links to the note at the bottom of the page. Notes are numbered sequentially throughout your document and can break across multiple pages.

To customize the appearance of the entry in the footnote listing, see [`footnote.entry`](/docs/reference/model/footnote/#definitions-entry). The footnote itself is realized as a normal superscript, so you can use a set rule on the [`super`](/docs/reference/text/super/) function to customize it. You can also apply a show rule to customize only the footnote marker (superscript number) in the running text.

## Example

```typst
Check the docs for more details.
#footnote[https://typst.app/docs]
```

The footnote automatically attaches itself to the preceding word, even if there is a space before it in the markup. To force space, you can use the string `#" "` or explicit [horizontal spacing](/docs/reference/layout/h/).

By giving a label to a footnote, you can have multiple references to it.

```typst
You can edit Typst documents online.
#footnote[https://typst.app/app] <fn>
Checkout Typst's website. @fn
And the online app. #footnote(<fn>)
```

_Note:_ Set and show rules in the scope where `footnote` is called may not apply to the footnote's content. See [here](https://github.com/typst/typst/issues/1467#issuecomment-1588799440) for more information.

## Accessibility

Footnotes will be read by Assistive Technology (AT) immediately after the spot in the text where they are referenced, just like how they appear in markup.

```typst
#footnote(
  numbering: str | function,
  body
) -> content
```

## Parameters

- numbering:
  - description: How to number footnotes. Accepts a [numbering pattern or function](/docs/reference/model/numbering/) taking a single number. By default, the footnote numbering continues throughout your document. If you prefer per-page footnote numbering, you can reset the footnote [counter](/docs/reference/introspection/counter/) in the page [header](/docs/reference/layout/page/#parameters-header). In the future, there might be a simpler way to achieve this. ```typst #set footnote(numbering: "*") Footnotes: #footnote[Star], #footnote[Dagger] ```
  - type: str | function
  - default: "1"
- body:
  - description: The content to put into the footnote. Can also be the label of another footnote this one should point to.
  - type: label | content
  - default: None


## Definitions
### footnote.entry

An entry in a footnote list.

This function is not intended to be called directly. Instead, it is used in set and show rules to customize footnote listings.

```typst
#show footnote.entry: set text(red)

My footnote listing
#footnote[It's down here]
has red text!
```

_Note:_ Footnote entry properties must be uniform across each page run (a page run is a sequence of pages without an explicit pagebreak in between). For this reason, set and show rules for footnote entries should be defined before any page content, typically at the very start of the document.

```typst
#footnote.entry(
  note,
  separator: content,
  clearance: length,
  gap: length,
  indent: length
) -> content
```

#### Parameters

- note:
  - description: The footnote for this entry. Its location can be used to determine the footnote counter state. ```typst #show footnote.entry: it => {  let loc = it.note.location()  numbering(   "1: ",   ..counter(footnote).at(loc),  )  it.note.body } Customized #footnote[Hello] listing #footnote[World! 🌏] ```
  - type: content
  - default: None
- separator:
  - description: The separator between the document body and the footnote listing. ```typst #set footnote.entry(  separator: repeat[.] ) Testing a different separator. #footnote[  Unconventional, but maybe  not that bad? ] ```
  - type: content
  - default: line (length : 30 % + 0pt, stroke : 0.5pt)
- clearance:
  - description: The amount of clearance between the document body and the separator. ```typst #set footnote.entry(clearance: 3em) Footnotes also need ... #footnote[  ... some space to breathe. ] ```
  - type: length
  - default: 1em
- gap:
  - description: The gap between footnote entries. ```typst #set footnote.entry(gap: 0.8em) Footnotes: #footnote[Spaced], #footnote[Apart] ```
  - type: length
  - default: 0.5em
- indent:
  - description: The indent of each footnote entry. ```typst #set footnote.entry(indent: 0em) Footnotes: #footnote[No], #footnote[Indent] ```
  - type: length
  - default: 1em


