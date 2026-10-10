# `checkpoint/`

Per-thread execution persistence: snapshots, pending writes, replay, time travel, and interrupt/resume. `base/__init__.py` supplies `BaseCheckpointSaver`, checkpoint records, metadata and creation helpers; `base/id.py` creates sortable UUIDs. `memory/__init__.py` is local/debug-only. `serde/` contains serializer/cipher protocols, JSON-plus-msgpack encoding, optional encryption, events, and serializer types. Pass a saver to `compile()` and a stable `configurable.thread_id` at invocation; checkpointed values must serialize.
