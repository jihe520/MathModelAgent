# Typed HTML

A typed layer over raw HTML elements.

The `html` module provides a typed layer over the raw [`html.elem`](/docs/reference/html/elem/) function that allows you to conveniently create HTML elements. HTML attributes are exposed as function parameters that accept Typst types and automatically take care of converting those into the appropriate HTML.

Some parameters are common to all typed HTML functions. These are listed at the bottom in the [Global Attributes](#global-attributes) section instead of explicitly on each element for readability.

## Example

```typst
#html.video(
  controls: true,
  width: 1280,
  height: 720,
  src: "sunrise.mp4",
)[
  Your browser does not support the video tag.
]
```

# html.a

Hyperlink.

```typst
#html.a(
  download: str,
  href: str,
  hreflang: str,
  ping: str | array,
  referrerpolicy: none | str,
  rel: str | array,
  target: str,
  type: str,
  body
) -> content
```

## Parameters

- download:
  - description: Whether to download the resource instead of navigating to it, and its filename if so.
  - type: str
  - default: None
- href:
  - description: Address of the hyperlink.
  - type: str
  - default: None
- hreflang:
  - description: Language of the linked resource.
  - type: str
  - default: None
- ping:
  - description: URLs to ping.
  - type: str | array
  - default: None
- referrerpolicy:
  - description: Referrer policy for fetches initiated by the element.
  - type: none | str
  - default: None
- rel:
  - description: Relationship between the location in the document containing the hyperlink and the destination resource.
  - type: str | array
  - default: None
- target:
  - description: Navigable for hyperlink navigation.
  - type: str
  - default: None
- type:
  - description: Hint for the type of the referenced resource.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.abbr

Abbreviation.

```typst
#html.abbr(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.address

Contact information for a page or article element.

```typst
#html.address(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.area

Hyperlink or dead area on an image map.

```typst
#html.area(
  alt: str,
  coords: array,
  download: str,
  href: str,
  ping: str | array,
  referrerpolicy: none | str,
  rel: str | array,
  shape: str,
  target: str
) -> content
```

## Parameters

- alt:
  - description: Replacement text for use when images are not available.
  - type: str
  - default: None
- coords:
  - description: Coordinates for the shape to be created in an image map. Expects an array of floating point numbers.
  - type: array
  - default: None
- download:
  - description: Whether to download the resource instead of navigating to it, and its filename if so.
  - type: str
  - default: None
- href:
  - description: Address of the hyperlink.
  - type: str
  - default: None
- ping:
  - description: URLs to ping.
  - type: str | array
  - default: None
- referrerpolicy:
  - description: Referrer policy for fetches initiated by the element.
  - type: none | str
  - default: None
- rel:
  - description: Relationship between the location in the document containing the hyperlink and the destination resource.
  - type: str | array
  - default: None
- shape:
  - description: The kind of shape to be created in an image map.
  - type: str
  - default: None
- target:
  - description: Navigable for hyperlink navigation.
  - type: str
  - default: None

# html.article

Self-contained syndicatable or reusable composition.

```typst
#html.article(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.aside

Sidebar for tangentially related content.

```typst
#html.aside(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.audio

Audio player.

```typst
#html.audio(
  autoplay: bool,
  controls: bool,
  crossorigin: str,
  loop: bool,
  muted: bool,
  preload: none | auto | str,
  src: str,
  body
) -> content
```

## Parameters

- autoplay:
  - description: Hint that the media resource can be started automatically when the page is loaded.
  - type: bool
  - default: None
- controls:
  - description: Show user agent controls.
  - type: bool
  - default: None
- crossorigin:
  - description: How the element handles crossorigin requests.
  - type: str
  - default: None
- loop:
  - description: Whether to loop the media resource.
  - type: bool
  - default: None
- muted:
  - description: Whether to mute the media resource by default.
  - type: bool
  - default: None
- preload:
  - description: Hints how much buffering the media resource will likely need.
  - type: none | auto | str
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.b

Keywords.

```typst
#html.b(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.base

Base URL and default target navigable for hyperlinks and forms.

```typst
#html.base(
  href: str,
  target: str
) -> content
```

## Parameters

- href:
  - description: Document base URL.
  - type: str
  - default: None
- target:
  - description: Default navigable for hyperlink navigation and form submission.
  - type: str
  - default: None

# html.bdi

Text directionality isolation.

```typst
#html.bdi(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.bdo

Text directionality formatting.

```typst
#html.bdo(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.blockquote

A section quoted from another source.

```typst
#html.blockquote(
  cite: str,
  body
) -> content
```

## Parameters

- cite:
  - description: Link to the source of the quotation or more information about the edit.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.body

Document body.

```typst
#html.body(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.br

Line break, e.g. in poem or postal address.

# html.button

Button control.

```typst
#html.button(
  command: str,
  commandfor: str,
  disabled: bool,
  form: str,
  formaction: str,
  formenctype: str,
  formmethod: str,
  formnovalidate: bool,
  formtarget: str,
  name: str,
  popovertarget: str,
  popovertargetaction: str,
  type: str,
  value: str,
  body
) -> content
```

## Parameters

- command:
  - description: Indicates to the targeted element which action to take.
  - type: str
  - default: None
- commandfor:
  - description: Targets another element to be invoked.
  - type: str
  - default: None
- disabled:
  - description: Whether the form control is disabled.
  - type: bool
  - default: None
- form:
  - description: Associates the element with a form element.
  - type: str
  - default: None
- formaction:
  - description: URL to use for form submission.
  - type: str
  - default: None
- formenctype:
  - description: Entry list encoding type to use for form submission.
  - type: str
  - default: None
- formmethod:
  - description: Variant to use for form submission.
  - type: str
  - default: None
- formnovalidate:
  - description: Bypass form control validation for form submission.
  - type: bool
  - default: None
- formtarget:
  - description: Navigable for form submission.
  - type: str
  - default: None
- name:
  - description: Name of the element to use for form submission and in the form.elements API.
  - type: str
  - default: None
- popovertarget:
  - description: Targets a popover element to toggle, show, or hide.
  - type: str
  - default: None
- popovertargetaction:
  - description: Indicates whether a targeted popover element is to be toggled, shown, or hidden.
  - type: str
  - default: None
- type:
  - description: Type of button.
  - type: str
  - default: None
- value:
  - description: Value to be used for form submission.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.canvas

Scriptable bitmap canvas.

```typst
#html.canvas(
  height: int,
  width: int,
  body
) -> content
```

## Parameters

- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.caption

Table caption.

```typst
#html.caption(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.cite

Title of a work.

```typst
#html.cite(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.code

Computer code.

```typst
#html.code(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.col

Table column.

```typst
#html.col(
  span: int
) -> content
```

## Parameters

- span:
  - description: Number of columns spanned by the element.
  - type: int
  - default: None

# html.colgroup

Group of columns in a table.

```typst
#html.colgroup(
  span: int,
  body
) -> content
```

## Parameters

- span:
  - description: Number of columns spanned by the element.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.data

Machine-readable equivalent.

```typst
#html.data(
  value: str,
  body
) -> content
```

## Parameters

- value:
  - description: Machine-readable value.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.datalist

Container for options for combo box control.

```typst
#html.datalist(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.dd

Content for corresponding dt element(s).

```typst
#html.dd(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.del

A removal from the document.

```typst
#html.del(
  cite: str,
  datetime: datetime,
  body
) -> content
```

## Parameters

- cite:
  - description: Link to the source of the quotation or more information about the edit.
  - type: str
  - default: None
- datetime:
  - description: Date and (optionally) time of the change.
  - type: datetime
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.details

Disclosure control for hiding details.

```typst
#html.details(
  name: str,
  open: bool,
  body
) -> content
```

## Parameters

- name:
  - description: Name of group of mutually-exclusive details elements.
  - type: str
  - default: None
- open:
  - description: Whether the details are visible.
  - type: bool
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.dfn

Defining instance.

```typst
#html.dfn(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.dialog

Dialog box or window.

```typst
#html.dialog(
  open: bool,
  body
) -> content
```

## Parameters

- open:
  - description: Whether the dialog box is showing.
  - type: bool
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.div

Generic flow container, or container for name-value groups in dl elements.

```typst
#html.div(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.dl

Association list consisting of zero or more name-value groups.

```typst
#html.dl(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.dt

Legend for corresponding dd element(s).

```typst
#html.dt(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.em

Stress emphasis.

```typst
#html.em(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.embed

Plugin.

```typst
#html.embed(
  height: int,
  src: str,
  type: str,
  width: int
) -> content
```

## Parameters

- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- type:
  - description: Type of embedded resource.
  - type: str
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None

# html.fieldset

Group of form controls.

```typst
#html.fieldset(
  disabled: bool,
  form: str,
  name: str,
  body
) -> content
```

## Parameters

- disabled:
  - description: Whether the descendant form controls, except any inside legend, are disabled.
  - type: bool
  - default: None
- form:
  - description: Associates the element with a form element.
  - type: str
  - default: None
- name:
  - description: Name of the element to use for form submission and in the form.elements API.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.figcaption

Caption for figure.

```typst
#html.figcaption(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.figure

Figure with optional caption.

```typst
#html.figure(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.footer

Footer for a page or section.

```typst
#html.footer(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.form

User-submittable form.

```typst
#html.form(
  accept-charset: str,
  action: str,
  autocomplete: bool,
  enctype: str,
  method: str,
  name: str,
  novalidate: bool,
  rel: str | array,
  target: str,
  body
) -> content
```

## Parameters

- accept-charset:
  - description: Character encodings to use for form submission.
  - type: str
  - default: None
- action:
  - description: URL to use for form submission.
  - type: str
  - default: None
- autocomplete:
  - description: Default setting for autofill feature for controls in the form.
  - type: bool
  - default: None
- enctype:
  - description: Entry list encoding type to use for form submission.
  - type: str
  - default: None
- method:
  - description: Variant to use for form submission.
  - type: str
  - default: None
- name:
  - description: Name of form to use in the document.forms API.
  - type: str
  - default: None
- novalidate:
  - description: Bypass form control validation for form submission.
  - type: bool
  - default: None
- rel:
  - description: Relationship between the document containing the form and its action destination
  - type: str | array
  - default: None
- target:
  - description: Navigable for form submission.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.h1

Heading.

```typst
#html.h1(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.h2

Heading.

```typst
#html.h2(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.h3

Heading.

```typst
#html.h3(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.h4

Heading.

```typst
#html.h4(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.h5

Heading.

```typst
#html.h5(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.h6

Heading.

```typst
#html.h6(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.head

Container for document metadata.

```typst
#html.head(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.header

Introductory or navigational aids for a page or section.

```typst
#html.header(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.hgroup

Heading container.

```typst
#html.hgroup(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.hr

Thematic break.

# html.html

Root element.

```typst
#html.html(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.i

Alternate voice.

```typst
#html.i(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.iframe

Child navigable.

```typst
#html.iframe(
  allow: str,
  allowfullscreen: bool,
  height: int,
  loading: str,
  name: str,
  referrerpolicy: none | str,
  sandbox: str | array,
  src: str,
  srcdoc: str,
  width: int,
  body
) -> content
```

## Parameters

- allow:
  - description: Permissions policy to be applied to the iframe\'s contents.
  - type: str
  - default: None
- allowfullscreen:
  - description: Whether to allow the iframe\'s contents to use requestFullscreen().
  - type: bool
  - default: None
- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- loading:
  - description: Used when determining loading deferral.
  - type: str
  - default: None
- name:
  - description: Name of content navigable.
  - type: str
  - default: None
- referrerpolicy:
  - description: Referrer policy for fetches initiated by the element.
  - type: none | str
  - default: None
- sandbox:
  - description: Security rules for nested content.
  - type: str | array
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- srcdoc:
  - description: A document to render in the iframe.
  - type: str
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.img

Image.

```typst
#html.img(
  alt: str,
  crossorigin: str,
  decoding: auto | str,
  fetchpriority: auto | str,
  height: int,
  ismap: bool,
  loading: str,
  referrerpolicy: none | str,
  sizes: array,
  src: str,
  srcset: array,
  usemap: str,
  width: int
) -> content
```

## Parameters

- alt:
  - description: Replacement text for use when images are not available.
  - type: str
  - default: None
- crossorigin:
  - description: How the element handles crossorigin requests.
  - type: str
  - default: None
- decoding:
  - description: Decoding hint to use when processing this image for presentation.
  - type: auto | str
  - default: None
- fetchpriority:
  - description: Sets the priority for fetches initiated by the element.
  - type: auto | str
  - default: None
- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- ismap:
  - description: Whether the image is a server-side image map.
  - type: bool
  - default: None
- loading:
  - description: Used when determining loading deferral.
  - type: str
  - default: None
- referrerpolicy:
  - description: Referrer policy for fetches initiated by the element.
  - type: none | str
  - default: None
- sizes:
  - description: Image sizes for different page layouts. Expects an array of dictionaries with the keys `condition` (string) and `size` (length).
  - type: array
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- srcset:
  - description: Images to use in different situations, e.g., high-resolution displays, small monitors, etc. Expects an array of dictionaries with the keys `src` (string) and `width` (integer) or `density` (float).
  - type: array
  - default: None
- usemap:
  - description: Name of image map to use.
  - type: str
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None

# html.input

Form control.

```typst
#html.input(
  accept: str | array,
  alpha: bool,
  alt: str,
  autocomplete: str | array,
  checked: bool,
  colorspace: str,
  dirname: str,
  disabled: bool,
  form: str,
  formaction: str,
  formenctype: str,
  formmethod: str,
  formnovalidate: bool,
  formtarget: str,
  height: int,
  list: str,
  max: float | datetime | str,
  maxlength: int,
  min: float | datetime | str,
  minlength: int,
  multiple: bool,
  name: str,
  pattern: str,
  placeholder: str,
  popovertarget: str,
  popovertargetaction: str,
  readonly: bool,
  required: bool,
  size: int,
  src: str,
  step: float | str,
  type: str,
  value: float | color | datetime | str | array,
  width: int
) -> content
```

## Parameters

- accept:
  - description: Hint for expected file type in file upload controls.
  - type: str | array
  - default: None
- alpha:
  - description: Allow the color\'s alpha component to be set.
  - type: bool
  - default: None
- alt:
  - description: Replacement text for use when images are not available.
  - type: str
  - default: None
- autocomplete:
  - description: Hint for form autofill feature.
  - type: str | array
  - default: None
- checked:
  - description: Whether the control is checked.
  - type: bool
  - default: None
- colorspace:
  - description: The color space of the serialized color.
  - type: str
  - default: None
- dirname:
  - description: Name of form control to use for sending the element\'s directionality in form submission.
  - type: str
  - default: None
- disabled:
  - description: Whether the form control is disabled.
  - type: bool
  - default: None
- form:
  - description: Associates the element with a form element.
  - type: str
  - default: None
- formaction:
  - description: URL to use for form submission.
  - type: str
  - default: None
- formenctype:
  - description: Entry list encoding type to use for form submission.
  - type: str
  - default: None
- formmethod:
  - description: Variant to use for form submission.
  - type: str
  - default: None
- formnovalidate:
  - description: Bypass form control validation for form submission.
  - type: bool
  - default: None
- formtarget:
  - description: Navigable for form submission.
  - type: str
  - default: None
- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- list:
  - description: List of autocomplete options.
  - type: str
  - default: None
- max:
  - description: Maximum value.
  - type: float | datetime | str
  - default: None
- maxlength:
  - description: Maximum length of value.
  - type: int
  - default: None
- min:
  - description: Minimum value.
  - type: float | datetime | str
  - default: None
- minlength:
  - description: Minimum length of value.
  - type: int
  - default: None
- multiple:
  - description: Whether to allow multiple values.
  - type: bool
  - default: None
- name:
  - description: Name of the element to use for form submission and in the form.elements API.
  - type: str
  - default: None
- pattern:
  - description: Pattern to be matched by the form control\'s value.
  - type: str
  - default: None
- placeholder:
  - description: User-visible label to be placed within the form control.
  - type: str
  - default: None
- popovertarget:
  - description: Targets a popover element to toggle, show, or hide.
  - type: str
  - default: None
- popovertargetaction:
  - description: Indicates whether a targeted popover element is to be toggled, shown, or hidden.
  - type: str
  - default: None
- readonly:
  - description: Whether to allow the value to be edited by the user.
  - type: bool
  - default: None
- required:
  - description: Whether the control is required for form submission.
  - type: bool
  - default: None
- size:
  - description: Size of the control.
  - type: int
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- step:
  - description: Granularity to be matched by the form control\'s value.
  - type: float | str
  - default: None
- type:
  - description: Type of form control.
  - type: str
  - default: None
- value:
  - description: Value of the form control.
  - type: float | color | datetime | str | array
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None

# html.ins

An addition to the document.

```typst
#html.ins(
  cite: str,
  datetime: datetime,
  body
) -> content
```

## Parameters

- cite:
  - description: Link to the source of the quotation or more information about the edit.
  - type: str
  - default: None
- datetime:
  - description: Date and (optionally) time of the change.
  - type: datetime
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.kbd

User input.

```typst
#html.kbd(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.label

Caption for a form control.

```typst
#html.label(
  for: str,
  body
) -> content
```

## Parameters

- for:
  - description: Associate the label with form control.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.legend

Caption for fieldset.

```typst
#html.legend(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.li

List item.

```typst
#html.li(
  value: int,
  body
) -> content
```

## Parameters

- value:
  - description: Ordinal value of the list item.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.link

Link metadata.

```typst
#html.link(
  as: str,
  blocking: str | array,
  color: color,
  crossorigin: str,
  disabled: bool,
  fetchpriority: auto | str,
  href: str,
  hreflang: str,
  imagesizes: array,
  imagesrcset: array,
  integrity: str,
  media: str,
  referrerpolicy: none | str,
  rel: str | array,
  sizes: array,
  type: str
) -> content
```

## Parameters

- as:
  - description: Potential destination for a preload request (for rel="preload" and rel="modulepreload").
  - type: str
  - default: None
- blocking:
  - description: Whether the element is potentially render-blocking.
  - type: str | array
  - default: None
- color:
  - description: Color to use when customizing a site\'s icon (for rel="mask-icon").
  - type: color
  - default: None
- crossorigin:
  - description: How the element handles crossorigin requests.
  - type: str
  - default: None
- disabled:
  - description: Whether the link is disabled.
  - type: bool
  - default: None
- fetchpriority:
  - description: Sets the priority for fetches initiated by the element.
  - type: auto | str
  - default: None
- href:
  - description: Address of the hyperlink.
  - type: str
  - default: None
- hreflang:
  - description: Language of the linked resource.
  - type: str
  - default: None
- imagesizes:
  - description: Image sizes for different page layouts (for rel="preload"). Expects an array of dictionaries with the keys `condition` (string) and `size` (length).
  - type: array
  - default: None
- imagesrcset:
  - description: Images to use in different situations, e.g., high-resolution displays, small monitors, etc. (for rel="preload"). Expects an array of dictionaries with the keys `src` (string) and `width` (integer) or `density` (float).
  - type: array
  - default: None
- integrity:
  - description: Integrity metadata used in Subresource Integrity checks.
  - type: str
  - default: None
- media:
  - description: Applicable media.
  - type: str
  - default: None
- referrerpolicy:
  - description: Referrer policy for fetches initiated by the element.
  - type: none | str
  - default: None
- rel:
  - description: Relationship between the document containing the hyperlink and the destination resource.
  - type: str | array
  - default: None
- sizes:
  - description: Sizes of the icons (for rel="icon"). Expects an array of sizes. Each size is specified as an array of two integers (width and height).
  - type: array
  - default: None
- type:
  - description: Hint for the type of the referenced resource.
  - type: str
  - default: None

# html.main

Container for the dominant contents of the document.

```typst
#html.main(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.map

Image map.

```typst
#html.map(
  name: str,
  body
) -> content
```

## Parameters

- name:
  - description: Name of image map to reference from the usemap attribute.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.mark

Highlight.

```typst
#html.mark(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.menu

Menu of commands.

```typst
#html.menu(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.meta

Text metadata.

```typst
#html.meta(
  charset: str,
  content: str,
  http-equiv: str,
  media: str,
  name: str
) -> content
```

## Parameters

- charset:
  - description: Character encoding declaration.
  - type: str
  - default: None
- content:
  - description: Value of the element.
  - type: str
  - default: None
- http-equiv:
  - description: Pragma directive.
  - type: str
  - default: None
- media:
  - description: Applicable media.
  - type: str
  - default: None
- name:
  - description: Metadata name.
  - type: str
  - default: None

# html.meter

Gauge.

```typst
#html.meter(
  high: float,
  low: float,
  max: float,
  min: float,
  optimum: float,
  value: float,
  body
) -> content
```

## Parameters

- high:
  - description: Low limit of high range.
  - type: float
  - default: None
- low:
  - description: High limit of low range.
  - type: float
  - default: None
- max:
  - description: Upper bound of range.
  - type: float
  - default: None
- min:
  - description: Lower bound of range.
  - type: float
  - default: None
- optimum:
  - description: Optimum value in gauge.
  - type: float
  - default: None
- value:
  - description: Current value of the element.
  - type: float
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.nav

Section with navigational links.

```typst
#html.nav(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.noscript

Fallback content for script.

```typst
#html.noscript(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.object

Image, child navigable, or plugin.

```typst
#html.object(
  data: str,
  form: str,
  height: int,
  name: str,
  type: str,
  width: int,
  body
) -> content
```

## Parameters

- data:
  - description: Address of the resource.
  - type: str
  - default: None
- form:
  - description: Associates the element with a form element.
  - type: str
  - default: None
- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- name:
  - description: Name of content navigable.
  - type: str
  - default: None
- type:
  - description: Type of embedded resource.
  - type: str
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.ol

Ordered list.

```typst
#html.ol(
  reversed: bool,
  start: int,
  type: str,
  body
) -> content
```

## Parameters

- reversed:
  - description: Number the list backwards.
  - type: bool
  - default: None
- start:
  - description: Starting value of the list.
  - type: int
  - default: None
- type:
  - description: Kind of list marker.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.optgroup

Group of options in a list box.

```typst
#html.optgroup(
  disabled: bool,
  label: str,
  body
) -> content
```

## Parameters

- disabled:
  - description: Whether the form control is disabled.
  - type: bool
  - default: None
- label:
  - description: User-visible label.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.option

Option in a list box or combo box control.

```typst
#html.option(
  disabled: bool,
  label: str,
  selected: bool,
  value: str,
  body
) -> content
```

## Parameters

- disabled:
  - description: Whether the form control is disabled.
  - type: bool
  - default: None
- label:
  - description: User-visible label.
  - type: str
  - default: None
- selected:
  - description: Whether the option is selected by default.
  - type: bool
  - default: None
- value:
  - description: Value to be used for form submission.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.output

Calculated output value.

```typst
#html.output(
  for: str | array,
  form: str,
  name: str,
  body
) -> content
```

## Parameters

- for:
  - description: Specifies controls from which the output was calculated.
  - type: str | array
  - default: None
- form:
  - description: Associates the element with a form element.
  - type: str
  - default: None
- name:
  - description: Name of the element to use for form submission and in the form.elements API.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.p

Paragraph.

```typst
#html.p(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.picture

Image.

```typst
#html.picture(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.pre

Block of preformatted text.

```typst
#html.pre(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.progress

Progress bar.

```typst
#html.progress(
  max: float,
  value: float,
  body
) -> content
```

## Parameters

- max:
  - description: Upper bound of range.
  - type: float
  - default: None
- value:
  - description: Current value of the element.
  - type: float
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.q

Quotation.

```typst
#html.q(
  cite: str,
  body
) -> content
```

## Parameters

- cite:
  - description: Link to the source of the quotation or more information about the edit.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.rp

Parenthesis for ruby annotation text.

```typst
#html.rp(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.rt

Ruby annotation text.

```typst
#html.rt(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.ruby

Ruby annotation(s).

```typst
#html.ruby(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.s

Inaccurate text.

```typst
#html.s(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.samp

Computer output.

```typst
#html.samp(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.script

Embedded script.

```typst
#html.script(
  async: bool,
  blocking: str | array,
  crossorigin: str,
  defer: bool,
  fetchpriority: auto | str,
  integrity: str,
  nomodule: bool,
  referrerpolicy: none | str,
  src: str,
  type: str,
  body
) -> content
```

## Parameters

- async:
  - description: Execute script when available, without blocking while fetching.
  - type: bool
  - default: None
- blocking:
  - description: Whether the element is potentially render-blocking.
  - type: str | array
  - default: None
- crossorigin:
  - description: How the element handles crossorigin requests.
  - type: str
  - default: None
- defer:
  - description: Defer script execution.
  - type: bool
  - default: None
- fetchpriority:
  - description: Sets the priority for fetches initiated by the element.
  - type: auto | str
  - default: None
- integrity:
  - description: Integrity metadata used in Subresource Integrity checks.
  - type: str
  - default: None
- nomodule:
  - description: Prevents execution in user agents that support module scripts.
  - type: bool
  - default: None
- referrerpolicy:
  - description: Referrer policy for fetches initiated by the element.
  - type: none | str
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- type:
  - description: Type of script.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.search

Container for search controls.

```typst
#html.search(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.section

Generic document or application section.

```typst
#html.section(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.select

List box control.

```typst
#html.select(
  autocomplete: str | array,
  disabled: bool,
  form: str,
  multiple: bool,
  name: str,
  required: bool,
  size: int,
  body
) -> content
```

## Parameters

- autocomplete:
  - description: Hint for form autofill feature.
  - type: str | array
  - default: None
- disabled:
  - description: Whether the form control is disabled.
  - type: bool
  - default: None
- form:
  - description: Associates the element with a form element.
  - type: str
  - default: None
- multiple:
  - description: Whether to allow multiple values.
  - type: bool
  - default: None
- name:
  - description: Name of the element to use for form submission and in the form.elements API.
  - type: str
  - default: None
- required:
  - description: Whether the control is required for form submission.
  - type: bool
  - default: None
- size:
  - description: Size of the control.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.slot

Shadow tree slot.

```typst
#html.slot(
  name: str,
  body
) -> content
```

## Parameters

- name:
  - description: Name of shadow tree slot.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.small

Side comment.

```typst
#html.small(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.source

Image source for img or media source for video or audio.

```typst
#html.source(
  height: int,
  media: str,
  sizes: array,
  src: str,
  srcset: array,
  type: str,
  width: int
) -> content
```

## Parameters

- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- media:
  - description: Applicable media.
  - type: str
  - default: None
- sizes:
  - description: Image sizes for different page layouts. Expects an array of dictionaries with the keys `condition` (string) and `size` (length).
  - type: array
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- srcset:
  - description: Images to use in different situations, e.g., high-resolution displays, small monitors, etc. Expects an array of dictionaries with the keys `src` (string) and `width` (integer) or `density` (float).
  - type: array
  - default: None
- type:
  - description: Type of embedded resource.
  - type: str
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None

# html.span

Generic phrasing container.

```typst
#html.span(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.strong

Importance.

```typst
#html.strong(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.style

Embedded styling information.

```typst
#html.style(
  blocking: str | array,
  media: str,
  body
) -> content
```

## Parameters

- blocking:
  - description: Whether the element is potentially render-blocking.
  - type: str | array
  - default: None
- media:
  - description: Applicable media.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.sub

Subscript.

```typst
#html.sub(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.summary

Caption for details.

```typst
#html.summary(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.sup

Superscript.

```typst
#html.sup(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.table

Table.

```typst
#html.table(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.tbody

Group of rows in a table.

```typst
#html.tbody(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.td

Table cell.

```typst
#html.td(
  colspan: int,
  headers: str | array,
  rowspan: int,
  body
) -> content
```

## Parameters

- colspan:
  - description: Number of columns that the cell is to span.
  - type: int
  - default: None
- headers:
  - description: The header cells for this cell.
  - type: str | array
  - default: None
- rowspan:
  - description: Number of rows that the cell is to span.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.template

Template.

```typst
#html.template(
  shadowrootclonable: bool,
  shadowrootcustomelementregistry: bool,
  shadowrootdelegatesfocus: bool,
  shadowrootmode: str,
  shadowrootserializable: bool,
  body
) -> content
```

## Parameters

- shadowrootclonable:
  - description: Sets clonable on a declarative shadow root.
  - type: bool
  - default: None
- shadowrootcustomelementregistry:
  - description: Enables declarative shadow roots to indicate they will use a custom element registry.
  - type: bool
  - default: None
- shadowrootdelegatesfocus:
  - description: Sets delegates focus on a declarative shadow root.
  - type: bool
  - default: None
- shadowrootmode:
  - description: Enables streaming declarative shadow roots.
  - type: str
  - default: None
- shadowrootserializable:
  - description: Sets serializable on a declarative shadow root.
  - type: bool
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.textarea

Multiline text controls.

```typst
#html.textarea(
  autocomplete: str | array,
  cols: int,
  dirname: str,
  disabled: bool,
  form: str,
  maxlength: int,
  minlength: int,
  name: str,
  placeholder: str,
  readonly: bool,
  required: bool,
  rows: int,
  wrap: str,
  body
) -> content
```

## Parameters

- autocomplete:
  - description: Hint for form autofill feature.
  - type: str | array
  - default: None
- cols:
  - description: Maximum number of characters per line.
  - type: int
  - default: None
- dirname:
  - description: Name of form control to use for sending the element\'s directionality in form submission.
  - type: str
  - default: None
- disabled:
  - description: Whether the form control is disabled.
  - type: bool
  - default: None
- form:
  - description: Associates the element with a form element.
  - type: str
  - default: None
- maxlength:
  - description: Maximum length of value.
  - type: int
  - default: None
- minlength:
  - description: Minimum length of value.
  - type: int
  - default: None
- name:
  - description: Name of the element to use for form submission and in the form.elements API.
  - type: str
  - default: None
- placeholder:
  - description: User-visible label to be placed within the form control.
  - type: str
  - default: None
- readonly:
  - description: Whether to allow the value to be edited by the user.
  - type: bool
  - default: None
- required:
  - description: Whether the control is required for form submission.
  - type: bool
  - default: None
- rows:
  - description: Number of lines to show.
  - type: int
  - default: None
- wrap:
  - description: How the value of the form control is to be wrapped for form submission.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.tfoot

Group of footer rows in a table.

```typst
#html.tfoot(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.th

Table header cell.

```typst
#html.th(
  abbr: str,
  colspan: int,
  headers: str | array,
  rowspan: int,
  scope: str,
  body
) -> content
```

## Parameters

- abbr:
  - description: Alternative label to use for the header cell when referencing the cell in other contexts.
  - type: str
  - default: None
- colspan:
  - description: Number of columns that the cell is to span.
  - type: int
  - default: None
- headers:
  - description: The header cells for this cell.
  - type: str | array
  - default: None
- rowspan:
  - description: Number of rows that the cell is to span.
  - type: int
  - default: None
- scope:
  - description: Specifies which cells the header cell applies to.
  - type: str
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.thead

Group of heading rows in a table.

```typst
#html.thead(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.time

Machine-readable equivalent of date- or time-related data.

```typst
#html.time(
  datetime: datetime | duration,
  body
) -> content
```

## Parameters

- datetime:
  - description: Machine-readable value.
  - type: datetime | duration
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.title

Document title.

```typst
#html.title(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.tr

Table row.

```typst
#html.tr(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.track

Timed text track.

```typst
#html.track(
  default: bool,
  kind: str,
  label: str,
  src: str,
  srclang: str
) -> content
```

## Parameters

- default:
  - description: Enable the track if no other text track is more suitable.
  - type: bool
  - default: None
- kind:
  - description: The type of text track.
  - type: str
  - default: None
- label:
  - description: User-visible label.
  - type: str
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- srclang:
  - description: Language of the text track.
  - type: str
  - default: None

# html.u

Unarticulated annotation.

```typst
#html.u(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.ul

List.

```typst
#html.ul(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.var

Variable.

```typst
#html.var(
  body
) -> content
```

## Parameters

- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.video

Video player.

```typst
#html.video(
  autoplay: bool,
  controls: bool,
  crossorigin: str,
  height: int,
  loop: bool,
  muted: bool,
  playsinline: bool,
  poster: str,
  preload: none | auto | str,
  src: str,
  width: int,
  body
) -> content
```

## Parameters

- autoplay:
  - description: Hint that the media resource can be started automatically when the page is loaded.
  - type: bool
  - default: None
- controls:
  - description: Show user agent controls.
  - type: bool
  - default: None
- crossorigin:
  - description: How the element handles crossorigin requests.
  - type: str
  - default: None
- height:
  - description: Vertical dimension.
  - type: int
  - default: None
- loop:
  - description: Whether to loop the media resource.
  - type: bool
  - default: None
- muted:
  - description: Whether to mute the media resource by default.
  - type: bool
  - default: None
- playsinline:
  - description: Encourage the user agent to display video content within the element\'s playback area.
  - type: bool
  - default: None
- poster:
  - description: Poster frame to show prior to video playback.
  - type: str
  - default: None
- preload:
  - description: Hints how much buffering the media resource will likely need.
  - type: none | auto | str
  - default: None
- src:
  - description: Address of the resource.
  - type: str
  - default: None
- width:
  - description: Horizontal dimension.
  - type: int
  - default: None
- body:
  - description: The contents of the HTML element.
  - type: content
  - default: None

# html.wbr

Line breaking opportunity.


