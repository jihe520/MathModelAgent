# Evaluate

# eval

Evaluates a string as Typst code.

This function should only be used as a last resort.

## Example

```typst
#eval("1 + 1") \
#eval("(1, 2, 3, 4)").len() \
#eval("*Markup!*", mode: "markup") \
```

```typst
#eval(
  source,
  mode: str,
  scope: dictionary
) -> any
```

## Parameters

- source:
  - description: A string of Typst code to evaluate.
  - type: str
  - default: None
- mode:
  - description: The [syntactical mode](/docs/reference/syntax/#modes) in which the string is parsed. ```typst #eval("= Heading", mode: "markup") #eval("1_2^3", mode: "math") ```
  - type: str
  - default: "code"
- scope:
  - description: A scope of definitions that are made available. ```typst #eval("x + 1", scope: (x: 2)) \\ #eval(  "abc/xyz",  mode: "math",  scope: (   abc: $a + b + c$,   xyz: $x + y + z$,  ), ) ```
  - type: dictionary
  - default: (:)


