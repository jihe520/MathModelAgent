# Attach

Subscript, superscripts, and limits.

Attachments can be displayed either as sub/superscripts, or limits. Typst automatically decides which is more suitable depending on the base, but you can also control this manually with the `scripts` and `limits` functions.

If you want the base to stretch to fit long top and bottom attachments (for example, an arrow with text above it), use the [`stretch`](/docs/reference/math/stretch/) function.

## Example

```typst
$ sum_(i=0)^n a_i = 2^(1+i) $
```

## Syntax

This function also has dedicated syntax for attachments after the base: Use the underscore (`_`) to indicate a subscript i.e. bottom attachment and the hat (`^`) to indicate a superscript i.e. top attachment.

# math.attach

A base with optional attachments.

```typst
$ attach(
  Pi, t: alpha, b: beta,
  tl: 1, tr: 2+3, bl: 4+5, br: 6,
) $
```

```typst
#math.attach(
  base,
  t: none | content,
  b: none | content,
  tl: none | content,
  bl: none | content,
  tr: none | content,
  br: none | content
) -> content
```

## Parameters

- base:
  - description: The base to which things are attached.
  - type: content
  - default: None
- t:
  - description: The top attachment, smartly positioned at top-right or above the base. You can wrap the base in `limits()` or `scripts()` to override the smart positioning.
  - type: none | content
  - default: none
- b:
  - description: The bottom attachment, smartly positioned at the bottom-right or below the base. You can wrap the base in `limits()` or `scripts()` to override the smart positioning.
  - type: none | content
  - default: none
- tl:
  - description: The top-left attachment (before the base).
  - type: none | content
  - default: none
- bl:
  - description: The bottom-left attachment (before base).
  - type: none | content
  - default: none
- tr:
  - description: The top-right attachment (after the base).
  - type: none | content
  - default: none
- br:
  - description: The bottom-right attachment (after the base).
  - type: none | content
  - default: none

# math.scripts

Forces a base to display attachments as scripts.

```typst
$ scripts(sum)_1^2 != sum_1^2 $
```

```typst
#math.scripts(
  body
) -> content
```

## Parameters

- body:
  - description: The base to attach the scripts to.
  - type: content
  - default: None

# math.limits

Forces a base to display attachments as limits.

```typst
$ limits(A)_1^2 != A_1^2 $
```

```typst
#math.limits(
  body,
  inline: bool
) -> content
```

## Parameters

- body:
  - description: The base to attach the limits to.
  - type: content
  - default: None
- inline:
  - description: Whether to also force limits in inline equations. When applying limits globally (e.g., through a show rule), it is typically a good idea to disable this.
  - type: bool
  - default: true


