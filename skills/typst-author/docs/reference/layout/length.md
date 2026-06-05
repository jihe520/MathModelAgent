# Length

A size or distance, possibly expressed with contextual units.

Typst supports the following length units:

- Points: `72pt`
- Millimeters: `254mm`
- Centimeters: `2.54cm`
- Inches: `1in`
- Relative to font size: `2.5em`

You can multiply lengths with and divide them by integers and floats.

## Example

```typst
#rect(width: 20pt)
#rect(width: 2em)
#rect(width: 1in)

#(3em + 5pt).em \
#(20pt).em \
#(40em + 2pt).abs \
#(5em).abs
```

## Fields

- `abs`: A length with just the absolute component of the current length (that is, excluding the `em` component).
- `em`: The amount of `em` units in this length, as a [float](/docs/reference/foundations/float/).


## Methods

## length.pt

Converts this length to points.

Fails with an error if this length has non-zero `em` units (such as `5em + 2pt` instead of just `2pt`). Use the `abs` field (such as in `(5em + 2pt).abs.pt()`) to ignore the `em` component of the length (thus converting only its absolute component).

## length.mm

Converts this length to millimeters.

Fails with an error if this length has non-zero `em` units. See the [`pt`](/docs/reference/layout/length/#definitions-pt) method for more details.

## length.cm

Converts this length to centimeters.

Fails with an error if this length has non-zero `em` units. See the [`pt`](/docs/reference/layout/length/#definitions-pt) method for more details.

## length.inches

Converts this length to inches.

Fails with an error if this length has non-zero `em` units. See the [`pt`](/docs/reference/layout/length/#definitions-pt) method for more details.

## length.to-absolute

Resolve this length to an absolute length.

```typst
#set text(size: 12pt)
#context [
  #(6pt).to-absolute() \
  #(6pt + 10em).to-absolute() \
  #(10em).to-absolute()
]

#set text(size: 6pt)
#context [
  #(6pt).to-absolute() \
  #(6pt + 10em).to-absolute() \
  #(10em).to-absolute()
]
```


