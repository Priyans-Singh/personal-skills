# v0_3/jsonrpc_adapter.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/jsonrpc_adapter.py`. SHA-256: `f575962cca7e4bb17131e155e20af196dbf4f8029eb030e5b2dbd372b86ccd02`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Server JSON-RPC path

`JSONRPC03Adapter` constructs RequestHandler03 and wraps supplied/default HTTP context builder. `supports_method` is membership in METHOD_TO_MODEL (ten legacy methods). Calling `handle_request(request_id, method, body, request)` assumes an outer router already parsed an envelope and selected this adapter. It looks up the model, validates full body, builds context, sets tenant from params/top-level if present (legacy models do not define tenant), and puts method/request_id in state. Streaming selection depends on passed method; actual dispatch depends on validated model.method. Unsupported lookup becomes the outer generic InternalError response rather than MethodNotFound.

Model validation catches Exception and returns current JSON-RPC InvalidRequestError with validation text in data. The outer handler catches Exception and converts to CoreInternalError containing str(e), including domain errors raised by downstream handlers. `_generate_error_response` preserves a CoreJSONRPCError dictionary, but a generic Exception becomes internal error. All use JSONResponse default HTTP status; JSON-RPC error remains body-level. Do not assume TaskNotFoundError gets its specific code from this adapter.

Non-streaming processing is decorated for expected version 0.3. It dispatches send/get/cancel/get-config/set-config/list-config/delete-config/extended-card; builds typed success envelopes with outer request_id and excludes None while serializing aliases. Delete returns result=None in the model, then exclude_none removes result from JSON. Client transport compensates when response has neither result nor error. Version decorator actually compares major only.

Streaming processing supports message/stream and tasks/resubscribe. It creates EventSourceResponse from nested `event_generator`, which iterates legacy success envelopes into SSE `data` JSON. Exceptions during iteration become a final legacy InternalError JSON-RPC SSE event using request_id; domain errors are not preserved as domain codes. Python CancelledError/GeneratorExit are BaseException and are not caught by these Exception handlers. Disconnect and generator cleanup belong to sse-starlette; no reconnect or resume ID is added.

## Auth and dependencies

HTTP identity is inherited from middleware/custom context builder. Version and both extension headers are context data, not authentication. This module imports sse-starlette and Starlette JSONResponse unconditionally before its optional Request guard; setting Any in the guard cannot make it usable without those packages. Error text is exposed/logged as implemented; provide application error discipline if sensitive exceptions can occur.

Fresh direct import of this adapter was locally observed to fail through a circular import: adapter → server.routes.common initializes server.routes.__init__ → jsonrpc_routes → jsonrpc_dispatcher → partially initialized adapter. Importing `a2a.server.routes` first was verified to succeed. Use the normal route package entry point before direct adapter integration; dependency availability alone does not ensure import order works.

```python
import a2a.server.routes  # initialize routes first in this installed release
from a2a.compat.v0_3.jsonrpc_adapter import JSONRPC03Adapter
adapter = JSONRPC03Adapter(core_handler, context_builder=my_context_builder)
assert adapter.supports_method('tasks/get')
# response = await adapter.handle_request(rpc_id, method, body, request)
```

The snippet is an integration shape requiring caller-supplied handler/builder; it makes no request.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import logging
from collections.abc import AsyncIterable, AsyncIterator
from typing import TYPE_CHECKING, Any
from sse_starlette.sse import EventSourceResponse
from starlette.responses import JSONResponse
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.context_builders import V03ServerCallContextBuilder
from a2a.compat.v0_3.request_handler import RequestHandler03
from a2a.server.context import ServerCallContext
from a2a.server.jsonrpc_models import InternalError as CoreInternalError
from a2a.server.jsonrpc_models import InvalidRequestError as CoreInvalidRequestError
from a2a.server.jsonrpc_models import JSONRPCError as CoreJSONRPCError
from a2a.server.routes.common import DefaultServerCallContextBuilder, ServerCallContextBuilder
from a2a.utils import constants
from a2a.utils.version_validator import validate_version
from starlette.requests import Request
from a2a.server.request_handlers.request_handler import RequestHandler
from starlette.requests import Request
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
```

## Declaration-by-declaration execution reference

### `JSONRPC03Adapter`

Source lines 50–280; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Adapter to make RequestHandler work with v0.3 JSONRPC API.

Declared operations: `__init__`, `supports_method`, `_generate_error_response`, `handle_request`, `_process_non_streaming_request`, `_process_streaming_request`. Each method is traced below; constructor determines retained state.

### `JSONRPC03Adapter.__init__`

Source lines 66–76; declaration kind `FunctionDef`.

Inputs: `(self, http_handler: 'RequestHandler', context_builder: 'ServerCallContextBuilder | None'=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.handler` from `RequestHandler03(request_handler=http_handler)`; output construction/calls here execute immediately when this method runs.
2. Assigns `self._context_builder` from `V03ServerCallContextBuilder(context_builder or DefaultServerCallContextBuilder())`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `RequestHandler03`, `V03ServerCallContextBuilder`, `DefaultServerCallContextBuilder`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, http_handler: 'RequestHandler', context_builder: 'ServerCallContextBuilder | None'=None):
    self.handler = RequestHandler03(request_handler=http_handler)
    self._context_builder = V03ServerCallContextBuilder(context_builder or DefaultServerCallContextBuilder())
```

</details>

### `JSONRPC03Adapter.supports_method`

Source lines 78–80; declaration kind `FunctionDef`.

Inputs: `(self, method: str)`. Output annotation: `bool`. Decorators: `none`.

Source intent: Returns True if the v0.3 adapter supports the given method name.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `method in self.METHOD_TO_MODEL`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def supports_method(self, method: str) -> bool:
    return method in self.METHOD_TO_MODEL
```

</details>

### `JSONRPC03Adapter._generate_error_response`

Source lines 82–100; declaration kind `FunctionDef`.

Inputs: `(self, request_id: 'str | int | None', error: 'Exception | CoreJSONRPCError')`. Output annotation: `JSONResponse`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(error, CoreJSONRPCError)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Assigns `internal_error` from `CoreInternalError(message=str(error))`; output construction/calls here execute immediately when this method runs.
3. Returns `JSONResponse({'jsonrpc': '2.0', 'id': request_id, 'error': internal_error.model_dump(by_alias=True)})`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `CoreInternalError`, `JSONResponse`, `error.model_dump`, `str`, `internal_error.model_dump`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _generate_error_response(self, request_id: 'str | int | None', error: 'Exception | CoreJSONRPCError') -> JSONResponse:
    if isinstance(error, CoreJSONRPCError):
        err_dict = error.model_dump(by_alias=True)
        return JSONResponse({'jsonrpc': '2.0', 'id': request_id, 'error': err_dict})
    internal_error = CoreInternalError(message=str(error))
    return JSONResponse({'jsonrpc': '2.0', 'id': request_id, 'error': internal_error.model_dump(by_alias=True)})
```

</details>

### `JSONRPC03Adapter.handle_request`

Source lines 102–145; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request_id: 'str | int | None', method: str, body: dict, request: Request)`. Output annotation: `'JSONResponse | EventSourceResponse'`. Decorators: `none`.

Source intent: Handles v0.3 specific JSON-RPC requests.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `Exception` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._context_builder.build`, `model_class.model_validate`, `hasattr`, `getattr`, `self._process_non_streaming_request`, `logger.exception`, `self._generate_error_response`, `self._process_streaming_request`, `CoreInternalError`, `CoreInvalidRequestError`, `str`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def handle_request(self, request_id: 'str | int | None', method: str, body: dict, request: Request) -> 'JSONResponse | EventSourceResponse':
    try:
        model_class = self.METHOD_TO_MODEL[method]
        try:
            specific_request = model_class.model_validate(body)
        except Exception as e:
            logger.exception('Failed to validate base JSON-RPC request for v0.3')
            return self._generate_error_response(request_id, CoreInvalidRequestError(data=str(e)))
        call_context = self._context_builder.build(request)
        call_context.tenant = getattr(specific_request.params, 'tenant', '') if hasattr(specific_request, 'params') else getattr(specific_request, 'tenant', '')
        call_context.state['method'] = method
        call_context.state['request_id'] = request_id
        if method in ('message/stream', 'tasks/resubscribe'):
            return await self._process_streaming_request(request_id, specific_request, call_context)
        return await self._process_non_streaming_request(request_id, specific_request, call_context)
    except Exception as e:
        logger.exception('Unhandled exception in v0.3 JSONRPCAdapter')
        return self._generate_error_response(request_id, CoreInternalError(message=str(e)))
```

</details>

### `JSONRPC03Adapter._process_non_streaming_request`

Source lines 148–235; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request_id: 'str | int | None', request_obj: Any, context: ServerCallContext)`. Output annotation: `JSONResponse`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `method` from `request_obj.method`; output construction/calls here execute immediately when this method runs.
2. Declares `result: Any`.
3. Branches on `method == 'message/send'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `JSONResponse(content=result.model_dump(mode='json', by_alias=True, exclude_none=True))`; this is the output/delegation boundary for this path.

Explicit errors: `ValueError(f'Unsupported method {method}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `JSONResponse`, `types_v03.SendMessageResponse`, `self.handler.on_message_send`, `types_v03.GetTaskResponse`, `result.model_dump`, `types_v03.SendMessageSuccessResponse`, `self.handler.on_get_task`, `types_v03.CancelTaskResponse`, `types_v03.GetTaskSuccessResponse`, `self.handler.on_cancel_task`, `types_v03.GetTaskPushNotificationConfigResponse`, `types_v03.CancelTaskSuccessResponse`, `self.handler.on_get_task_push_notification_config`, `types_v03.SetTaskPushNotificationConfigResponse`, `types_v03.GetTaskPushNotificationConfigSuccessResponse`, `self.handler.on_create_task_push_notification_config`, `types_v03.ListTaskPushNotificationConfigResponse`, `types_v03.SetTaskPushNotificationConfigSuccessResponse`, `self.handler.on_list_task_push_notification_configs`, `types_v03.DeleteTaskPushNotificationConfigResponse`, `types_v03.ListTaskPushNotificationConfigSuccessResponse`, `self.handler.on_delete_task_push_notification_config`, `types_v03.GetAuthenticatedExtendedCardResponse`, `ValueError`, `types_v03.DeleteTaskPushNotificationConfigSuccessResponse`, `self.handler.on_get_extended_agent_card`, `types_v03.GetAuthenticatedExtendedCardSuccessResponse`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def _process_non_streaming_request(self, request_id: 'str | int | None', request_obj: Any, context: ServerCallContext) -> JSONResponse:
    method = request_obj.method
    result: Any
    if method == 'message/send':
        res_msg = await self.handler.on_message_send(request_obj, context)
        result = types_v03.SendMessageResponse(root=types_v03.SendMessageSuccessResponse(id=request_id, result=res_msg))
    elif method == 'tasks/get':
        res_get = await self.handler.on_get_task(request_obj, context)
        result = types_v03.GetTaskResponse(root=types_v03.GetTaskSuccessResponse(id=request_id, result=res_get))
    elif method == 'tasks/cancel':
        res_cancel = await self.handler.on_cancel_task(request_obj, context)
        result = types_v03.CancelTaskResponse(root=types_v03.CancelTaskSuccessResponse(id=request_id, result=res_cancel))
    elif method == 'tasks/pushNotificationConfig/get':
        res_get_push = await self.handler.on_get_task_push_notification_config(request_obj, context)
        result = types_v03.GetTaskPushNotificationConfigResponse(root=types_v03.GetTaskPushNotificationConfigSuccessResponse(id=request_id, result=res_get_push))
    elif method == 'tasks/pushNotificationConfig/set':
        res_set_push = await self.handler.on_create_task_push_notification_config(request_obj, context)
        result = types_v03.SetTaskPushNotificationConfigResponse(root=types_v03.SetTaskPushNotificationConfigSuccessResponse(id=request_id, result=res_set_push))
    elif method == 'tasks/pushNotificationConfig/list':
        res_list_push = await self.handler.on_list_task_push_notification_configs(request_obj, context)
        result = types_v03.ListTaskPushNotificationConfigResponse(root=types_v03.ListTaskPushNotificationConfigSuccessResponse(id=request_id, result=res_list_push))
    elif method == 'tasks/pushNotificationConfig/delete':
        await self.handler.on_delete_task_push_notification_config(request_obj, context)
        result = types_v03.DeleteTaskPushNotificationConfigResponse(root=types_v03.DeleteTaskPushNotificationConfigSuccessResponse(id=request_id, result=None))
    elif method == 'agent/getAuthenticatedExtendedCard':
        res_card = await self.handler.on_get_extended_agent_card(request_obj, context)
        result = types_v03.GetAuthenticatedExtendedCardResponse(root=types_v03.GetAuthenticatedExtendedCardSuccessResponse(id=request_id, result=res_card))
    else:
        raise ValueError(f'Unsupported method {method}')
    return JSONResponse(content=result.model_dump(mode='json', by_alias=True, exclude_none=True))
```

</details>

### `JSONRPC03Adapter._process_streaming_request`

Source lines 238–280; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request_id: 'str | int | None', request_obj: Any, context: ServerCallContext)`. Output annotation: `EventSourceResponse`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `method` from `request_obj.method`; output construction/calls here execute immediately when this method runs.
2. Branches on `method == 'message/stream'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Defines closure `event_generator` capturing enclosing locals; its separate entry below documents deferred execution.
4. Returns `EventSourceResponse(event_generator(stream_gen))`; this is the output/delegation boundary for this path.

Yielded output expressions: `{'data': item.model_dump_json(by_alias=True, exclude_none=True)}`, `{'data': err_resp.model_dump_json(by_alias=True, exclude_none=True)}`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: `ValueError(f'Unsupported streaming method {method}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `EventSourceResponse`, `self.handler.on_message_send_stream`, `event_generator`, `self.handler.on_subscribe_to_task`, `ValueError`, `logger.exception`, `types_v03.InternalError`, `types_v03.SendStreamingMessageResponse`, `item.model_dump_json`, `str`, `types_v03.JSONRPCErrorResponse`, `err_resp.model_dump_json`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def _process_streaming_request(self, request_id: 'str | int | None', request_obj: Any, context: ServerCallContext) -> EventSourceResponse:
    method = request_obj.method
    if method == 'message/stream':
        stream_gen = self.handler.on_message_send_stream(request_obj, context)
    elif method == 'tasks/resubscribe':
        stream_gen = self.handler.on_subscribe_to_task(request_obj, context)
    else:
        raise ValueError(f'Unsupported streaming method {method}')

    async def event_generator(stream: AsyncIterable[Any]) -> AsyncIterator[dict[str, str]]:
        try:
            async for item in stream:
                yield {'data': item.model_dump_json(by_alias=True, exclude_none=True)}
        except Exception as e:
            logger.exception('Error during stream generation in v0.3 JSONRPCAdapter')
            err = types_v03.InternalError(message=str(e))
            err_resp = types_v03.SendStreamingMessageResponse(root=types_v03.JSONRPCErrorResponse(id=request_id, error=err))
            yield {'data': err_resp.model_dump_json(by_alias=True, exclude_none=True)}
    return EventSourceResponse(event_generator(stream_gen))
```

</details>

### `JSONRPC03Adapter._process_streaming_request.event_generator`

Source lines 254–278; declaration kind `AsyncFunctionDef`.

Inputs: `(stream: AsyncIterable[Any])`. Output annotation: `AsyncIterator[dict[str, str]]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `Exception` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.

Yielded output expressions: `{'data': item.model_dump_json(by_alias=True, exclude_none=True)}`, `{'data': err_resp.model_dump_json(by_alias=True, exclude_none=True)}`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `logger.exception`, `types_v03.InternalError`, `types_v03.SendStreamingMessageResponse`, `item.model_dump_json`, `str`, `types_v03.JSONRPCErrorResponse`, `err_resp.model_dump_json`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def event_generator(stream: AsyncIterable[Any]) -> AsyncIterator[dict[str, str]]:
    try:
        async for item in stream:
            yield {'data': item.model_dump_json(by_alias=True, exclude_none=True)}
    except Exception as e:
        logger.exception('Error during stream generation in v0.3 JSONRPCAdapter')
        err = types_v03.InternalError(message=str(e))
        err_resp = types_v03.SendStreamingMessageResponse(root=types_v03.JSONRPCErrorResponse(id=request_id, error=err))
        yield {'data': err_resp.model_dump_json(by_alias=True, exclude_none=True)}
```

</details>
