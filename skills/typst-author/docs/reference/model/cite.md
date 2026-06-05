# Cite

# cite

Cite a work from the bibliography.

Before you starting citing, you need to add a [bibliography](/docs/reference/model/bibliography/) somewhere in your document.

## Example

```typst
This was already noted by
pirates long ago. @arrgh

Multiple sources say ...
@arrgh @netwok.

You can also call `cite`
explicitly. #cite(<arrgh>)

#bibliography("works.bib")
```

If your source name contains certain characters such as slashes, which are not recognized by the `<>` syntax, you can explicitly call `label` instead.

```typst
Computer Modern is an example of a modernist serif typeface.
#cite(label("DBLP:books/lib/Knuth86a")).
```

## Syntax

This function indirectly has dedicated syntax. [References](/docs/reference/model/ref/) can be used to cite works from the bibliography. The label then corresponds to the citation key.

```typst
#cite(
  key,
  supplement: none | content,
  form: none | str,
  style: auto | str | bytes
) -> content
```

## Parameters

- key:
  - description: The citation key that identifies the entry in the bibliography that shall be cited, as a label. ```typst // All the same @netwok \\ #cite(<netwok>) \\ #cite(label("netwok")) ```
  - type: label
  - default: None
- supplement:
  - description: A supplement for the citation such as page or chapter number. In reference syntax, the supplement can be added in square brackets: ```typst This has been proven. @distress[p.~7] #bibliography("works.bib") ```
  - type: none | content
  - default: none
- form:
  - description: The kind of citation to produce. Different forms are useful in different scenarios: A normal citation is useful as a source at the end of a sentence, while a "prose" citation is more suitable for inclusion in the flow of text. If set to `none`, the cited work is included in the bibliography, but nothing will be displayed. ```typst #cite(<netwok>, form: "prose") show the outsized effects of pirate life on the human psyche. ```
  - type: none | str
  - default: "normal"
- style:
  - description: The citation style. This can be: - `auto` to automatically use the [bibliography\'s style](/docs/reference/model/bibliography/#parameters-style) for citations. - A string with the name of one of the built-in styles (see below). Some of the styles listed below appear twice, once with their full name and once with a short alias. - A path string to a [CSL file](https://citationstyles.org/). For more details about paths, see the [Paths section](/docs/reference/syntax/#paths). - Raw bytes from which a CSL style should be decoded.
  - type: auto | str | bytes
  - default: auto


