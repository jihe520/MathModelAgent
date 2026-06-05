# Relative Length

A length in relation to some known length.

This type is a combination of a [length](/docs/reference/layout/length/) with a [ratio](/docs/reference/layout/ratio/). It results from addition and subtraction of a length and a ratio. Wherever a relative length is expected, you can also use a bare length or ratio.

## Relative to the page

A common use case is setting the width or height of a layout element (e.g., [block](/docs/reference/layout/block/), [rect](/docs/reference/visualize/rect/), etc.) as a certain percentage of the width of the page. Here, the rectangle's width is set to `25%`, so it takes up one fourth of the page's _inner_ width (the width minus margins).

```typst
#rect(width: 25%)
```

Bare lengths or ratios are always valid where relative lengths are expected, but the two can also be freely mixed:

```typst
#rect(width: 25% + 1cm)
```

If you're trying to size an element so that it takes up the page's _full_ width, you have a few options (this highly depends on your exact use case):

1. Set page margins to `0pt` (`#set page(margin: 0pt)`)
2. Multiply the ratio by the known full page width (`21cm * 69%`)
3. Use padding which will negate the margins (`#pad(x: -2.5cm, ...)`)
4. Use the page [background](/docs/reference/layout/page/#parameters-background) or [foreground](/docs/reference/layout/page/#parameters-foreground) field as those don't take margins into account (note that it will render the content outside of the document flow, see [place](/docs/reference/layout/place/) to control the content position)

## Relative to a container

When a layout element (e.g. a [rect](/docs/reference/visualize/rect/)) is nested in another layout container (e.g. a [block](/docs/reference/layout/block/)) instead of being a direct descendant of the page, relative widths become relative to the container:

```typst
#block(
  width: 100pt,
  fill: aqua,
  rect(width: 50%),
)
```

## Scripting

You can multiply relative lengths by [ratios](/docs/reference/layout/ratio/), [integers](/docs/reference/foundations/int/), and [floats](/docs/reference/foundations/float/).

A relative length has the following fields:

- `length`: Its [length](/docs/reference/layout/length/) component.
- `ratio`: Its [ratio](/docs/reference/layout/ratio/) component.

```typst
#(100% - 50pt).length \
#(100% - 50pt).ratio
```


