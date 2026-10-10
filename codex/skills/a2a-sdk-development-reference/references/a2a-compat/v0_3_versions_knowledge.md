# v0_3/versions.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/versions.py`. SHA-256: `f29d96fcde67db58bc0ebd1ffc53baea2fd093a9e9f080c1ee9f0255d4e9669f`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Execution and version distinction

`is_legacy_version(version)` returns false for `None`, empty strings, and `packaging.version.InvalidVersion`. Otherwise it parses PEP 440 versions and tests `Version('0.3') <= v < Version('1.0')`. This is a numeric interval, not strict membership in 0.3.x: 0.4 passes and 0.3rc1 precedes the lower bound. It performs no network negotiation. Card conversion uses it to filter usable interfaces; missing interface versions are independently accepted there.

Do not equate this test with server `validate_version`: the inspected external decorator compares **major only**, despite its docstring describing major/minor. An expected 0.3 handler therefore accepts valid 0.x values including 0.2. Missing context skips enforcement by using expected version; missing/empty HTTP version defaults to 0.3. Compatibility gRPC handler does not apply this decorator.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
from packaging.version import InvalidVersion, Version
from a2a.utils.constants import PROTOCOL_VERSION_0_3, PROTOCOL_VERSION_1_0
```

## Declaration-by-declaration execution reference

### `is_legacy_version`

Source lines 8–18; declaration kind `FunctionDef`.

Inputs: `(version: str | None)`. Output annotation: `bool`. Decorators: `none`.

Source intent: Determines if the given version is a legacy protocol version (>=0.3 and <1.0).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not version`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Runs guarded operations; catches `InvalidVersion` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `Version`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def is_legacy_version(version: str | None) -> bool:
    if not version:
        return False
    try:
        v = Version(version)
        return Version(PROTOCOL_VERSION_0_3) <= v < Version(PROTOCOL_VERSION_1_0)
    except InvalidVersion:
        return False
```

</details>
