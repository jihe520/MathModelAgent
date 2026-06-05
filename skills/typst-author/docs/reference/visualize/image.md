# Image

# image

A raster or vector graphic.

You can wrap the image in a [`figure`](/docs/reference/model/figure/) to give it a number and caption.

Like most elements, images are _block-level_ by default and thus do not integrate themselves into adjacent paragraphs. To force an image to become inline, put it into a [`box`](/docs/reference/layout/box/).

## Example

```typst
#figure(
  image("molecular.jpg", width: 80%),
  caption: [
    A step in the molecular testing
    pipeline of our lab.
  ],
)
```

```typst
#image(
  source,
  format: auto | str | dictionary,
  width: auto | relative,
  height: auto | relative | fraction,
  alt: none | str,
  page: int,
  fit: str,
  scaling: auto | str,
  icc: auto | str | bytes
) -> content
```

## Parameters

- source:
  - description: A [path](/docs/reference/syntax/#paths) to an image file or raw bytes making up an image in one of the supported [formats](/docs/reference/visualize/image/#parameters-format). Bytes can be used to specify raw pixel data in a row-major, left-to-right, top-to-bottom format. ```typst #let original = read("diagram.svg") #let changed = original.replace(  "#2B80FF", // blue  green.to-hex(), ) #image(bytes(original)) #image(bytes(changed)) ```
  - type: str | bytes
  - default: None
- format:
  - description: The image\'s format. By default, the format is detected automatically. Typically, you thus only need to specify this when providing raw bytes as the [`source`](/docs/reference/visualize/image/#parameters-source) (even then, Typst will try to figure out the format automatically, but that\'s not always possible). Supported formats are `"png"`, `"jpg"`, `"gif"`, `"svg"`, `"pdf"`, `"webp"` as well as raw pixel data. Note that several restrictions apply when using PDF files as images: - When exporting to PDF, any PDF image file used must have a version equal to or lower than the [export target PDF version](/docs/reference/pdf/#pdf-versions). - PDF files as images are currently not supported when exporting with a specific PDF standard, like PDF/A-3 or PDF/UA-1. In these cases, you can instead use SVGs to embed vector images. - The image file must not be password-protected. - Tags in your PDF image will not be preserved. Instead, you must provide an [alternative description](/docs/reference/visualize/image/#parameters-alt) to make the image accessible. When providing raw pixel data as the `source`, you must specify a dictionary with the following keys as the `format`: - `encoding` ([str](/docs/reference/foundations/str/)): The encoding of the pixel data. One of:  - `"rgb8"` (three 8-bit channels: red, green, blue)  - `"rgba8"` (four 8-bit channels: red, green, blue, alpha)  - `"luma8"` (one 8-bit channel)  - `"lumaa8"` (two 8-bit channels: luma and alpha) - `width` ([int](/docs/reference/foundations/int/)): The pixel width of the image. - `height` ([int](/docs/reference/foundations/int/)): The pixel height of the image. The pixel width multiplied by the height multiplied by the channel count for the specified encoding must then match the `source` data. ```typst #image(  read(   "tetrahedron.svg",   encoding: none,  ),  format: "svg",  width: 2cm, ) #image(  bytes(range(16).map(x => x * 16)),  format: (   encoding: "luma8",   width: 4,   height: 4,  ),  width: 2cm, ) ```
  - type: auto | str | dictionary
  - default: auto
- width:
  - description: The width of the image.
  - type: auto | relative
  - default: auto
- height:
  - description: The height of the image.
  - type: auto | relative | fraction
  - default: auto
- alt:
  - description: An alternative description of the image. This text is used by Assistive Technology (AT) like screen readers to describe the image to users with visual impairments. When the image is wrapped in a [`figure`](/docs/reference/model/figure/), use this parameter rather than the [figure\'s `alt` parameter](/docs/reference/model/figure/#parameters-alt) to describe the image. The only exception to this rule is when the image and the other contents in the figure form a single semantic unit. In this case, use the figure\'s `alt` parameter to describe the entire composition and do not use this parameter. You can learn how to write good alternative descriptions in the [Accessibility Guide](/docs/guides/accessibility/#textual-representations).
  - type: none | str
  - default: none
- page:
  - description: The page number that should be embedded as an image. This attribute only has an effect for PDF files.
  - type: int
  - default: 1
- fit:
  - description: How the image should adjust itself to a given area (the area is defined by the `width` and `height` fields). Note that `fit` doesn\'t visually change anything if the area\'s aspect ratio is the same as the image\'s one. ```typst #set page(width: 300pt, height: 50pt, margin: 10pt) #image("tiger.jpg", width: 100%, fit: "cover") #image("tiger.jpg", width: 100%, fit: "contain") #image("tiger.jpg", width: 100%, fit: "stretch") ```
  - type: str
  - default: "cover"
- scaling:
  - description: A hint to viewers how they should scale the image. When set to `auto`, the default is left up to the viewer. For PNG export, Typst will default to smooth scaling, like most PDF and SVG viewers. _Note:_ The exact look may differ across PDF viewers.
  - type: auto | str
  - default: auto
- icc:
  - description: An ICC profile for the image. ICC profiles define how to interpret the colors in an image. When set to `auto`, Typst will try to extract an ICC profile from the image.
  - type: auto | str | bytes
  - default: auto


## Definitions
### image.decode

Decode a raster or vector graphic from bytes or a string.

```typst
#image.decode(
  data,
  format: auto | str | dictionary,
  width: auto | relative,
  height: auto | relative | fraction,
  alt: none | str,
  fit: str,
  scaling: auto | str
) -> content
```

#### Parameters

- data:
  - description: The data to decode as an image. Can be a string for SVGs.
  - type: str | bytes
  - default: None
- format:
  - description: The image\'s format. Detected automatically by default.
  - type: auto | str | dictionary
  - default: None
- width:
  - description: The width of the image.
  - type: auto | relative
  - default: None
- height:
  - description: The height of the image.
  - type: auto | relative | fraction
  - default: None
- alt:
  - description: A text describing the image.
  - type: none | str
  - default: None
- fit:
  - description: How the image should adjust itself to a given area.
  - type: str
  - default: None
- scaling:
  - description: A hint to viewers how they should scale the image.
  - type: auto | str
  - default: None


