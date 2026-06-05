# Numbering

# numbering

Applies a numbering to a sequence of numbers.

A numbering defines how a sequence of numbers should be displayed as content. It is defined either through a pattern string or an arbitrary function.

A numbering pattern consists of counting symbols, for which the actual number is substituted, their prefixes, and one suffix. The prefixes and the suffix are displayed as-is.

## Example

```typst
#numbering("1.1)", 1, 2, 3) \
#numbering("1.a.i", 1, 2) \
#numbering("I – 1", 12, 2) \
#numbering(
  (..nums) => nums
    .pos()
    .map(str)
    .join(".") + ")",
  1, 2, 3,
)
```

## Numbering patterns and numbering functions

There are multiple instances where you can provide a numbering pattern or function in Typst. For example, when defining how to number [headings](/docs/reference/model/heading/) or [figures](/docs/reference/model/figure/). Every time, the expected format is the same as the one described below for the [`numbering`](/docs/reference/model/numbering/#parameters-numbering) parameter.

The following example illustrates that a numbering function is just a regular [function](/docs/reference/foundations/function/) that accepts numbers and returns [`content`](/docs/reference/foundations/content/).

```typst
#let unary(.., last) = "|" * last
#set heading(numbering: unary)
= First heading
= Second heading
= Third heading
```

```typst
#numbering(
  numbering,
  numbers
) -> any
```

## Parameters

- numbering:
  - description: Defines how the numbering works. **Counting symbols** are `1`, `a`, `A`, `i`, `I`, `α`, `Α`, `一`, `壹`, `あ`, `い`, `ア`, `イ`, `א`, `가`, `ㄱ`, `*`, `١`, `۱`, `१`, `১`, `ক`, `①`, and `⓵`. They are replaced by the number in the sequence, preserving the original case. The `*` character means that symbols should be used to count, in the order of `*`, `†`, `‡`, `§`, `¶`, `‖`. If there are more than six items, the number is represented using repeated symbols. **Suffixes** are all characters after the last counting symbol. They are displayed as-is at the end of any rendered number. **Prefixes** are all characters that are neither counting symbols nor suffixes. They are displayed as-is at in front of their rendered equivalent of their counting symbol. This parameter can also be an arbitrary function that gets each number as an individual argument. When given a function, the `numbering` function just forwards the arguments to that function. While this is not particularly useful in itself, it means that you can just give arbitrary numberings to the `numbering` function without caring whether they are defined as a pattern or function.
  - type: str | function
  - default: None
- numbers:
  - description: The numbers to apply the numbering to. Must be non-negative. In general, numbers are counted from one. A number of zero indicates that the first element has not yet appeared. If `numbering` is a pattern and more numbers than counting symbols are given, the last counting symbol with its prefix is repeated.
  - type: int
  - default: None


