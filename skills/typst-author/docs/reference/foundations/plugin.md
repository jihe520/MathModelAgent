# Plugin

# plugin

Loads a WebAssembly module.

The resulting [module](/docs/reference/foundations/module/) will contain one Typst [function](/docs/reference/foundations/function/) for each function export of the loaded WebAssembly module.

Typst WebAssembly plugins need to follow a specific [protocol](/docs/reference/foundations/plugin/#protocol). To run as a plugin, a program needs to be compiled to a 32-bit shared WebAssembly library. Plugin functions may accept multiple [byte buffers](/docs/reference/foundations/bytes/) as arguments and return a single byte buffer. They should typically be wrapped in idiomatic Typst functions that perform the necessary conversions between native Typst types and bytes by leveraging [`str`](/docs/reference/foundations/str/#constructor), [`bytes`](/docs/reference/foundations/bytes/#constructor), and [data loading functions](/docs/reference/data-loading/).

For security reasons, plugins run in isolation from your system. This means that printing, reading files, or similar things are not supported.

## Example

```typst
#let myplugin = plugin("hello.wasm")
#let concat(a, b) = str(
  myplugin.concatenate(
    bytes(a),
    bytes(b),
  )
)

#concat("hello", "world")
```

Since the plugin function returns a module, it can be used with import syntax:

```typst
#import plugin("hello.wasm"): concatenate
```

## Purity

Plugin functions **must be pure:** A plugin function call must not have any observable side effects on future plugin calls and given the same arguments, it must always return the same value.

The reason for this is that Typst functions must be pure (which is quite fundamental to the language design) and, since Typst function can call plugin functions, this requirement is inherited. In particular, if a plugin function is called twice with the same arguments, Typst might cache the results and call your function only once. Moreover, Typst may run multiple instances of your plugin in multiple threads, with no state shared between them.

Typst does not enforce plugin function purity (for efficiency reasons), but calling an impure function will lead to unpredictable and irreproducible results and must be avoided.

That said, mutable operations _can be_ useful for plugins that require costly runtime initialization. Due to the purity requirement, such initialization cannot be performed through a normal function call. Instead, Typst exposes a [plugin transition API](/docs/reference/foundations/plugin/#definitions-transition), which executes a function call and then creates a derived module with new functions which will observe the side effects produced by the transition call. The original plugin remains unaffected.

## Plugins and Packages

Any Typst code can make use of a plugin simply by including a WebAssembly file and loading it. However, because the byte-based plugin interface is quite low-level, plugins are typically exposed through a package containing the plugin and idiomatic wrapper functions.

## WASI

Many compilers will use the [WASI ABI](https://wasi.dev/) by default or as their only option (e.g. emscripten), which allows printing, reading files, etc. This ABI will not directly work with Typst. You will either need to compile to a different target or [stub all functions](https://github.com/astrale-sharp/wasm-minimal-protocol/tree/master/crates/wasi-stub).

## Protocol

To be used as a plugin, a WebAssembly module must conform to the following protocol:

### Exports

A plugin module can export functions to make them callable from Typst. To conform to the protocol, an exported function should:

- Take `n` 32-bit integer arguments `a_1`, `a_2`, ..., `a_n` (interpreted as lengths, so `usize/size_t` may be preferable), and return one 32-bit integer.
- The function should first allocate a buffer `buf` of length `a_1 + a_2 + ... + a_n`, and then call `wasm_minimal_protocol_write_args_to_buffer(buf.ptr)`.
- The `a_1` first bytes of the buffer now constitute the first argument, the `a_2` next bytes the second argument, and so on.
- The function can now do its job with the arguments and produce an output buffer. Before returning, it should call `wasm_minimal_protocol_send_result_to_host` to send its result back to the host.
- To signal success, the function should return `0`.
- To signal an error, the function should return `1`. The written buffer is then interpreted as an UTF-8 encoded error message.

### Imports

Plugin modules need to import two functions that are provided by the runtime. (Types and functions are described using WAT syntax.)

- `(import "typst_env" "wasm_minimal_protocol_write_args_to_buffer" (func (param i32)))` Writes the arguments for the current function into a plugin-allocated buffer. When a plugin function is called, it [receives the lengths](#exports) of its input buffers as arguments. It should then allocate a buffer whose capacity is at least the sum of these lengths. It should then call this function with a `ptr` to the buffer to fill it with the arguments, one after another.
- `(import "typst_env" "wasm_minimal_protocol_send_result_to_host" (func (param i32 i32)))` Sends the output of the current function to the host (Typst). The first parameter shall be a pointer to a buffer (`ptr`), while the second is the length of that buffer (`len`). The memory pointed at by `ptr` can be freed immediately after this function returns. If the message should be interpreted as an error message, it should be encoded as UTF-8.

## Resources

For more resources, check out the [wasm-minimal-protocol repository](https://github.com/astrale-sharp/wasm-minimal-protocol). It contains:

- A list of example plugin implementations and a test runner for these examples
- Wrappers to help you write your plugin in Rust (Zig wrapper in development)
- A stubber for WASI

```typst
#plugin(
  source
) -> module
```

## Parameters

- source:
  - description: A [path](/docs/reference/syntax/#paths) to a WebAssembly file or raw WebAssembly bytes.
  - type: str | bytes
  - default: None


## Definitions
### plugin.transition

Calls a plugin function that has side effects and returns a new module with plugin functions that are guaranteed to have observed the results of the mutable call.

Note that calling an impure function through a normal function call (without use of the transition API) is forbidden and leads to unpredictable behaviour. Read the [section on purity](/docs/reference/foundations/plugin/#purity) for more details.

In the example below, we load the plugin `hello-mut.wasm` which exports two functions: The `get()` function retrieves a global array as a string. The `add(value)` function adds a value to the global array.

We call `add` via the transition API. The call `mutated.get()` on the derived module will observe the addition. Meanwhile the original module remains untouched as demonstrated by the `base.get()` call.

_Note:_ Due to limitations in the internal WebAssembly implementation, the transition API can only guarantee to reflect changes in the plugin's memory, not in WebAssembly globals. If your plugin relies on changes to globals being visible after transition, you might want to avoid use of the transition API for now. We hope to lift this limitation in the future.

```typst
#let base = plugin("hello-mut.wasm")
#assert.eq(base.get(), "[]")

#let mutated = plugin.transition(base.add, "hello")
#assert.eq(base.get(), "[]")
#assert.eq(mutated.get(), "[hello]")
```

```typst
#plugin.transition(
  func,
  arguments
) -> module
```

#### Parameters

- func:
  - description: The plugin function to call.
  - type: function
  - default: None
- arguments:
  - description: The byte buffers to call the function with.
  - type: bytes
  - default: None


