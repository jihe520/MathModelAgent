# Left/Right

Delimiter matching.

The `lr` function allows you to match two delimiters and scale them with the content they contain. While this also happens automatically for delimiters that match syntactically, `lr` allows you to match two arbitrary delimiters and control their size exactly. Apart from the `lr` function, Typst provides a few more functions that create delimiter pairings for absolute, ceiled, and floored values as well as norms.

To prevent a delimiter from being matched by Typst, and thus auto-scaled, escape it with a backslash. To instead disable auto-scaling completely, use `set math.lr(size: 1em)`.

## Example

```typst
$ [a, b/2] $
$ lr(]sum_(x=1)^n], size: #50%) x $
$ abs((x + y) / 2) $
$ \{ (x / y) \} $
#set math.lr(size: 1em)
$ { (a / b), a, b in (0; 1/2] } $
```

# math.lr

Scales delimiters.

While matched delimiters scale by default, this can be used to scale unmatched delimiters and to control the delimiter scaling more precisely.

```typst
#math.lr(
  size: relative,
  body
) -> content
```

## Parameters

- size:
  - description: The size of the brackets, relative to the height of the wrapped content.
  - type: relative
  - default: 100 % + 0pt
- body:
  - description: The delimited content, including the delimiters.
  - type: content
  - default: None

# math.mid

Scales delimiters vertically to the nearest surrounding `lr()` group.

```typst
$ { x mid(|) sum_(i=1)^n w_i|f_i (x)| < 1 } $
```

```typst
#math.mid(
  body
) -> content
```

## Parameters

- body:
  - description: The content to be scaled.
  - type: content
  - default: None

# math.abs

Takes the absolute value of an expression.

```typst
$ abs(x/2) $
```

```typst
#math.abs(
  size: relative,
  body
) -> content
```

## Parameters

- size:
  - description: The size of the brackets, relative to the height of the wrapped content.
  - type: relative
  - default: None
- body:
  - description: The expression to take the absolute value of.
  - type: content
  - default: None

# math.norm

Takes the norm of an expression.

```typst
$ norm(x/2) $
```

```typst
#math.norm(
  size: relative,
  body
) -> content
```

## Parameters

- size:
  - description: The size of the brackets, relative to the height of the wrapped content.
  - type: relative
  - default: None
- body:
  - description: The expression to take the norm of.
  - type: content
  - default: None

# math.floor

Floors an expression.

```typst
$ floor(x/2) $
```

```typst
#math.floor(
  size: relative,
  body
) -> content
```

## Parameters

- size:
  - description: The size of the brackets, relative to the height of the wrapped content.
  - type: relative
  - default: None
- body:
  - description: The expression to floor.
  - type: content
  - default: None

# math.ceil

Ceils an expression.

```typst
$ ceil(x/2) $
```

```typst
#math.ceil(
  size: relative,
  body
) -> content
```

## Parameters

- size:
  - description: The size of the brackets, relative to the height of the wrapped content.
  - type: relative
  - default: None
- body:
  - description: The expression to ceil.
  - type: content
  - default: None

# math.round

Rounds an expression.

```typst
$ round(x/2) $
```

```typst
#math.round(
  size: relative,
  body
) -> content
```

## Parameters

- size:
  - description: The size of the brackets, relative to the height of the wrapped content.
  - type: relative
  - default: None
- body:
  - description: The expression to round.
  - type: content
  - default: None


