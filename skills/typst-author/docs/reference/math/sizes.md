# Sizes

Forced size styles for expressions within formulas.

These functions allow manual configuration of the size of equation elements to make them look as in a display/inline equation or as if used in a root or sub/superscripts.

# math.display

Forced display style in math.

This is the normal size for block equations.

```typst
$sum_i x_i/2 = display(sum_i x_i/2)$
```

```typst
#math.display(
  body,
  cramped: bool
) -> content
```

## Parameters

- body:
  - description: The content to size.
  - type: content
  - default: None
- cramped:
  - description: Whether to impose a height restriction for exponents, like regular sub- and superscripts do.
  - type: bool
  - default: false

# math.inline

Forced inline (text) style in math.

This is the normal size for inline equations.

```typst
$ sum_i x_i/2
    = inline(sum_i x_i/2) $
```

```typst
#math.inline(
  body,
  cramped: bool
) -> content
```

## Parameters

- body:
  - description: The content to size.
  - type: content
  - default: None
- cramped:
  - description: Whether to impose a height restriction for exponents, like regular sub- and superscripts do.
  - type: bool
  - default: false

# math.script

Forced script style in math.

This is the smaller size used in powers or sub- or superscripts.

```typst
$sum_i x_i/2 = script(sum_i x_i/2)$
```

```typst
#math.script(
  body,
  cramped: bool
) -> content
```

## Parameters

- body:
  - description: The content to size.
  - type: content
  - default: None
- cramped:
  - description: Whether to impose a height restriction for exponents, like regular sub- and superscripts do.
  - type: bool
  - default: true

# math.sscript

Forced second script style in math.

This is the smallest size, used in second-level sub- and superscripts (script of the script).

```typst
$sum_i x_i/2 = sscript(sum_i x_i/2)$
```

```typst
#math.sscript(
  body,
  cramped: bool
) -> content
```

## Parameters

- body:
  - description: The content to size.
  - type: content
  - default: None
- cramped:
  - description: Whether to impose a height restriction for exponents, like regular sub- and superscripts do.
  - type: bool
  - default: true


