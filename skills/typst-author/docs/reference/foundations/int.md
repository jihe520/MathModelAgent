# Integer

A whole number.

The number can be negative, zero, or positive. As Typst uses 64 bits to store integers, integers cannot be smaller than `-9223372036854775808` or larger than `9223372036854775807`. Integer literals are always positive, so a negative integer such as `-1` is semantically the negation `-` of the positive literal `1`. A positive integer greater than the maximum value and a negative integer less than or equal to the minimum value cannot be represented as an integer literal, and are instead parsed as a `float`. The minimum integer value can still be obtained through integer arithmetic.

The number can also be specified as hexadecimal, octal, or binary by starting it with a zero followed by either `x`, `o`, or `b`.

You can convert a value to an integer with this type's constructor.

## Example

```typst
#(1 + 2) \
#(2 - 5) \
#(3 + 4 < 8)

#0xff \
#0o10 \
#0b1001
```

## Constructor
## int

Converts a value to an integer. Raises an error if there is an attempt to produce an integer larger than the maximum 64-bit signed integer or smaller than the minimum 64-bit signed integer.

- Booleans are converted to `0` or `1`.
- Floats and decimals are rounded to the next 64-bit integer towards zero.
- Strings are parsed in base 10.

```typst
#int(false) \
#int(true) \
#int(2.7) \
#int(decimal("3.8")) \
#(int("27") + int("4"))
```

```typst
#int(
  value
) -> int
```

### Parameters

- value:
  - description: The value that should be converted to an integer.
  - type: bool | int | float | str | decimal
  - default: None


## Methods

## int.signum

Calculates the sign of an integer.

- If the number is positive, returns `1`.
- If the number is negative, returns `-1`.
- If the number is zero, returns `0`.

```typst
#(5).signum() \
#(-5).signum() \
#(0).signum()
```

## int.bit-not

Calculates the bitwise NOT of an integer.

For the purposes of this function, the operand is treated as a signed integer of 64 bits.

```typst
#4.bit-not() \
#(-1).bit-not()
```

## int.bit-and

Calculates the bitwise AND between two integers.

For the purposes of this function, the operands are treated as signed integers of 64 bits.

```typst
#128.bit-and(192)
```

```typst
#int.bit-and(
  rhs
) -> int
```

### Parameters

- rhs:
  - description: The right-hand operand of the bitwise AND.
  - type: int
  - default: None

## int.bit-or

Calculates the bitwise OR between two integers.

For the purposes of this function, the operands are treated as signed integers of 64 bits.

```typst
#64.bit-or(32)
```

```typst
#int.bit-or(
  rhs
) -> int
```

### Parameters

- rhs:
  - description: The right-hand operand of the bitwise OR.
  - type: int
  - default: None

## int.bit-xor

Calculates the bitwise XOR between two integers.

For the purposes of this function, the operands are treated as signed integers of 64 bits.

```typst
#64.bit-xor(96)
```

```typst
#int.bit-xor(
  rhs
) -> int
```

### Parameters

- rhs:
  - description: The right-hand operand of the bitwise XOR.
  - type: int
  - default: None

## int.bit-lshift

Shifts the operand's bits to the left by the specified amount.

For the purposes of this function, the operand is treated as a signed integer of 64 bits. An error will occur if the result is too large to fit in a 64-bit integer.

```typst
#33.bit-lshift(2) \
#(-1).bit-lshift(3)
```

```typst
#int.bit-lshift(
  shift
) -> int
```

### Parameters

- shift:
  - description: The amount of bits to shift. Must not be negative.
  - type: int
  - default: None

## int.bit-rshift

Shifts the operand's bits to the right by the specified amount. Performs an arithmetic shift by default (extends the sign bit to the left, such that negative numbers stay negative), but that can be changed by the `logical` parameter.

For the purposes of this function, the operand is treated as a signed integer of 64 bits.

```typst
#64.bit-rshift(2) \
#(-8).bit-rshift(2) \
#(-8).bit-rshift(2, logical: true)
```

```typst
#int.bit-rshift(
  shift,
  logical: bool
) -> int
```

### Parameters

- shift:
  - description: The amount of bits to shift. Must not be negative. Shifts larger than 63 are allowed and will cause the return value to saturate. For non-negative numbers, the return value saturates at `0`, while, for negative numbers, it saturates at `-1` if `logical` is set to `false`, or `0` if it is `true`. This behavior is consistent with just applying this operation multiple times. Therefore, the shift will always succeed.
  - type: int
  - default: None
- logical:
  - description: Toggles whether a logical (unsigned) right shift should be performed instead of arithmetic right shift. If this is `true`, negative operands will not preserve their sign bit, and bits which appear to the left after the shift will be `0`. This parameter has no effect on non-negative operands.
  - type: bool
  - default: false

## int.from-bytes

Converts bytes to an integer.

```typst
#int.from-bytes(bytes((0, 0, 0, 0, 0, 0, 0, 1))) \
#int.from-bytes(bytes((1, 0, 0, 0, 0, 0, 0, 0)), endian: "big")
```

```typst
#int.from-bytes(
  bytes,
  endian: str,
  signed: bool
) -> int
```

### Parameters

- bytes:
  - description: The bytes that should be converted to an integer. Must be of length at most 8 so that the result fits into a 64-bit signed integer.
  - type: bytes
  - default: None
- endian:
  - description: The endianness of the conversion.
  - type: str
  - default: "little"
- signed:
  - description: Whether the bytes should be treated as a signed integer. If this is `true` and the most significant bit is set, the resulting number will negative.
  - type: bool
  - default: true

## int.to-bytes

Converts an integer to bytes.

```typst
#array(10000.to-bytes(endian: "big")) \
#array(10000.to-bytes(size: 4))
```

```typst
#int.to-bytes(
  endian: str,
  size: int
) -> bytes
```

### Parameters

- endian:
  - description: The endianness of the conversion.
  - type: str
  - default: "little"
- size:
  - description: The size in bytes of the resulting bytes (must be at least zero). If the integer is too large to fit in the specified size, the conversion will truncate the remaining bytes based on the endianness. To keep the same resulting value, if the endianness is big-endian, the truncation will happen at the rightmost bytes. Otherwise, if the endianness is little-endian, the truncation will happen at the leftmost bytes. Be aware that if the integer is negative and the size is not enough to make the number fit, when passing the resulting bytes to `int.from-bytes`, the resulting number might be positive, as the most significant bit might not be set to 1.
  - type: int
  - default: 8


