# Introspection

Interactions between document parts.

This category is home to Typst's introspection capabilities: With the `counter` function, you can access and manipulate page, section, figure, and equation counters or create custom ones. Meanwhile, the `query` function lets you search for elements in the document to construct things like a list of figures or headers which show the current chapter title.

Most of the functions are _contextual._ It is recommended to read the chapter on [context](/docs/reference/context/) before continuing here.

## Definitions

| Name | Description |
| --- | --- |
| [`counter`](/reference/introspection/counter/) | Counts through pages, elements, and more. |
| [`here`](/reference/introspection/here/) | Provides the current location in the document. |
| [`locate`](/reference/introspection/locate/) | Determines the location of an element in the document. |
| [`location`](/reference/introspection/location/) | Identifies an element in the document. |
| [`metadata`](/reference/introspection/metadata/) | Exposes a value to the query system without producing visible content. |
| [`query`](/reference/introspection/query/) | Finds elements in the document. |
| [`state`](/reference/introspection/state/) | Manages stateful parts of your document. |

