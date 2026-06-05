# Text Operator

# math.op

A text operator in an equation.

## Example

```typst
$ tan x = (sin x)/(cos x) $
$ op("custom",
     limits: #true)_(n->oo) n $
```

## Predefined Operators

Typst predefines the operators `arccos`, `arcsin`, `arctan`, `arg`, `cos`, `cosh`, `cot`, `coth`, `csc`, `csch`, `ctg`, `deg`, `det`, `dim`, `exp`, `gcd`, `lcm`, `hom`, `id`, `im`, `inf`, `ker`, `lg`, `lim`, `liminf`, `limsup`, `ln`, `log`, `max`, `min`, `mod`, `Pr`, `sec`, `sech`, `sin`, `sinc`, `sinh`, `sup`, `tan`, `tanh`, `tg` and `tr`.

```typst
#math.op(
  text,
  limits: bool
) -> content
```

## Parameters

- text:
  - description: The operator\'s text.
  - type: content
  - default: None
- limits:
  - description: Whether the operator should show attachments as limits in display mode.
  - type: bool
  - default: false


