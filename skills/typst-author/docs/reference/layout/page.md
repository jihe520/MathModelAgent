# Page

# page

Layouts its child onto one or multiple pages.

Although this function is primarily used in set rules to affect page properties, it can also be used to explicitly render its argument onto a set of pages of its own.

Pages can be set to use `auto` as their width or height. In this case, the pages will grow to fit their content on the respective axis.

The [Guide for Page Setup](/docs/guides/page-setup/) explains how to use this and related functions to set up a document with many examples.

## Example

```typst
#set page("us-letter")

There you go, US friends!
```

## Accessibility

The contents of the page's header, footer, foreground, and background are invisible to Assistive Technology (AT) like screen readers. Only the body of the page is read by AT. Do not include vital information not included elsewhere in the document in these areas.

```typst
#page(
  paper: str,
  width: auto | length,
  height: auto | length,
  flipped: bool,
  margin: auto | relative | dictionary,
  binding: auto | alignment,
  columns: int,
  fill: none | auto | color | gradient | tiling,
  numbering: none | str | function,
  supplement: none | auto | content,
  number-align: alignment,
  header: none | auto | content,
  header-ascent: relative,
  footer: none | auto | content,
  footer-descent: relative,
  background: none | content,
  foreground: none | content,
  body: content
) -> content
```

## Parameters

- paper:
  - description: A standard paper size to set width and height. This is just a shorthand for setting `width` and `height` and, as such, cannot be retrieved in a context expression.
  - type: str
  - default: "a4"
- width:
  - description: The width of the page. ```typst #set page(  width: 3cm,  margin: (x: 0cm), ) #for i in range(3) {  box(square(width: 1cm)) } ```
  - type: auto | length
  - default: 595.28pt
- height:
  - description: The height of the page. If this is set to `auto`, page breaks can only be triggered manually by inserting a [page break](/docs/reference/layout/pagebreak/) or by adding another non-empty page set rule. Most examples throughout this documentation use `auto` for the height of the page to dynamically grow and shrink to fit their content.
  - type: auto | length
  - default: 841.89pt
- flipped:
  - description: Whether the page is flipped into landscape orientation. ```typst #set page(  "us-business-card",  flipped: true,  fill: rgb("f2e5dd"), ) #set align(bottom + end) #text(14pt)[*Sam H. Richards*] \\ _Procurement Manager_ #set text(10pt) 17 Main Street \\ New York, NY 10001 \\ +1 555 555 5555 ```
  - type: bool
  - default: false
- margin:
  - description: The page\'s margins. - `auto`: The margins are set automatically to 2.5/21 times the smaller dimension of the page. This results in 2.5 cm margins for an A4 page. - A single length: The same margin on all sides. - A dictionary: With a dictionary, the margins can be set individually. The dictionary can contain the following keys in order of precedence:  - `top`: The top margin.  - `right`: The right margin.  - `bottom`: The bottom margin.  - `left`: The left margin.  - `inside`: The margin at the inner side of the page (where the [binding](/docs/reference/layout/page/#parameters-binding) is).  - `outside`: The margin at the outer side of the page (opposite to the [binding](/docs/reference/layout/page/#parameters-binding)).  - `x`: The horizontal margins.  - `y`: The vertical margins.  - `rest`: The margins on all sides except those for which the dictionary explicitly sets a size. All keys are optional; omitted keys will use their previously set value, or the default margin if never set. In addition, the values for `left` and `right` are mutually exclusive with the values for `inside` and `outside`. ```typst #set page( width: 3cm, height: 4cm, margin: (x: 8pt, y: 4pt), ) #rect(  width: 100%,  height: 100%,  fill: aqua, ) ```
  - type: auto | relative | dictionary
  - default: auto
- binding:
  - description: On which side the pages will be bound. - `auto`: Equivalent to `left` if the [text direction](/docs/reference/text/text/#parameters-dir) is left-to-right and `right` if it is right-to-left. - `left`: Bound on the left side. - `right`: Bound on the right side. This affects the meaning of the `inside` and `outside` options for margins.
  - type: auto | alignment
  - default: auto
- columns:
  - description: How many columns the page has. If you need to insert columns into a page or other container, you can also use the [`columns` function](/docs/reference/layout/columns/). ```typst #set page(columns: 2, height: 4.8cm) Climate change is one of the most pressing issues of our time, with the potential to devastate communities, ecosystems, and economies around the world. It\'s clear that we need to take urgent action to reduce our carbon emissions and mitigate the impacts of a rapidly changing climate. ```
  - type: int
  - default: 1
- fill:
  - description: The page\'s background fill. Setting this to something non-transparent instructs the printer to color the complete page. If you are considering larger production runs, it may be more environmentally friendly and cost-effective to source pre-dyed pages and not set this property. When set to `none`, the background becomes transparent. Note that PDF pages will still appear with a (usually white) background in viewers, but they are actually transparent. (If you print them, no color is used for the background.) The default of `auto` results in `none` for PDF output, and `white` for PNG and SVG. ```typst #set page(fill: rgb("444352")) #set text(fill: rgb("fdfdfd")) *Dark mode enabled.* ```
  - type: none | auto | color | gradient | tiling
  - default: auto
- numbering:
  - description: How to number the pages. You can refer to the Page Setup Guide for [customizing page numbers](/docs/guides/page-setup/#page-numbers). Accepts a [numbering pattern or function](/docs/reference/model/numbering/) taking one or two numbers: 1. The first number is the current page number. 2. The second number is the total number of pages. In a numbering pattern, the second number can be omitted. If a function is passed, it will receive one argument in the context of links or references, and two arguments when producing the visible page numbers. These are logical numbers controlled by the page counter, and may thus not match the physical numbers. Specifically, they are the [current](/docs/reference/introspection/counter/#definitions-get) and the [final](/docs/reference/introspection/counter/#definitions-final) value of `counter(page)`. See the [`counter`](/docs/reference/introspection/counter/#page-counter) documentation for more details. If an explicit [`footer`](/docs/reference/layout/page/#parameters-footer) (or [`header`](/docs/reference/layout/page/#parameters-header) for [top-aligned](/docs/reference/layout/page/#parameters-number-align) numbering) is given, the numbering is ignored. ```typst #set page(  height: 100pt,  margin: (top: 16pt, bottom: 24pt),  numbering: "1 / 1", ) #lorem(48) ```
  - type: none | str | function
  - default: none
- supplement:
  - description: A supplement for the pages. For page references, this is added before the page number. ```typst #set page(numbering: "1.", supplement: [p.]) = Introduction <intro> We are on #ref(<intro>, form: "page")! ```
  - type: none | auto | content
  - default: auto
- number-align:
  - description: The alignment of the page numbering. If the vertical component is `top`, the numbering is placed into the header and if it is `bottom`, it is placed in the footer. Horizon alignment is forbidden. If an explicit matching `header` or `footer` is given, the numbering is ignored. ```typst #set page(  margin: (top: 16pt, bottom: 24pt),  numbering: "1",  number-align: right, ) #lorem(30) ```
  - type: alignment
  - default: center + bottom
- header:
  - description: The page\'s header. Fills the top margin of each page. - Content: Shows the content as the header. - `auto`: Shows the page number if a [`numbering`](/docs/reference/layout/page/#parameters-numbering) is set and [`number-align`](/docs/reference/layout/page/#parameters-number-align) is `top`. - `none`: Suppresses the header. ```typst #set par(justify: true) #set page(  margin: (top: 32pt, bottom: 20pt),  header: [   #set text(8pt)   #smallcaps[Typst Academy]   #h(1fr) _Exercise Sheet 3_  ], ) #lorem(19) ```
  - type: none | auto | content
  - default: auto
- header-ascent:
  - description: The amount the header is raised into the top margin.
  - type: relative
  - default: 30 % + 0pt
- footer:
  - description: The page\'s footer. Fills the bottom margin of each page. - Content: Shows the content as the footer. - `auto`: Shows the page number if a [`numbering`](/docs/reference/layout/page/#parameters-numbering) is set and [`number-align`](/docs/reference/layout/page/#parameters-number-align) is `bottom`. - `none`: Suppresses the footer. For just a page number, the `numbering` property typically suffices. If you want to create a custom footer but still display the page number, you can directly access the [page counter](/docs/reference/introspection/counter/). ```typst #set par(justify: true) #set page(  height: 100pt,  margin: 20pt,  footer: context [   #set align(right)   #set text(8pt)   #counter(page).display(    "1 of I",    both: true,   )  ] ) #lorem(48) ```
  - type: none | auto | content
  - default: auto
- footer-descent:
  - description: The amount the footer is lowered into the bottom margin.
  - type: relative
  - default: 30 % + 0pt
- background:
  - description: Content in the page\'s background. This content will be placed behind the page\'s body. It can be used to place a background image or a watermark. ```typst #set page(background: rotate(24deg,  text(18pt, fill: rgb("FFCBC4"))[   *CONFIDENTIAL*  ] )) = Typst\'s secret plans In the year 2023, we plan to take over the world (of typesetting). ```
  - type: none | content
  - default: none
- foreground:
  - description: Content in the page\'s foreground. This content will overlay the page\'s body. ```typst #set page(foreground: text(24pt)[🤓]) Reviewer 2 has marked our paper "Weak Reject" because they did not understand our approach... ```
  - type: none | content
  - default: none
- body:
  - description: The contents of the page(s). Multiple pages will be created if the content does not fit on a single page. A new page with the page properties prior to the function invocation will be created after the body has been typeset.
  - type: content
  - default: []


