# Panic

# panic

Fails with an error.

Arguments are displayed to the user (not rendered in the document) as strings, converting with `repr` if necessary.

## Example

The code below produces the error `panicked with: "this is wrong"`.

```typst
#panic("this is wrong")
```

```typst
#panic(
  values
) -> 
```

## Parameters

- values:
  - description: The values to panic with and display to the user.
  - type: any
  - default: None


