# Cases

# math.cases

A case distinction.

Content across different branches can be aligned with the `&` symbol.

## Example

```typst
$ f(x, y) := cases(
  1 "if" (x dot y)/2 <= 0,
  2 "if" x "is even",
  3 "if" x in NN,
  4 "else",
) $
```

```typst
#math.cases(
  delim: none | str | array | symbol,
  reverse: bool,
  gap: relative,
  children
) -> content
```

## Parameters

- delim:
  - description: The delimiter to use. Can be a single character specifying the left delimiter, in which case the right delimiter is inferred. Otherwise, can be an array containing a left and a right delimiter. ```typst #set math.cases(delim: "[") $ x = cases(1, 2) $ ```
  - type: none | str | array | symbol
  - default: ("{", "}")
- reverse:
  - description: Whether the direction of cases should be reversed. ```typst #set math.cases(reverse: true) $ cases(1, 2) = x $ ```
  - type: bool
  - default: false
- gap:
  - description: The gap between branches. ```typst #set math.cases(gap: 1em) $ x = cases(1, 2) $ ```
  - type: relative
  - default: 0 % + 0.2em
- children:
  - description: The branches of the case distinction.
  - type: content
  - default: None


