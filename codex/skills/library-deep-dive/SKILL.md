---
name: library-deep-dive
description: "Create a deep, execution-oriented Markdown reference for a local library or package, tracing every source file, public API, helper, and integration. Use only when explicitly invoked for thorough library analysis; do not use for ordinary code review or a narrow API question."
---

# Library Deep Dive

Create a source-grounded Markdown guide that lets the reader understand how the library executes, not merely what its names are.

## Scope and outcome

Treat the requested library/package directory as the primary source of truth. Include every source file under it, including private helpers, integrations, model/value modules, generated-looking wrappers, README examples when they explain behavior, and direct supporting files outside it that the package imports to implement its public behavior.

Do not duplicate a sibling package merely because it shares a name. Include it only when it is a direct implementation dependency; state why it is included and leave unrelated sibling modules for their own guide.

Create one or more clearly named `*_knowledge.md` files in the user's workspace unless they specify another location. The guide must include:

- a mental model and identity/resource hierarchy where applicable;
- end-to-end execution flows for the most important paths;
- module/package map and public import surface;
- function/class-level explanation of behavior, inputs, output, side effects, error behavior, and delegation where meaningful;
- integrations and framework adapters;
- lifecycle, async/concurrency, authorization, retry, consistency, and destructive-operation semantics when present;
- operational failure modes and safe defaults;
- a callable index proving no helper was silently skipped.

## Workflow

1. Inventory source files before writing. Use fast path-aware file discovery and include nested integration directories.
2. Identify the primary public entry points, then trace from each through its called helpers, client/service boundaries, serialization, callbacks, and state transitions.
3. Inspect implementation, not only docstrings or README examples. Capture non-obvious behavior such as local validation, defaulting, implicit I/O, response normalization, dynamic forwarding, buffering, retries, status polling, and error swallowing.
4. Separate stable concepts from version-sensitive observations. State the inspected source location/version/date when it helps the reader avoid treating the guide as universal documentation.
5. Explain function families compactly only when they are genuine identity-inserting delegates or mechanically identical wrappers. Otherwise document their distinct behavior.
6. Validate coverage mechanically after drafting. For a language with parseable source, enumerate declared callables/classes and compare their names against the guide. Investigate every omission; do not use a name-only check as a substitute for explaining behavior.
7. Run whitespace/format checks appropriate to the workspace. Report created files and validation outcome succinctly.

Read [the language routing guide](references/language-routing.md) before inventory when the package language is not obvious or is not Python.

## Evidence rules

- Prefer source code over generated documentation for implementation claims.
- Mark inferred behavior as inference; do not claim an external service guarantee that local code cannot establish.
- Preserve exact distinction between control plane/data plane, configuration/runtime, and persistence/cache layers when the source makes one.
- Describe credentials and tokens by destination and lifetime. Do not reproduce secrets, raw credentials, or authorization data.
- Do not invoke cloud APIs, create resources, or make destructive calls merely to document a library. Source inspection is read-only unless the user separately asks for a live test.

## Quality bar

The reader should be able to answer: “What object exists when?”, “What call happens next?”, “Which inputs become wire fields?”, “What is persisted or retried?”, and “Which errors are surfaced, transformed, or swallowed?” If the guide cannot answer these for a core path, keep tracing.
