# Variants

Alternate typefaces within formulas.

These functions are distinct from the [`text`](/docs/reference/text/text/) function because math fonts contain multiple variants of each letter.

# math.serif

Serif (roman) font style in math.

This is already the default.

```typst
#math.serif(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.sans

Sans-serif font style in math.

```typst
$ sans(A B C) $
```

```typst
#math.sans(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.frak

Fraktur font style in math.

```typst
$ frak(P) $
```

```typst
#math.frak(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.mono

Monospace font style in math.

```typst
$ mono(x + y = z) $
```

```typst
#math.mono(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.bb

Blackboard bold (double-struck) font style in math.

For uppercase latin letters, blackboard bold is additionally available through [symbols](/docs/reference/symbols/sym/) of the form `NN` and `RR`.

```typst
$ bb(b) $
$ bb(N) = NN $
$ f: NN -> RR $
```

```typst
#math.bb(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.cal

Calligraphic (chancery) font style in math.

```typst
Let $cal(P)$ be the set of ...
```

This is the default calligraphic/script style for most math fonts. See [`scr`](/docs/reference/math/variants/#functions-scr) for more on how to get the other style (roundhand).

```typst
#math.cal(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None

# math.scr

Script (roundhand) font style in math.

```typst
$scr(L)$ is not the set of linear
maps $cal(L)$.
```

There are two ways that fonts can support differentiating `cal` and `scr`. The first is using Unicode variation sequences. This works out of the box in Typst, however only a few math fonts currently support this.

The other way is using [font features](/docs/reference/text/text/#parameters-features). For example, the roundhand style might be available in a font through the _stylistic set 1_ (`ss01`) feature. To use it in Typst, you could then define your own version of `scr` like in the example below.

```typst
#let scr(it) = text(
  stylistic-set: 1,
  $cal(it)$,
)

We establish $cal(P) != scr(P)$.
```

```typst
#math.scr(
  body
) -> content
```

## Parameters

- body:
  - description: The content to style.
  - type: content
  - default: None


