# Accent

# math.accent

Attaches an accent to a base.

## Example

```typst
$grave(a) = accent(a, `)$ \
$arrow(a) = accent(a, arrow)$ \
$tilde(a) = accent(a, \u{0303})$
```

```typst
#math.accent(
  base,
  accent,
  size: relative,
  dotless: bool
) -> content
```

## Parameters

- base:
  - description: The base to which the accent is applied. May consist of multiple letters. ```typst $arrow(A B C)$ ```
  - type: content
  - default: None
- accent:
  - description: The accent to apply to the base. Supported accents include: | Accent | Name | Codepoint | | --- | --- | --- | | Grave | `grave` | ``` | | Acute | `acute` | `´` | | Circumflex | `hat` | `^` | | Tilde | `tilde` | `~` | | Macron | `macron` | `¯` | | Dash | `dash` | `‾` | | Breve | `breve` | `˘` | | Dot | `dot` | `.` | | Double dot, Diaeresis | `dot.double`, `diaer` | `¨` | | Triple dot | `dot.triple` | `⃛` | | Quadruple dot | `dot.quad` | `⃜` | | Circle | `circle` | `∘` | | Double acute | `acute.double` | `˝` | | Caron | `caron` | `ˇ` | | Right arrow | `arrow`, `->` | `→` | | Left arrow | `arrow.l`, `<-` | `←` | | Left/Right arrow | `arrow.l.r` | `↔` | | Right harpoon | `harpoon` | `⇀` | | Left harpoon | `harpoon.lt` | `↼` |
  - type: str | content
  - default: None
- size:
  - description: The size of the accent, relative to the width of the base. ```typst $dash(A, size: #150%)$ ```
  - type: relative
  - default: 100 % + 0pt
- dotless:
  - description: Whether to remove the dot on top of lowercase i and j when adding a top accent. This enables the `dtls` OpenType feature. ```typst $hat(dotless: #false, i)$ ```
  - type: bool
  - default: true


