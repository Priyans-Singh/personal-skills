# v0_3/context_builders.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/context_builders.py`. SHA-256: `470322aa4ff3d76e038f6e460cf97f2b3c872e03056588df20e2f1d789241771`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Server identity and extensions

`V03ServerCallContextBuilder(inner)` and `V03GrpcServerCallContextBuilder(inner)` retain the builder, then call its `build` once per request. They mutate the returned `requested_extensions` set with a union of parsed legacy values and return that same context. They preserve user, tenant, state, and current extensions from the inner builder. The extension parser splits comma-separated values, trims whitespace, removes empties, and deduplicates in a set.

`_get_legacy_grpc_extensions(context)` reads invocation metadata, returns `[]` for `None`, matches metadata keys case-insensitively, and decodes byte values as UTF-8. Invalid byte sequences raise `UnicodeDecodeError`; nothing catches it here. Repeated values stay in the list until the common parser deduplicates them.

Default HTTP builder snapshots headers into context state and adapts middleware-provided user/auth. Without middleware user, it uses `UnauthenticatedUser`. Default gRPC builder stores the live gRPC context in state and uses an unauthenticated user; authentication requires a custom inner builder. Extension requests are capability negotiation data, not proof of identity. No context persistence, credential refresh, or authorization enforcement is added by this module.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
from typing import TYPE_CHECKING
from a2a.compat.v0_3.extension_headers import LEGACY_HTTP_EXTENSION_HEADER
from a2a.extensions.common import get_requested_extensions
from a2a.server.context import ServerCallContext
import grpc
from starlette.requests import Request
from a2a.server.request_handlers.grpc_handler import GrpcServerCallContextBuilder
from a2a.server.routes.common import ServerCallContextBuilder
```

## Declaration-by-declaration execution reference

### `_get_legacy_grpc_extensions`

Source lines 26–37; declaration kind `FunctionDef`.

Inputs: `(context: 'grpc.aio.ServicerContext')`. Output annotation: `list[str]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `md` from `context.invocation_metadata()`; output construction/calls here execute immediately when this method runs.
2. Branches on `md is None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Assigns `lower_key` from `LEGACY_HTTP_EXTENSION_HEADER.lower()`; output construction/calls here execute immediately when this method runs.
4. Returns `[e if isinstance(e, str) else e.decode('utf-8') for k, e in md if k.lower() == lower_key]`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.invocation_metadata`, `LEGACY_HTTP_EXTENSION_HEADER.lower`, `isinstance`, `e.decode`, `k.lower`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _get_legacy_grpc_extensions(context: 'grpc.aio.ServicerContext') -> list[str]:
    md = context.invocation_metadata()
    if md is None:
        return []
    lower_key = LEGACY_HTTP_EXTENSION_HEADER.lower()
    return [e if isinstance(e, str) else e.decode('utf-8') for k, e in md if k.lower() == lower_key]
```

</details>

### `V03ServerCallContextBuilder`

Source lines 40–56; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Wraps a ServerCallContextBuilder to also accept the legacy header. Recognizes the v0.3 ``X-A2A-Extensions`` HTTP header in addition to the spec ``A2A-Extensions``.

Declared operations: `__init__`, `build`. Each method is traced below; constructor determines retained state.

### `V03ServerCallContextBuilder.__init__`

Source lines 47–48; declaration kind `FunctionDef`.

Inputs: `(self, inner: 'ServerCallContextBuilder')`. Output annotation: `None`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self._inner` from `inner`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, inner: 'ServerCallContextBuilder') -> None:
    self._inner = inner
```

</details>

### `V03ServerCallContextBuilder.build`

Source lines 50–56; declaration kind `FunctionDef`.

Inputs: `(self, request: 'Request')`. Output annotation: `ServerCallContext`. Decorators: `none`.

Source intent: Builds a ServerCallContext, merging legacy extension headers.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `context` from `self._inner.build(request)`; output construction/calls here execute immediately when this method runs.
2. Updates `context.requested_extensions` with `get_requested_extensions(request.headers.getlist(LEGACY_HTTP_EXTENSION_HEADER))` using `BitOr`; mutable state may change in place.
3. Returns `context`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._inner.build`, `get_requested_extensions`, `request.headers.getlist`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def build(self, request: 'Request') -> ServerCallContext:
    context = self._inner.build(request)
    context.requested_extensions |= get_requested_extensions(request.headers.getlist(LEGACY_HTTP_EXTENSION_HEADER))
    return context
```

</details>

### `V03GrpcServerCallContextBuilder`

Source lines 59–75; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Wraps a GrpcServerCallContextBuilder to also accept the legacy metadata. Recognizes the v0.3 ``X-A2A-Extensions`` gRPC metadata key in addition to the spec ``A2A-Extensions``.

Declared operations: `__init__`, `build`. Each method is traced below; constructor determines retained state.

### `V03GrpcServerCallContextBuilder.__init__`

Source lines 66–67; declaration kind `FunctionDef`.

Inputs: `(self, inner: 'GrpcServerCallContextBuilder')`. Output annotation: `None`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self._inner` from `inner`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, inner: 'GrpcServerCallContextBuilder') -> None:
    self._inner = inner
```

</details>

### `V03GrpcServerCallContextBuilder.build`

Source lines 69–75; declaration kind `FunctionDef`.

Inputs: `(self, context: 'grpc.aio.ServicerContext')`. Output annotation: `ServerCallContext`. Decorators: `none`.

Source intent: Builds a ServerCallContext, merging legacy extension metadata.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `server_context` from `self._inner.build(context)`; output construction/calls here execute immediately when this method runs.
2. Updates `server_context.requested_extensions` with `get_requested_extensions(_get_legacy_grpc_extensions(context))` using `BitOr`; mutable state may change in place.
3. Returns `server_context`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._inner.build`, `get_requested_extensions`, `_get_legacy_grpc_extensions`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def build(self, context: 'grpc.aio.ServicerContext') -> ServerCallContext:
    server_context = self._inner.build(context)
    server_context.requested_extensions |= get_requested_extensions(_get_legacy_grpc_extensions(context))
    return server_context
```

</details>
