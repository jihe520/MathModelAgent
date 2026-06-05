# Gradient

A color gradient.

Typst supports linear gradients through the [`gradient.linear` function](/docs/reference/visualize/gradient/#definitions-linear), radial gradients through the [`gradient.radial` function](/docs/reference/visualize/gradient/#definitions-radial), and conic gradients through the [`gradient.conic` function](/docs/reference/visualize/gradient/#definitions-conic).

A gradient can be used for the following purposes:

- As a fill to paint the interior of a shape: `rect(fill: gradient.linear(..))`
- As a stroke to paint the outline of a shape: `rect(stroke: 1pt + gradient.linear(..))`
- As the fill of text: `set text(fill: gradient.linear(..))`
- As a color map you can [sample](/docs/reference/visualize/gradient/#definitions-sample) from: `gradient.linear(..).sample(50%)`

## Examples

```typst
#stack(
  dir: ltr,
  spacing: 1fr,
  square(fill: gradient.linear(..color.map.rainbow)),
  square(fill: gradient.radial(..color.map.rainbow)),
  square(fill: gradient.conic(..color.map.rainbow)),
)
```

Gradients are also supported on text, but only when setting the [relativeness](/docs/reference/visualize/gradient/#definitions-relative) to either `auto` (the default value) or `"parent"`. To create word-by-word or glyph-by-glyph gradients, you can wrap the words or characters of your text in [boxes](/docs/reference/layout/box/) manually or through a [show rule](/docs/reference/styling/#show-rules).

```typst
#set text(fill: gradient.linear(red, blue))
#let rainbow(content) = {
  set text(fill: gradient.linear(..color.map.rainbow))
  box(content)
}

This is a gradient on text, but with a #rainbow[twist]!
```

## Stops

A gradient is composed of a series of stops. Each of these stops has a color and an offset. The offset is a [ratio](/docs/reference/layout/ratio/) between `0%` and `100%` or an angle between `0deg` and `360deg`. The offset is a relative position that determines how far along the gradient the stop is located. The stop's color is the color of the gradient at that position. You can choose to omit the offsets when defining a gradient. In this case, Typst will space all stops evenly.

Typst predefines color maps that you can use as stops. See the [`color`](/docs/reference/visualize/color/#predefined-color-maps) documentation for more details.

## Relativeness

The location of the `0%` and `100%` stops depends on the dimensions of a container. This container can either be the shape that it is being painted on, or the closest surrounding container. This is controlled by the `relative` argument of a gradient constructor. By default, gradients are relative to the shape they are being painted on, unless the gradient is applied on text, in which case they are relative to the closest ancestor container.

Typst determines the ancestor container as follows:

- For shapes that are placed at the root/top level of the document, the closest ancestor is the page itself.
- For other shapes, the ancestor is the innermost [`block`](/docs/reference/layout/block/) or [`box`](/docs/reference/layout/box/) that contains the shape. This includes the boxes and blocks that are implicitly created by show rules and elements. For example, a [`rotate`](/docs/reference/layout/rotate/) will not affect the parent of a gradient, but a [`grid`](/docs/reference/layout/grid/) will.

## Color spaces and interpolation

Gradients can be interpolated in any color space. By default, gradients are interpolated in the [Oklab](/docs/reference/visualize/color/#definitions-oklab) color space, which is a [perceptually uniform](https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/index.html) color space. This means that the gradient will be perceived as having a smooth progression of colors. This is particularly useful for data visualization.

However, you can choose to interpolate the gradient in any supported color space you want, but beware that some color spaces are not suitable for perceptually interpolating between colors. Consult the table below when choosing an interpolation space.

| Color space | Perceptually uniform? |
| --- | --- |
| [Oklab](/docs/reference/visualize/color/#definitions-oklab) | _Yes_ |
| [Oklch](/docs/reference/visualize/color/#definitions-oklch) | _Yes_ |
| [sRGB](/docs/reference/visualize/color/#definitions-rgb) | _No_ |
| [linear-RGB](/docs/reference/visualize/color/#definitions-linear-rgb) | _Yes_ |
| [CMYK](/docs/reference/visualize/color/#definitions-cmyk) | _No_ |
| [Grayscale](/docs/reference/visualize/color/#definitions-luma) | _Yes_ |
| [HSL](/docs/reference/visualize/color/#definitions-hsl) | _No_ |
| [HSV](/docs/reference/visualize/color/#definitions-hsv) | _No_ |

## Direction

Some gradients are sensitive to direction. For example, a linear gradient has an angle that determines its direction. Typst uses a clockwise angle, with 0° being from left to right, 90° from top to bottom, 180° from right to left, and 270° from bottom to top.

```typst
#stack(
  dir: ltr,
  spacing: 1fr,
  square(fill: gradient.linear(red, blue, angle: 0deg)),
  square(fill: gradient.linear(red, blue, angle: 90deg)),
  square(fill: gradient.linear(red, blue, angle: 180deg)),
  square(fill: gradient.linear(red, blue, angle: 270deg)),
)
```

## Note on file sizes

Gradients can be quite large, especially if they have many stops. This is because gradients are stored as a list of colors and offsets, which can take up a lot of space. If you are concerned about file sizes, you should consider the following:

- SVG gradients are currently inefficiently encoded. This will be improved in the future.
- PDF gradients in the [`color.oklab`](/docs/reference/visualize/color/#definitions-oklab), [`color.hsv`](/docs/reference/visualize/color/#definitions-hsv), [`color.hsl`](/docs/reference/visualize/color/#definitions-hsl), and [`color.oklch`](/docs/reference/visualize/color/#definitions-oklch) color spaces are stored as a list of [`color.rgb`](/docs/reference/visualize/color/#definitions-rgb) colors with extra stops in between. This avoids needing to encode these color spaces in your PDF file, but it does add extra stops to your gradient, which can increase the file size.


## Methods

## gradient.linear

Creates a new linear gradient, in which colors transition along a straight line.

```typst
#rect(
  width: 100%,
  height: 20pt,
  fill: gradient.linear(
    ..color.map.viridis,
  ),
)
```

```typst
#gradient.linear(
  stops,
  space: any,
  relative: auto | str,
  dir,
  angle
) -> gradient
```

### Parameters

- stops:
  - description: The color [stops](#stops) of the gradient.
  - type: color | array
  - default: None
- space:
  - description: The color space in which to interpolate the gradient. Defaults to a perceptually uniform color space called [Oklab](/docs/reference/visualize/color/#definitions-oklab).
  - type: any
  - default: oklab
- relative:
  - description: The [relative placement](#relativeness) of the gradient. For an element placed at the root/top level of the document, the parent is the page itself. For other elements, the parent is the innermost block, box, column, grid, or stack that contains the element.
  - type: auto | str
  - default: auto
- dir:
  - description: The direction of the gradient.
  - type: direction
  - default: ltr
- angle:
  - description: The angle of the gradient.
  - type: angle
  - default: None

## gradient.radial

Creates a new radial gradient, in which colors radiate away from an origin.

The gradient is defined by two circles: the focal circle and the end circle. The focal circle is a circle with center `focal-center` and radius `focal-radius`, that defines the points at which the gradient starts and has the color of the first stop. The end circle is a circle with center `center` and radius `radius`, that defines the points at which the gradient ends and has the color of the last stop. The gradient is then interpolated between these two circles.

Using these four values, also called the focal point for the starting circle and the center and radius for the end circle, we can define a gradient with more interesting properties than a basic radial gradient.

```typst
#stack(
  dir: ltr,
  spacing: 1fr,
  circle(fill: gradient.radial(
    ..color.map.viridis,
  )),
  circle(fill: gradient.radial(
    ..color.map.viridis,
    focal-center: (10%, 40%),
    focal-radius: 5%,
  )),
)
```

```typst
#gradient.radial(
  stops,
  space: any,
  relative: auto | str,
  center: array,
  radius: ratio,
  focal-center: auto | array,
  focal-radius: ratio
) -> gradient
```

### Parameters

- stops:
  - description: The color [stops](#stops) of the gradient.
  - type: color | array
  - default: None
- space:
  - description: The color space in which to interpolate the gradient. Defaults to a perceptually uniform color space called [Oklab](/docs/reference/visualize/color/#definitions-oklab).
  - type: any
  - default: oklab
- relative:
  - description: The [relative placement](#relativeness) of the gradient. For an element placed at the root/top level of the document, the parent is the page itself. For other elements, the parent is the innermost block, box, column, grid, or stack that contains the element.
  - type: auto | str
  - default: auto
- center:
  - description: The center of the end circle of the gradient. A value of `(50%, 50%)` means that the end circle is centered inside of its container.
  - type: array
  - default: (50 % , 50 % )
- radius:
  - description: The radius of the end circle of the gradient. By default, it is set to `50%`. The ending radius must be bigger than the focal radius.
  - type: ratio
  - default: 50 %
- focal-center:
  - description: The center of the focal circle of the gradient. The focal center must be inside of the end circle. A value of `(50%, 50%)` means that the focal circle is centered inside of its container. By default it is set to the same as the center of the last circle.
  - type: auto | array
  - default: auto
- focal-radius:
  - description: The radius of the focal circle of the gradient. The focal center must be inside of the end circle. By default, it is set to `0%`. The focal radius must be smaller than the ending radius\\`.
  - type: ratio
  - default: 0 %

## gradient.conic

Creates a new conic gradient, in which colors change radially around a center point.

You can control the center point of the gradient by using the `center` argument. By default, the center point is the center of the shape.

```typst
#stack(
  dir: ltr,
  spacing: 1fr,
  circle(fill: gradient.conic(
    ..color.map.viridis,
  )),
  circle(fill: gradient.conic(
    ..color.map.viridis,
    center: (20%, 30%),
  )),
)
```

```typst
#gradient.conic(
  stops,
  angle: angle,
  space: any,
  relative: auto | str,
  center: array
) -> gradient
```

### Parameters

- stops:
  - description: The color [stops](#stops) of the gradient.
  - type: color | array
  - default: None
- angle:
  - description: The angle of the gradient.
  - type: angle
  - default: 0deg
- space:
  - description: The color space in which to interpolate the gradient. Defaults to a perceptually uniform color space called [Oklab](/docs/reference/visualize/color/#definitions-oklab).
  - type: any
  - default: oklab
- relative:
  - description: The [relative placement](#relativeness) of the gradient. For an element placed at the root/top level of the document, the parent is the page itself. For other elements, the parent is the innermost block, box, column, grid, or stack that contains the element.
  - type: auto | str
  - default: auto
- center:
  - description: The center of the circle of the gradient. A value of `(50%, 50%)` means that the circle is centered inside of its container.
  - type: array
  - default: (50 % , 50 % )

## gradient.sharp

Creates a sharp version of this gradient.

Sharp gradients have discrete jumps between colors, instead of a smooth transition. They are particularly useful for creating color lists for a preset gradient.

```typst
#set rect(width: 100%, height: 20pt)
#let grad = gradient.linear(..color.map.rainbow)
#rect(fill: grad)
#rect(fill: grad.sharp(5))
#rect(fill: grad.sharp(5, smoothness: 20%))
```

```typst
#gradient.sharp(
  steps,
  smoothness: ratio
) -> gradient
```

### Parameters

- steps:
  - description: The number of stops in the gradient.
  - type: int
  - default: None
- smoothness:
  - description: How much to smooth the gradient.
  - type: ratio
  - default: 0 %

## gradient.repeat

Repeats this gradient a given number of times, optionally mirroring it at every second repetition.

```typst
#circle(
  radius: 40pt,
  fill: gradient
    .radial(aqua, white)
    .repeat(4),
)
```

```typst
#gradient.repeat(
  repetitions,
  mirror: bool
) -> gradient
```

### Parameters

- repetitions:
  - description: The number of times to repeat the gradient.
  - type: int
  - default: None
- mirror:
  - description: Whether to mirror the gradient at every second repetition, i.e., the first instance (and all odd ones) stays unchanged. ```typst #circle(  radius: 40pt,  fill: gradient   .conic(green, black)   .repeat(2, mirror: true) ) ```
  - type: bool
  - default: false

## gradient.kind

Returns the kind of this gradient.

## gradient.stops

Returns the stops of this gradient.

## gradient.space

Returns the mixing space of this gradient.

## gradient.relative

Returns the relative placement of this gradient.

## gradient.angle

Returns the angle of this gradient.

Returns `none` if the gradient is neither linear nor conic.

## gradient.center

Returns the center of this gradient.

Returns `none` if the gradient is neither radial nor conic.

## gradient.radius

Returns the radius of this gradient.

Returns `none` if the gradient is not radial.

## gradient.focal-center

Returns the focal-center of this gradient.

Returns `none` if the gradient is not radial.

## gradient.focal-radius

Returns the focal-radius of this gradient.

Returns `none` if the gradient is not radial.

## gradient.sample

Sample the gradient at a given position.

The position is either a position along the gradient (a [ratio](/docs/reference/layout/ratio/) between `0%` and `100%`) or an [angle](/docs/reference/layout/angle/). Any value outside of this range will be clamped.

```typst
#gradient.sample(
  t
) -> color
```

### Parameters

- t:
  - description: The position at which to sample the gradient.
  - type: angle | ratio
  - default: None

## gradient.samples

Samples the gradient at multiple positions at once and returns the results as an array.

```typst
#gradient.samples(
  ts
) -> array
```

### Parameters

- ts:
  - description: The positions at which to sample the gradient.
  - type: angle | ratio
  - default: None


