# `utils/constants.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/constants.py`. SHA-256: `b84e9f71430ba2f801b99e739e0d1f44c61299d81943e3618c6fe63ed75c6bd1`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
from enum import Enum
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
AGENT_CARD_WELL_KNOWN_PATH = '/.well-known/agent-card.json'
```

```python
DEFAULT_RPC_URL = '/'
```

```python
DEFAULT_LIST_TASKS_PAGE_SIZE = 50
```

```python
MAX_LIST_TASKS_PAGE_SIZE = 100
```

```python
JSONRPC_PARSE_ERROR_CODE = -32700
```

```python
VERSION_HEADER = 'A2A-Version'
```

```python
PROTOCOL_VERSION_1_0 = '1.0'
```

```python
PROTOCOL_VERSION_0_3 = '0.3'
```

```python
PROTOCOL_VERSION_CURRENT = PROTOCOL_VERSION_1_0
```

## Declarations and execution

### `TransportProtocol` (line 15)

Coverage ID: `constants.py:15:TransportProtocol`.

str/Enum constants JSONRPC, HTTP+JSON, GRPC. Used as binding selection labels; values do not instantiate transports or negotiate protocol.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class TransportProtocol(str, Enum):
    JSONRPC = 'JSONRPC'
    HTTP_JSON = 'HTTP+JSON'
    GRPC = 'GRPC'
```
