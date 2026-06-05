# Decimal

A fixed-point decimal number type.

This type should be used for precise arithmetic operations on numbers represented in base 10. A typical use case is representing currency.

## Example

```typst
Decimal: #(decimal("0.1") + decimal("0.2")) \
Float: #(0.1 + 0.2)
```

## Construction and casts

To create a decimal number, use the `decimal(string)` constructor, such as in `decimal("3.141592653")` **(note the double quotes!)**. This constructor preserves all given fractional digits, provided they are representable as per the limits specified below (otherwise, an error is raised).

You can also convert any [integer](/docs/reference/foundations/int/) to a decimal with the `decimal(int)` constructor, e.g. `decimal(59)`. However, note that constructing a decimal from a [floating-point number](/docs/reference/foundations/float/), while supported, **is an imprecise conversion and therefore discouraged.** A warning will be raised if Typst detects that there was an accidental `float` to `decimal` cast through its constructor, e.g. if writing `decimal(3.14)` (note the lack of double quotes, indicating this is an accidental `float` cast and therefore imprecise). It is recommended to use strings for constant decimal values instead (e.g. `decimal("3.14")`).

The precision of a `float` to `decimal` cast can be slightly improved by rounding the result to 15 digits with [`calc.round`](/docs/reference/foundations/calc/#functions-round), but there are still no precision guarantees for that kind of conversion.

## Operations

Basic arithmetic operations are supported on two decimals and on pairs of decimals and integers.

Built-in operations between `float` and `decimal` are not supported in order to guard against accidental loss of precision. They will raise an error instead.

Certain `calc` functions, such as trigonometric functions and power between two real numbers, are also only supported for `float` (although raising `decimal` to integer exponents is supported). You can opt into potentially imprecise operations with the `float(decimal)` constructor, which casts the `decimal` number into a `float`, allowing for operations without precision guarantees.

## Displaying decimals

To display a decimal, simply insert the value into the document. To only display a certain number of digits, [round](/docs/reference/foundations/calc/#functions-round) the decimal first. Localized formatting of decimals and other numbers is not yet supported, but planned for the future.

You can convert decimals to strings using the [`str`](/docs/reference/foundations/str/) constructor. This way, you can post-process the displayed representation, e.g. to replace the period with a comma (as a stand-in for proper built-in localization to languages that use the comma).

## Precision and limits

A `decimal` number has a limit of 28 to 29 significant base-10 digits. This includes the sum of digits before and after the decimal point. As such, numbers with more fractional digits have a smaller range. The maximum and minimum `decimal` numbers have a value of `79228162514264337593543950335` and `-79228162514264337593543950335` respectively. In contrast with [`float`](/docs/reference/foundations/float/), this type does not support infinity or NaN, so overflowing or underflowing operations will raise an error.

Typical operations between `decimal` numbers, such as addition, multiplication, and [power](/docs/reference/foundations/calc/#functions-pow) to an integer, will be highly precise due to their fixed-point representation. Note, however, that multiplication and division may not preserve all digits in some edge cases: while they are considered precise, digits past the limits specified above are rounded off and lost, so some loss of precision beyond the maximum representable digits is possible. Note that this behavior can be observed not only when dividing, but also when multiplying by numbers between 0 and 1, as both operations can push a number's fractional digits beyond the limits described above, leading to rounding. When those two operations do not surpass the digit limits, they are fully precise.

## Constructor
## decimal

Converts a value to a `decimal`.

It is recommended to use a string to construct the decimal number, or an [integer](/docs/reference/foundations/int/) (if desired). The string must contain a number in the format `"3.14159"` (or `"-3.141519"` for negative numbers). The fractional digits are fully preserved; if that's not possible due to the limit of significant digits (around 28 to 29) having been reached, an error is raised as the given decimal number wouldn't be representable.

While this constructor can be used with [floating-point numbers](/docs/reference/foundations/float/) to cast them to `decimal`, doing so is **discouraged** as **this cast is
inherently imprecise.** It is easy to accidentally perform this cast by writing `decimal(1.234)` (note the lack of double quotes), which is why Typst will emit a warning in that case. Please write `decimal("1.234")` instead for that particular case (initialization of a constant decimal). Also note that floats that are NaN or infinite cannot be cast to decimals and will raise an error.

```typst
#decimal("1.222222222222222")
```

```typst
#decimal(
  value
) -> decimal
```

### Parameters

- value:
  - description: The value that should be converted to a decimal.
  - type: bool | int | float | str | decimal
  - default: None


