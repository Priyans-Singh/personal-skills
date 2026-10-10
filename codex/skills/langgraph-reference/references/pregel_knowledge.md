# `pregel/`

The compiled-graph execution engine. `main.py` exposes `Pregel`/`NodeBuilder`; `_loop.py` runs sync/async supersteps; `_algo.py` prepares tasks/applies writes; `_read.py` and `_write.py` implement channel I/O; `_retry.py` owns retries/timeouts; `_runner.py` coordinates task failure/cancellation; `_checkpoint.py` restores/saves snapshots. `remote.py` runs remote graph behavior. Other files provide scheduling, stream callbacks, validation, drawing, debug payloads, and protocols. Use this directly only for advanced engine integrations.
