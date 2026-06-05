# Counter

Counts through pages, elements, and more.

With the counter function, you can access and modify counters for pages, headings, figures, and more. Moreover, you can define custom counters for other things you want to count.

Since counters change throughout the course of the document, their current value is _contextual._ It is recommended to read the chapter on [context](/docs/reference/context/) before continuing here.

## Accessing a counter

To access the raw value of a counter, we can use the [`get`](/docs/reference/introspection/counter/#definitions-get) function. This function returns an [array](/docs/reference/foundations/array/): Counters can have multiple levels (in the case of headings for sections, subsections, and so on), and each item in the array corresponds to one level.

```typst
#set heading(numbering: "1.")

= Introduction
Raw value of heading counter is
#context counter(heading).get()
```

## Displaying a counter

Often, we want to display the value of a counter in a more human-readable way. To do that, we can call the [`display`](/docs/reference/introspection/counter/#definitions-display) function on the counter. This function retrieves the current counter value and formats it either with a provided or with an automatically inferred [numbering](/docs/reference/model/numbering/).

```typst
#set heading(numbering: "1.")

= Introduction
Some text here.

= Background
The current value is: #context {
  counter(heading).display()
}

Or in roman numerals: #context {
  counter(heading).display("I")
}
```

## Modifying a counter

To modify a counter, you can use the `step` and `update` methods:

- The `step` method increases the value of the counter by one. Because counters can have multiple levels , it optionally takes a `level` argument. If given, the counter steps at the given depth.
- The `update` method allows you to arbitrarily modify the counter. In its basic form, you give it an integer (or an array for multiple levels). For more flexibility, you can instead also give it a function that receives the current value and returns a new value.

The heading counter is stepped before the heading is displayed, so `Analysis` gets the number seven even though the counter is at six after the second update.

```typst
#set heading(numbering: "1.")

= Introduction
#counter(heading).step()

= Background
#counter(heading).update(3)
#counter(heading).update(n => n * 2)

= Analysis
Let's skip 7.1.
#counter(heading).step(level: 2)

== Analysis
Still at #context {
  counter(heading).display()
}
```

## Page counter

The page counter is special. It is automatically stepped at each pagebreak. But like other counters, you can also step it manually. For example, you could have Roman page numbers for your preface, then switch to Arabic page numbers for your main content and reset the page counter to one.

```typst
#set page(numbering: "(i)")

= Preface
The preface is numbered with
roman numerals.

#set page(numbering: "1 / 1")
#counter(page).update(1)

= Main text
Here, the counter is reset to one.
We also display both the current
page and total number of pages in
Arabic numbers.
```

## Custom counters

To define your own counter, call the `counter` function with a string as a key. This key identifies the counter globally.

```typst
#let mine = counter("mycounter")
#context mine.display() \
#mine.step()
#context mine.display() \
#mine.update(c => c * 3)
#context mine.display()
```

## How to step

When you define and use a custom counter, in general, you should first step the counter and then display it. This way, the stepping behaviour of a counter can depend on the element it is stepped for. If you were writing a counter for, let's say, theorems, your theorem's definition would thus first include the counter step and only then display the counter and the theorem's contents.

```typst
#let c = counter("theorem")
#let theorem(it) = block[
  #c.step()
  *Theorem #context c.display():*
  #it
]

#theorem[$1 = 1$]
#theorem[$2 < 3$]
```

The rationale behind this is best explained on the example of the heading counter: An update to the heading counter depends on the heading's level. By stepping directly before the heading, we can correctly step from `1` to `1.1` when encountering a level 2 heading. If we were to step after the heading, we wouldn't know what to step to.

Because counters should always be stepped before the elements they count, they always start at zero. This way, they are at one for the first display (which happens after the first step).

## Time travel

Counters can travel through time! You can find out the final value of the counter before it is reached and even determine what the value was at any particular location in the document.

```typst
#let mine = counter("mycounter")

= Values
#context [
  Value here: #mine.get() \
  At intro: #mine.at(<intro>) \
  Final value: #mine.final()
]

#mine.update(n => n + 3)

= Introduction <intro>
#lorem(10)

#mine.step()
#mine.step()
```

## Other kinds of state

The `counter` type is closely related to [state](/docs/reference/introspection/state/) type. Read its documentation for more details on state management in Typst and why it doesn't just use normal variables for counters.

## Constructor
## counter

Create a new counter identified by a key.

```typst
#counter(
  key
) -> counter
```

### Parameters

- key:
  - description: The key that identifies this counter globally. - If it is a string, creates a custom counter that is only affected by manual updates, - If it is the [`page`](/docs/reference/layout/page/) function, counts through pages, - If it is a [selector](/docs/reference/foundations/selector/), counts through elements that match the selector. For example,  - provide an element function: counts elements of that type,  - provide a [`where`](/docs/reference/foundations/function/#definitions-where) selector: counts a type of element with specific fields,  - provide a [`<label>`](/docs/reference/foundations/label/): counts elements with that label.
  - type: str | label | selector | location | function
  - default: None


## Methods

## counter.get

Retrieves the value of the counter at the current location. Always returns an array of integers, even if the counter has just one number.

This is equivalent to `counter.at(here())`.

## counter.display

Displays the current value of the counter with a numbering and returns the formatted output.

```typst
#counter.display(
  numbering,
  both: bool
) -> any
```

### Parameters

- numbering:
  - description: A [numbering pattern or a function](/docs/reference/model/numbering/), which specifies how to display the counter. If given a function, that function receives each number of the counter as a separate argument. If the amount of numbers varies, e.g. for the heading argument, you can use an [argument sink](/docs/reference/foundations/arguments/). If this is omitted or set to `auto`, displays the counter with the numbering style for the counted element or with the pattern `"1.1"` if no such style exists.
  - type: auto | str | function
  - default: auto
- both:
  - description: If enabled, displays the current and final top-level count together. Both can be styled through a single numbering pattern. This is used by the page numbering property to display the current and total number of pages when a pattern like `"1 / 1"` is given.
  - type: bool
  - default: false

## counter.at

Retrieves the value of the counter at the given location. Always returns an array of integers, even if the counter has just one number.

The `selector` must match exactly one element in the document. The most useful kinds of selectors for this are [labels](/docs/reference/foundations/label/) and [locations](/docs/reference/introspection/location/).

```typst
#counter.at(
  selector
) -> int array
```

### Parameters

- selector:
  - description: The place at which the counter\'s value should be retrieved.
  - type: label | selector | location | function
  - default: None

## counter.final

Retrieves the value of the counter at the end of the document. Always returns an array of integers, even if the counter has just one number.

## counter.step

Increases the value of the counter by one.

The update will be in effect at the position where the returned content is inserted into the document. If you don't put the output into the document, nothing happens! This would be the case, for example, if you write `let _ = counter(page).step()`. Counter updates are always applied in layout order and in that case, Typst wouldn't know when to step the counter.

```typst
#counter.step(
  level: int
) -> content
```

### Parameters

- level:
  - description: The depth at which to step the counter. Defaults to `1`.
  - type: int
  - default: 1

## counter.update

Updates the value of the counter.

Just like with `step`, the update only occurs if you put the resulting content into the document.

```typst
#counter.update(
  update
) -> content
```

### Parameters

- update:
  - description: If given an integer or array of integers, sets the counter to that value. If given a function, that function receives the previous counter value (with each number as a separate argument) and has to return the new value (integer or array).
  - type: int | array | function
  - default: None


