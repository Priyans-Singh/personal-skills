# `store/`

Cross-thread application data, distinct from checkpoints. `BaseStore` offers namespaced `get`, `put`, `search`, `delete`, and namespace listing; `base/batch.py` batches operations; `base/embed.py` resolves embedding/index paths. `InMemoryStore` is process-local and can perform vector search when configured. Namespace by tenant/user yourself: the store does not impose authorization. `delete` is destructive and TTL/index capabilities depend on the adapter.
