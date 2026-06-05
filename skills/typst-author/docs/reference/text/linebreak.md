# Line Break

# linebreak

Inserts a line break.

Advances the paragraph to the next line. A single trailing line break at the end of a paragraph is ignored, but more than one creates additional empty lines.

## Example

```typst
*Date:* 26.12.2022 \
*Topic:* Infrastructure Test \
*Severity:* High \
```

## Syntax

This function also has dedicated syntax: To insert a line break, simply write a backslash followed by whitespace. This always creates an unjustified break.

```typst
#linebreak(
  justify: bool
) -> content
```

## Parameters

- justify:
  - description: Whether to justify the line before the break. This is useful if you found a better line break opportunity in your justified text than Typst did. ```typst #set par(justify: true) #let jb = linebreak(justify: true) I have manually tuned the #jb line breaks in this paragraph #jb for an _interesting_ result. #jb ```
  - type: bool
  - default: false


