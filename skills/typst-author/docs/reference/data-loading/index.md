# Data Loading

Data loading from external files.

These functions help you with loading and embedding data, for example from the results of an experiment.

## Encoding

Some of the functions are also capable of encoding, e.g. [`cbor.encode`](/docs/reference/data-loading/cbor/#definitions-encode). They facilitate passing structured data to [plugins](/docs/reference/foundations/plugin/).

However, each data format has its own native types. Therefore, for an arbitrary Typst value, the encode-to-decode roundtrip might be lossy. In general, numbers, strings, and [arrays](/docs/reference/foundations/array/) or [dictionaries](/docs/reference/foundations/dictionary/) composed of them can be reliably converted, while other types may fall back to strings via [`repr`](/docs/reference/foundations/repr/), which is [for debugging purposes only](/docs/reference/foundations/repr/#debugging-only). Please refer to the page of each data format for details.

## Definitions

| Name | Description |
| --- | --- |
| [`cbor`](/reference/data-loading/cbor/) | Reads structured data from a CBOR file. |
| [`csv`](/reference/data-loading/csv/) | Reads structured data from a CSV file. |
| [`json`](/reference/data-loading/json/) | Reads structured data from a JSON file. |
| [`read`](/reference/data-loading/read/) | Reads plain text or data from a file. |
| [`toml`](/reference/data-loading/toml/) | Reads structured data from a TOML file. |
| [`xml`](/reference/data-loading/xml/) | Reads structured data from an XML file. |
| [`yaml`](/reference/data-loading/yaml/) | Reads structured data from a YAML file. |

