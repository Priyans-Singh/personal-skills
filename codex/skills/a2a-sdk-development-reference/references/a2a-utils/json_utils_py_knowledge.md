# `utils/json_utils.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/json_utils.py`. SHA-256: `23b580cdd9ae44f641d8fb5d15547215b00020a8a2954b9e24c3a90bba76a8bc`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import json
from typing import Any
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

## Declarations and execution

### `dumps` (line 8)

Coverage ID: `json_utils.py:8:dumps`.

Calls json.dumps with ensure_ascii=False only. Returns Unicode str; caller must encode for wire. Default JSON separators, NaN handling, and TypeError behavior remain standard-library behavior.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)
```
