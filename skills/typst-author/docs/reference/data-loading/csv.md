# CSV

# csv

Reads structured data from a CSV file.

The CSV file will be read and parsed into a 2-dimensional array of strings: Each row in the CSV file will be represented as an array of strings, and all rows will be collected into a single array. Header rows will not be stripped.

## Example

```typst
#let results = csv("example.csv")

#table(
  columns: 2,
  [*Condition*], [*Result*],
  ..results.flatten(),
)
```

```typst
#csv(
  source,
  delimiter: str,
  row-type: type
) -> array
```

## Parameters

- source:
  - description: A [path](/docs/reference/syntax/#paths) to a CSV file or raw CSV bytes.
  - type: str | bytes
  - default: None
- delimiter:
  - description: The delimiter that separates columns in the CSV file. Must be a single ASCII character.
  - type: str
  - default: ","
- row-type:
  - description: How to represent the file\'s rows. - If set to `array`, each row is represented as a plain array of strings. - If set to `dictionary`, each row is represented as a dictionary mapping from header keys to strings. This option only makes sense when a header row is present in the CSV file.
  - type: type
  - default: array


## Definitions
### csv.decode

Reads structured data from a CSV string/bytes.

```typst
#csv.decode(
  data,
  delimiter: str,
  row-type: type
) -> array
```

#### Parameters

- data:
  - description: CSV data.
  - type: str | bytes
  - default: None
- delimiter:
  - description: The delimiter that separates columns in the CSV file. Must be a single ASCII character.
  - type: str
  - default: ","
- row-type:
  - description: How to represent the file\'s rows. - If set to `array`, each row is represented as a plain array of strings. - If set to `dictionary`, each row is represented as a dictionary mapping from header keys to strings. This option only makes sense when a header row is present in the CSV file.
  - type: type
  - default: array


