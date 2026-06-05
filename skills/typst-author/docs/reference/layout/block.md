# Block

# block

A block-level container.

Such a container can be used to separate content, size it, and give it a background or border.

Blocks are also the primary way to control whether text becomes part of a paragraph or not. See [the paragraph documentation](/docs/reference/model/par/#what-becomes-a-paragraph) for more details.

## Examples

With a block, you can give a background to content while still allowing it to break across multiple pages.

```typst
#set page(height: 100pt)
#block(
  fill: luma(230),
  inset: 8pt,
  radius: 4pt,
  lorem(30),
)
```

Blocks are also useful to force elements that would otherwise be inline to become block-level, especially when writing show rules.

```typst
#show heading: it => it.body
= Blockless
More text.

#show heading: it => block(it.body)
= Blocky
More text.
```

```typst
#block(
  width: auto | relative,
  height: auto | relative | fraction,
  breakable: bool,
  fill: none | color | gradient | tiling,
  stroke: none | length | color | gradient | stroke | tiling | dictionary,
  radius: relative | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  spacing: relative | fraction,
  above: auto | relative | fraction,
  below: auto | relative | fraction,
  clip: bool,
  sticky: bool,
  body
) -> content
```

## Parameters

- width:
  - description: The block\'s width. ```typst #set align(center) #block(  width: 60%,  inset: 8pt,  fill: silver,  lorem(10), ) ```
  - type: auto | relative
  - default: auto
- height:
  - description: The block\'s height. When the height is larger than the remaining space on a page and [`breakable`](/docs/reference/layout/block/#parameters-breakable) is `true`, the block will continue on the next page with the remaining height. ```typst #set page(height: 80pt) #set align(center) #block(  width: 80%,  height: 150%,  fill: aqua, ) ```
  - type: auto | relative | fraction
  - default: auto
- breakable:
  - description: Whether the block can be broken and continue on the next page. ```typst #set page(height: 80pt) The following block will jump to its own page. #block(  breakable: false,  lorem(15), ) ```
  - type: bool
  - default: true
- fill:
  - description: The block\'s background color. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-fill) for more details.
  - type: none | color | gradient | tiling
  - default: none
- stroke:
  - description: The block\'s border color. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-stroke) for more details.
  - type: none | length | color | gradient | stroke | tiling | dictionary
  - default: (:)
- radius:
  - description: How much to round the block\'s corners. See the [rectangle\'s documentation](/docs/reference/visualize/rect/#parameters-radius) for more details.
  - type: relative | dictionary
  - default: (:)
- inset:
  - description: How much to pad the block\'s content. See the [box\'s documentation](/docs/reference/layout/box/#parameters-inset) for more details.
  - type: relative | dictionary
  - default: (:)
- outset:
  - description: How much to expand the block\'s size without affecting the layout. See the [box\'s documentation](/docs/reference/layout/box/#parameters-outset) for more details.
  - type: relative | dictionary
  - default: (:)
- spacing:
  - description: The spacing around the block. When `auto`, inherits the paragraph [`spacing`](/docs/reference/model/par/#parameters-spacing). For two adjacent blocks, the larger of the first block\'s `above` and the second block\'s `below` spacing wins. Moreover, block spacing takes precedence over paragraph [`spacing`](/docs/reference/model/par/#parameters-spacing). Note that this is only a shorthand to set `above` and `below` to the same value. Since the values for `above` and `below` might differ, a [context](/docs/reference/context/) block only provides access to `block.above` and `block.below`, not to `block.spacing` directly. This property can be used in combination with a show rule to adjust the spacing around arbitrary block-level elements. ```typst #set align(center) #show math.equation: set block(above: 8pt, below: 16pt) This sum of $x$ and $y$: $ x + y = z $ A second paragraph. ```
  - type: relative | fraction
  - default: 1.2em
- above:
  - description: The spacing between this block and its predecessor.
  - type: auto | relative | fraction
  - default: auto
- below:
  - description: The spacing between this block and its successor.
  - type: auto | relative | fraction
  - default: auto
- clip:
  - description: Whether to clip the content inside the block. Clipping is useful when the block\'s content is larger than the block itself, as any content that exceeds the block\'s bounds will be hidden. ```typst #block(  width: 50pt,  height: 50pt,  clip: true,  image("tiger.jpg", width: 100pt, height: 100pt) ) ```
  - type: bool
  - default: false
- sticky:
  - description: Whether this block must stick to the following one, with no break in between. This is, by default, set on heading blocks to prevent orphaned headings at the bottom of the page. ```typst // Disable stickiness of headings. #show heading: set block(sticky: false) #lorem(20) = Chapter #lorem(10) ```
  - type: bool
  - default: false
- body:
  - description: The contents of the block.
  - type: none | content
  - default: none


