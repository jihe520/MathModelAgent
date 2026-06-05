# Emphasis

# emph

Emphasizes content by toggling italics.

- If the current [text style](/docs/reference/text/text/#parameters-style) is `"normal"`, this turns it into `"italic"`.
- If it is already `"italic"` or `"oblique"`, it turns it back to `"normal"`.

## Example

```typst
This is _emphasized._ \
This is #emph[too.]

#show emph: it => {
  text(blue, it.body)
}

This is _emphasized_ differently.
```

## Syntax

This function also has dedicated syntax: To emphasize content, simply enclose it in underscores (`_`). Note that this only works at word boundaries. To emphasize part of a word, you have to use the function.

```typst
#emph(
  body
) -> content
```

## Parameters

- body:
  - description: The content to emphasize.
  - type: content
  - default: None


