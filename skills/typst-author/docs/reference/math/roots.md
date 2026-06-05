# Roots

Square and non-square roots.

## Example

```typst
$ sqrt(3 - 2 sqrt(2)) = sqrt(2) - 1 $
$ root(3, x) $
```

# math.root

A general root.

```typst
$ root(3, x) $
```

```typst
#math.root(
  index,
  radicand
) -> content
```

## Parameters

- index:
  - description: Which root of the radicand to take.
  - type: none | content
  - default: none
- radicand:
  - description: The expression to take the root of.
  - type: content
  - default: None

# math.sqrt

A square root.

```typst
$ sqrt(3 - 2 sqrt(2)) = sqrt(2) - 1 $
```

```typst
#math.sqrt(
  radicand
) -> content
```

## Parameters

- radicand:
  - description: The expression to take the square root of.
  - type: content
  - default: None


