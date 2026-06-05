# Bytes

A sequence of bytes.

This is conceptually similar to an array of [integers](/docs/reference/foundations/int/) between `0` and `255`, but represented much more efficiently. You can iterate over it using a [for loop](/docs/reference/scripting/#loops).

You can convert

- a [string](/docs/reference/foundations/str/) or an [array](/docs/reference/foundations/array/) of integers to bytes with the [`bytes`](/docs/reference/foundations/bytes/) constructor
- bytes to a string with the [`str`](/docs/reference/foundations/str/) constructor, with UTF-8 encoding
- bytes to an array of integers with the [`array`](/docs/reference/foundations/array/) constructor

When [reading](/docs/reference/data-loading/read/) data from a file, you can decide whether to load it as a string or as raw bytes.

```typst
#bytes((123, 160, 22, 0)) \
#bytes("Hello 😃")

#let data = read(
  "rhino.png",
  encoding: none,
)

// Magic bytes.
#array(data.slice(0, 4)) \
#str(data.slice(1, 4))
```

## Constructor
## bytes

Converts a value to bytes.

- Strings are encoded in UTF-8.
- Arrays of integers between `0` and `255` are converted directly. The dedicated byte representation is much more efficient than the array representation and thus typically used for large byte buffers (e.g. image data).

```typst
#bytes("Hello 😃") \
#bytes((123, 160, 22, 0))
```

```typst
#bytes(
  value
) -> bytes
```

### Parameters

- value:
  - description: The value that should be converted to bytes.
  - type: str | bytes | array
  - default: None


## Methods

## bytes.len

The length in bytes.

## bytes.at

Returns the byte at the specified index. Returns the default value if the index is out of bounds or fails with an error if no default value was specified.

```typst
#bytes.at(
  index,
  default: any
) -> any
```

### Parameters

- index:
  - description: The index at which to retrieve the byte.
  - type: int
  - default: None
- default:
  - description: A default value to return if the index is out of bounds.
  - type: any
  - default: None

## bytes.slice

Extracts a subslice of the bytes. Fails with an error if the start or end index is out of bounds.

```typst
#bytes.slice(
  start,
  end,
  count: int
) -> bytes
```

### Parameters

- start:
  - description: The start index (inclusive).
  - type: int
  - default: None
- end:
  - description: The end index (exclusive). If omitted, the whole slice until the end is extracted.
  - type: none | int
  - default: none
- count:
  - description: The number of items to extract. This is equivalent to passing `start + count` as the `end` position. Mutually exclusive with `end`.
  - type: int
  - default: None


