# `utils/errors.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/errors.py`. SHA-256: `dc637617d06887f5c6a12b8d034b19dfdb85a0cecb895639ac2ff1c8fff5ed38`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
from typing import NamedTuple
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
__all__ = ['A2A_ERROR_MAPPING', 'A2A_ERROR_REASONS', 'A2A_REASON_TO_ERROR', 'A2A_REST_ERROR_MAPPING', 'JSON_RPC_ERROR_CODE_MAP', 'ErrorMapping', 'ExtensionSupportRequiredError', 'InternalError', 'InvalidAgentResponseError', 'InvalidParamsError', 'InvalidRequestError', 'JSONParseError', 'MethodNotFoundError', 'PushNotificationNotSupportedError', 'TaskNotCancelableError', 'TaskNotFoundError', 'UnsupportedOperationError', 'VersionNotSupportedError']
```

```python
JSON_RPC_ERROR_CODE_MAP: dict[type[A2AError], int] = {TaskNotFoundError: -32001, TaskNotCancelableError: -32002, PushNotificationNotSupportedError: -32003, UnsupportedOperationError: -32004, ContentTypeNotSupportedError: -32005, InvalidAgentResponseError: -32006, ExtendedAgentCardNotConfiguredError: -32007, ExtensionSupportRequiredError: -32008, VersionNotSupportedError: -32009, InvalidParamsError: -32602, InvalidRequestError: -32600, MethodNotFoundError: -32601, InternalError: -32603, JSONParseError: -32700}
```

```python
A2A_ERROR_MAPPING: dict[type[A2AError], ErrorMapping] = {TaskNotFoundError: ErrorMapping(404, 'NOT_FOUND', 'TASK_NOT_FOUND'), TaskNotCancelableError: ErrorMapping(400, 'FAILED_PRECONDITION', 'TASK_NOT_CANCELABLE'), PushNotificationNotSupportedError: ErrorMapping(400, 'FAILED_PRECONDITION', 'PUSH_NOTIFICATION_NOT_SUPPORTED'), UnsupportedOperationError: ErrorMapping(400, 'FAILED_PRECONDITION', 'UNSUPPORTED_OPERATION'), ContentTypeNotSupportedError: ErrorMapping(400, 'INVALID_ARGUMENT', 'CONTENT_TYPE_NOT_SUPPORTED'), InvalidAgentResponseError: ErrorMapping(500, 'INTERNAL', 'INVALID_AGENT_RESPONSE'), ExtendedAgentCardNotConfiguredError: ErrorMapping(400, 'FAILED_PRECONDITION', 'EXTENDED_AGENT_CARD_NOT_CONFIGURED'), ExtensionSupportRequiredError: ErrorMapping(400, 'FAILED_PRECONDITION', 'EXTENSION_SUPPORT_REQUIRED'), VersionNotSupportedError: ErrorMapping(400, 'FAILED_PRECONDITION', 'VERSION_NOT_SUPPORTED'), InvalidParamsError: ErrorMapping(400, 'INVALID_ARGUMENT', 'INVALID_PARAMS'), InvalidRequestError: ErrorMapping(400, 'INVALID_ARGUMENT', 'INVALID_REQUEST'), MethodNotFoundError: ErrorMapping(404, 'NOT_FOUND', 'METHOD_NOT_FOUND'), InternalError: ErrorMapping(500, 'INTERNAL', 'INTERNAL_ERROR')}
```

```python
A2A_REST_ERROR_MAPPING = A2A_ERROR_MAPPING
```

```python
A2A_ERROR_REASONS = {cls: mapping.reason for cls, mapping in A2A_ERROR_MAPPING.items()}
```

```python
A2A_REASON_TO_ERROR = {mapping.reason: cls for cls, mapping in A2A_ERROR_MAPPING.items()}
```

## Declarations and execution

### `ErrorMapping` (line 10)

Coverage ID: `errors.py:10:ErrorMapping`.

NamedTuple of HTTP integer, gRPC status-name string, and reason. Maps are keyed by exact exception type rather than inheritance.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class ErrorMapping(NamedTuple):
    http_code: int
    grpc_status: str
    reason: str
```

### `A2AError` (line 18)

Coverage ID: `errors.py:18:A2AError`.

Base Exception storing message and data. Truthy custom message replaces class default; empty message does not. Data is retained by reference, not scrubbed or copied; error handlers expose it to clients and logs.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class A2AError(Exception):
    message: str = 'A2A Error'
    data: dict | None = None

    def __init__(self, message: str | None=None, data: dict | None=None):
        if message:
            self.message = message
        self.data = data
        super().__init__(self.message)
```

### `A2AError.__init__` (line 24)

Coverage ID: `errors.py:24:A2AError.__init__`.

Accepts optional message/data, stores data, passes effective message to Exception.__init__. No field validation, transport code, credentials handling, or retry state.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def __init__(self, message: str | None=None, data: dict | None=None):
    if message:
        self.message = message
    self.data = data
    super().__init__(self.message)
```

### `TaskNotFoundError` (line 31)

Coverage ID: `errors.py:31:TaskNotFoundError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class TaskNotFoundError(A2AError):
    message = 'Task not found'
```

### `TaskNotCancelableError` (line 37)

Coverage ID: `errors.py:37:TaskNotCancelableError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class TaskNotCancelableError(A2AError):
    message = 'Task cannot be canceled'
```

### `PushNotificationNotSupportedError` (line 43)

Coverage ID: `errors.py:43:PushNotificationNotSupportedError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class PushNotificationNotSupportedError(A2AError):
    message = 'Push Notification is not supported'
```

### `UnsupportedOperationError` (line 49)

Coverage ID: `errors.py:49:UnsupportedOperationError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class UnsupportedOperationError(A2AError):
    message = 'This operation is not supported'
```

### `ContentTypeNotSupportedError` (line 55)

Coverage ID: `errors.py:55:ContentTypeNotSupportedError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class ContentTypeNotSupportedError(A2AError):
    message = 'Incompatible content types'
```

### `InternalError` (line 61)

Coverage ID: `errors.py:61:InternalError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class InternalError(A2AError):
    message = 'Internal error'
```

### `InvalidAgentResponseError` (line 67)

Coverage ID: `errors.py:67:InvalidAgentResponseError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class InvalidAgentResponseError(A2AError):
    message = 'Invalid agent response'
```

### `ExtendedAgentCardNotConfiguredError` (line 73)

Coverage ID: `errors.py:73:ExtendedAgentCardNotConfiguredError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class ExtendedAgentCardNotConfiguredError(A2AError):
    message = 'Authenticated Extended Card is not configured'
```

### `InvalidParamsError` (line 79)

Coverage ID: `errors.py:79:InvalidParamsError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class InvalidParamsError(A2AError):
    message = 'Invalid params'
```

### `InvalidRequestError` (line 85)

Coverage ID: `errors.py:85:InvalidRequestError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class InvalidRequestError(A2AError):
    message = 'Invalid Request'
```

### `MethodNotFoundError` (line 91)

Coverage ID: `errors.py:91:MethodNotFoundError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class MethodNotFoundError(A2AError):
    message = 'Method not found'
```

### `JSONParseError` (line 97)

Coverage ID: `errors.py:97:JSONParseError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class JSONParseError(A2AError):
    message = 'Invalid JSON payload'
```

### `ExtensionSupportRequiredError` (line 103)

Coverage ID: `errors.py:103:ExtensionSupportRequiredError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class ExtensionSupportRequiredError(A2AError):
    message = 'Extension support required'
```

### `VersionNotSupportedError` (line 109)

Coverage ID: `errors.py:109:VersionNotSupportedError`.

A2AError subclass; inherits constructor/data/message override semantics. Default message is shown in class body below. Exact class keys in errors.py decide HTTP/gRPC/JSON-RPC mappings; this class itself never sends a response.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class VersionNotSupportedError(A2AError):
    message = 'Version not supported'
```
