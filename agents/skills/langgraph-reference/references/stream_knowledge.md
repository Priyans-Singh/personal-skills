# `stream/`

Structured output during a graph run. `run_stream.py` provides sync/async run and subgraph stream wrappers; `transformers.py` turns runtime activity into values, updates, messages, lifecycle, checkpoints, debug, task, or subgraph events. `_mux.py`, `_convert.py`, `_types.py`, and `stream_channel.py` are event plumbing. Application code normally calls a compiled graph's `stream()` or `astream()`.
