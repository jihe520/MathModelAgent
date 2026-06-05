# Class

# math.class

Forced use of a certain math class.

This is useful to treat certain symbols as if they were of a different class, e.g. to make a symbol behave like a relation. The class of a symbol defines the way it is laid out, including spacing around it, and how its scripts are attached by default. Note that the latter can always be overridden using [`limits`](/docs/reference/math/attach/#functions-limits) and [`scripts`](/docs/reference/math/attach/#functions-scripts).

## Example

```typst
#let loves = math.class(
  "relation",
  sym.suit.heart,
)

$x loves y and y loves 5$
```

```typst
#math.class(
  class,
  body
) -> content
```

## Parameters

- class:
  - description: The class to apply to the content.
  - type: str
  - default: None
- body:
  - description: The content to which the class is applied.
  - type: content
  - default: None


