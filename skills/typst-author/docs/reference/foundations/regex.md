# Regex

A regular expression.

Can be used as a [show rule selector](/docs/reference/styling/#show-rules) and with [string methods](/docs/reference/foundations/str/) like `find`, `split`, and `replace`.

[See here](https://docs.rs/regex/latest/regex/#syntax) for a specification of the supported syntax.

## Example

```typst
// Works with string methods.
#"a,b;c".split(regex("[,;]"))

// Works with show rules.
#show regex("\\d+"): set text(red)

The numbers 1 to 10.
```

## Constructor
## regex

Create a regular expression from a string.

```typst
#regex(
  regex
) -> regex
```

### Parameters

- regex:
  - description: The regular expression as a string. Both Typst strings and regular expressions use backslashes for escaping. To produce a regex escape sequence that is also valid in Typst, you need to escape the backslash itself (e.g., writing `regex("\\\\\\\\")` for the regex `\\\\`). Regex escape sequences that are not valid Typst escape sequences (e.g., `\\d` and `\\b`) can be entered into strings directly, but it\'s good practice to still escape them to avoid ambiguity (i.e., `regex("\\\\b\\\\d")`). See the [list of valid string escape sequences](/docs/reference/foundations/str/#escapes). If you need many escape sequences, you can also create a raw element and extract its text to use it for your regular expressions: `regex(`\\d+\\.\\d+\\.\\d+`.text)`.
  - type: str
  - default: None


