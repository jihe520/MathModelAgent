# String

A sequence of Unicode codepoints.

You can iterate over the grapheme clusters of the string using a [for loop](/docs/reference/scripting/#loops). Grapheme clusters are basically characters but keep together things that belong together, e.g. multiple codepoints that together form a flag emoji. Strings can be added with the `+` operator, [joined together](/docs/reference/scripting/#blocks) and multiplied with integers.

Typst provides utility methods for string manipulation. Many of these methods (e.g., [`split`](/docs/reference/foundations/str/#definitions-split), [`trim`](/docs/reference/foundations/str/#definitions-trim) and [`replace`](/docs/reference/foundations/str/#definitions-replace)) operate on _patterns:_ A pattern can be either a string or a [regular expression](/docs/reference/foundations/regex/). This makes the methods quite versatile.

All lengths and indices are expressed in terms of UTF-8 bytes. Indices are zero-based and negative indices wrap around to the end of the string.

You can convert a value to a string with this type's constructor.

## Example

```typst
#"hello world!" \
#"\"hello\n  world\"!" \
#"1 2 3".split() \
#"1,2;3".split(regex("[,;]")) \
#(regex("\\d+") in "ten euros") \
#(regex("\\d+") in "10 euros")
```

## Escape sequences

Just like in markup, you can escape a few symbols in strings:

- `\\` for a backslash
- `\"` for a quote
- `\n` for a newline
- `\r` for a carriage return
- `\t` for a tab
- `\u\{1f600\}` for a hexadecimal Unicode escape sequence

## Constructor
## str

Converts a value to a string.

- Integers are formatted in base 10. This can be overridden with the optional `base` parameter.
- Floats are formatted in base 10 and never in exponential notation.
- Negative integers and floats are formatted with the Unicode minus sign ("−" U+2212) instead of the ASCII minus sign ("-" U+002D).
- From labels the name is extracted.
- Bytes are decoded as UTF-8.

If you wish to convert from and to Unicode code points, see the [`to-unicode`](/docs/reference/foundations/str/#definitions-to-unicode) and [`from-unicode`](/docs/reference/foundations/str/#definitions-from-unicode) functions.

```typst
#str(10) \
#str(4000, base: 16) \
#str(2.7) \
#str(1e8) \
#str(<intro>)
```

```typst
#str(
  value,
  base: int
) -> str
```

### Parameters

- value:
  - description: The value that should be converted to a string.
  - type: int | float | str | bytes | label | decimal | version | type
  - default: None
- base:
  - description: The base (radix) to display integers in, between 2 and 36.
  - type: int
  - default: 10


## Methods

## str.len

The length of the string in UTF-8 encoded bytes.

## str.first

Extracts the first grapheme cluster of the string.

Returns the provided default value if the string is empty or fails with an error if no default value was specified.

```typst
#str.first(
  default: str
) -> str
```

### Parameters

- default:
  - description: A default value to return if the string is empty.
  - type: str
  - default: None

## str.last

Extracts the last grapheme cluster of the string.

Returns the provided default value if the string is empty or fails with an error if no default value was specified.

```typst
#str.last(
  default: str
) -> str
```

### Parameters

- default:
  - description: A default value to return if the string is empty.
  - type: str
  - default: None

## str.at

Extracts the first grapheme cluster after the specified index. Returns the default value if the index is out of bounds or fails with an error if no default value was specified.

```typst
#str.at(
  index,
  default: any
) -> any
```

### Parameters

- index:
  - description: The byte index. If negative, indexes from the back.
  - type: int
  - default: None
- default:
  - description: A default value to return if the index is out of bounds.
  - type: any
  - default: None

## str.slice

Extracts a substring of the string. Fails with an error if the start or end index is out of bounds.

```typst
#str.slice(
  start,
  end,
  count: int
) -> str
```

### Parameters

- start:
  - description: The start byte index (inclusive). If negative, indexes from the back.
  - type: int
  - default: None
- end:
  - description: The end byte index (exclusive). If omitted, the whole slice until the end of the string is extracted. If negative, indexes from the back.
  - type: none | int
  - default: none
- count:
  - description: The number of bytes to extract. This is equivalent to passing `start + count` as the `end` position. Mutually exclusive with `end`.
  - type: int
  - default: None

## str.clusters

Returns the grapheme clusters of the string as an array of substrings.

## str.codepoints

Returns the Unicode codepoints of the string as an array of substrings.

## str.to-unicode

Converts a character into its corresponding code point.

```typst
#"a".to-unicode() \
#("a\u{0300}"
   .codepoints()
   .map(str.to-unicode))
```

```typst
#str.to-unicode(
  character
) -> int
```

### Parameters

- character:
  - description: The character that should be converted.
  - type: str
  - default: None

## str.from-unicode

Converts a unicode code point into its corresponding string.

```typst
#str.from-unicode(97)
```

```typst
#str.from-unicode(
  value
) -> str
```

### Parameters

- value:
  - description: The code point that should be converted.
  - type: int
  - default: None

## str.normalize

Normalizes the string to the given Unicode normal form.

This is useful when manipulating strings containing Unicode combining characters.

```typst
#assert.eq("é".normalize(form: "nfd"), "e\u{0301}")
#assert.eq("ſ́".normalize(form: "nfkc"), "ś")
```

```typst
#str.normalize(
  form: str
) -> str
```

### Parameters

- form:
  - description: 
  - type: str
  - default: "nfc"

## str.contains

Whether the string contains the specified pattern.

This method also has dedicated syntax: You can write `"bc" in "abcd"` instead of `"abcd".contains("bc")`.

```typst
#str.contains(
  pattern
) -> bool
```

### Parameters

- pattern:
  - description: The pattern to search for.
  - type: str | regex
  - default: None

## str.starts-with

Whether the string starts with the specified pattern.

```typst
#str.starts-with(
  pattern
) -> bool
```

### Parameters

- pattern:
  - description: The pattern the string might start with.
  - type: str | regex
  - default: None

## str.ends-with

Whether the string ends with the specified pattern.

```typst
#str.ends-with(
  pattern
) -> bool
```

### Parameters

- pattern:
  - description: The pattern the string might end with.
  - type: str | regex
  - default: None

## str.find

Searches for the specified pattern in the string and returns the first match as a string or `none` if there is no match.

```typst
#str.find(
  pattern
) -> none str
```

### Parameters

- pattern:
  - description: The pattern to search for.
  - type: str | regex
  - default: None

## str.position

Searches for the specified pattern in the string and returns the index of the first match as an integer or `none` if there is no match.

```typst
#str.position(
  pattern
) -> none int
```

### Parameters

- pattern:
  - description: The pattern to search for.
  - type: str | regex
  - default: None

## str.match

Searches for the specified pattern in the string and returns a dictionary with details about the first match or `none` if there is no match.

The returned dictionary has the following keys:

- `start`: The start offset of the match
- `end`: The end offset of the match
- `text`: The text that matched.
- `captures`: An array containing a string for each matched capturing group. The first item of the array contains the first matched capturing, not the whole match! This is empty unless the `pattern` was a regex with capturing groups.

```typst
#let pat = regex("not (a|an) (apple|cat)")
#"I'm a doctor, not an apple.".match(pat) \
#"I am not a cat!".match(pat)
```

```typst
#assert.eq("Is there a".match("for this?"), none)
#"The time of my life.".match(regex("[mit]+e"))
```

```typst
#str.match(
  pattern
) -> none dictionary
```

### Parameters

- pattern:
  - description: The pattern to search for.
  - type: str | regex
  - default: None

## str.matches

Searches for the specified pattern in the string and returns an array of dictionaries with details about all matches. For details about the returned dictionaries, see [above](/docs/reference/foundations/str/#definitions-match).

```typst
#"Day by Day.".matches("Day")
```

```typst
#str.matches(
  pattern
) -> array
```

### Parameters

- pattern:
  - description: The pattern to search for.
  - type: str | regex
  - default: None

## str.replace

Replace at most `count` occurrences of the given pattern with a replacement string or function (beginning from the start). If no count is given, all occurrences are replaced.

```typst
#str.replace(
  pattern,
  replacement,
  count: int
) -> str
```

### Parameters

- pattern:
  - description: The pattern to search for.
  - type: str | regex
  - default: None
- replacement:
  - description: The string to replace the matches with or a function that gets a dictionary for each match and can return individual replacement strings. The dictionary passed to the function has the same shape as the dictionary returned by [`match`](/docs/reference/foundations/str/#definitions-match).
  - type: str | function
  - default: None
- count:
  - description: If given, only the first `count` matches of the pattern are placed.
  - type: int
  - default: None

## str.trim

Removes matches of a pattern from one or both sides of the string, once or repeatedly and returns the resulting string.

```typst
#str.trim(
  pattern,
  at: alignment,
  repeat: bool
) -> str
```

### Parameters

- pattern:
  - description: The pattern to search for. If `none`, trims white spaces.
  - type: none | str | regex
  - default: none
- at:
  - description: Can be `start` or `end` to only trim the start or end of the string. If omitted, both sides are trimmed.
  - type: alignment
  - default: None
- repeat:
  - description: Whether to repeatedly removes matches of the pattern or just once. Defaults to `true`.
  - type: bool
  - default: true

## str.split

Splits a string at matches of a specified pattern and returns an array of the resulting parts.

When the empty string is used as a separator, it separates every character (i.e., Unicode code point) in the string, along with the beginning and end of the string. In practice, this means that the resulting list of parts will contain the empty string at the start and end of the list.

```typst
#str.split(
  pattern
) -> array
```

### Parameters

- pattern:
  - description: The pattern to split at. Defaults to whitespace.
  - type: none | str | regex
  - default: none

## str.rev

Reverse the string.


