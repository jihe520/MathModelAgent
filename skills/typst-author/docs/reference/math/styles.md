# Styles

Alternate letterforms within formulas.

These functions are distinct from the [`text`](/docs/reference/text/text/) function because math fonts contain multiple variants of each letter.

# math.upright

Upright (non-italic) font style in math.

```typst
$ upright(A) != A $
```

```typst
#math.upright(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.italic

Italic font style in math.

For roman letters and greek lowercase letters, this is already the default.

```typst
#math.italic(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.bold

Bold font style in math.

```typst
$ bold(A) := B^+ $
```

```typst
#math.bold(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None


