# Selector

A filter for selecting elements within the document.

To construct a selector you can:

- use an [element function](/docs/reference/foundations/function/#element-functions)
- filter for an element function with [specific fields](/docs/reference/foundations/function/#definitions-where)
- use a [string](/docs/reference/foundations/str/) or [regular expression](/docs/reference/foundations/regex/)
- use a [`<label>`](/docs/reference/foundations/label/)
- use a [`location`](/docs/reference/introspection/location/)
- call the [`selector`](/docs/reference/foundations/selector/) constructor to convert any of the above types into a selector value and use the methods below to refine it

Selectors are used to [apply styling rules](/docs/reference/styling/#show-rules) to elements. You can also use selectors to [query](/docs/reference/introspection/query/) the document for certain types of elements.

Furthermore, you can pass a selector to several of Typst's built-in functions to configure their behaviour. One such example is the [outline](/docs/reference/model/outline/) where it can be used to change which elements are listed within the outline.

Multiple selectors can be combined using the methods shown below. However, not all kinds of selectors are supported in all places, at the moment.

## Example

```typst
#context query(
  heading.where(level: 1)
    .or(heading.where(level: 2))
)

= This will be found
== So will this
=== But this will not.
```

## Constructor
## selector

Turns a value into a selector. The following values are accepted:

- An element function like a `heading` or `figure`.
- A [string](/docs/reference/foundations/str/) or [regular expression](/docs/reference/foundations/regex/).
- A `<label>`.
- A [`location`](/docs/reference/introspection/location/).
- A more complex selector like `heading.where(level: 1)`.

```typst
#selector(
  target
) -> selector
```

### Parameters

- target:
  - description: Can be an element function like a `heading` or `figure`, a `<label>` or a more complex selector like `heading.where(level: 1)`.
  - type: str | regex | label | selector | location | function
  - default: None


## Methods

## selector.or

Selects all elements that match this or any of the other selectors.

```typst
#selector.or(
  others
) -> selector
```

### Parameters

- others:
  - description: The other selectors to match on.
  - type: str | regex | label | selector | location | function
  - default: None

## selector.and

Selects all elements that match this and all of the other selectors.

```typst
#selector.and(
  others
) -> selector
```

### Parameters

- others:
  - description: The other selectors to match on.
  - type: str | regex | label | selector | location | function
  - default: None

## selector.before

Returns a modified selector that will only match elements that occur before the first match of `end`.

```typst
#selector.before(
  end,
  inclusive: bool
) -> selector
```

### Parameters

- end:
  - description: The original selection will end at the first match of `end`.
  - type: label | selector | location | function
  - default: None
- inclusive:
  - description: Whether `end` itself should match or not. This is only relevant if both selectors match the same type of element. Defaults to `true`.
  - type: bool
  - default: true

## selector.after

Returns a modified selector that will only match elements that occur after the first match of `start`.

```typst
#selector.after(
  start,
  inclusive: bool
) -> selector
```

### Parameters

- start:
  - description: The original selection will start at the first match of `start`.
  - type: label | selector | location | function
  - default: None
- inclusive:
  - description: Whether `start` itself should match or not. This is only relevant if both selectors match the same type of element. Defaults to `true`.
  - type: bool
  - default: true


