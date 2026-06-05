# Under/Over

Delimiters above or below parts of an equation.

The braces and brackets further allow you to add an optional annotation below or above themselves.

# math.underline

A horizontal line under content.

```typst
$ underline(1 + 2 + ... + 5) $
```

```typst
#math.underline(
  body
) -> content
```

## Parameters

- body:
  - description: The content above the line.
  - type: content
  - default: None

# math.overline

A horizontal line over content.

```typst
$ overline(1 + 2 + ... + 5) $
```

```typst
#math.overline(
  body
) -> content
```

## Parameters

- body:
  - description: The content below the line.
  - type: content
  - default: None

# math.underbrace

A horizontal brace under content, with an optional annotation below.

```typst
$ underbrace(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.underbrace(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content above the brace.
  - type: content
  - default: None
- annotation:
  - description: The optional content below the brace.
  - type: none | content
  - default: none

# math.overbrace

A horizontal brace over content, with an optional annotation above.

```typst
$ overbrace(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.overbrace(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content below the brace.
  - type: content
  - default: None
- annotation:
  - description: The optional content above the brace.
  - type: none | content
  - default: none

# math.underbracket

A horizontal bracket under content, with an optional annotation below.

```typst
$ underbracket(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.underbracket(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content above the bracket.
  - type: content
  - default: None
- annotation:
  - description: The optional content below the bracket.
  - type: none | content
  - default: none

# math.overbracket

A horizontal bracket over content, with an optional annotation above.

```typst
$ overbracket(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.overbracket(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content below the bracket.
  - type: content
  - default: None
- annotation:
  - description: The optional content above the bracket.
  - type: none | content
  - default: none

# math.underparen

A horizontal parenthesis under content, with an optional annotation below.

```typst
$ underparen(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.underparen(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content above the parenthesis.
  - type: content
  - default: None
- annotation:
  - description: The optional content below the parenthesis.
  - type: none | content
  - default: none

# math.overparen

A horizontal parenthesis over content, with an optional annotation above.

```typst
$ overparen(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.overparen(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content below the parenthesis.
  - type: content
  - default: None
- annotation:
  - description: The optional content above the parenthesis.
  - type: none | content
  - default: none

# math.undershell

A horizontal tortoise shell bracket under content, with an optional annotation below.

```typst
$ undershell(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.undershell(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content above the tortoise shell bracket.
  - type: content
  - default: None
- annotation:
  - description: The optional content below the tortoise shell bracket.
  - type: none | content
  - default: none

# math.overshell

A horizontal tortoise shell bracket over content, with an optional annotation above.

```typst
$ overshell(0 + 1 + dots.c + n, n + 1 "numbers") $
```

```typst
#math.overshell(
  body,
  annotation
) -> content
```

## Parameters

- body:
  - description: The content below the tortoise shell bracket.
  - type: content
  - default: None
- annotation:
  - description: The optional content above the tortoise shell bracket.
  - type: none | content
  - default: none


