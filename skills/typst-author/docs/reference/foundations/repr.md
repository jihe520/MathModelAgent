# Representation

# repr

Returns the string representation of a value.

When inserted into content, most values are displayed as this representation in monospace with syntax-highlighting. The exceptions are `none`, integers, floats, strings, content, and functions.

## Example

```typst
#none vs #repr(none) \
#"hello" vs #repr("hello") \
#(1, 2) vs #repr((1, 2)) \
#[*Hi*] vs #repr([*Hi*])
```

## For debugging purposes only

This function is for debugging purposes. Its output should not be considered stable and may change at any time.

To be specific, having the same `repr` does not guarantee that values are equivalent, and `repr` is not a strict inverse of [`eval`](/docs/reference/foundations/eval/). In the following example, for readability, the [`length`](/docs/reference/layout/length/) is rounded to two significant digits and the parameter list and body of the [unnamed `function`](/docs/reference/foundations/function/#unnamed) are omitted.

```typst
#assert(2pt / 3 < 0.67pt)
#repr(2pt / 3)

#repr(x => x + 1)
```

```typst
#repr(
  value
) -> str
```

## Parameters

- value:
  - description: The value whose string representation to produce.
  - type: any
  - default: None


