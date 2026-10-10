# `func/`

Function-style durable workflows. `@task` turns sync/async work into a future-like, checkpoint-aware work unit; call `.result()` or await it, allowing fan-out. `@entrypoint` creates a runnable workflow with optional checkpointer/store/cache; `entrypoint.final(value, save)` returns one value while persisting another as `previous`. Tasks must be called from an entrypoint or graph and their checkpointed inputs/outputs must serialize.
