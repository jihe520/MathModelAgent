# Quote

# quote

Displays a quote alongside an optional attribution.

## Example

```typst
Plato is often misquoted as the author of #quote[I know that I know
nothing], however, this is a derivation form his original quote:

#set quote(block: true)

#quote(attribution: [Plato])[
  ... ἔοικα γοῦν τούτου γε σμικρῷ τινι αὐτῷ τούτῳ σοφώτερος εἶναι, ὅτι
  ἃ μὴ οἶδα οὐδὲ οἴομαι εἰδέναι.
]
#quote(attribution: [from the Henry Cary literal translation of 1897])[
  ... I seem, then, in just this little thing to be wiser than this man at
  any rate, that what I do not know I do not think I know either.
]
```

By default block quotes are padded left and right by `1em`, alignment and padding can be controlled with show rules:

```typst
#set quote(block: true)
#show quote: set align(center)
#show quote: set pad(x: 5em)

#quote[
  You cannot pass... I am a servant of the Secret Fire, wielder of the
  flame of Anor. You cannot pass. The dark fire will not avail you,
  flame of Udûn. Go back to the Shadow! You cannot pass.
]
```

```typst
#quote(
  block: bool,
  quotes: auto | bool,
  attribution: none | label | content,
  body
) -> content
```

## Parameters

- block:
  - description: Whether this is a block quote. ```typst An inline citation would look like this: #quote(  attribution: [René Descartes] )[  cogito, ergo sum ], and a block equation like this: #quote(  block: true,  attribution: [JFK] )[  Ich bin ein Berliner. ] ```
  - type: bool
  - default: false
- quotes:
  - description: Whether double quotes should be added around this quote. The double quotes used are inferred from the `quotes` property on [smartquote](/docs/reference/text/smartquote/), which is affected by the `lang` property on [text](/docs/reference/text/text/). - `true`: Wrap this quote in double quotes. - `false`: Do not wrap this quote in double quotes. - `auto`: Infer whether to wrap this quote in double quotes based on the `block` property. If `block` is `false`, double quotes are automatically added. ```typst #set text(lang: "de") Ein deutsch-sprechender Author zitiert unter umständen JFK: #quote[Ich bin ein Berliner.] #set text(lang: "en") And an english speaking one may translate the quote: #quote[I am a Berliner.] ```
  - type: auto | bool
  - default: auto
- attribution:
  - description: The attribution of this quote, usually the author or source. Can be a label pointing to a bibliography entry or any content. By default only displayed for block quotes, but can be changed using a `show` rule. ```typst #quote(attribution: [René Descartes])[  cogito, ergo sum ] #show quote.where(block: false): it => {  ["] + h(0pt, weak: true) + it.body + h(0pt, weak: true) + ["]  if it.attribution != none [ (#it.attribution)] } #quote(  attribution: link("https://typst.app/home")[typst.app] )[  Compose papers faster ] #set quote(block: true) #quote(attribution: <tolkien54>)[  You cannot pass... I am a servant  of the Secret Fire, wielder of the  flame of Anor. You cannot pass. The  dark fire will not avail you, flame  of Udûn. Go back to the Shadow! You  cannot pass. ] #bibliography("works.bib", style: "apa") ```
  - type: none | label | content
  - default: none
- body:
  - description: The quote.
  - type: content
  - default: None


