# TOML

# toml

Reads structured data from a TOML file.

The file must contain a valid TOML table. The TOML values will be converted into corresponding Typst values as listed in the [table below](#conversion).

The function returns a dictionary representing the TOML table.

The TOML file in the example consists of a table with the keys `title`, `version`, and `authors`.

## Example

```typst
#let details = toml("details.toml")

Title: #details.title \
Version: #details.version \
Authors: #(details.authors
  .join(", ", last: " and "))
```

## Conversion details

First of all, TOML documents are tables. Other values must be put in a table to be encoded or decoded.

| TOML value | Converted into Typst |
| --- | --- |
| string | [`str`](/docs/reference/foundations/str/) |
| integer | [`int`](/docs/reference/foundations/int/) |
| float | [`float`](/docs/reference/foundations/float/) |
| boolean | [`bool`](/docs/reference/foundations/bool/) |
| datetime | [`datetime`](/docs/reference/foundations/datetime/) |
| array | [`array`](/docs/reference/foundations/array/) |
| table | [`dictionary`](/docs/reference/foundations/dictionary/) |

| Typst value | Converted into TOML |
| --- | --- |
| types that can be converted from TOML | corresponding TOML value |
| `none` | ignored |
| [`bytes`](/docs/reference/foundations/bytes/) | string via [`repr`](/docs/reference/foundations/repr/) |
| [`symbol`](/docs/reference/foundations/symbol/) | string |
| [`content`](/docs/reference/foundations/content/) | a table describing the content |
| other types ([`length`](/docs/reference/layout/length/), etc.) | string via [`repr`](/docs/reference/foundations/repr/) |

### Notes

- Be aware that TOML integers larger than 263-1 or smaller than -263 cannot be represented losslessly in Typst, and an error will be thrown according to the [specification](https://toml.io/en/v1.0.0#integer).
- Bytes are not encoded as TOML arrays for performance and readability reasons. Consider using [`cbor.encode`](/docs/reference/data-loading/cbor/#definitions-encode) for binary data.
- The `repr` function is [for debugging purposes only](/docs/reference/foundations/repr/#debugging-only), and its output is not guaranteed to be stable across Typst versions.

```typst
#toml(
  source
) -> dictionary
```

## Parameters

- source:
  - description: A [path](/docs/reference/syntax/#paths) to a TOML file or raw TOML bytes.
  - type: str | bytes
  - default: None


## Definitions
### toml.decode

Reads structured data from a TOML string/bytes.

```typst
#toml.decode(
  data
) -> dictionary
```

#### Parameters

- data:
  - description: TOML data.
  - type: str | bytes
  - default: None

### toml.encode

Encodes structured data into a TOML string.

```typst
#toml.encode(
  value,
  pretty: bool
) -> str
```

#### Parameters

- value:
  - description: Value to be encoded. TOML documents are tables. Therefore, only dictionaries are suitable.
  - type: dictionary
  - default: None
- pretty:
  - description: Whether to pretty-print the resulting TOML.
  - type: bool
  - default: true


