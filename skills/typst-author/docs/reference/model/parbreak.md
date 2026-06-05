# Paragraph Break

# parbreak

A paragraph break.

This starts a new paragraph. Especially useful when used within code like [for loops](/docs/reference/scripting/#loops). Multiple consecutive paragraph breaks collapse into a single one.

## Example

```typst
#for i in range(3) {
  [Blind text #i: ]
  lorem(5)
  parbreak()
}
```

## Syntax

Instead of calling this function, you can insert a blank line into your markup to create a paragraph break.


