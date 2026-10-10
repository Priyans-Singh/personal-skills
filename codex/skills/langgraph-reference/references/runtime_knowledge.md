# `runtime.py`

`Runtime[Context]` is injectable into graph nodes/middleware and carries immutable context, optional store, stream writer, heartbeat, previous functional-workflow value, and execution/server metadata. `RunControl.request_drain()` requests cooperative stop at a superstep boundary. `get_runtime()` accesses the current runtime; long async functional tasks can call `heartbeat()` to avoid idle timeout.
