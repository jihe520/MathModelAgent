# Bibliography

# bibliography

A bibliography / reference listing.

You can create a new bibliography by calling this function with a path to a bibliography file in either one of two formats:

- A Hayagriva `.yaml`/`.yml` file. Hayagriva is a new bibliography file format designed for use with Typst. Visit its [documentation](https://github.com/typst/hayagriva/blob/main/docs/file-format.md) for more details.
- A BibLaTeX `.bib` file.

As soon as you add a bibliography somewhere in your document, you can start citing things with reference syntax (`@key`) or explicit calls to the [citation](/docs/reference/model/cite/) function (`#cite(<key>)`). The bibliography will only show entries for works that were referenced in the document.

## Styles

Typst offers a wide selection of built-in [citation and bibliography styles](/docs/reference/model/bibliography/#parameters-style). Beyond those, you can add and use custom [CSL](https://citationstyles.org/) (Citation Style Language) files. Wondering which style to use? Here are some good defaults based on what discipline you're working in:

| Fields | Typical Styles |
| --- | --- |
| Engineering, IT | `"ieee"` |
| Psychology, Life Sciences | `"apa"` |
| Social sciences | `"chicago-author-date"` |
| Humanities | `"mla"`, `"chicago-notes"`, `"harvard-cite-them-right"` |
| Economics | `"harvard-cite-them-right"` |
| Physics | `"american-physics-society"` |

## Example

```typst
This was already noted by
pirates long ago. @arrgh

Multiple sources say ...
@arrgh @netwok.

#bibliography("works.bib")
```

```typst
#bibliography(
  sources,
  title: none | auto | content,
  full: bool,
  style: str | bytes
) -> content
```

## Parameters

- sources:
  - description: One or multiple paths to or raw bytes for Hayagriva `.yaml` and/or BibLaTeX `.bib` files. This can be a: - A path string to load a bibliography file from the given path. For more details about paths, see the [Paths section](/docs/reference/syntax/#paths). - Raw bytes from which the bibliography should be decoded. - An array where each item is one of the above.
  - type: str | bytes | array
  - default: None
- title:
  - description: The title of the bibliography. - When set to `auto`, an appropriate title for the [text language](/docs/reference/text/text/#parameters-lang) will be used. This is the default. - When set to `none`, the bibliography will not have a title. - A custom title can be set by passing content. The bibliography\'s heading will not be numbered by default, but you can force it to be with a show-set rule: `show bibliography: set heading(numbering: "1.")`
  - type: none | auto | content
  - default: auto
- full:
  - description: Whether to include all works from the given bibliography files, even those that weren\'t cited in the document. To selectively add individual cited works without showing them, you can also use the `cite` function with [`form`](/docs/reference/model/cite/#parameters-form) set to `none`.
  - type: bool
  - default: false
- style:
  - description: The bibliography style. This can be: - A string with the name of one of the built-in styles (see below). Some of the styles listed below appear twice, once with their full name and once with a short alias. - A path string to a [CSL file](https://citationstyles.org/). For more details about paths, see the [Paths section](/docs/reference/syntax/#paths). - Raw bytes from which a CSL style should be decoded.
  - type: str | bytes
  - default: "ieee"


