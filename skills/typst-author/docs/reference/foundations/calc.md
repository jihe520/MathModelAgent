# Calculation

Module for calculations and processing of numeric values.

These definitions are part of the `calc` module and not imported by default. In addition to the functions listed below, the `calc` module also defines the constants `pi`, `tau`, `e`, and `inf`.

# calc.abs

Calculates the absolute value of a numeric value.

```typst
#calc.abs(-5) \
#calc.abs(5pt - 2cm) \
#calc.abs(2fr) \
#calc.abs(decimal("-342.440"))
```

```typst
#calc.abs(
  value
) -> any
```

## Parameters

- value:
  - description: The value whose absolute value to calculate.
  - type: int | float | length | angle | ratio | fraction | decimal
  - default: None

# calc.pow

Raises a value to some exponent.

```typst
#calc.pow(2, 3) \
#calc.pow(decimal("2.5"), 2)
```

```typst
#calc.pow(
  base,
  exponent
) -> int float decimal
```

## Parameters

- base:
  - description: The base of the power. If this is a [`decimal`](/docs/reference/foundations/decimal/), the exponent can only be an [integer](/docs/reference/foundations/int/).
  - type: int | float | decimal
  - default: None
- exponent:
  - description: The exponent of the power.
  - type: int | float
  - default: None

# calc.exp

Raises a value to some exponent of e.

```typst
#calc.exp(1)
```

```typst
#calc.exp(
  exponent
) -> float
```

## Parameters

- exponent:
  - description: The exponent of the power.
  - type: int | float
  - default: None

# calc.sqrt

Calculates the square root of a number.

```typst
#calc.sqrt(16) \
#calc.sqrt(2.5)
```

```typst
#calc.sqrt(
  value
) -> float
```

## Parameters

- value:
  - description: The number whose square root to calculate. Must be non-negative.
  - type: int | float
  - default: None

# calc.root

Calculates the real nth root of a number.

If the number is negative, then n must be odd.

```typst
#calc.root(16.0, 4) \
#calc.root(27.0, 3)
```

```typst
#calc.root(
  radicand,
  index
) -> float
```

## Parameters

- radicand:
  - description: The expression to take the root of.
  - type: float
  - default: None
- index:
  - description: Which root of the radicand to take.
  - type: int
  - default: None

# calc.sin

Calculates the sine of an angle.

When called with an integer or a float, they will be interpreted as radians.

```typst
#calc.sin(1.5) \
#calc.sin(90deg)
```

```typst
#calc.sin(
  angle
) -> float
```

## Parameters

- angle:
  - description: The angle whose sine to calculate.
  - type: int | float | angle
  - default: None

# calc.cos

Calculates the cosine of an angle.

When called with an integer or a float, they will be interpreted as radians.

```typst
#calc.cos(1.5) \
#calc.cos(90deg)
```

```typst
#calc.cos(
  angle
) -> float
```

## Parameters

- angle:
  - description: The angle whose cosine to calculate.
  - type: int | float | angle
  - default: None

# calc.tan

Calculates the tangent of an angle.

When called with an integer or a float, they will be interpreted as radians.

```typst
#calc.tan(1.5) \
#calc.tan(90deg)
```

```typst
#calc.tan(
  angle
) -> float
```

## Parameters

- angle:
  - description: The angle whose tangent to calculate.
  - type: int | float | angle
  - default: None

# calc.asin

Calculates the arcsine of a number.

```typst
#calc.asin(0) \
#calc.asin(1)
```

```typst
#calc.asin(
  value
) -> angle
```

## Parameters

- value:
  - description: The number whose arcsine to calculate. Must be between -1 and 1.
  - type: int | float
  - default: None

# calc.acos

Calculates the arccosine of a number.

```typst
#calc.acos(0) \
#calc.acos(1)
```

```typst
#calc.acos(
  value
) -> angle
```

## Parameters

- value:
  - description: The number whose arccosine to calculate. Must be between -1 and 1.
  - type: int | float
  - default: None

# calc.atan

Calculates the arctangent of a number.

```typst
#calc.atan(0) \
#calc.atan(1)
```

```typst
#calc.atan(
  value
) -> angle
```

## Parameters

- value:
  - description: The number whose arctangent to calculate.
  - type: int | float
  - default: None

# calc.atan2

Calculates the four-quadrant arctangent of a coordinate.

The arguments are `(x, y)`, not `(y, x)`.

```typst
#calc.atan2(1, 1) \
#calc.atan2(-2, -3)
```

```typst
#calc.atan2(
  x,
  y
) -> angle
```

## Parameters

- x:
  - description: The X coordinate.
  - type: int | float
  - default: None
- y:
  - description: The Y coordinate.
  - type: int | float
  - default: None

# calc.sinh

Calculates the hyperbolic sine of a hyperbolic angle.

```typst
#calc.sinh(0) \
#calc.sinh(1.5)
```

```typst
#calc.sinh(
  value
) -> float
```

## Parameters

- value:
  - description: The hyperbolic angle whose hyperbolic sine to calculate.
  - type: float
  - default: None

# calc.cosh

Calculates the hyperbolic cosine of a hyperbolic angle.

```typst
#calc.cosh(0) \
#calc.cosh(1.5)
```

```typst
#calc.cosh(
  value
) -> float
```

## Parameters

- value:
  - description: The hyperbolic angle whose hyperbolic cosine to calculate.
  - type: float
  - default: None

# calc.tanh

Calculates the hyperbolic tangent of a hyperbolic angle.

```typst
#calc.tanh(0) \
#calc.tanh(1.5)
```

```typst
#calc.tanh(
  value
) -> float
```

## Parameters

- value:
  - description: The hyperbolic angle whose hyperbolic tangent to calculate.
  - type: float
  - default: None

# calc.log

Calculates the logarithm of a number.

If the base is not specified, the logarithm is calculated in base 10.

```typst
#calc.log(100)
```

```typst
#calc.log(
  value,
  base: float
) -> float
```

## Parameters

- value:
  - description: The number whose logarithm to calculate. Must be strictly positive.
  - type: int | float
  - default: None
- base:
  - description: The base of the logarithm. May not be zero.
  - type: float
  - default: 10.0

# calc.ln

Calculates the natural logarithm of a number.

```typst
#calc.ln(calc.e)
```

```typst
#calc.ln(
  value
) -> float
```

## Parameters

- value:
  - description: The number whose logarithm to calculate. Must be strictly positive.
  - type: int | float
  - default: None

# calc.fact

Calculates the factorial of a number.

```typst
#calc.fact(5)
```

```typst
#calc.fact(
  number
) -> int
```

## Parameters

- number:
  - description: The number whose factorial to calculate. Must be non-negative.
  - type: int
  - default: None

# calc.perm

Calculates a permutation.

Returns the `k`-permutation of `n`, or the number of ways to choose `k` items from a set of `n` with regard to order.

```typst
$ "perm"(n, k) &= n!/((n - k)!) \
  "perm"(5, 3) &= #calc.perm(5, 3) $
```

```typst
#calc.perm(
  base,
  numbers
) -> int
```

## Parameters

- base:
  - description: The base number. Must be non-negative.
  - type: int
  - default: None
- numbers:
  - description: The number of permutations. Must be non-negative.
  - type: int
  - default: None

# calc.binom

Calculates a binomial coefficient.

Returns the `k`-combination of `n`, or the number of ways to choose `k` items from a set of `n` without regard to order.

```typst
#calc.binom(10, 5)
```

```typst
#calc.binom(
  n,
  k
) -> int
```

## Parameters

- n:
  - description: The upper coefficient. Must be non-negative.
  - type: int
  - default: None
- k:
  - description: The lower coefficient. Must be non-negative.
  - type: int
  - default: None

# calc.gcd

Calculates the greatest common divisor of two integers.

This will error if the result of integer division would be larger than the maximum 64-bit signed integer.

```typst
#calc.gcd(7, 42)
```

```typst
#calc.gcd(
  a,
  b
) -> int
```

## Parameters

- a:
  - description: The first integer.
  - type: int
  - default: None
- b:
  - description: The second integer.
  - type: int
  - default: None

# calc.lcm

Calculates the least common multiple of two integers.

```typst
#calc.lcm(96, 13)
```

```typst
#calc.lcm(
  a,
  b
) -> int
```

## Parameters

- a:
  - description: The first integer.
  - type: int
  - default: None
- b:
  - description: The second integer.
  - type: int
  - default: None

# calc.floor

Rounds a number down to the nearest integer.

If the number is already an integer, it is returned unchanged.

Note that this function will always return an [integer](/docs/reference/foundations/int/), and will error if the resulting [`float`](/docs/reference/foundations/float/) or [`decimal`](/docs/reference/foundations/decimal/) is larger than the maximum 64-bit signed integer or smaller than the minimum for that type.

```typst
#calc.floor(500.1)
#assert(calc.floor(3) == 3)
#assert(calc.floor(3.14) == 3)
#assert(calc.floor(decimal("-3.14")) == -4)
```

```typst
#calc.floor(
  value
) -> int
```

## Parameters

- value:
  - description: The number to round down.
  - type: int | float | decimal
  - default: None

# calc.ceil

Rounds a number up to the nearest integer.

If the number is already an integer, it is returned unchanged.

Note that this function will always return an [integer](/docs/reference/foundations/int/), and will error if the resulting [`float`](/docs/reference/foundations/float/) or [`decimal`](/docs/reference/foundations/decimal/) is larger than the maximum 64-bit signed integer or smaller than the minimum for that type.

```typst
#calc.ceil(500.1)
#assert(calc.ceil(3) == 3)
#assert(calc.ceil(3.14) == 4)
#assert(calc.ceil(decimal("-3.14")) == -3)
```

```typst
#calc.ceil(
  value
) -> int
```

## Parameters

- value:
  - description: The number to round up.
  - type: int | float | decimal
  - default: None

# calc.trunc

Returns the integer part of a number.

If the number is already an integer, it is returned unchanged.

Note that this function will always return an [integer](/docs/reference/foundations/int/), and will error if the resulting [`float`](/docs/reference/foundations/float/) or [`decimal`](/docs/reference/foundations/decimal/) is larger than the maximum 64-bit signed integer or smaller than the minimum for that type.

```typst
#calc.trunc(15.9)
#assert(calc.trunc(3) == 3)
#assert(calc.trunc(-3.7) == -3)
#assert(calc.trunc(decimal("8493.12949582390")) == 8493)
```

```typst
#calc.trunc(
  value
) -> int
```

## Parameters

- value:
  - description: The number to truncate.
  - type: int | float | decimal
  - default: None

# calc.fract

Returns the fractional part of a number.

If the number is an integer, returns `0`.

```typst
#calc.fract(-3.1)
#assert(calc.fract(3) == 0)
#assert(calc.fract(decimal("234.23949211")) == decimal("0.23949211"))
```

```typst
#calc.fract(
  value
) -> int float decimal
```

## Parameters

- value:
  - description: The number to truncate.
  - type: int | float | decimal
  - default: None

# calc.round

Rounds a number to the nearest integer.

Half-integers are rounded away from zero.

Optionally, a number of decimal places can be specified. If negative, its absolute value will indicate the amount of significant integer digits to remove before the decimal point.

Note that this function will return the same type as the operand. That is, applying `round` to a [`float`](/docs/reference/foundations/float/) will return a `float`, and to a [`decimal`](/docs/reference/foundations/decimal/), another `decimal`. You may explicitly convert the output of this function to an integer with [`int`](/docs/reference/foundations/int/), but note that such a conversion will error if the `float` or `decimal` is larger than the maximum 64-bit signed integer or smaller than the minimum integer.

In addition, this function can error if there is an attempt to round beyond the maximum or minimum integer or `decimal`. If the number is a `float`, such an attempt will cause `float.inf` or `-float.inf` to be returned for maximum and minimum respectively.

```typst
#calc.round(3.1415, digits: 2)
#assert(calc.round(3) == 3)
#assert(calc.round(3.14) == 3)
#assert(calc.round(3.5) == 4.0)
#assert(calc.round(3333.45, digits: -2) == 3300.0)
#assert(calc.round(-48953.45, digits: -3) == -49000.0)
#assert(calc.round(3333, digits: -2) == 3300)
#assert(calc.round(-48953, digits: -3) == -49000)
#assert(calc.round(decimal("-6.5")) == decimal("-7"))
#assert(calc.round(decimal("7.123456789"), digits: 6) == decimal("7.123457"))
#assert(calc.round(decimal("3333.45"), digits: -2) == decimal("3300"))
#assert(calc.round(decimal("-48953.45"), digits: -3) == decimal("-49000"))
```

```typst
#calc.round(
  value,
  digits: int
) -> int float decimal
```

## Parameters

- value:
  - description: The number to round.
  - type: int | float | decimal
  - default: None
- digits:
  - description: If positive, the number of decimal places. If negative, the number of significant integer digits that should be removed before the decimal point.
  - type: int
  - default: 0

# calc.clamp

Clamps a number between a minimum and maximum value.

```typst
#calc.clamp(5, 0, 4)
#assert(calc.clamp(5, 0, 10) == 5)
#assert(calc.clamp(5, 6, 10) == 6)
#assert(calc.clamp(decimal("5.45"), 2, decimal("45.9")) == decimal("5.45"))
#assert(calc.clamp(decimal("5.45"), decimal("6.75"), 12) == decimal("6.75"))
```

```typst
#calc.clamp(
  value,
  min,
  max
) -> int float decimal
```

## Parameters

- value:
  - description: The number to clamp.
  - type: int | float | decimal
  - default: None
- min:
  - description: The inclusive minimum value.
  - type: int | float | decimal
  - default: None
- max:
  - description: The inclusive maximum value.
  - type: int | float | decimal
  - default: None

# calc.min

Determines the minimum of a sequence of values.

```typst
#calc.min(1, -3, -5, 20, 3, 6) \
#calc.min("typst", "is", "cool")
```

```typst
#calc.min(
  values
) -> any
```

## Parameters

- values:
  - description: The sequence of values from which to extract the minimum. Must not be empty.
  - type: any
  - default: None

# calc.max

Determines the maximum of a sequence of values.

```typst
#calc.max(1, -3, -5, 20, 3, 6) \
#calc.max("typst", "is", "cool")
```

```typst
#calc.max(
  values
) -> any
```

## Parameters

- values:
  - description: The sequence of values from which to extract the maximum. Must not be empty.
  - type: any
  - default: None

# calc.even

Determines whether an integer is even.

```typst
#calc.even(4) \
#calc.even(5) \
#range(10).filter(calc.even)
```

```typst
#calc.even(
  value
) -> bool
```

## Parameters

- value:
  - description: The number to check for evenness.
  - type: int
  - default: None

# calc.odd

Determines whether an integer is odd.

```typst
#calc.odd(4) \
#calc.odd(5) \
#range(10).filter(calc.odd)
```

```typst
#calc.odd(
  value
) -> bool
```

## Parameters

- value:
  - description: The number to check for oddness.
  - type: int
  - default: None

# calc.rem

Calculates the remainder of two numbers.

The value `calc.rem(x, y)` always has the same sign as `x`, and is smaller in magnitude than `y`.

This can error if given a [`decimal`](/docs/reference/foundations/decimal/) input and the dividend is too small in magnitude compared to the divisor.

```typst
#calc.rem(7, 3) \
#calc.rem(7, -3) \
#calc.rem(-7, 3) \
#calc.rem(-7, -3) \
#calc.rem(1.75, 0.5)
```

```typst
#calc.rem(
  dividend,
  divisor
) -> int float decimal
```

## Parameters

- dividend:
  - description: The dividend of the remainder.
  - type: int | float | decimal
  - default: None
- divisor:
  - description: The divisor of the remainder.
  - type: int | float | decimal
  - default: None

# calc.div-euclid

Performs euclidean division of two numbers.

The result of this computation is that of a division rounded to the integer `n` such that the dividend is greater than or equal to `n` times the divisor.

This can error if the resulting number is larger than the maximum value or smaller than the minimum value for its type.

```typst
#calc.div-euclid(7, 3) \
#calc.div-euclid(7, -3) \
#calc.div-euclid(-7, 3) \
#calc.div-euclid(-7, -3) \
#calc.div-euclid(1.75, 0.5) \
#calc.div-euclid(decimal("1.75"), decimal("0.5"))
```

```typst
#calc.div-euclid(
  dividend,
  divisor
) -> int float decimal
```

## Parameters

- dividend:
  - description: The dividend of the division.
  - type: int | float | decimal
  - default: None
- divisor:
  - description: The divisor of the division.
  - type: int | float | decimal
  - default: None

# calc.rem-euclid

This calculates the least nonnegative remainder of a division.

Warning: Due to a floating point round-off error, the remainder may equal the absolute value of the divisor if the dividend is much smaller in magnitude than the divisor and the dividend is negative. This only applies for floating point inputs.

In addition, this can error if given a [`decimal`](/docs/reference/foundations/decimal/) input and the dividend is too small in magnitude compared to the divisor.

```typst
#calc.rem-euclid(7, 3) \
#calc.rem-euclid(7, -3) \
#calc.rem-euclid(-7, 3) \
#calc.rem-euclid(-7, -3) \
#calc.rem-euclid(1.75, 0.5) \
#calc.rem-euclid(decimal("1.75"), decimal("0.5"))
```

```typst
#calc.rem-euclid(
  dividend,
  divisor
) -> int float decimal
```

## Parameters

- dividend:
  - description: The dividend of the remainder.
  - type: int | float | decimal
  - default: None
- divisor:
  - description: The divisor of the remainder.
  - type: int | float | decimal
  - default: None

# calc.quo

Calculates the quotient (floored division) of two numbers.

Note that this function will always return an [integer](/docs/reference/foundations/int/), and will error if the resulting number is larger than the maximum 64-bit signed integer or smaller than the minimum for that type.

```typst
$ "quo"(a, b) &= floor(a/b) \
  "quo"(14, 5) &= #calc.quo(14, 5) \
  "quo"(3.46, 0.5) &= #calc.quo(3.46, 0.5) $
```

```typst
#calc.quo(
  dividend,
  divisor
) -> int
```

## Parameters

- dividend:
  - description: The dividend of the quotient.
  - type: int | float | decimal
  - default: None
- divisor:
  - description: The divisor of the quotient.
  - type: int | float | decimal
  - default: None

# calc.norm

Calculates the p-norm of a sequence of values.

```typst
#calc.norm(1, 2, -3, 0.5) \
#calc.norm(p: 3, 1, 2)
```

```typst
#calc.norm(
  p: float,
  values
) -> float
```

## Parameters

- p:
  - description: The p value to calculate the p-norm of.
  - type: float
  - default: 2.0
- values:
  - description: The sequence of values from which to calculate the p-norm. Returns `0.0` if empty.
  - type: float
  - default: None


