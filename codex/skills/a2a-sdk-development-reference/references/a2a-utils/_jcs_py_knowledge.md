# `utils/_jcs.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/_jcs.py`. SHA-256: `7819fff63662f565be8def76fbf7bc2d04776a70690e6f05664826d68f08603e`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
from __future__ import annotations
import math
import re
from typing import Any
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
MAX_DEPTH = 128
```

```python
_SAFE_INT_MAX = 2 ** 53 - 1
```

```python
_SAFE_INT_MIN = -2 ** 53 + 1
```

```python
_EXPONENT_EXPANSION_CEILING = 21
```

```python
_EXPONENT_EXPANSION_FLOOR = -7
```

```python
_ESCAPE_RE = re.compile('[\\x00-\\x1f\\\\"]')
```

```python
_ESCAPE_MAP = {'\\': '\\\\', '"': '\\"', '\x08': '\\b', '\x0c': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t'}
```

## Declarations and execution

### `CanonicalizationError` (line 62)

Coverage ID: `_jcs.py:62:CanonicalizationError`.

ValueError subclass for values without interoperable canonical JSON representation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class CanonicalizationError(ValueError):
    pass
```

### `canonicalize` (line 66)

Coverage ID: `_jcs.py:66:canonicalize`.

Builds output fragments via _write depth=0, joins to str, then UTF-8 encodes as validation. Unpaired surrogate becomes chained CanonicalizationError. Does not return bytes or hash.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def canonicalize(obj: Any) -> str:
    out: list[str] = []
    _write(obj, out, 0)
    canonical = ''.join(out)
    try:
        canonical.encode('utf-8')
    except UnicodeEncodeError as e:
        raise CanonicalizationError('value contains text that is not valid Unicode') from e
    return canonical
```

### `_write` (line 98)

Coverage ID: `_jcs.py:98:_write`.

Recursive fragment accumulator, rejects depth>128. list/tuple serialize as arrays; dict keys sorted by _sorted_items then _quote; scalar delegates _format_scalar. Cycles eventually hit depth bound. Mutates output list only.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _write(obj: Any, out: list[str], depth: int) -> None:
    if depth > MAX_DEPTH:
        raise CanonicalizationError(f'nesting exceeds the maximum depth of {MAX_DEPTH}')
    if isinstance(obj, (list, tuple)):
        out.append('[')
        for index, element in enumerate(obj):
            if index:
                out.append(',')
            _write(element, out, depth + 1)
        out.append(']')
    elif isinstance(obj, dict):
        out.append('{')
        for index, (key, value) in enumerate(_sorted_items(obj)):
            if index:
                out.append(',')
            out.append(_quote(key))
            out.append(':')
            _write(value, out, depth + 1)
        out.append('}')
    else:
        out.append(_format_scalar(obj))
```

### `_format_scalar` (line 125)

Coverage ID: `_jcs.py:125:_format_scalar`.

None/bool/int/float/str dispatch in that order (bool precedes int). Integers outside ±(2**53-1) rejected. float delegates _format_number; string _quote; unsupported type CanonicalizationError.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _format_scalar(obj: Any) -> str:
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, int):
        if obj < _SAFE_INT_MIN or obj > _SAFE_INT_MAX:
            raise CanonicalizationError(f'{obj} is outside the range of integers a JSON number can represent exactly')
        return str(obj)
    if isinstance(obj, float):
        return _format_number(obj)
    if isinstance(obj, str):
        return _quote(obj)
    raise CanonicalizationError(f'{type(obj).__name__} has no JSON representation')
```

### `_sorted_items` (line 148)

Coverage ID: `_jcs.py:148:_sorted_items`.

Returns sorted items by UTF-16 big-endian encoded keys. AttributeError becomes non-string-key CanonicalizationError; UnicodeEncodeError becomes invalid-key error. This does not guarantee every exotic key type yields canonical error (a bytes.encode missing method is handled; custom encode behavior can escape).

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _sorted_items(obj: dict[Any, Any]) -> list[tuple[str, Any]]:
    try:
        return sorted(obj.items(), key=lambda kv: kv[0].encode('utf-16-be'))
    except AttributeError as e:
        raise CanonicalizationError('object keys must be strings') from e
    except UnicodeEncodeError as e:
        raise CanonicalizationError('object key contains text that is not valid Unicode') from e
```

### `_quote` (line 167)

Coverage ID: `_jcs.py:167:_quote`.

Escapes backslash, quote, C0 controls with short escapes where mapped; leaves other Unicode literal. Regex substitution uses private lambda; UTF-8 validity checked at canonicalize boundary.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _quote(value: str) -> str:
    return '"' + _ESCAPE_RE.sub(lambda m: _ESCAPE_MAP[m.group(0)], value) + '"'
```

### `_format_number` (line 172)

Coverage ID: `_jcs.py:172:_format_number`.

Rejects NaN/infinity; both zero signs → 0. Negative recurses positive. Starts str(float), removes padded exponent zero/integral .0; expands positive exponent <21 and negative >-7 into decimal; otherwise exponent retained. Returns str, no numeric mutation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _format_number(value: float) -> str:
    if math.isnan(value) or math.isinf(value):
        raise CanonicalizationError(f'{value} is not a JSON number')
    if value == 0:
        return '0'
    if value < 0:
        return '-' + _format_number(-value)
    stringified = str(value)
    exponent_str = ''
    exponent_value = 0
    separator = stringified.find('e')
    if separator > 0:
        exponent_str = stringified[separator:]
        if exponent_str[2:3] == '0':
            exponent_str = exponent_str[:2] + exponent_str[3:]
        stringified = stringified[0:separator]
        exponent_value = int(exponent_str[1:])
    first = stringified
    dot = ''
    last = ''
    separator = stringified.find('.')
    if separator > 0:
        dot = '.'
        first = stringified[:separator]
        last = stringified[separator + 1:]
    if last == '0':
        dot = ''
        last = ''
    if 0 < exponent_value < _EXPONENT_EXPANSION_CEILING:
        first += last
        last = ''
        dot = ''
        exponent_str = ''
        first += '0' * (exponent_value - len(first) + 1)
    elif _EXPONENT_EXPANSION_FLOOR < exponent_value < 0:
        last = first + last
        first = '0'
        dot = '.'
        exponent_str = ''
        last = '0' * (-exponent_value - 1) + last
    return f'{first}{dot}{last}{exponent_str}'
```
