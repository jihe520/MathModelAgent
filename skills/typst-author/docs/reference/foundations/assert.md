# Assert

# assert

Ensures that a condition is fulfilled.

Fails with an error if the condition is not fulfilled. Does not produce any output in the document.

If you wish to test equality between two values, see [`assert.eq`](/docs/reference/foundations/assert/#definitions-eq) and [`assert.ne`](/docs/reference/foundations/assert/#definitions-ne).

## Example

```typst
#assert(1 < 2, message: "math broke")
```

```typst
#assert(
  condition,
  message: str
) -> 
```

## Parameters

- condition:
  - description: The condition that must be true for the assertion to pass.
  - type: bool
  - default: None
- message:
  - description: The error message when the assertion fails.
  - type: str
  - default: None


## Definitions
### assert.eq

Ensures that two values are equal.

Fails with an error if the first value is not equal to the second. Does not produce any output in the document.

```typst
#assert.eq(10, 10)
```

```typst
#assert.eq(
  left,
  right,
  message: str
) -> 
```

#### Parameters

- left:
  - description: The first value to compare.
  - type: any
  - default: None
- right:
  - description: The second value to compare.
  - type: any
  - default: None
- message:
  - description: An optional message to display on error instead of the representations of the compared values.
  - type: str
  - default: None

### assert.ne

Ensures that two values are not equal.

Fails with an error if the first value is equal to the second. Does not produce any output in the document.

```typst
#assert.ne(3, 4)
```

```typst
#assert.ne(
  left,
  right,
  message: str
) -> 
```

#### Parameters

- left:
  - description: The first value to compare.
  - type: any
  - default: None
- right:
  - description: The second value to compare.
  - type: any
  - default: None
- message:
  - description: An optional message to display on error instead of the representations of the compared values.
  - type: str
  - default: None


