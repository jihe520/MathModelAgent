# Frame

# html.frame

An element that lays out its content as an inline SVG.

Sometimes, converting Typst content to HTML is not desirable. This can be the case for plots and other content that relies on positioning and styling to convey its message.

This function allows you to use the Typst layout engine that would also be used for PDF, SVG, and PNG export to render a part of your document exactly how it would appear when exported in one of these formats. It embeds the content as an inline SVG.

```typst
#html.frame(
  body
) -> content
```

## Parameters

- body:
  - description: The content that shall be laid out.
  - type: content
  - default: None


