# Spacing (H)

# h

Inserts horizontal spacing into a paragraph.

The spacing can be absolute, relative, or fractional. In the last case, the remaining space on the line is distributed among all fractional spacings according to their relative fractions.

## Example

```typst
First #h(1cm) Second \
First #h(30%) Second
```

## Fractional spacing

With fractional spacing, you can align things within a line without forcing a paragraph break (like [`align`](/docs/reference/layout/align/) would). Each fractionally sized element gets space based on the ratio of its fraction to the sum of all fractions.

```typst
First #h(1fr) Second \
First #h(1fr) Second #h(1fr) Third \
First #h(2fr) Second #h(1fr) Third
```

## Mathematical Spacing

In [mathematical formulas](/docs/reference/math/), you can additionally use these constants to add spacing between elements: `thin` (1/6 em), `med` (2/9 em), `thick` (5/18 em), `quad` (1 em), `wide` (2 em).

```typst
#h(
  amount,
  weak: bool
) -> content
```

## Parameters

- amount:
  - description: How much spacing to insert.
  - type: relative | fraction
  - default: None
- weak:
  - description: If `true`, the spacing collapses at the start or end of a paragraph. Moreover, from multiple adjacent weak spacings all but the largest one collapse. Weak spacing in markup also causes all adjacent markup spaces to be removed, regardless of the amount of spacing inserted. To force a space next to weak spacing, you can explicitly write `#" "` (for a normal space) or `~` (for a non-breaking space). The latter can be useful to create a construct that always attaches to the preceding word with one non-breaking space, independently of whether a markup space existed in front or not. ```typst #h(1cm, weak: true) We identified a group of _weak_ specimens that fail to manifest in most cases. However, when #h(8pt, weak: true) supported #h(8pt, weak: true) on both sides, they do show up. Further #h(0pt, weak: true) more, even the smallest of them swallow adjacent markup spaces. ```
  - type: bool
  - default: false


