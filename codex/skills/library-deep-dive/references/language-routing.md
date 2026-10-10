# Language Routing

Choose the cheapest reliable inventory and declaration check for the source language. Do not force a language-specific parser when a package contains multiple languages; inventory each relevant source set and document cross-language boundaries.

| Source | Inventory and callable coverage approach |
|---|---|
| Python | Inspect `*.py`; use `ast` to enumerate functions, async functions, and classes. Include nested functions when they materially implement a public flow. |
| JavaScript / TypeScript | Inspect `*.js`, `*.mjs`, `*.cjs`, `*.ts`, `*.tsx`; trace exports, classes, functions, and framework registration. Use installed parser/tooling only when available; otherwise combine precise text search with manual source inspection. |
| Go | Inspect `*.go`; trace exported types/functions, methods, interface implementations, package initialization, and context/error propagation. |
| Java / Kotlin | Inspect source roots; trace public API, overloads, annotations, dependency injection/configuration, async/reactive boundaries, and exception translation. |
| Rust | Inspect crate modules, `pub` API, traits/implementations, macros that create behavior, feature gates, and `Result` propagation. |
| Other / mixed | Establish file extensions and the package's public entrypoint first. Use the ecosystem's available static tooling where practical, then verify important paths directly in source. |

For generated bindings, distinguish generated request-shape code from handwritten orchestration. Still index both if they are inside scope, but focus explanation on the points where applications enter, values are transformed, requests are dispatched, or errors are handled.
