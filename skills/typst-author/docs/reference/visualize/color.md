# Color

A color in a specific color space.

Typst supports:

- sRGB through the [`rgb` function](/docs/reference/visualize/color/#definitions-rgb)
- Device CMYK through the [`cmyk` function](/docs/reference/visualize/color/#definitions-cmyk)
- D65 Gray through the [`luma` function](/docs/reference/visualize/color/#definitions-luma)
- Oklab through the [`oklab` function](/docs/reference/visualize/color/#definitions-oklab)
- Oklch through the [`oklch` function](/docs/reference/visualize/color/#definitions-oklch)
- Linear RGB through the [`color.linear-rgb` function](/docs/reference/visualize/color/#definitions-linear-rgb)
- HSL through the [`color.hsl` function](/docs/reference/visualize/color/#definitions-hsl)
- HSV through the [`color.hsv` function](/docs/reference/visualize/color/#definitions-hsv)

## Example

```typst
#rect(fill: aqua)
```

## Predefined colors

Typst defines the following built-in colors:

| Color | Definition |
| --- | --- |
| `black` | `luma(0)` |
| `gray` | `luma(170)` |
| `silver` | `luma(221)` |
| `white` | `luma(255)` |
| `navy` | `rgb("#001f3f")` |
| `blue` | `rgb("#0074d9")` |
| `aqua` | `rgb("#7fdbff")` |
| `teal` | `rgb("#39cccc")` |
| `eastern` | `rgb("#239dad")` |
| `purple` | `rgb("#b10dc9")` |
| `fuchsia` | `rgb("#f012be")` |
| `maroon` | `rgb("#85144b")` |
| `red` | `rgb("#ff4136")` |
| `orange` | `rgb("#ff851b")` |
| `yellow` | `rgb("#ffdc00")` |
| `olive` | `rgb("#3d9970")` |
| `green` | `rgb("#2ecc40")` |
| `lime` | `rgb("#01ff70")` |

The predefined colors and the most important color constructors are available globally and also in the color type's scope, so you can write either `color.red` or just `red`.

## Predefined color maps

Typst also includes a number of preset color maps that can be used for [gradients](/docs/reference/visualize/gradient/#stops). These are simply arrays of colors defined in the module `color.map`.

```typst
#circle(fill: gradient.linear(..color.map.crest))
```

| Map | Details |
| --- | --- |
| `turbo` | A perceptually uniform rainbow-like color map. Read [this blog post](https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html) for more details. |
| `cividis` | A blue to gray to yellow color map. See [this blog post](https://bids.github.io/colormap/) for more details. |
| `rainbow` | Cycles through the full color spectrum. This color map is best used by setting the interpolation color space to [HSL](/docs/reference/visualize/color/#definitions-hsl). The rainbow gradient is **not suitable** for data visualization because it is not perceptually uniform, so the differences between values become unclear to your readers. It should only be used for decorative purposes. |
| `spectral` | Red to yellow to blue color map. |
| `viridis` | A purple to teal to yellow color map. |
| `inferno` | A black to red to yellow color map. |
| `magma` | A black to purple to yellow color map. |
| `plasma` | A purple to pink to yellow color map. |
| `rocket` | A black to red to white color map. |
| `mako` | A black to teal to white color map. |
| `vlag` | A light blue to white to red color map. |
| `icefire` | A light teal to black to orange color map. |
| `flare` | A orange to purple color map that is perceptually uniform. |
| `crest` | A light green to blue color map. |

Some popular presets are not included because they are not available under a free licence. Others, like [Jet](https://jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap/), are not included because they are not color blind friendly. Feel free to use or create a package with other presets that are useful to you!


## Methods

## color.luma

Create a grayscale color.

A grayscale color is represented internally by a single `lightness` component.

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

```typst
#for x in range(250, step: 50) {
  box(square(fill: luma(x)))
}
```

```typst
#color.luma(
  lightness,
  alpha,
  color
) -> color
```

### Parameters

- lightness:
  - description: The lightness component.
  - type: int | ratio
  - default: None
- alpha:
  - description: The alpha component.
  - type: ratio
  - default: None
- color:
  - description: Alternatively: The color to convert to grayscale. If this is given, the `lightness` should not be given.
  - type: color
  - default: None

## color.oklab

Create an [Oklab](https://bottosson.github.io/posts/oklab/) color.

This color space is well suited for the following use cases:

- Color manipulation such as saturating while keeping perceived hue
- Creating grayscale images with uniform perceived lightness
- Creating smooth and uniform color transition and gradients

A linear Oklab color is represented internally by an array of four components:

- lightness ([`ratio`](/docs/reference/layout/ratio/))
- a ([`float`](/docs/reference/foundations/float/) or [`ratio`](/docs/reference/layout/ratio/). Ratios are relative to `0.4`; meaning `50%` is equal to `0.2`)
- b ([`float`](/docs/reference/foundations/float/) or [`ratio`](/docs/reference/layout/ratio/). Ratios are relative to `0.4`; meaning `50%` is equal to `0.2`)
- alpha ([`ratio`](/docs/reference/layout/ratio/))

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

```typst
#square(
  fill: oklab(27%, 20%, -3%, 50%)
)
```

```typst
#color.oklab(
  lightness,
  a,
  b,
  alpha,
  color
) -> color
```

### Parameters

- lightness:
  - description: The lightness component.
  - type: ratio
  - default: None
- a:
  - description: The a ("green/red") component.
  - type: float | ratio
  - default: None
- b:
  - description: The b ("blue/yellow") component.
  - type: float | ratio
  - default: None
- alpha:
  - description: The alpha component.
  - type: ratio
  - default: None
- color:
  - description: Alternatively: The color to convert to Oklab. If this is given, the individual components should not be given.
  - type: color
  - default: None

## color.oklch

Create an [Oklch](https://bottosson.github.io/posts/oklab/) color.

This color space is well suited for the following use cases:

- Color manipulation involving lightness, chroma, and hue
- Creating grayscale images with uniform perceived lightness
- Creating smooth and uniform color transition and gradients

A linear Oklch color is represented internally by an array of four components:

- lightness ([`ratio`](/docs/reference/layout/ratio/))
- chroma ([`float`](/docs/reference/foundations/float/) or [`ratio`](/docs/reference/layout/ratio/). Ratios are relative to `0.4`; meaning `50%` is equal to `0.2`)
- hue ([`angle`](/docs/reference/layout/angle/))
- alpha ([`ratio`](/docs/reference/layout/ratio/))

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

```typst
#square(
  fill: oklch(40%, 0.2, 160deg, 50%)
)
```

```typst
#color.oklch(
  lightness,
  chroma,
  hue,
  alpha,
  color
) -> color
```

### Parameters

- lightness:
  - description: The lightness component.
  - type: ratio
  - default: None
- chroma:
  - description: The chroma component.
  - type: float | ratio
  - default: None
- hue:
  - description: The hue component.
  - type: angle
  - default: None
- alpha:
  - description: The alpha component.
  - type: ratio
  - default: None
- color:
  - description: Alternatively: The color to convert to Oklch. If this is given, the individual components should not be given.
  - type: color
  - default: None

## color.linear-rgb

Create an RGB(A) color with linear luma.

This color space is similar to sRGB, but with the distinction that the color component are not gamma corrected. This makes it easier to perform color operations such as blending and interpolation. Although, you should prefer to use the [`oklab` function](/docs/reference/visualize/color/#definitions-oklab) for these.

A linear RGB(A) color is represented internally by an array of four components:

- red ([`ratio`](/docs/reference/layout/ratio/))
- green ([`ratio`](/docs/reference/layout/ratio/))
- blue ([`ratio`](/docs/reference/layout/ratio/))
- alpha ([`ratio`](/docs/reference/layout/ratio/))

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

```typst
#square(fill: color.linear-rgb(
  30%, 50%, 10%,
))
```

```typst
#color.linear-rgb(
  red,
  green,
  blue,
  alpha,
  color
) -> color
```

### Parameters

- red:
  - description: The red component.
  - type: int | ratio
  - default: None
- green:
  - description: The green component.
  - type: int | ratio
  - default: None
- blue:
  - description: The blue component.
  - type: int | ratio
  - default: None
- alpha:
  - description: The alpha component.
  - type: int | ratio
  - default: None
- color:
  - description: Alternatively: The color to convert to linear RGB(A). If this is given, the individual components should not be given.
  - type: color
  - default: None

## color.rgb

Create an RGB(A) color.

The color is specified in the sRGB color space.

An RGB(A) color is represented internally by an array of four components:

- red ([`ratio`](/docs/reference/layout/ratio/))
- green ([`ratio`](/docs/reference/layout/ratio/))
- blue ([`ratio`](/docs/reference/layout/ratio/))
- alpha ([`ratio`](/docs/reference/layout/ratio/))

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

```typst
#square(fill: rgb("#b1f2eb"))
#square(fill: rgb(87, 127, 230))
#square(fill: rgb(25%, 13%, 65%))
```

```typst
#color.rgb(
  red,
  green,
  blue,
  alpha,
  hex,
  color
) -> color
```

### Parameters

- red:
  - description: The red component.
  - type: int | ratio
  - default: None
- green:
  - description: The green component.
  - type: int | ratio
  - default: None
- blue:
  - description: The blue component.
  - type: int | ratio
  - default: None
- alpha:
  - description: The alpha component.
  - type: int | ratio
  - default: None
- hex:
  - description: Alternatively: The color in hexadecimal notation. Accepts three, four, six or eight hexadecimal digits and optionally a leading hash. If this is given, the individual components should not be given. ```typst #text(16pt, rgb("#239dad"))[  *Typst* ] ```
  - type: str
  - default: None
- color:
  - description: Alternatively: The color to convert to RGB(a). If this is given, the individual components should not be given.
  - type: color
  - default: None

## color.cmyk

Create a CMYK color.

This is useful if you want to target a specific printer. The conversion to RGB for display preview might differ from how your printer reproduces the color.

A CMYK color is represented internally by an array of four components:

- cyan ([`ratio`](/docs/reference/layout/ratio/))
- magenta ([`ratio`](/docs/reference/layout/ratio/))
- yellow ([`ratio`](/docs/reference/layout/ratio/))
- key ([`ratio`](/docs/reference/layout/ratio/))

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

Note that CMYK colors are not currently supported when PDF/A output is enabled.

```typst
#square(
  fill: cmyk(27%, 0%, 3%, 5%)
)
```

```typst
#color.cmyk(
  cyan,
  magenta,
  yellow,
  key,
  color
) -> color
```

### Parameters

- cyan:
  - description: The cyan component.
  - type: ratio
  - default: None
- magenta:
  - description: The magenta component.
  - type: ratio
  - default: None
- yellow:
  - description: The yellow component.
  - type: ratio
  - default: None
- key:
  - description: The key component.
  - type: ratio
  - default: None
- color:
  - description: Alternatively: The color to convert to CMYK. If this is given, the individual components should not be given.
  - type: color
  - default: None

## color.hsl

Create an HSL color.

This color space is useful for specifying colors by hue, saturation and lightness. It is also useful for color manipulation, such as saturating while keeping perceived hue.

An HSL color is represented internally by an array of four components:

- hue ([`angle`](/docs/reference/layout/angle/))
- saturation ([`ratio`](/docs/reference/layout/ratio/))
- lightness ([`ratio`](/docs/reference/layout/ratio/))
- alpha ([`ratio`](/docs/reference/layout/ratio/))

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

```typst
#square(
  fill: color.hsl(30deg, 50%, 60%)
)
```

```typst
#color.hsl(
  hue,
  saturation,
  lightness,
  alpha,
  color
) -> color
```

### Parameters

- hue:
  - description: The hue angle.
  - type: angle
  - default: None
- saturation:
  - description: The saturation component.
  - type: int | ratio
  - default: None
- lightness:
  - description: The lightness component.
  - type: int | ratio
  - default: None
- alpha:
  - description: The alpha component.
  - type: int | ratio
  - default: None
- color:
  - description: Alternatively: The color to convert to HSL. If this is given, the individual components should not be given.
  - type: color
  - default: None

## color.hsv

Create an HSV color.

This color space is useful for specifying colors by hue, saturation and value. It is also useful for color manipulation, such as saturating while keeping perceived hue.

An HSV color is represented internally by an array of four components:

- hue ([`angle`](/docs/reference/layout/angle/))
- saturation ([`ratio`](/docs/reference/layout/ratio/))
- value ([`ratio`](/docs/reference/layout/ratio/))
- alpha ([`ratio`](/docs/reference/layout/ratio/))

These components are also available using the [`components`](/docs/reference/visualize/color/#definitions-components) method.

```typst
#square(
  fill: color.hsv(30deg, 50%, 60%)
)
```

```typst
#color.hsv(
  hue,
  saturation,
  value,
  alpha,
  color
) -> color
```

### Parameters

- hue:
  - description: The hue angle.
  - type: angle
  - default: None
- saturation:
  - description: The saturation component.
  - type: int | ratio
  - default: None
- value:
  - description: The value component.
  - type: int | ratio
  - default: None
- alpha:
  - description: The alpha component.
  - type: int | ratio
  - default: None
- color:
  - description: Alternatively: The color to convert to HSL. If this is given, the individual components should not be given.
  - type: color
  - default: None

## color.components

Extracts the components of this color.

The size and values of this array depends on the color space. You can obtain the color space using [`space`](/docs/reference/visualize/color/#definitions-space). Below is a table of the color spaces and their components:

| Color space | C1 | C2 | C3 | C4 |
| --- | --- | --- | --- | --- |
| [`luma`](/docs/reference/visualize/color/#definitions-luma) | Lightness |  |  |  |
| [`oklab`](/docs/reference/visualize/color/#definitions-oklab) | Lightness | `a` | `b` | Alpha |
| [`oklch`](/docs/reference/visualize/color/#definitions-oklch) | Lightness | Chroma | Hue | Alpha |
| [`linear-rgb`](/docs/reference/visualize/color/#definitions-linear-rgb) | Red | Green | Blue | Alpha |
| [`rgb`](/docs/reference/visualize/color/#definitions-rgb) | Red | Green | Blue | Alpha |
| [`cmyk`](/docs/reference/visualize/color/#definitions-cmyk) | Cyan | Magenta | Yellow | Key |
| [`hsl`](/docs/reference/visualize/color/#definitions-hsl) | Hue | Saturation | Lightness | Alpha |
| [`hsv`](/docs/reference/visualize/color/#definitions-hsv) | Hue | Saturation | Value | Alpha |

For the meaning and type of each individual value, see the documentation of the corresponding color space. The alpha component is optional and only included if the `alpha` argument is `true`. The length of the returned array depends on the number of components and whether the alpha component is included.

```typst
// note that the alpha component is included by default
#rgb(40%, 60%, 80%).components()
```

```typst
#color.components(
  alpha: bool
) -> array
```

### Parameters

- alpha:
  - description: Whether to include the alpha component.
  - type: bool
  - default: true

## color.space

Returns the constructor function for this color's space.

Returns one of:

- [`luma`](/docs/reference/visualize/color/#definitions-luma)
- [`oklab`](/docs/reference/visualize/color/#definitions-oklab)
- [`oklch`](/docs/reference/visualize/color/#definitions-oklch)
- [`linear-rgb`](/docs/reference/visualize/color/#definitions-linear-rgb)
- [`rgb`](/docs/reference/visualize/color/#definitions-rgb)
- [`cmyk`](/docs/reference/visualize/color/#definitions-cmyk)
- [`hsl`](/docs/reference/visualize/color/#definitions-hsl)
- [`hsv`](/docs/reference/visualize/color/#definitions-hsv)

```typst
#let color = cmyk(1%, 2%, 3%, 4%)
#(color.space() == cmyk)
```

## color.to-hex

Returns the color's RGB(A) hex representation (such as `#ffaa32` or `#020304fe`). The alpha component (last two digits in `#020304fe`) is omitted if it is equal to `ff` (255 / 100%).

## color.lighten

Lightens a color by a given factor.

```typst
#color.lighten(
  factor
) -> color
```

### Parameters

- factor:
  - description: The factor to lighten the color by.
  - type: ratio
  - default: None

## color.darken

Darkens a color by a given factor.

```typst
#color.darken(
  factor
) -> color
```

### Parameters

- factor:
  - description: The factor to darken the color by.
  - type: ratio
  - default: None

## color.saturate

Increases the saturation of a color by a given factor.

```typst
#color.saturate(
  factor
) -> color
```

### Parameters

- factor:
  - description: The factor to saturate the color by.
  - type: ratio
  - default: None

## color.desaturate

Decreases the saturation of a color by a given factor.

```typst
#color.desaturate(
  factor
) -> color
```

### Parameters

- factor:
  - description: The factor to desaturate the color by.
  - type: ratio
  - default: None

## color.negate

Produces the complementary color using a provided color space. You can think of it as the opposite side on a color wheel.

```typst
#square(fill: yellow)
#square(fill: yellow.negate())
#square(fill: yellow.negate(space: rgb))
```

```typst
#color.negate(
  space: any
) -> color
```

### Parameters

- space:
  - description: The color space used for the transformation. By default, a perceptual color space is used.
  - type: any
  - default: oklab

## color.rotate

Rotates the hue of the color by a given angle.

```typst
#color.rotate(
  angle,
  space: any
) -> color
```

### Parameters

- angle:
  - description: The angle to rotate the hue by.
  - type: angle
  - default: None
- space:
  - description: The color space used to rotate. By default, this happens in a perceptual color space ([`oklch`](/docs/reference/visualize/color/#definitions-oklch)).
  - type: any
  - default: oklch

## color.mix

Create a color by mixing two or more colors.

In color spaces with a hue component (hsl, hsv, oklch), only two colors can be mixed at once. Mixing more than two colors in such a space will result in an error!

```typst
#set block(height: 20pt, width: 100%)
#block(fill: red.mix(blue))
#block(fill: red.mix(blue, space: rgb))
#block(fill: color.mix(red, blue, white))
#block(fill: color.mix((red, 70%), (blue, 30%)))
```

```typst
#color.mix(
  colors,
  space: any
) -> color
```

### Parameters

- colors:
  - description: The colors, optionally with weights, specified as a pair (array of length two) of color and weight (float or ratio). The weights do not need to add to `100%`, they are relative to the sum of all weights.
  - type: color | array
  - default: None
- space:
  - description: The color space to mix in. By default, this happens in a perceptual color space ([`oklab`](/docs/reference/visualize/color/#definitions-oklab)).
  - type: any
  - default: oklab

## color.transparentize

Makes a color more transparent by a given factor.

This method is relative to the existing alpha value. If the scale is positive, calculates `alpha - alpha * scale`. Negative scales behave like `color.opacify(-scale)`.

```typst
#block(fill: red)[opaque]
#block(fill: red.transparentize(50%))[half red]
#block(fill: red.transparentize(75%))[quarter red]
```

```typst
#color.transparentize(
  scale
) -> color
```

### Parameters

- scale:
  - description: The factor to change the alpha value by.
  - type: ratio
  - default: None

## color.opacify

Makes a color more opaque by a given scale.

This method is relative to the existing alpha value. If the scale is positive, calculates `alpha + scale - alpha * scale`. Negative scales behave like `color.transparentize(-scale)`.

```typst
#let half-red = red.transparentize(50%)
#block(fill: half-red.opacify(100%))[opaque]
#block(fill: half-red.opacify(50%))[three quarters red]
#block(fill: half-red.opacify(-50%))[one quarter red]
```

```typst
#color.opacify(
  scale
) -> color
```

### Parameters

- scale:
  - description: The scale to change the alpha value by.
  - type: ratio
  - default: None


