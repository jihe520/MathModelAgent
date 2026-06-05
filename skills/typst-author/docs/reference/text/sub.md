# Subscript

# sub

Renders text in subscript.

The text is rendered smaller and its baseline is lowered.

## Example

```typst
Revenue#sub[yearly]
```

```typst
#sub(
  typographic: bool,
  baseline: auto | length,
  size: auto | length,
  body
) -> content
```

## Parameters

- typographic:
  - description: Whether to use subscript glyphs from the font if available. Ideally, subscripts glyphs are provided by the font (using the `subs` OpenType feature). Otherwise, Typst is able to synthesize subscripts by lowering and scaling down regular glyphs. When this is set to `false`, synthesized glyphs will be used regardless of whether the font provides dedicated subscript glyphs. When `true`, synthesized glyphs may still be used in case the font does not provide the necessary subscript glyphs. ```typst N#sub(typographic: true)[1] N#sub(typographic: false)[1] ```
  - type: bool
  - default: true
- baseline:
  - description: The downward baseline shift for synthesized subscripts. This only applies to synthesized subscripts. In other words, this has no effect if `typographic` is `true` and the font provides the necessary subscript glyphs. If set to `auto`, the baseline is shifted according to the metrics provided by the font, with a fallback to `0.2em` in case the font does not define the necessary metrics.
  - type: auto | length
  - default: auto
- size:
  - description: The font size for synthesized subscripts. This only applies to synthesized subscripts. In other words, this has no effect if `typographic` is `true` and the font provides the necessary subscript glyphs. If set to `auto`, the size is scaled according to the metrics provided by the font, with a fallback to `0.6em` in case the font does not define the necessary metrics.
  - type: auto | length
  - default: auto
- body:
  - description: The text to display in subscript.
  - type: content
  - default: None


