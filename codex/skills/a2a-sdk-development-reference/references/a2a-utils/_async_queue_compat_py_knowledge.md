# `utils/_async_queue_compat.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/_async_queue_compat.py`. SHA-256: `aa2f776d08e557597859547df72e02eaa5aef962befc086060082947bdd2dfbe`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import sys
from typing import Any
from asyncio import Queue as AsyncQueue
from asyncio import QueueShutDown
import culsans
from culsans import AsyncQueue
from culsans import AsyncQueueShutDown as QueueShutDown
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
__all__ = ['AsyncQueue', 'QueueShutDown', 'create_async_queue']
```

## Declarations and execution

### `create_async_queue` (line 12)

Coverage ID: `_async_queue_compat.py:12:create_async_queue`.

Conditional duplicate declaration: Python ≥3.13 returns asyncio.Queue(maxsize); older Python returns culsans.Queue(maxsize).async_q. maxsize=0 means unbounded. QueueShutDown aliases selected implementation; caller owns queue shutdown/backpressure. No retry or persistence.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def create_async_queue(maxsize: int=0) -> AsyncQueue[Any]:
    return AsyncQueue(maxsize=maxsize)
```

### `create_async_queue` (line 23)

Coverage ID: `_async_queue_compat.py:23:create_async_queue`.

Conditional duplicate declaration: Python ≥3.13 returns asyncio.Queue(maxsize); older Python returns culsans.Queue(maxsize).async_q. maxsize=0 means unbounded. QueueShutDown aliases selected implementation; caller owns queue shutdown/backpressure. No retry or persistence.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def create_async_queue(maxsize: int=0) -> AsyncQueue[Any]:
    return culsans.Queue(maxsize=maxsize).async_q
```
