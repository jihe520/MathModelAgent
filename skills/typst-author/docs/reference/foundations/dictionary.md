# Dictionary

A map from string keys to values.

You can construct a dictionary by enclosing comma-separated `key: value` pairs in parentheses. The values do not have to be of the same type. Since empty parentheses already yield an empty array, you have to use the special `(:)` syntax to create an empty dictionary.

A dictionary is conceptually similar to an [array](/docs/reference/foundations/array/), but it is indexed by strings instead of integers. You can access and create dictionary entries with the `.at()` method. If you know the key statically, you can alternatively use [field access notation](/docs/reference/scripting/#fields) (`.key`) to access the value. To check whether a key is present in the dictionary, use the `in` keyword.

You can iterate over the pairs in a dictionary using a [for loop](/docs/reference/scripting/#loops). This will iterate in the order the pairs were inserted / declared initially.

Dictionaries can be added with the `+` operator and [joined together](/docs/reference/scripting/#blocks). They can also be [spread](/docs/reference/foundations/arguments/#spreading) into a function call or another dictionary[1](#1) with the `..spread` operator. In each case, if a key appears multiple times, the last value will override the others.

## Example

```typst
#let dict = (
  name: "Typst",
  born: 2019,
)

#dict.name \
#(dict.launch = 20)
#dict.len() \
#dict.keys() \
#dict.values() \
#dict.at("born") \
#dict.insert("city", "Berlin")
#("name" in dict)
```

[^1]: When spreading into a dictionary, if all items between the parentheses are spread, you have to use the special `(:..spread)` syntax. Otherwise, it will spread into an array.

## Constructor
## dictionary

Converts a value into a dictionary.

Note that this function is only intended for conversion of a dictionary-like value to a dictionary, not for creation of a dictionary from individual pairs. Use the dictionary syntax `(key: value)` instead.

```typst
#dictionary(sys).at("version")
```

```typst
#dictionary(
  value
) -> dictionary
```

### Parameters

- value:
  - description: The value that should be converted to a dictionary.
  - type: module
  - default: None


## Methods

## dictionary.len

The number of pairs in the dictionary.

## dictionary.at

Returns the value associated with the specified key in the dictionary. May be used on the left-hand side of an assignment if the key is already present in the dictionary. Returns the default value if the key is not part of the dictionary or fails with an error if no default value was specified.

```typst
#dictionary.at(
  key,
  default: any
) -> any
```

### Parameters

- key:
  - description: The key at which to retrieve the item.
  - type: str
  - default: None
- default:
  - description: A default value to return if the key is not part of the dictionary.
  - type: any
  - default: None

## dictionary.insert

Inserts a new pair into the dictionary. If the dictionary already contains this key, the value is updated.

To insert multiple pairs at once, you can just alternatively another dictionary with the `+=` operator.

```typst
#dictionary.insert(
  key,
  value
) -> 
```

### Parameters

- key:
  - description: The key of the pair that should be inserted.
  - type: str
  - default: None
- value:
  - description: The value of the pair that should be inserted.
  - type: any
  - default: None

## dictionary.remove

Removes a pair from the dictionary by key and return the value.

```typst
#dictionary.remove(
  key,
  default: any
) -> any
```

### Parameters

- key:
  - description: The key of the pair to remove.
  - type: str
  - default: None
- default:
  - description: A default value to return if the key does not exist.
  - type: any
  - default: None

## dictionary.keys

Returns the keys of the dictionary as an array in insertion order.

## dictionary.values

Returns the values of the dictionary as an array in insertion order.

## dictionary.pairs

Returns the keys and values of the dictionary as an array of pairs. Each pair is represented as an array of length two.


