# Smartquote

# smartquote

A language-aware quote that reacts to its context.

Automatically turns into an appropriate opening or closing quote based on the active [text language](/docs/reference/text/text/#parameters-lang).

## Example

```typst
"This is in quotes."

#set text(lang: "de")
"Das ist in Anführungszeichen."

#set text(lang: "fr")
"C'est entre guillemets."
```

## Syntax

This function also has dedicated syntax: The normal quote characters (`'` and `"`). Typst automatically makes your quotes smart.

```typst
#smartquote(
  double: bool,
  enabled: bool,
  alternative: bool,
  quotes: auto | str | array | dictionary
) -> content
```

## Parameters

- double:
  - description: Whether this should be a double quote.
  - type: bool
  - default: true
- enabled:
  - description: Whether smart quotes are enabled. To disable smartness for a single quote, you can also escape it with a backslash. ```typst #set smartquote(enabled: false) These are "dumb" quotes. ```
  - type: bool
  - default: true
- alternative:
  - description: Whether to use alternative quotes. Does nothing for languages that don\'t have alternative quotes, or if explicit quotes were set. ```typst #set text(lang: "de") #set smartquote(alternative: true) "Das ist in anderen Anführungszeichen." ```
  - type: bool
  - default: false
- quotes:
  - description: The quotes to use. - When set to `auto`, the appropriate single quotes for the [text language](/docs/reference/text/text/#parameters-lang) will be used. This is the default. - Custom quotes can be passed as a string, array, or dictionary of either  - [string](/docs/reference/foundations/str/): a string consisting of two characters containing the opening and closing double quotes (characters here refer to Unicode grapheme clusters)  - [array](/docs/reference/foundations/array/): an array containing the opening and closing double quotes  - [dictionary](/docs/reference/foundations/dictionary/): a dictionary containing the double and single quotes, each specified as either `auto`, string, or array ```typst #set text(lang: "de") \'Das sind normale Anführungszeichen.\' #set smartquote(quotes: "()") "Das sind eigene Anführungszeichen." #set smartquote(quotes: (single: ("[[", "]]"), double: auto)) \'Das sind eigene Anführungszeichen.\' ```
  - type: auto | str | array | dictionary
  - default: auto


