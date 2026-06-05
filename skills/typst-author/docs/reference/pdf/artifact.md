# Artifact

# pdf.artifact

Marks content as a PDF artifact.

Artifacts are parts of the document that are not meant to be read by Assistive Technology (AT), such as screen readers. Typical examples include purely decorative images that do not contribute to the meaning of the document, watermarks, or repeated content such as page numbers.

Typst will automatically mark certain content, such as page headers, footers, backgrounds, and foregrounds, as artifacts. Likewise, paths and shapes are automatically marked as artifacts, but their content is not. Repetitions of table headers and footers are also marked as artifacts.

Once something is marked as an artifact, you cannot make any of its contents accessible again. If you need to mark only part of something as an artifact, you may need to use this function multiple times.

If you are unsure what constitutes an artifact, check the [Accessibility Guide](/docs/guides/accessibility/#artifacts).

In the future, this function may be moved out of the `pdf` module, making it possible to hide content in HTML export from AT.

```typst
#pdf.artifact(
  kind: str,
  body
) -> content
```

## Parameters

- kind:
  - description: The artifact kind. This will govern how the PDF reader treats the artifact during reflow and content extraction (e.g. copy and paste).
  - type: str
  - default: "other"
- body:
  - description: The content that is an artifact.
  - type: content
  - default: None


