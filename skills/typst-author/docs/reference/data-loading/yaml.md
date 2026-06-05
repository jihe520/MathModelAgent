# YAML

# yaml

Reads structured data from a YAML file.

The file must contain a valid YAML object or array. The YAML values will be converted into corresponding Typst values as listed in the [table below](#conversion).

The function returns a dictionary, an array or, depending on the YAML file, another YAML data type.

The YAML files in the example contain objects with authors as keys, each with a sequence of their own submapping with the keys "title" and "published".

## Example

```typst
#let bookshelf(contents) = {
  for (author, works) in contents {
    author
    for work in works [
      - #work.title (#work.published)
    ]
  }
}

#bookshelf(
  yaml("scifi-authors.yaml")
)
```

## Conversion details

| YAML value | Converted into Typst |
| --- | --- |
| null-values (`null`, `~` or empty ``) | `none` |
| boolean | [`bool`](/docs/reference/foundations/bool/) |
| number | [`float`](/docs/reference/foundations/float/) or [`int`](/docs/reference/foundations/int/) |
| string | [`str`](/docs/reference/foundations/str/) |
| sequence | [`array`](/docs/reference/foundations/array/) |
| mapping | [`dictionary`](/docs/reference/foundations/dictionary/) |

| Typst value | Converted into YAML |
| --- | --- |
| types that can be converted from YAML | corresponding YAML value |
| [`bytes`](/docs/reference/foundations/bytes/) | string via [`repr`](/docs/reference/foundations/repr/) |
| [`symbol`](/docs/reference/foundations/symbol/) | string |
| [`content`](/docs/reference/foundations/content/) | a mapping describing the content |
| other types ([`length`](/docs/reference/layout/length/), etc.) | string via [`repr`](/docs/reference/foundations/repr/) |

### Notes

- In most cases, YAML numbers will be converted to floats or integers depending on whether they are whole numbers. However, be aware that integers larger than 263-1 or smaller than -263 will be converted to floating-point numbers, which may result in an approximative value.
- Custom YAML tags are ignored, though the loaded value will still be present.
- Bytes are not encoded as YAML sequences for performance and readability reasons. Consider using [`cbor.encode`](/docs/reference/data-loading/cbor/#definitions-encode) for binary data.
- The `repr` function is [for debugging purposes only](/docs/reference/foundations/repr/#debugging-only), and its output is not guaranteed to be stable across Typst versions.

```typst
#yaml(
  source
) -> any
```

## Parameters

- source:
  - description: A [path](/docs/reference/syntax/#paths) to a YAML file or raw YAML bytes.
  - type: str | bytes
  - default: None


## Definitions
### yaml.decode

Reads structured data from a YAML string/bytes.

```typst
#yaml.decode(
  data
) -> any
```

#### Parameters

- data:
  - description: YAML data.
  - type: str | bytes
  - default: None

### yaml.encode

Encode structured data into a YAML string.

```typst
#yaml.encode(
  value
) -> str
```

#### Parameters

- value:
  - description: Value to be encoded.
  - type: any
  - default: None


