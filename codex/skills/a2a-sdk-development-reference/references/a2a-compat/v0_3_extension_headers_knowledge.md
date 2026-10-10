# v0_3/extension_headers.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/extension_headers.py`. SHA-256: `c9504d278b31e5057ad7ccfab2f93f1b721d213d1fa550031b2540e82934137a`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Header lifetime and mutation

`LEGACY_HTTP_EXTENSION_HEADER` is `X-A2A-Extensions`, built from current `A2A-Extensions`. `add_legacy_extension_header(parameters)` mutates its mapping in place, returns `None`, and copies the current header value only when the exact current-case key exists and the exact legacy key does not. It never overwrites an explicit legacy value. This is case-sensitive mapping logic, even though HTTP itself is case-insensitive. Lowercase service parameter keys do not trigger mirroring. It does not parse or merge values.

Transports copy call-context service parameters before calling this helper; their extra header lives in request-local kwargs or metadata. No auth credential lookup occurs here. Use canonical-case `A2A-Extensions` when constructing `ClientCallContext.service_parameters` to obtain both headers.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
from a2a.client.service_parameters import ServiceParameters
from a2a.extensions.common import HTTP_EXTENSION_HEADER
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
LEGACY_HTTP_EXTENSION_HEADER = f'X-{HTTP_EXTENSION_HEADER}'
```

## Declaration-by-declaration execution reference

### `add_legacy_extension_header`

Source lines 15–27; declaration kind `FunctionDef`.

Inputs: `(parameters: ServiceParameters)`. Output annotation: `None`. Decorators: `none`.

Source intent: Mirrors the ``A2A-Extensions`` parameter under its legacy name in-place. Used by v0.3 compat client transports so that requests can be understood by older v0.3 servers that only recognize ``X-A2A-Extensions``.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `HTTP_EXTENSION_HEADER in parameters and LEGACY_HTTP_EXTENSION_HEADER not in parameters`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def add_legacy_extension_header(parameters: ServiceParameters) -> None:
    if HTTP_EXTENSION_HEADER in parameters and LEGACY_HTTP_EXTENSION_HEADER not in parameters:
        parameters[LEGACY_HTTP_EXTENSION_HEADER] = parameters[HTTP_EXTENSION_HEADER]
```

</details>
