# Fraction

# math.frac

A mathematical fraction.

## Example

```typst
$ 1/2 < (x+1)/2 $
$ ((x+1)) / 2 = frac(a, b) $
```

## Syntax

This function also has dedicated syntax: Use a slash to turn neighbouring expressions into a fraction. Multiple atoms can be grouped into a single expression using round grouping parentheses. Such parentheses are removed from the output, but you can nest multiple to force them.

```typst
#math.frac(
  num,
  denom,
  style: str
) -> content
```

## Parameters

- num:
  - description: The fraction\'s numerator.
  - type: content
  - default: None
- denom:
  - description: The fraction\'s denominator.
  - type: content
  - default: None
- style:
  - description: How the fraction should be laid out. ```typst $ frac(x, y, style: "vertical") $ $ frac(x, y, style: "skewed") $ $ frac(x, y, style: "horizontal") $ ``` ```typst #set math.frac(style: "skewed") $ a / b $ ``` ```typst // Grouping parentheses are removed. #set math.frac(style: "vertical") $ (a + b) / b $ // Grouping parentheses are removed. #set math.frac(style: "skewed") $ (a + b) / b $ // Grouping parentheses are retained. #set math.frac(style: "horizontal") $ (a + b) / b $ ``` ```typst // This changes the style for inline equations only. #show math.equation.where(block: false): set math.frac(style: "horizontal") This $(x-y)/z = 3$ is inline math, and this is block math: $ (x-y)/z = 3 $ ```
  - type: str
  - default: "vertical"


