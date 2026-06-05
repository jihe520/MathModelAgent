# Standard Library

A module that contains all globally accessible items.

## Using "shadowed" definitions

The `std` module is useful whenever you overrode a name from the global scope (this is called _shadowing_). For instance, you might have used the name `text` for a parameter. To still access the `text` element, write `std.text`.

```typst
#let par = [My special paragraph.]
#let special(text) = {
  set std.text(style: "italic")
  set std.par.line(numbering: "1")
  text
}

#special(par)

#lorem(10)
```

## Conditional access

You can also use this in combination with the [dictionary constructor](/docs/reference/foundations/dictionary/) to conditionally access global definitions. This can, for instance, be useful to use new or experimental functionality when it is available, while falling back to an alternative implementation if used on an older Typst version. In particular, this allows us to create [polyfills](https://en.wikipedia.org/wiki/Polyfill_(programming)).

This can be as simple as creating an alias to prevent warning messages, for example, conditionally using `pattern` in Typst version 0.12, but using [`tiling`](/docs/reference/visualize/tiling/) in newer versions. Since the parameters accepted by the `tiling` function match those of the older `pattern` function, using the `tiling` function when available and falling back to `pattern` otherwise will unify the usage across all versions. Note that, when creating a polyfill, [`sys.version`](/docs/reference/foundations/sys/) can also be very useful.

```typst
#let tiling = if "tiling" in std { tiling } else { pattern }

...
```


