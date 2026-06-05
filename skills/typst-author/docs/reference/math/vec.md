# Vector

# math.vec

A column vector.

Content in the vector's elements can be aligned with the [`align`](/docs/reference/math/vec/#parameters-align) parameter, or the `&` symbol.

This function is for typesetting vector components. To typeset a symbol that represents a vector, [`arrow`](/docs/reference/math/accent/) and [`bold`](/docs/reference/math/styles/#functions-bold) are commonly used.

## Example

```typst
$ vec(a, b, c) dot vec(1, 2, 3)
    = a + 2b + 3c $
```

```typst
#math.vec(
  delim: none | str | array | symbol,
  align: alignment,
  gap: relative,
  children
) -> content
```

## Parameters

- delim:
  - description: The delimiter to use. Can be a single character specifying the left delimiter, in which case the right delimiter is inferred. Otherwise, can be an array containing a left and a right delimiter. ```typst #set math.vec(delim: "[") $ vec(1, 2) $ ```
  - type: none | str | array | symbol
  - default: ("(", ")")
- align:
  - description: The horizontal alignment that each element should have. ```typst #set math.vec(align: right) $ vec(-1, 1, -1) $ ```
  - type: alignment
  - default: center
- gap:
  - description: The gap between elements. ```typst #set math.vec(gap: 1em) $ vec(1, 2) $ ```
  - type: relative
  - default: 0 % + 0.2em
- children:
  - description: The elements of the vector.
  - type: content
  - default: None


