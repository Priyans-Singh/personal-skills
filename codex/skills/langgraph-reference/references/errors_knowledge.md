# `errors.py`

Execution exceptions and error codes. Key surfaced failures: `InvalidUpdateError` for invalid/conflicting writes, `GraphRecursionError` for loop limits, `EmptyInputError`, `NodeTimeoutError`, and task lookup errors. `GraphInterrupt` is engine control flow; use `interrupt()` instead of the deprecated `NodeInterrupt`. `GraphDrained` indicates cooperative stop with a resumable checkpoint.
