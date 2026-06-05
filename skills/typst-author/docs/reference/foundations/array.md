# Array

A sequence of values.

You can construct an array by enclosing a comma-separated sequence of values in parentheses. The values do not have to be of the same type.

You can access and update array items with the `.at()` method. Indices are zero-based and negative indices wrap around to the end of the array. You can iterate over an array using a [for loop](/docs/reference/scripting/#loops). Arrays can be added together with the `+` operator, [joined together](/docs/reference/scripting/#blocks) and multiplied with integers.

**Note:** An array of length one needs a trailing comma, as in `(1,)`. This is to disambiguate from a simple parenthesized expressions like `(1 + 2) * 3`. An empty array is written as `()`.

## Example

```typst
#let values = (1, 7, 4, -3, 2)

#values.at(0) \
#(values.at(0) = 3)
#values.at(-1) \
#values.find(calc.even) \
#values.filter(calc.odd) \
#values.map(calc.abs) \
#values.rev() \
#(1, (2, 3)).flatten() \
#(("A", "B", "C")
    .join(", ", last: " and "))
```

## Constructor
## array

Converts a value to an array.

Note that this function is only intended for conversion of a collection-like value to an array, not for creation of an array from individual items. Use the array syntax `(1, 2, 3)` (or `(1,)` for a single-element array) instead.

```typst
#let hi = "Hello 😃"
#array(bytes(hi))
```

```typst
#array(
  value
) -> array
```

### Parameters

- value:
  - description: The value that should be converted to an array.
  - type: bytes | array | version
  - default: None


## Methods

## array.len

The number of values in the array.

## array.first

Returns the first item in the array. May be used on the left-hand side an assignment. Returns the default value if the array is empty or fails with an error is no default value was specified.

```typst
#array.first(
  default: any
) -> any
```

### Parameters

- default:
  - description: A default value to return if the array is empty.
  - type: any
  - default: None

## array.last

Returns the last item in the array. May be used on the left-hand side of an assignment. Returns the default value if the array is empty or fails with an error is no default value was specified.

```typst
#array.last(
  default: any
) -> any
```

### Parameters

- default:
  - description: A default value to return if the array is empty.
  - type: any
  - default: None

## array.at

Returns the item at the specified index in the array. May be used on the left-hand side of an assignment. Returns the default value if the index is out of bounds or fails with an error if no default value was specified.

```typst
#array.at(
  index,
  default: any
) -> any
```

### Parameters

- index:
  - description: The index at which to retrieve the item. If negative, indexes from the back.
  - type: int
  - default: None
- default:
  - description: A default value to return if the index is out of bounds.
  - type: any
  - default: None

## array.push

Adds a value to the end of the array.

```typst
#array.push(
  value
) -> 
```

### Parameters

- value:
  - description: The value to insert at the end of the array.
  - type: any
  - default: None

## array.pop

Removes the last item from the array and returns it. Fails with an error if the array is empty.

## array.insert

Inserts a value into the array at the specified index, shifting all subsequent elements to the right. Fails with an error if the index is out of bounds.

To replace an element of an array, use [`at`](/docs/reference/foundations/array/#definitions-at).

```typst
#array.insert(
  index,
  value
) -> 
```

### Parameters

- index:
  - description: The index at which to insert the item. If negative, indexes from the back.
  - type: int
  - default: None
- value:
  - description: The value to insert into the array.
  - type: any
  - default: None

## array.remove

Removes the value at the specified index from the array and return it.

```typst
#array.remove(
  index,
  default: any
) -> any
```

### Parameters

- index:
  - description: The index at which to remove the item. If negative, indexes from the back.
  - type: int
  - default: None
- default:
  - description: A default value to return if the index is out of bounds.
  - type: any
  - default: None

## array.slice

Extracts a subslice of the array. Fails with an error if the start or end index is out of bounds.

```typst
#array.slice(
  start,
  end,
  count: int
) -> array
```

### Parameters

- start:
  - description: The start index (inclusive). If negative, indexes from the back.
  - type: int
  - default: None
- end:
  - description: The end index (exclusive). If omitted, the whole slice until the end of the array is extracted. If negative, indexes from the back.
  - type: none | int
  - default: none
- count:
  - description: The number of items to extract. This is equivalent to passing `start + count` as the `end` position. Mutually exclusive with `end`.
  - type: int
  - default: None

## array.contains

Whether the array contains the specified value.

This method also has dedicated syntax: You can write `2 in (1, 2, 3)` instead of `(1, 2, 3).contains(2)`.

```typst
#array.contains(
  value
) -> bool
```

### Parameters

- value:
  - description: The value to search for.
  - type: any
  - default: None

## array.find

Searches for an item for which the given function returns `true` and returns the first match or `none` if there is no match.

```typst
#array.find(
  searcher
) -> any none
```

### Parameters

- searcher:
  - description: The function to apply to each item. Must return a boolean.
  - type: function
  - default: None

## array.position

Searches for an item for which the given function returns `true` and returns the index of the first match or `none` if there is no match.

```typst
#array.position(
  searcher
) -> none int
```

### Parameters

- searcher:
  - description: The function to apply to each item. Must return a boolean.
  - type: function
  - default: None

## array.range

Create an array consisting of a sequence of numbers.

If you pass just one positional parameter, it is interpreted as the `end` of the range. If you pass two, they describe the `start` and `end` of the range.

This function is available both in the array function's scope and globally.

```typst
#range(5) \
#range(2, 5) \
#range(20, step: 4) \
#range(21, step: 4) \
#range(5, 2, step: -1)
```

```typst
#array.range(
  start,
  end,
  step: int
) -> array
```

### Parameters

- start:
  - description: The start of the range (inclusive).
  - type: int
  - default: 0
- end:
  - description: The end of the range (exclusive).
  - type: int
  - default: None
- step:
  - description: The distance between the generated numbers.
  - type: int
  - default: 1

## array.filter

Produces a new array with only the items from the original one for which the given function returns true.

```typst
#array.filter(
  test
) -> array
```

### Parameters

- test:
  - description: The function to apply to each item. Must return a boolean.
  - type: function
  - default: None

## array.map

Produces a new array in which all items from the original one were transformed with the given function.

```typst
#array.map(
  mapper
) -> array
```

### Parameters

- mapper:
  - description: The function to apply to each item.
  - type: function
  - default: None

## array.enumerate

Returns a new array with the values alongside their indices.

The returned array consists of `(index, value)` pairs in the form of length-2 arrays. These can be [destructured](/docs/reference/scripting/#bindings) with a let binding or for loop.

```typst
#for (i, value) in ("A", "B", "C").enumerate() {
  [#i: #value \ ]
}

#("A", "B", "C").enumerate(start: 1)
```

```typst
#array.enumerate(
  start: int
) -> array
```

### Parameters

- start:
  - description: The index returned for the first pair of the returned list.
  - type: int
  - default: 0

## array.zip

Zips the array with other arrays.

Returns an array of arrays, where the `i`th inner array contains all the `i`th elements from each original array.

If the arrays to be zipped have different lengths, they are zipped up to the last element of the shortest array and all remaining elements are ignored.

This function is variadic, meaning that you can zip multiple arrays together at once: `(1, 2).zip(("A", "B"), (10, 20))` yields `((1, "A", 10), (2, "B", 20))`.

```typst
#array.zip(
  exact: bool,
  others
) -> array
```

### Parameters

- exact:
  - description: Whether all arrays have to have the same length. For example, `(1, 2).zip((1, 2, 3), exact: true)` produces an error.
  - type: bool
  - default: false
- others:
  - description: The arrays to zip with.
  - type: array
  - default: None

## array.fold

Folds all items into a single value using an accumulator function.

```typst
#let array = (1, 2, 3, 4)
#array.fold(0, (acc, x) => acc + x)
```

```typst
#array.fold(
  init,
  folder
) -> any
```

### Parameters

- init:
  - description: The initial value to start with.
  - type: any
  - default: None
- folder:
  - description: The folding function. Must have two parameters: One for the accumulated value and one for an item.
  - type: function
  - default: None

## array.sum

Sums all items (works for all types that can be added).

```typst
#array.sum(
  default: any
) -> any
```

### Parameters

- default:
  - description: What to return if the array is empty. Must be set if the array can be empty.
  - type: any
  - default: None

## array.product

Calculates the product of all items (works for all types that can be multiplied).

```typst
#array.product(
  default: any
) -> any
```

### Parameters

- default:
  - description: What to return if the array is empty. Must be set if the array can be empty.
  - type: any
  - default: None

## array.any

Whether the given function returns `true` for any item in the array.

```typst
#array.any(
  test
) -> bool
```

### Parameters

- test:
  - description: The function to apply to each item. Must return a boolean.
  - type: function
  - default: None

## array.all

Whether the given function returns `true` for all items in the array.

```typst
#array.all(
  test
) -> bool
```

### Parameters

- test:
  - description: The function to apply to each item. Must return a boolean.
  - type: function
  - default: None

## array.flatten

Combine all nested arrays into a single flat one.

## array.rev

Return a new array with the same items, but in reverse order.

## array.split

Split the array at occurrences of the specified value.

```typst
#(1, 1, 2, 3, 2, 4, 5).split(2)
```

```typst
#array.split(
  at
) -> array
```

### Parameters

- at:
  - description: The value to split at.
  - type: any
  - default: None

## array.join

Combine all items in the array into one.

```typst
#array.join(
  separator,
  last: any,
  default: any | none
) -> any
```

### Parameters

- separator:
  - description: A value to insert between each item of the array.
  - type: any | none
  - default: none
- last:
  - description: An alternative separator between the last two items.
  - type: any
  - default: None
- default:
  - description: What to return if the array is empty.
  - type: any | none
  - default: none

## array.intersperse

Returns an array with a copy of the separator value placed between adjacent elements.

```typst
#("A", "B", "C").intersperse("-")
```

```typst
#array.intersperse(
  separator
) -> array
```

### Parameters

- separator:
  - description: The value that will be placed between each adjacent element.
  - type: any
  - default: None

## array.chunks

Splits an array into non-overlapping chunks, starting at the beginning, ending with a single remainder chunk.

All chunks but the last have `chunk-size` elements. If `exact` is set to `true`, the remainder is dropped if it contains less than `chunk-size` elements.

```typst
#let array = (1, 2, 3, 4, 5, 6, 7, 8)
#array.chunks(3) \
#array.chunks(3, exact: true)
```

```typst
#array.chunks(
  chunk-size,
  exact: bool
) -> array
```

### Parameters

- chunk-size:
  - description: How many elements each chunk may at most contain.
  - type: int
  - default: None
- exact:
  - description: Whether to keep the remainder if its size is less than `chunk-size`.
  - type: bool
  - default: false

## array.windows

Returns sliding windows of `window-size` elements over an array.

If the array length is less than `window-size`, this will return an empty array.

```typst
#let array = (1, 2, 3, 4, 5, 6, 7, 8)
#array.windows(5)
```

```typst
#array.windows(
  window-size
) -> array
```

### Parameters

- window-size:
  - description: How many elements each window will contain.
  - type: int
  - default: None

## array.sorted

Return a sorted version of this array, optionally by a given key function. The sorting algorithm used is stable.

Returns an error if a pair of values selected for comparison could not be compared, or if the key or comparison function (if given) yield an error.

To sort according to multiple criteria at once, e.g. in case of equality between some criteria, the key function can return an array. The results are in lexicographic order.

```typst
#let array = (
  (a: 2, b: 4),
  (a: 1, b: 5),
  (a: 2, b: 3),
)
#array.sorted(key: it => (it.a, it.b))
```

```typst
#array.sorted(
  key: function,
  by: function
) -> array
```

### Parameters

- key:
  - description: If given, applies this function to each element in the array to determine the keys to sort by.
  - type: function
  - default: None
- by:
  - description: If given, uses this function to compare every two elements in the array. The function will receive two elements in the array for comparison, and should return a boolean indicating their order: `true` indicates that the elements are in order, while `false` indicates that they should be swapped. To keep the sort stable, if the two elements are equal, the function should return `true`. If this function does not order the elements properly (e.g., by returning `false` for both `(x, y)` and `(y, x)`, or for `(x, x)`), the resulting array will be in unspecified order. When used together with `key`, `by` will be passed the keys instead of the elements. ```typst #(  "sorted",  "by",  "decreasing",  "length", ).sorted(  key: s => s.len(),  by: (l, r) => l >= r, ) ```
  - type: function
  - default: None

## array.dedup

Deduplicates all items in the array.

Returns a new array with all duplicate items removed. Only the first element of each duplicate is kept.

```typst
#(3, 3, 1, 2, 3).dedup()
```

```typst
#array.dedup(
  key: function
) -> array
```

### Parameters

- key:
  - description: If given, applies this function to each element in the array to determine the keys to deduplicate by. ```typst #("apple", "banana", " apple ").dedup(key: s => s.trim()) ```
  - type: function
  - default: None

## array.to-dict

Converts an array of pairs into a dictionary. The first value of each pair is the key, the second the value.

If the same key occurs multiple times, the last value is selected.

```typst
#(
  ("apples", 2),
  ("peaches", 3),
  ("apples", 5),
).to-dict()
```

## array.reduce

Reduces the elements to a single one, by repeatedly applying a reducing operation.

If the array is empty, returns `none`, otherwise, returns the result of the reduction.

The reducing function is a closure with two arguments: an "accumulator", and an element.

For arrays with at least one element, this is the same as [`array.fold`](/docs/reference/foundations/array/#definitions-fold) with the first element of the array as the initial accumulator value, folding every subsequent element into it.

```typst
#let array = (2, 1, 4, 3)
#array.reduce((acc, x) => calc.max(acc, x))
```

```typst
#array.reduce(
  reducer
) -> any
```

### Parameters

- reducer:
  - description: The reducing function. Must have two parameters: One for the accumulated value and one for an item.
  - type: function
  - default: None


