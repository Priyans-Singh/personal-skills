# `utils/task.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/task.py`. SHA-256: `96e2a55554b30626e34b4b4635db7a0b954c8905fe488f32cab8bf7506ad9820`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import binascii
from base64 import b64decode, b64encode
from typing import Literal, Protocol, runtime_checkable
from a2a.types.a2a_pb2 import Task
from a2a.utils.constants import MAX_LIST_TASKS_PAGE_SIZE
from a2a.utils.errors import InvalidParamsError
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
_ENCODING = 'utf-8'
```

## Declarations and execution

### `HistoryLengthConfig` (line 14)

Coverage ID: `task.py:14:HistoryLengthConfig`.

Runtime-checkable structural protocol: history_length integer plus HasField; no data is allocated or validated by the protocol itself.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
@runtime_checkable
class HistoryLengthConfig(Protocol):
    history_length: int

    def HasField(self, field_name: Literal['history_length']) -> bool:
        """Checks if a field is set.

        This method name matches the generated Protobuf code.
        """
        ...
```

### `HistoryLengthConfig.HasField` (line 19)

Coverage ID: `task.py:19:HistoryLengthConfig.HasField`.

Protocol declaration only. Concrete protobuf configuration answers whether optional history_length is set; implementation is supplied by the caller.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def HasField(self, field_name: Literal['history_length']) -> bool:
    ...
```

### `validate_history_length` (line 27)

Coverage ID: `task.py:27:validate_history_length`.

Rejects negative config.history_length with InvalidParamsError. None passes; presence is not checked. Returns None; does not mutate configuration.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def validate_history_length(config: HistoryLengthConfig | None) -> None:
    if config and config.history_length < 0:
        raise InvalidParamsError(message='history length must be non-negative')
```

### `apply_history_length` (line 33)

Coverage ID: `task.py:33:apply_history_length`.

Uses HasField to distinguish absent from explicitly zero. None/absent, empty history, or already-short history returns the original Task identity. Zero with history copies and clears history. Positive shorter limit copies and retains newest suffix. Negative is left unchanged: call validate_history_length separately. Copies retain status/artifacts/metadata; no persistence update.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def apply_history_length(task: Task, config: HistoryLengthConfig | None) -> Task:
    if config is None or not config.HasField('history_length'):
        return task
    history_length = config.history_length
    if history_length == 0:
        if not task.history:
            return task
        task_copy = Task()
        task_copy.CopyFrom(task)
        task_copy.ClearField('history')
        return task_copy
    if history_length > 0 and task.history:
        if len(task.history) <= history_length:
            return task
        task_copy = Task()
        task_copy.CopyFrom(task)
        del task_copy.history[:-history_length]
        return task_copy
    return task
```

### `validate_page_size` (line 73)

Coverage ID: `task.py:73:validate_page_size`.

Returns None for integers 1..100; below 1 or above MAX_LIST_TASKS_PAGE_SIZE raises InvalidParamsError with the respective bound. No automatic defaulting or type coercion.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def validate_page_size(page_size: int) -> None:
    if page_size < 1:
        raise InvalidParamsError(message='minimum page size is 1')
    if page_size > MAX_LIST_TASKS_PAGE_SIZE:
        raise InvalidParamsError(message=f'maximum page size is {MAX_LIST_TASKS_PAGE_SIZE}')
```

### `encode_page_token` (line 90)

Coverage ID: `task.py:90:encode_page_token`.

UTF-8 task ID → standard base64 ASCII string. Reversible cursor, not encryption, signature, authorization, or stable snapshot.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def encode_page_token(task_id: str) -> str:
    return b64encode(task_id.encode(_ENCODING)).decode(_ENCODING)
```

### `decode_page_token` (line 102)

Coverage ID: `task.py:102:decode_page_token`.

Adds missing base64 padding, decodes UTF-8. binascii.Error and UnicodeDecodeError become InvalidParamsError chained from original. b64decode uses default non-strict validation; junk may be ignored and empty input yields empty ID.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def decode_page_token(page_token: str) -> str:
    encoded_str = page_token
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += '=' * (4 - missing_padding)
    try:
        decoded = b64decode(encoded_str.encode(_ENCODING)).decode(_ENCODING)
    except (binascii.Error, UnicodeDecodeError) as e:
        raise InvalidParamsError('Token is not a valid base64-encoded cursor.') from e
    return decoded
```
