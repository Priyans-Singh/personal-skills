# `config.py`

Runtime-context accessors. `get_config()` returns the active `RunnableConfig`; `get_store()` returns the compiled/runtime store; `get_stream_writer()` writes `stream_mode="custom"` events. They must run inside a graph/runnable context; otherwise configuration access fails. Async context propagation requires Python 3.11+.
