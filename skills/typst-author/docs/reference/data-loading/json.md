# JSON

# json

Reads structured data from a JSON file.

The file must contain a valid JSON value, such as object or array. The JSON values will be converted into corresponding Typst values as listed in the [table below](#conversion).

The function returns a dictionary, an array or, depending on the JSON file, another JSON data type.

The JSON files in the example contain objects with the keys `temperature`, `unit`, and `weather`.

## Example

```typst
#let forecast(day) = block[
  #box(square(
    width: 2cm,
    inset: 8pt,
    fill: if day.weather == "sunny" {
      yellow
    } else {
      aqua
    },
    align(
      bottom + right,
      strong(day.weather),
    ),
  ))
  #h(6pt)
  #set text(22pt, baseline: -8pt)
  #day.temperature °#day.unit
]

#forecast(json("monday.json"))
#forecast(json("tuesday.json"))
```

## Conversion details

| JSON value | Converted into Typst |
| --- | --- |
| `null` | `none` |
| bool | [`bool`](/docs/reference/foundations/bool/) |
| number | [`float`](/docs/reference/foundations/float/) or [`int`](/docs/reference/foundations/int/) |
| string | [`str`](/docs/reference/foundations/str/) |
| array | [`array`](/docs/reference/foundations/array/) |
| object | [`dictionary`](/docs/reference/foundations/dictionary/) |

| Typst value | Converted into JSON |
| --- | --- |
| types that can be converted from JSON | corresponding JSON value |
| [`bytes`](/docs/reference/foundations/bytes/) | string via [`repr`](/docs/reference/foundations/repr/) |
| [`symbol`](/docs/reference/foundations/symbol/) | string |
| [`content`](/docs/reference/foundations/content/) | an object describing the content |
| other types ([`length`](/docs/reference/layout/length/), etc.) | string via [`repr`](/docs/reference/foundations/repr/) |

### Notes

- In most cases, JSON numbers will be converted to floats or integers depending on whether they are whole numbers. However, be aware that integers larger than 263-1 or smaller than -263 will be converted to floating-point numbers, which may result in an approximative value.
- Bytes are not encoded as JSON arrays for performance and readability reasons. Consider using [`cbor.encode`](/docs/reference/data-loading/cbor/#definitions-encode) for binary data.
- The `repr` function is [for debugging purposes only](/docs/reference/foundations/repr/#debugging-only), and its output is not guaranteed to be stable across Typst versions.

```typst
#json(
  source
) -> any
```

## Parameters

- source:
  - description: A [path](/docs/reference/syntax/#paths) to a JSON file or raw JSON bytes.
  - type: str | bytes
  - default: None


## Definitions
### json.decode

Reads structured data from a JSON string/bytes.

```typst
#json.decode(
  data
) -> any
```

#### Parameters

- data:
  - description: JSON data.
  - type: str | bytes
  - default: None

### json.encode

Encodes structured data into a JSON string.

```typst
#json.encode(
  value,
  pretty: bool
) -> str
```

#### Parameters

- value:
  - description: Value to be encoded.
  - type: any
  - default: None
- pretty:
  - description: Whether to pretty print the JSON with newlines and indentation.
  - type: bool
  - default: true


