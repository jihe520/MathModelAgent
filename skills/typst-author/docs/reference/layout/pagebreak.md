# Page Break

# pagebreak

A manual page break.

Must not be used inside any containers.

## Example

```typst
The next page contains
more details on compound theory.
#pagebreak()

== Compound Theory
In 1984, the first ...
```

Even without manual page breaks, content will be automatically paginated based on the configured page size. You can set [the page height](/docs/reference/layout/page/#parameters-height) to `auto` to let the page grow dynamically until a manual page break occurs.

Pagination tries to avoid single lines of text at the top or bottom of a page (these are called _widows_ and _orphans_). You can adjust the [`text.costs`](/docs/reference/text/text/#parameters-costs) parameter to disable this behavior.

```typst
#pagebreak(
  weak: bool,
  to: none | str
) -> content
```

## Parameters

- weak:
  - description: If `true`, the page break is skipped if the current page is already empty.
  - type: bool
  - default: false
- to:
  - description: If given, ensures that the next page will be an even/odd page, with an empty page in between if necessary. ```typst #set page(height: 30pt) First. #pagebreak(to: "odd") Third. ```
  - type: none | str
  - default: none


