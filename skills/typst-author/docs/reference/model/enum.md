# Numbered List

# enum

A numbered list.

Displays a sequence of items vertically and numbers them consecutively.

## Example

```typst
Automatically numbered:
+ Preparations
+ Analysis
+ Conclusions

Manually numbered:
2. What is the first step?
5. I am confused.
+  Moving on ...

Multiple lines:
+ This enum item has multiple
  lines because the next line
  is indented.

Function call.
#enum[First][Second]
```

You can easily switch all your enumerations to a different numbering style with a set rule.

```typst
#set enum(numbering: "a)")

+ Starting off ...
+ Don't forget step two
```

You can also use [`enum.item`](/docs/reference/model/enum/#definitions-item) to programmatically customize the number of each item in the enumeration:

```typst
#enum(
  enum.item(1)[First step],
  enum.item(5)[Fifth step],
  enum.item(10)[Tenth step]
)
```

## Syntax

This functions also has dedicated syntax:

- Starting a line with a plus sign creates an automatically numbered enumeration item.
- Starting a line with a number followed by a dot creates an explicitly numbered enumeration item.

Enumeration items can contain multiple paragraphs and other block-level content. All content that is indented more than an item's marker becomes part of that item.

```typst
#enum(
  tight: bool,
  numbering: str | function,
  start: auto | int,
  full: bool,
  reversed: bool,
  indent: length,
  body-indent: length,
  spacing: auto | length,
  number-align: alignment,
  children
) -> content
```

## Parameters

- tight:
  - description: Defines the default [spacing](/docs/reference/model/enum/#parameters-spacing) of the enumeration. If it is `false`, the items are spaced apart with [paragraph spacing](/docs/reference/model/par/#parameters-spacing). If it is `true`, they use [paragraph leading](/docs/reference/model/par/#parameters-leading) instead. This makes the list more compact, which can look better if the items are short. In markup mode, the value of this parameter is determined based on whether items are separated with a blank line. If items directly follow each other, this is set to `true`; if items are separated by a blank line, this is set to `false`. The markup-defined tightness cannot be overridden with set rules. ```typst + If an enum has a lot of text, and  maybe other inline content, it  should not be tight anymore. + To make an enum wide, simply  insert a blank line between the  items. ```
  - type: bool
  - default: true
- numbering:
  - description: How to number the enumeration. Accepts a [numbering pattern or function](/docs/reference/model/numbering/). If the numbering pattern contains multiple counting symbols, they apply to nested enums. If given a function, the function receives one argument if `full` is `false` and multiple arguments if `full` is `true`. ```typst #set enum(numbering: "1.a)") + Different + Numbering  + Nested  + Items + Style #set enum(numbering: n => super[#n]) + Superscript + Numbering! ```
  - type: str | function
  - default: "1."
- start:
  - description: Which number to start the enumeration with. ```typst #enum(  start: 3,  [Skipping],  [Ahead], ) ```
  - type: auto | int
  - default: auto
- full:
  - description: Whether to display the full numbering, including the numbers of all parent enumerations. ```typst #set enum(numbering: "1.a)", full: true) + Cook  + Heat water  + Add ingredients + Eat ```
  - type: bool
  - default: false
- reversed:
  - description: Whether to reverse the numbering for this enumeration. ```typst #set enum(reversed: true) + Coffee + Tea + Milk ```
  - type: bool
  - default: false
- indent:
  - description: The indentation of each item.
  - type: length
  - default: 0pt
- body-indent:
  - description: The space between the numbering and the body of each item.
  - type: length
  - default: 0.5em
- spacing:
  - description: The spacing between the items of the enumeration. If set to `auto`, uses paragraph [`leading`](/docs/reference/model/par/#parameters-leading) for tight enumerations and paragraph [`spacing`](/docs/reference/model/par/#parameters-spacing) for wide (non-tight) enumerations.
  - type: auto | length
  - default: auto
- number-align:
  - description: The alignment that enum numbers should have. By default, this is set to `end + top`, which aligns enum numbers towards end of the current text direction (in left-to-right script, for example, this is the same as `right`) and at the top of the line. The choice of `end` for horizontal alignment of enum numbers is usually preferred over `start`, as numbers then grow away from the text instead of towards it, avoiding certain visual issues. This option lets you override this behaviour, however. (Also to note is that the [unordered list](/docs/reference/model/list/) uses a different method for this, by giving the `marker` content an alignment directly.). ```typst #set enum(number-align: start + bottom) Here are some powers of two: 1. One 2. Two 4. Four 8. Eight 16. Sixteen 32. Thirty two ```
  - type: alignment
  - default: end + top
- children:
  - description: The numbered list\'s items. When using the enum syntax, adjacent items are automatically collected into enumerations, even through constructs like for loops. ```typst #for phase in (  "Launch",  "Orbit",  "Descent", ) [+ #phase] ```
  - type: content | array
  - default: None


## Definitions
### enum.item

An enumeration item.

```typst
#enum.item(
  number,
  body
) -> content
```

#### Parameters

- number:
  - description: The item\'s number.
  - type: auto | int
  - default: auto
- body:
  - description: The item\'s body.
  - type: content
  - default: None


