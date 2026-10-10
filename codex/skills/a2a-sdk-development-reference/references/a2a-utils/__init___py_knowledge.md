# `utils/__init__.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/__init__.py`. SHA-256: `a9350876cae4bc9a636c2b556262ad4ccdaf39530bb2708d7d0c42480dee1e26`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
from a2a.utils import proto_utils
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH, DEFAULT_RPC_URL, TransportProtocol
from a2a.utils.proto_utils import to_stream_response
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
__all__ = ['AGENT_CARD_WELL_KNOWN_PATH', 'DEFAULT_RPC_URL', 'TransportProtocol', 'proto_utils', 'to_stream_response']
```

## Declarations and execution
