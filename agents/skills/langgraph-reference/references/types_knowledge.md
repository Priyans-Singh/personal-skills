# `types.py`

Shared public controls and data contracts: `Command` (update/goto/resume), `Send` (fan-out), `interrupt`, `RetryPolicy`, `TimeoutPolicy`, `CachePolicy`, `Overwrite`, state snapshots, tasks, and stream payloads. `interrupt()` requires a checkpointer and restarts the node on resume, so side effects before it must be idempotent or deferred.
