# v0_3/rest_adapter.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/rest_adapter.py`. SHA-256: `4b00f81a05925444fb5c407deeef1e497c630332263069da4293d34119ae3d1e`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## HTTP routes and response lifetime

`REST03Adapter` constructs REST03Handler and a legacy-aware context builder. `routes()` returns partial-bound handlers, not an ASGI app and not registered routes. Mount `(path, method)` entries in the outer app. It supports POST send/stream/cancel, GET and POST subscribe, GET task, GET config, POST config-create, GET config-list, and GET `/v1/card`. No ListTasks or push-config DELETE route exists. Paths retain `/v1/` despite 0.3 wire protocol.

`_handle_request` builds context, awaits method(request, context), wraps dict in JSONResponse and is decorated by external rest_error_handler. `_handle_streaming_request` first `await request.body()` to pre-consume it for SSE; ValueError/RuntimeError/OSError become InvalidRequestError. It builds context and nested event_generator json_utils.dumps each item, then EventSourceResponse. The external stream decorator converts construction-time errors to JSONResponse, but logs and re-raises iteration errors after headers, rather than emitting JSON-RPC error envelopes.

Optional import guard sets Request/Response/EventSourceResponse to Any when packages absent; no constructor check enforces availability, so attempted response creation can fail later. In the inspected environment Starlette and sse-starlette are available. Inner builder owns user identity and auth; no credentials are acquired, persisted or refreshed. Disconnect/cancel behavior is framework-owned; no retries or stream replay here.

```python
from a2a.compat.v0_3.rest_adapter import REST03Adapter
adapter = REST03Adapter(core_handler)
route_map = adapter.routes()  # pass these entries to the application's route setup
assert ('/v1/tasks/{id}:subscribe', 'POST') in route_map
```

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import functools
import logging
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Callable
from typing import TYPE_CHECKING, Any
from a2a.compat.v0_3.context_builders import V03ServerCallContextBuilder
from a2a.compat.v0_3.rest_handler import REST03Handler
from a2a.server.routes.common import DefaultServerCallContextBuilder, ServerCallContextBuilder
from a2a.utils import json_utils
from a2a.utils.error_handlers import rest_error_handler, rest_stream_error_handler
from a2a.utils.errors import InvalidRequestError
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from a2a.server.context import ServerCallContext
from a2a.server.request_handlers.request_handler import RequestHandler
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
```

## Declaration-by-declaration execution reference

### `REST03Adapter`

Source lines 52–154; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Adapter to make RequestHandler work with v0.3 RESTful API. Defines v0.3 REST request processors and their routes, as well as managing response generation including Server-Sent Events (SSE).

Declared operations: `__init__`, `_handle_request`, `_handle_streaming_request`, `routes`. Each method is traced below; constructor determines retained state.

### `REST03Adapter.__init__`

Source lines 58–66; declaration kind `FunctionDef`.

Inputs: `(self, http_handler: 'RequestHandler', context_builder: 'ServerCallContextBuilder | None'=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.handler` from `REST03Handler(request_handler=http_handler)`; output construction/calls here execute immediately when this method runs.
2. Assigns `self._context_builder` from `V03ServerCallContextBuilder(context_builder or DefaultServerCallContextBuilder())`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `REST03Handler`, `V03ServerCallContextBuilder`, `DefaultServerCallContextBuilder`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, http_handler: 'RequestHandler', context_builder: 'ServerCallContextBuilder | None'=None):
    self.handler = REST03Handler(request_handler=http_handler)
    self._context_builder = V03ServerCallContextBuilder(context_builder or DefaultServerCallContextBuilder())
```

</details>

### `REST03Adapter._handle_request`

Source lines 69–76; declaration kind `AsyncFunctionDef`.

Inputs: `(self, method: 'Callable[[Request, ServerCallContext], Awaitable[Any]]', request: Request)`. Output annotation: `Response`. Decorators: `rest_error_handler`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `call_context` from `self._context_builder.build(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `response` from `await method(request, call_context)`; output construction/calls here execute immediately when this method runs.
3. Returns `JSONResponse(content=response)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._context_builder.build`, `JSONResponse`, `method`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@rest_error_handler
async def _handle_request(self, method: 'Callable[[Request, ServerCallContext], Awaitable[Any]]', request: Request) -> Response:
    call_context = self._context_builder.build(request)
    response = await method(request, call_context)
    return JSONResponse(content=response)
```

</details>

### `REST03Adapter._handle_streaming_request`

Source lines 79–101; declaration kind `AsyncFunctionDef`.

Inputs: `(self, method: 'Callable[[Request, ServerCallContext], AsyncIterable[Any]]', request: Request)`. Output annotation: `EventSourceResponse`. Decorators: `rest_stream_error_handler`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `(ValueError, RuntimeError, OSError)` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.
2. Assigns `call_context` from `self._context_builder.build(request)`; output construction/calls here execute immediately when this method runs.
3. Defines closure `event_generator` capturing enclosing locals; its separate entry below documents deferred execution.
4. Returns `EventSourceResponse(event_generator(method(request, call_context)))`; this is the output/delegation boundary for this path.

Yielded output expressions: `json_utils.dumps(item)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: `InvalidRequestError(message=f'Failed to pre-consume request body: {e}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._context_builder.build`, `EventSourceResponse`, `event_generator`, `request.body`, `InvalidRequestError`, `method`, `json_utils.dumps`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@rest_stream_error_handler
async def _handle_streaming_request(self, method: 'Callable[[Request, ServerCallContext], AsyncIterable[Any]]', request: Request) -> EventSourceResponse:
    try:
        await request.body()
    except (ValueError, RuntimeError, OSError) as e:
        raise InvalidRequestError(message=f'Failed to pre-consume request body: {e}') from e
    call_context = self._context_builder.build(request)

    async def event_generator(stream: AsyncIterable[Any]) -> AsyncIterator[str]:
        async for item in stream:
            yield json_utils.dumps(item)
    return EventSourceResponse(event_generator(method(request, call_context)))
```

</details>

### `REST03Adapter._handle_streaming_request.event_generator`

Source lines 93–97; declaration kind `AsyncFunctionDef`.

Inputs: `(stream: AsyncIterable[Any])`. Output annotation: `AsyncIterator[str]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Asynchronously iterates `stream` into `item`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `json_utils.dumps(item)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `json_utils.dumps`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def event_generator(stream: AsyncIterable[Any]) -> AsyncIterator[str]:
    async for item in stream:
        yield json_utils.dumps(item)
```

</details>

### `REST03Adapter.routes`

Source lines 103–154; declaration kind `FunctionDef`.

Inputs: `(self)`. Output annotation: `dict[tuple[str, str], Callable[[Request], Any]]`. Decorators: `none`.

Source intent: Constructs a dictionary of API routes and their corresponding handlers.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Declares `routes: dict[tuple[str, str], Callable[[Request], Any]]` and initializes from `{('/v1/message:send', 'POST'): functools.partial(self._handle_request, self.handler.on_message_send), ('/v1/message:stream', 'POST'): functools.partial(self._handle_streaming_request, self.handler.on_message_send_stream), ('/v1/tasks/{id}:cancel', 'POST'): functools.partial(self._handle_request, self.handler.on_cancel_task), ('/v1/tasks/{id}:subscribe', 'GET … (full expression in body below)`.
2. Returns `routes`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `functools.partial`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def routes(self) -> dict[tuple[str, str], Callable[[Request], Any]]:
    routes: dict[tuple[str, str], Callable[[Request], Any]] = {('/v1/message:send', 'POST'): functools.partial(self._handle_request, self.handler.on_message_send), ('/v1/message:stream', 'POST'): functools.partial(self._handle_streaming_request, self.handler.on_message_send_stream), ('/v1/tasks/{id}:cancel', 'POST'): functools.partial(self._handle_request, self.handler.on_cancel_task), ('/v1/tasks/{id}:subscribe', 'GET'): functools.partial(self._handle_streaming_request, self.handler.on_subscribe_to_task), ('/v1/tasks/{id}:subscribe', 'POST'): functools.partial(self._handle_streaming_request, self.handler.on_subscribe_to_task), ('/v1/tasks/{id}', 'GET'): functools.partial(self._handle_request, self.handler.on_get_task), ('/v1/tasks/{id}/pushNotificationConfigs/{push_id}', 'GET'): functools.partial(self._handle_request, self.handler.get_push_notification), ('/v1/tasks/{id}/pushNotificationConfigs', 'POST'): functools.partial(self._handle_request, self.handler.set_push_notification), ('/v1/tasks/{id}/pushNotificationConfigs', 'GET'): functools.partial(self._handle_request, self.handler.list_push_notifications), ('/v1/card', 'GET'): functools.partial(self._handle_request, self.handler.on_get_extended_agent_card)}
    return routes
```

</details>
