# Content

A piece of document content.

This type is at the heart of Typst. All markup you write and most [functions](/docs/reference/foundations/function/) you call produce content values. You can create a content value by enclosing markup in square brackets. This is also how you pass content to functions.

## Example

```typst
Type of *Hello!* is
#type([*Hello!*])
```

Content can be added with the `+` operator, [joined together](/docs/reference/scripting/#blocks) and multiplied with integers. Wherever content is expected, you can also pass a [string](/docs/reference/foundations/str/) or `none`.

## Representation

Content consists of elements with fields. When constructing an element with its _element function,_ you provide these fields as arguments and when you have a content value, you can access its fields with [field access syntax](/docs/reference/scripting/#field-access).

Some fields are required: These must be provided when constructing an element and as a consequence, they are always available through field access on content of that type. Required fields are marked as such in the documentation.

Most fields are optional: Like required fields, they can be passed to the element function to configure them for a single element. However, these can also be configured with [set rules](/docs/reference/styling/#set-rules) to apply them to all elements within a scope. Optional fields are only available with field access syntax when they were explicitly passed to the element function, not when they result from a set rule.

Each element has a default appearance. However, you can also completely customize its appearance with a [show rule](/docs/reference/styling/#show-rules). The show rule is passed the element. It can access the element's field and produce arbitrary content from it.

In the web app, you can hover over a content variable to see exactly which elements the content is composed of and what fields they have. Alternatively, you can inspect the output of the [`repr`](/docs/reference/foundations/repr/) function.


## Methods

## content.func

The content's element function. This function can be used to create the element contained in this content. It can be used in set and show rules for the element. Can be compared with global functions to check whether you have a specific kind of element.

## content.has

Whether the content has the specified field.

```typst
#content.has(
  field
) -> bool
```

### Parameters

- field:
  - description: The field to look for.
  - type: str
  - default: None

## content.at

Access the specified field on the content. Returns the default value if the field does not exist or fails with an error if no default value was specified.

```typst
#content.at(
  field,
  default: any
) -> any
```

### Parameters

- field:
  - description: The field to access.
  - type: str
  - default: None
- default:
  - description: A default value to return if the field does not exist.
  - type: any
  - default: None

## content.fields

Returns the fields of this content.

```typst
#rect(
  width: 10cm,
  height: 10cm,
).fields()
```

## content.location

The location of the content. This is only available on content returned by [query](/docs/reference/introspection/query/) or provided by a [show rule](/docs/reference/styling/#show-rules), for other content it will be `none`. The resulting location can be used with [counters](/docs/reference/introspection/counter/), [state](/docs/reference/introspection/state/) and [queries](/docs/reference/introspection/query/).


