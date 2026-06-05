# Visualize

Drawing and data visualization.

If you want to create more advanced drawings or plots, also have a look at the [CeTZ](https://github.com/johannes-wolf/cetz) package as well as more specialized [packages](https://typst.app/universe/) for your use case.

## Accessibility

All shapes and paths drawn by Typst are automatically marked as [artifacts](/docs/reference/pdf/artifact/) to make them invisible to Assistive Technology (AT) during PDF export. However, their contents (if any) remain accessible.

If you are using the functions in this model to create an illustration with semantic meaning, make it accessible by wrapping it in a [`figure`](/docs/reference/model/figure/) function call. Use its [`alt` parameter](/docs/reference/model/figure/#parameters-alt) to provide an [alternative description](/docs/guides/accessibility/#textual-representations).

## Definitions

| Name | Description |
| --- | --- |
| [`circle`](/reference/visualize/circle/) | A circle with optional content. |
| [`color`](/reference/visualize/color/) | A color in a specific color space. |
| [`curve`](/reference/visualize/curve/) | A curve consisting of movements, lines, and Bézier segments. |
| [`ellipse`](/reference/visualize/ellipse/) | An ellipse with optional content. |
| [`gradient`](/reference/visualize/gradient/) | A color gradient. |
| [`image`](/reference/visualize/image/) | A raster or vector graphic. |
| [`line`](/reference/visualize/line/) | A line from one point to another. |
| [`path`](/reference/visualize/path/) | A path through a list of points, connected by Bézier curves. |
| [`polygon`](/reference/visualize/polygon/) | A closed polygon. |
| [`rect`](/reference/visualize/rect/) | A rectangle with optional content. |
| [`square`](/reference/visualize/square/) | A square with optional content. |
| [`stroke`](/reference/visualize/stroke/) | Defines how to draw a line. |
| [`tiling`](/reference/visualize/tiling/) | A repeating tiling fill. |

