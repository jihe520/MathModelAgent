# State

Manages stateful parts of your document.

Let's say you have some computations in your document and want to remember the result of your last computation to use it in the next one. You might try something similar to the code below and expect it to output 10, 13, 26, and 21. However this **does not work** in Typst. If you test this code, you will see that Typst complains with the following error message: _Variables from
outside the function are read-only and cannot be modified._

```typst
// This doesn't work!
#let star = 0
#let compute(expr) = {
  star = eval(
    expr.replace("⭐", str(star))
  )
  [New value is #star.]
}

#compute("10") \
#compute("⭐ + 3") \
#compute("⭐ * 2") \
#compute("⭐ - 5")
```

## State and document markup

Why does it do that? Because, in general, this kind of computation with side effects is problematic in document markup and Typst is upfront about that. For the results to make sense, the computation must proceed in the same order in which the results will be laid out in the document. In our simple example, that's the case, but in general it might not be.

Let's look at a slightly different, but similar kind of state: The heading numbering. We want to increase the heading counter at each heading. Easy enough, right? Just add one. Well, it's not that simple. Consider the following example:

```typst
#set heading(numbering: "1.")
#let template(body) = [
  = Outline
  ...
  #body
]

#show: template

= Introduction
...
```

Here, Typst first processes the body of the document after the show rule, sees the `Introduction` heading, then passes the resulting content to the `template` function and only then sees the `Outline`. Just counting up would number the `Introduction` with `1` and the `Outline` with `2`.

## Managing state in Typst

So what do we do instead? We use Typst's state management system. Calling the `state` function with an identifying string key and an optional initial value gives you a state value which exposes a few functions. The two most important ones are `get` and `update`:

- The [`get`](/docs/reference/introspection/state/#definitions-get) function retrieves the current value of the state. Because the value can vary over the course of the document, it is a _contextual_ function that can only be used when [context](/docs/reference/context/) is available.
- The [`update`](/docs/reference/introspection/state/#definitions-update) function modifies the state. You can give it any value. If given a non-function value, it sets the state to that value. If given a function, that function receives the previous state and has to return the new state.

Our initial example would now look like this:

```typst
#let star = state("star", 0)
#let compute(expr) = {
  star.update(old =>
    eval(expr.replace("⭐", str(old)))
  )
  [New value is #context star.get().]
}

#compute("10") \
#compute("⭐ + 3") \
#compute("⭐ * 2") \
#compute("⭐ - 5")
```

State managed by Typst is always updated in layout order, not in evaluation order. The `update` method returns content and its effect occurs at the position where the returned content is inserted into the document.

As a result, we can now also store some of the computations in variables, but they still show the correct results:

```typst
...

#let more = [
  #compute("⭐ * 2") \
  #compute("⭐ - 5")
]

#compute("10") \
#compute("⭐ + 3") \
#more
```

This example is of course a bit silly, but in practice this is often exactly what you want! A good example are heading counters, which is why Typst's [counting system](/docs/reference/introspection/counter/) is very similar to its state system.

## Time Travel

By using Typst's state management system you also get time travel capabilities! We can find out what the value of the state will be at any position in the document from anywhere else. In particular, the `at` method gives us the value of the state at any particular location and the `final` methods gives us the value of the state at the end of the document.

```typst
...

Value at `<here>` is
#context star.at(<here>)

#compute("10") \
#compute("⭐ + 3") \
*Here.* <here> \
#compute("⭐ * 2") \
#compute("⭐ - 5")
```

## A word of caution

To resolve the values of all states, Typst evaluates parts of your code multiple times. However, there is no guarantee that your state manipulation can actually be completely resolved.

For instance, if you generate state updates depending on the final value of a state, the results might never converge. The example below illustrates this. We initialize our state with `1` and then update it to its own final value plus 1. So it should be `2`, but then its final value is `2`, so it should be `3`, and so on. This example displays a finite value because Typst simply gives up after a few attempts.

```typst
// This is bad!
#let x = state("key", 1)
#context x.update(x.final() + 1)
#context x.get()
```

In general, you should try not to generate state updates from within context expressions. If possible, try to express your updates as non-contextual values or functions that compute the new value from the previous value. Sometimes, it cannot be helped, but in those cases it is up to you to ensure that the result converges.

## Constructor
## state

Create a new state identified by a key.

```typst
#state(
  key,
  init
) -> state
```

### Parameters

- key:
  - description: The key that identifies this state. Any [updates](/docs/reference/introspection/state/#definitions-update) to the state will be identified with the string key. If you construct multiple states with the same `key`, then updating any one will affect all of them.
  - type: str
  - default: None
- init:
  - description: The initial value of the state. If you construct multiple states with the same `key` but different `init` values, they will each use their own initial value but share updates. Specifically, the value of a state at some location in the document will be computed from that state\'s initial value and all preceding updates for the state\'s key. ```typst #let banana = state("key", "🍌") #let broccoli = state("key", "🥦") #banana.update(it => it + "😋") #context [  - #state("key", "🍎").get()  - #banana.get()  - #broccoli.get() ] ```
  - type: any
  - default: none


## Methods

## state.get

Retrieves the value of the state at the current location.

This is equivalent to `state.at(here())`.

## state.at

Retrieves the value of the state at the given selector's unique match.

The `selector` must match exactly one element in the document. The most useful kinds of selectors for this are [labels](/docs/reference/foundations/label/) and [locations](/docs/reference/introspection/location/).

```typst
#state.at(
  selector
) -> any
```

### Parameters

- selector:
  - description: The place at which the state\'s value should be retrieved.
  - type: label | selector | location | function
  - default: None

## state.final

Retrieves the value of the state at the end of the document.

## state.update

Updates the value of the state.

Returns an invisible piece of [content](/docs/reference/foundations/content/) that must be inserted into the document to take effect. This invisible content tells Typst that the specified update should take place wherever the content is inserted into the document.

State is a part of your document and runs like a thread embedded in the document content. The value of a state is the result of all state updates that happened in the document up until that point.

That's why `state.update` returns an invisible sliver of content that you need to return and include in the document — a state update that is not "placed" in the document does not happen, and "when" it happens is determined by where you place it. That's also why you need [context](/docs/reference/context/) to read state: You need to use the current document position to know where on the state's "thread" you are.

Storing a state update in a variable (e.g. `let my-update = state("key").update(c => c * 2)`) will have no effect by itself. Only once you insert the variable `#my-update` somewhere into the document content, the update will take effect — at the position where it was inserted. You can also use `#my-update` multiple times at different positions. Then, the update will take effect multiple times as well.

In contrast to [`get`](/docs/reference/introspection/state/#definitions-get), [`at`](/docs/reference/introspection/state/#definitions-at), and [`final`](/docs/reference/introspection/state/#definitions-final), this function does not require [context](/docs/reference/context/). This is because, to create the state update, we do not need to know where in the document we are. We only need this information to resolve the state's value.

```typst
#state.update(
  update
) -> content
```

### Parameters

- update:
  - description: A value to update to or a function to update with. - If given a non-function value, sets the state to that value. - If given a function, that function receives the state\'s previous value and has to return the state\'s new value. When updating the state based on its previous value, you should prefer the function form instead of retrieving the previous value from the [context](/docs/reference/context/). This allows the compiler to resolve the final state efficiently, minimizing the number of [layout iterations](/docs/reference/context/#compiler-iterations) required. In the following example, `fill.update(f => not f)` will paint odd [items in the bullet list](/docs/reference/model/list/#definitions-item) as expected. However, if it\'s replaced with `context fill.update(not fill.get())`, then layout will not converge within 5 attempts, as each update will take one additional iteration to propagate. ```typst #let fill = state("fill", false) #show list.item: it => {  fill.update(f => not f)  context {   set text(fill: fuchsia) if fill.get()   it  } } #lorem(5).split().map(list.item).join() ```
  - type: any | function
  - default: None


