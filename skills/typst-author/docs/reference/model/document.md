# Document

# document

The root element of a document and its metadata.

All documents are automatically wrapped in a `document` element. You cannot create a document element yourself. This function is only used with [set rules](/docs/reference/styling/#set-rules) to specify document metadata. Such a set rule must not occur inside of any layout container.

```typst
#set document(title: [Hello])

This has no visible output, but
embeds metadata into the PDF!
```

Note that metadata set with this function is not rendered within the document. Instead, it is embedded in the compiled PDF file.

```typst
#document(
  title: none | content,
  author: str | array,
  description: none | content,
  keywords: str | array,
  date: none | auto | datetime
) -> content
```

## Parameters

- title:
  - description: The document\'s title. This is rendered as the title of the PDF viewer window or the browser tab of the page. Adding a title is important for accessibility, as it makes it easier to navigate to your document and identify it among other open documents. When exporting to PDF/UA, a title is required. While this can be arbitrary content, PDF viewers only support plain text titles, so the conversion might be lossy.
  - type: none | content
  - default: none
- author:
  - description: The document\'s authors.
  - type: str | array
  - default: ()
- description:
  - description: The document\'s description.
  - type: none | content
  - default: none
- keywords:
  - description: The document\'s keywords.
  - type: str | array
  - default: ()
- date:
  - description: The document\'s creation date. If this is `auto` (default), Typst uses the current date and time. Setting it to `none` prevents Typst from embedding any creation date into the PDF metadata. The year component must be at least zero in order to be embedded into a PDF. If you want to create byte-by-byte reproducible PDFs, set this to something other than `auto`.
  - type: none | auto | datetime
  - default: auto


