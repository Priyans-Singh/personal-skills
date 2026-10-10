# `cache/`

Cache node/work results, separate from checkpoints and stores. `base/__init__.py` defines `BaseCache`; `memory/__init__.py` provides process-local `InMemoryCache`; `redis/__init__.py` provides `RedisCache`. Use a cache for recomputable work, never as the only durable record.
