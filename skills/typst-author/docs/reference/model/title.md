# Title

# title

A document title.

This should be used to display the main title of the whole document and should occur only once per document. In contrast, level 1 [headings](/docs/reference/model/heading/) are intended to be used for the top-level sections of the document.

Note that additional frontmatter (like an author list) that should appear together with the title does not belong in its body.

In HTML export, this shows as a `h1` element while level 1 headings show as `h2` elements.

## Example

```typst
#set document(
  title: [Interstellar Mail Delivery]
)

#title()

= Introduction
In recent years, ...
```

```typst
#title(
  body
) -> content
```

## Parameters

- body:
  - description: The content of the title. When omitted (or `auto`), this will default to [`document.title`](/docs/reference/model/document/#parameters-title). In this case, a document title must have been previously set with `set document(title: [..])`. ```typst #set document(title: "Course ABC, Homework 1") #title[Homework 1] ... ```
  - type: auto | content
  - default: auto


