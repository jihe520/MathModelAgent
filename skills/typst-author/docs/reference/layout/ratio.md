# Ratio

A ratio of a whole.

A ratio is written as a number, followed by a percent sign. Ratios most often appear as part of a [relative length](/docs/reference/layout/relative/), to specify the size of some layout element relative to the page or some container.

```typst
#rect(width: 25%)
```

However, they can also describe any other property that is relative to some base, e.g. an amount of [horizontal scaling](/docs/reference/layout/scale/#parameters-x) or the [height of parentheses](/docs/reference/math/lr/#functions-lr-size) relative to the height of the content they enclose.

## Scripting

Within your own code, you can use ratios as you like. You can multiply them with various other types as shown below:

| Multiply by | Example | Result |
| --- | --- | --- |
| [`ratio`](/docs/reference/layout/ratio/) | `27% * 10%` | `2.7%` |
| [`length`](/docs/reference/layout/length/) | `27% * 100pt` | `27pt` |
| [`relative`](/docs/reference/layout/relative/) | `27% * (10% + 100pt)` | `2.7% + 27pt` |
| [`angle`](/docs/reference/layout/angle/) | `27% * 100deg` | `27deg` |
| [`int`](/docs/reference/foundations/int/) | `27% * 2` | `54%` |
| [`float`](/docs/reference/foundations/float/) | `27% * 0.37037` | `10%` |
| [`fraction`](/docs/reference/layout/fraction/) | `27% * 3fr` | `0.81fr` |

When ratios are [displayed](/docs/reference/foundations/repr/) in the document, they are rounded to two significant digits for readability.


