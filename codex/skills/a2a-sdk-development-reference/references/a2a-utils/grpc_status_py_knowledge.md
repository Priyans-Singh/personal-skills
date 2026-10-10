# `utils/grpc_status.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/grpc_status.py`. SHA-256: `c8f6f49bcb1e4bb5827694eb913471a61bcbb1643bb736d15286239a27866ea4`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import logging
from typing import Any, NamedTuple
from google.rpc import status_pb2
import grpc
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
logger = logging.getLogger(__name__)
```

```python
GRPC_STATUS_DETAILS_BIN_KEY = 'grpc-status-details-bin'
```

## Declarations and execution

### `GrpcStatus` (line 19)

Coverage ID: `grpc_status.py:19:GrpcStatus`.

NamedTuple(code, details, trailing_metadata); code is runtime grpc.StatusCode; metadata carries serialized google.rpc.Status.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class GrpcStatus(NamedTuple):
    code: Any
    details: str
    trailing_metadata: tuple
```

### `status_to_grpc` (line 27)

Coverage ID: `grpc_status.py:27:status_to_grpc`.

Requires grpc or raises explicit ImportError. Matches status.code against grpc.StatusCode numeric values; unknown code raises ValueError. Serializes entire Status into grpc-status-details-bin trailer and returns GrpcStatus; no RPC occurs.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def status_to_grpc(status: status_pb2.Status) -> GrpcStatus:
    if grpc is None:
        raise ImportError('gRPC is not installed. Install with: pip install a2a-sdk[grpc]')
    for x in grpc.StatusCode:
        if x.value[0] == status.code:
            grpc_code = x
            break
    else:
        raise ValueError(f'Invalid status code {status.code}')
    bin_data = status.SerializeToString()
    metadata = ((GRPC_STATUS_DETAILS_BIN_KEY, bin_data),)
    return GrpcStatus(grpc_code, status.message, metadata)
```

### `status_from_call` (line 46)

Coverage ID: `grpc_status.py:46:status_from_call`.

Requires grpc. Calls synchronous trailing_metadata(); absent accessor/empty metadata/no matching key yields None. Parses first matching binary trailer, validates numeric code and exact message against call.code()/details(); mismatch ValueError and malformed protobuf DecodeError propagate. Not suitable for awaitable metadata accessors without adaptation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def status_from_call(call: Any) -> status_pb2.Status | None:
    if grpc is None:
        raise ImportError('gRPC is not installed. Install with: pip install a2a-sdk[grpc]')
    if not hasattr(call, 'trailing_metadata'):
        return None
    trailing_metadata = call.trailing_metadata()
    if not trailing_metadata:
        return None
    for k, v in trailing_metadata:
        if k == GRPC_STATUS_DETAILS_BIN_KEY:
            status = status_pb2.Status()
            status.ParseFromString(v)
            if call.code().value[0] != status.code:
                raise ValueError(f'Mismatched status code: proto={status.code}, call={call.code()}')
            if call.details() != status.message:
                raise ValueError(f'Mismatched status message: proto={status.message!r}, call={call.details()!r}')
            return status
    return None
```
