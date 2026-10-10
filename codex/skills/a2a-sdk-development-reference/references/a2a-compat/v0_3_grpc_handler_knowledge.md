# v0_3/grpc_handler.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/grpc_handler.py`. SHA-256: `a2b888ecde2c47195f235e7329c06f0d3375e194d061d944557be2c0b0e5ff43`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## gRPC service execution

`CompatGrpcHandler` subclasses generated legacy A2AServiceServicer; construction wraps current handler in RequestHandler03 and supplied/default gRPC context builder in V03GrpcServerCallContextBuilder. Register using legacy `add_A2AServiceServicer_to_server`, not current namespace registration. It implements ten RPCs with a nested `_handler` closure per RPC. These closures perform legacy protobuf → pivot conversion, bridge call, then pivot → legacy protobuf; synthetic JSON-RPC IDs are 0. Send selects task/msg; streams iterate and yield one converted event at a time.

`_handle_unary` builds context and awaits closure inside try, catches only core A2AError, calls abort_context, and returns supplied empty protobuf fallback only if abort returns. In real grpc.aio abort normally raises; fallback is useful for unusual/mock contexts, not a successful error response. `_handle_stream` similarly catches only A2AError during context creation and iteration. Non-domain exceptions such as ValueError/Pydantic/UTF-8 failures escape to gRPC framework handling.

`abort_context` uses external exact-type `_ERROR_CODE_MAP`; known errors map to INVALID_ARGUMENT, NOT_FOUND, INTERNAL or FAILED_PRECONDITION and details `ClassName: message`. Unknown error subclass becomes UNKNOWN and different text. `_extract_task_id` and `_extract_task_and_config_id` use prefix regex matching, raise InvalidParamsError on mismatch. Get/cancel/subscription use FromProto resource helpers; config get/delete use both extracted groups; config list only parent task, ignoring page_size/page_token. Create uses nested config fields, ignores top-level config_id. Delete returns google.protobuf.Empty after delegate completion. GetAgentCard means extended card via core handler, not an unauthenticated static-card bypass.

No validate_version decorator, tenant extraction, request-state method/request ID insertion, or metadata deadline processing occurs here. Default builder does not authenticate users. Supply a builder for authenticated identity and use server/channel interceptors for transport policy. Cancellation of RPC propagates through awaits/generators; this adapter does not explicitly cancel an executor or shield calls. No retry, stream replay or buffering. Optional grpcio is absent in inspected environment, so this module is source-reviewed and cannot be imported there without additional dependency installation (not performed).

```python
# Requires grpcio; registration only, no server startup shown.
from a2a.compat.v0_3.grpc_handler import CompatGrpcHandler
from a2a.compat.v0_3.a2a_v0_3_pb2_grpc import add_A2AServiceServicer_to_server
add_A2AServiceServicer_to_server(CompatGrpcHandler(core_handler), server)
```

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import logging
from collections.abc import AsyncIterable, Awaitable, Callable
from typing import TypeVar
import grpc
import grpc.aio
from google.protobuf import empty_pb2
from a2a.compat.v0_3 import a2a_v0_3_pb2, a2a_v0_3_pb2_grpc, proto_utils
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.context_builders import V03GrpcServerCallContextBuilder
from a2a.compat.v0_3.request_handler import RequestHandler03
from a2a.server.context import ServerCallContext
from a2a.server.request_handlers.grpc_handler import _ERROR_CODE_MAP, DefaultGrpcServerCallContextBuilder, GrpcServerCallContextBuilder
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.utils.errors import A2AError, InvalidParamsError
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
TResponse = TypeVar('TResponse')
```

## Declaration-by-declaration execution reference

### `CompatGrpcHandler`

Source lines 37–362; declaration kind `ClassDef`.

Bases: `a2a_v0_3_pb2_grpc.A2AServiceServicer`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Backward compatible gRPC handler for A2A v0.3.

Declared operations: `__init__`, `_handle_unary`, `_handle_stream`, `_extract_task_id`, `_extract_task_and_config_id`, `abort_context`, `SendMessage`, `SendStreamingMessage`, `GetTask`, `CancelTask`, `TaskSubscription`, `CreateTaskPushNotificationConfig`, `GetTaskPushNotificationConfig`, `ListTaskPushNotificationConfig`, `GetAgentCard`, `DeleteTaskPushNotificationConfig`. Each method is traced below; constructor determines retained state.

### `CompatGrpcHandler.__init__`

Source lines 40–56; declaration kind `FunctionDef`.

Inputs: `(self, request_handler: RequestHandler, context_builder: GrpcServerCallContextBuilder | None=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Initializes the CompatGrpcHandler. Args: request_handler: The underlying `RequestHandler` instance to delegate requests to. context_builder: The CallContextBuilder object. If none the DefaultCallContextBuilder is used.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.handler03` from `RequestHandler03(request_handler=request_handler)`; output construction/calls here execute immediately when this method runs.
2. Assigns `self._context_builder` from `V03GrpcServerCallContextBuilder(context_builder or DefaultGrpcServerCallContextBuilder())`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `RequestHandler03`, `V03GrpcServerCallContextBuilder`, `DefaultGrpcServerCallContextBuilder`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, request_handler: RequestHandler, context_builder: GrpcServerCallContextBuilder | None=None):
    self.handler03 = RequestHandler03(request_handler=request_handler)
    self._context_builder = V03GrpcServerCallContextBuilder(context_builder or DefaultGrpcServerCallContextBuilder())
```

</details>

### `CompatGrpcHandler._handle_unary`

Source lines 58–72; declaration kind `AsyncFunctionDef`.

Inputs: `(self, context: grpc.aio.ServicerContext, handler_func: Callable[[ServerCallContext], Awaitable[TResponse]], default_response: TResponse)`. Output annotation: `TResponse`. Decorators: `none`.

Source intent: Centralized error handling and context management for unary calls.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `A2AError` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.
2. Returns `default_response`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._context_builder.build`, `handler_func`, `self.abort_context`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handle_unary(self, context: grpc.aio.ServicerContext, handler_func: Callable[[ServerCallContext], Awaitable[TResponse]], default_response: TResponse) -> TResponse:
    try:
        server_context = self._context_builder.build(context)
        result = await handler_func(server_context)
    except A2AError as e:
        await self.abort_context(e, context)
    else:
        return result
    return default_response
```

</details>

### `CompatGrpcHandler._handle_stream`

Source lines 74–85; declaration kind `AsyncFunctionDef`.

Inputs: `(self, context: grpc.aio.ServicerContext, handler_func: Callable[[ServerCallContext], AsyncIterable[TResponse]])`. Output annotation: `AsyncIterable[TResponse]`. Decorators: `none`.

Source intent: Centralized error handling and context management for streaming calls.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `A2AError` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.

Yielded output expressions: `item`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._context_builder.build`, `handler_func`, `self.abort_context`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handle_stream(self, context: grpc.aio.ServicerContext, handler_func: Callable[[ServerCallContext], AsyncIterable[TResponse]]) -> AsyncIterable[TResponse]:
    try:
        server_context = self._context_builder.build(context)
        async for item in handler_func(server_context):
            yield item
    except A2AError as e:
        await self.abort_context(e, context)
```

</details>

### `CompatGrpcHandler._extract_task_id`

Source lines 87–92; declaration kind `FunctionDef`.

Inputs: `(self, resource_name: str)`. Output annotation: `str`. Decorators: `none`.

Source intent: Extracts task_id from resource name.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `m` from `proto_utils.TASK_NAME_MATCH.match(resource_name)`; output construction/calls here execute immediately when this method runs.
2. Branches on `not m`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `m.group(1)`; this is the output/delegation boundary for this path.

Explicit errors: `InvalidParamsError(message=f'No task for {resource_name}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `proto_utils.TASK_NAME_MATCH.match`, `m.group`, `InvalidParamsError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _extract_task_id(self, resource_name: str) -> str:
    m = proto_utils.TASK_NAME_MATCH.match(resource_name)
    if not m:
        raise InvalidParamsError(message=f'No task for {resource_name}')
    return m.group(1)
```

</details>

### `CompatGrpcHandler._extract_task_and_config_id`

Source lines 94–103; declaration kind `FunctionDef`.

Inputs: `(self, resource_name: str)`. Output annotation: `tuple[str, str]`. Decorators: `none`.

Source intent: Extracts task_id and config_id from resource name.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `m` from `proto_utils.TASK_PUSH_CONFIG_NAME_MATCH.match(resource_name)`; output construction/calls here execute immediately when this method runs.
2. Branches on `not m`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `(m.group(1), m.group(2))`; this is the output/delegation boundary for this path.

Explicit errors: `InvalidParamsError(message=f'Bad resource name {resource_name}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `proto_utils.TASK_PUSH_CONFIG_NAME_MATCH.match`, `InvalidParamsError`, `m.group`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _extract_task_and_config_id(self, resource_name: str) -> tuple[str, str]:
    m = proto_utils.TASK_PUSH_CONFIG_NAME_MATCH.match(resource_name)
    if not m:
        raise InvalidParamsError(message=f'Bad resource name {resource_name}')
    return (m.group(1), m.group(2))
```

</details>

### `CompatGrpcHandler.abort_context`

Source lines 105–119; declaration kind `AsyncFunctionDef`.

Inputs: `(self, error: A2AError, context: grpc.aio.ServicerContext)`. Output annotation: `None`. Decorators: `none`.

Source intent: Sets the grpc errors appropriately in the context.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `code` from `_ERROR_CODE_MAP.get(type(error))`; output construction/calls here execute immediately when this method runs.
2. Branches on `code`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `_ERROR_CODE_MAP.get`, `type`, `context.abort`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def abort_context(self, error: A2AError, context: grpc.aio.ServicerContext) -> None:
    code = _ERROR_CODE_MAP.get(type(error))
    if code:
        await context.abort(code, f'{type(error).__name__}: {error.message}')
    else:
        await context.abort(grpc.StatusCode.UNKNOWN, f'Unknown error type: {error}')
```

</details>

### `CompatGrpcHandler.SendMessage`

Source lines 121–147; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.SendMessageRequest, context: grpc.aio.ServicerContext)`. Output annotation: `a2a_v0_3_pb2.SendMessageResponse`. Decorators: `none`.

Source intent: Handles the 'SendMessage' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, a2a_v0_3_pb2.SendMessageResponse())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.SendMessageRequest`, `isinstance`, `a2a_v0_3_pb2.SendMessageResponse`, `self._handle_unary`, `self.handler03.on_message_send`, `proto_utils.FromProto.message_send_params`, `proto_utils.ToProto.message`, `proto_utils.ToProto.task`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def SendMessage(self, request: a2a_v0_3_pb2.SendMessageRequest, context: grpc.aio.ServicerContext) -> a2a_v0_3_pb2.SendMessageResponse:

    async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.SendMessageResponse:
        req_v03 = types_v03.SendMessageRequest(id=0, params=proto_utils.FromProto.message_send_params(request))
        result = await self.handler03.on_message_send(req_v03, server_context)
        if isinstance(result, types_v03.Task):
            return a2a_v0_3_pb2.SendMessageResponse(task=proto_utils.ToProto.task(result))
        return a2a_v0_3_pb2.SendMessageResponse(msg=proto_utils.ToProto.message(result))
    return await self._handle_unary(context, _handler, a2a_v0_3_pb2.SendMessageResponse())
```

</details>

### `CompatGrpcHandler.SendMessage._handler`

Source lines 128–143; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `a2a_v0_3_pb2.SendMessageResponse`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `types_v03.SendMessageRequest(id=0, params=proto_utils.FromProto.message_send_params(request))`; output construction/calls here execute immediately when this method runs.
2. Assigns `result` from `await self.handler03.on_message_send(req_v03, server_context)`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(result, types_v03.Task)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `a2a_v0_3_pb2.SendMessageResponse(msg=proto_utils.ToProto.message(result))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.SendMessageRequest`, `isinstance`, `a2a_v0_3_pb2.SendMessageResponse`, `self.handler03.on_message_send`, `proto_utils.FromProto.message_send_params`, `proto_utils.ToProto.message`, `proto_utils.ToProto.task`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.SendMessageResponse:
    req_v03 = types_v03.SendMessageRequest(id=0, params=proto_utils.FromProto.message_send_params(request))
    result = await self.handler03.on_message_send(req_v03, server_context)
    if isinstance(result, types_v03.Task):
        return a2a_v0_3_pb2.SendMessageResponse(task=proto_utils.ToProto.task(result))
    return a2a_v0_3_pb2.SendMessageResponse(msg=proto_utils.ToProto.message(result))
```

</details>

### `CompatGrpcHandler.SendStreamingMessage`

Source lines 149–170; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.SendMessageRequest, context: grpc.aio.ServicerContext)`. Output annotation: `AsyncIterable[a2a_v0_3_pb2.StreamResponse]`. Decorators: `none`.

Source intent: Handles the 'SendStreamingMessage' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Asynchronously iterates `self._handle_stream(context, _handler)` into `item`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `item`, `proto_utils.ToProto.stream_response(v03_stream_resp.result)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._handle_stream`, `types_v03.SendMessageRequest`, `self.handler03.on_message_send_stream`, `proto_utils.FromProto.message_send_params`, `proto_utils.ToProto.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def SendStreamingMessage(self, request: a2a_v0_3_pb2.SendMessageRequest, context: grpc.aio.ServicerContext) -> AsyncIterable[a2a_v0_3_pb2.StreamResponse]:

    async def _handler(server_context: ServerCallContext) -> AsyncIterable[a2a_v0_3_pb2.StreamResponse]:
        req_v03 = types_v03.SendMessageRequest(id=0, params=proto_utils.FromProto.message_send_params(request))
        async for v03_stream_resp in self.handler03.on_message_send_stream(req_v03, server_context):
            yield proto_utils.ToProto.stream_response(v03_stream_resp.result)
    async for item in self._handle_stream(context, _handler):
        yield item
```

</details>

### `CompatGrpcHandler.SendStreamingMessage._handler`

Source lines 156–167; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `AsyncIterable[a2a_v0_3_pb2.StreamResponse]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `types_v03.SendMessageRequest(id=0, params=proto_utils.FromProto.message_send_params(request))`; output construction/calls here execute immediately when this method runs.
2. Asynchronously iterates `self.handler03.on_message_send_stream(req_v03, server_context)` into `v03_stream_resp`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `proto_utils.ToProto.stream_response(v03_stream_resp.result)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.SendMessageRequest`, `self.handler03.on_message_send_stream`, `proto_utils.FromProto.message_send_params`, `proto_utils.ToProto.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> AsyncIterable[a2a_v0_3_pb2.StreamResponse]:
    req_v03 = types_v03.SendMessageRequest(id=0, params=proto_utils.FromProto.message_send_params(request))
    async for v03_stream_resp in self.handler03.on_message_send_stream(req_v03, server_context):
        yield proto_utils.ToProto.stream_response(v03_stream_resp.result)
```

</details>

### `CompatGrpcHandler.GetTask`

Source lines 172–188; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.GetTaskRequest, context: grpc.aio.ServicerContext)`. Output annotation: `a2a_v0_3_pb2.Task`. Decorators: `none`.

Source intent: Handles the 'GetTask' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, a2a_v0_3_pb2.Task())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.GetTaskRequest`, `proto_utils.ToProto.task`, `self._handle_unary`, `self.handler03.on_get_task`, `a2a_v0_3_pb2.Task`, `proto_utils.FromProto.task_query_params`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def GetTask(self, request: a2a_v0_3_pb2.GetTaskRequest, context: grpc.aio.ServicerContext) -> a2a_v0_3_pb2.Task:

    async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.Task:
        req_v03 = types_v03.GetTaskRequest(id=0, params=proto_utils.FromProto.task_query_params(request))
        task = await self.handler03.on_get_task(req_v03, server_context)
        return proto_utils.ToProto.task(task)
    return await self._handle_unary(context, _handler, a2a_v0_3_pb2.Task())
```

</details>

### `CompatGrpcHandler.GetTask._handler`

Source lines 179–186; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `a2a_v0_3_pb2.Task`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `types_v03.GetTaskRequest(id=0, params=proto_utils.FromProto.task_query_params(request))`; output construction/calls here execute immediately when this method runs.
2. Assigns `task` from `await self.handler03.on_get_task(req_v03, server_context)`; output construction/calls here execute immediately when this method runs.
3. Returns `proto_utils.ToProto.task(task)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.GetTaskRequest`, `proto_utils.ToProto.task`, `self.handler03.on_get_task`, `proto_utils.FromProto.task_query_params`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.Task:
    req_v03 = types_v03.GetTaskRequest(id=0, params=proto_utils.FromProto.task_query_params(request))
    task = await self.handler03.on_get_task(req_v03, server_context)
    return proto_utils.ToProto.task(task)
```

</details>

### `CompatGrpcHandler.CancelTask`

Source lines 190–206; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.CancelTaskRequest, context: grpc.aio.ServicerContext)`. Output annotation: `a2a_v0_3_pb2.Task`. Decorators: `none`.

Source intent: Handles the 'CancelTask' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, a2a_v0_3_pb2.Task())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.CancelTaskRequest`, `proto_utils.ToProto.task`, `self._handle_unary`, `self.handler03.on_cancel_task`, `a2a_v0_3_pb2.Task`, `proto_utils.FromProto.task_id_params`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def CancelTask(self, request: a2a_v0_3_pb2.CancelTaskRequest, context: grpc.aio.ServicerContext) -> a2a_v0_3_pb2.Task:

    async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.Task:
        req_v03 = types_v03.CancelTaskRequest(id=0, params=proto_utils.FromProto.task_id_params(request))
        task = await self.handler03.on_cancel_task(req_v03, server_context)
        return proto_utils.ToProto.task(task)
    return await self._handle_unary(context, _handler, a2a_v0_3_pb2.Task())
```

</details>

### `CompatGrpcHandler.CancelTask._handler`

Source lines 197–204; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `a2a_v0_3_pb2.Task`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `types_v03.CancelTaskRequest(id=0, params=proto_utils.FromProto.task_id_params(request))`; output construction/calls here execute immediately when this method runs.
2. Assigns `task` from `await self.handler03.on_cancel_task(req_v03, server_context)`; output construction/calls here execute immediately when this method runs.
3. Returns `proto_utils.ToProto.task(task)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.CancelTaskRequest`, `proto_utils.ToProto.task`, `self.handler03.on_cancel_task`, `proto_utils.FromProto.task_id_params`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.Task:
    req_v03 = types_v03.CancelTaskRequest(id=0, params=proto_utils.FromProto.task_id_params(request))
    task = await self.handler03.on_cancel_task(req_v03, server_context)
    return proto_utils.ToProto.task(task)
```

</details>

### `CompatGrpcHandler.TaskSubscription`

Source lines 208–229; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.TaskSubscriptionRequest, context: grpc.aio.ServicerContext)`. Output annotation: `AsyncIterable[a2a_v0_3_pb2.StreamResponse]`. Decorators: `none`.

Source intent: Handles the 'TaskSubscription' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Asynchronously iterates `self._handle_stream(context, _handler)` into `item`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `item`, `proto_utils.ToProto.stream_response(v03_stream_resp.result)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._handle_stream`, `types_v03.TaskResubscriptionRequest`, `self.handler03.on_subscribe_to_task`, `proto_utils.FromProto.task_id_params`, `proto_utils.ToProto.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def TaskSubscription(self, request: a2a_v0_3_pb2.TaskSubscriptionRequest, context: grpc.aio.ServicerContext) -> AsyncIterable[a2a_v0_3_pb2.StreamResponse]:

    async def _handler(server_context: ServerCallContext) -> AsyncIterable[a2a_v0_3_pb2.StreamResponse]:
        req_v03 = types_v03.TaskResubscriptionRequest(id=0, params=proto_utils.FromProto.task_id_params(request))
        async for v03_stream_resp in self.handler03.on_subscribe_to_task(req_v03, server_context):
            yield proto_utils.ToProto.stream_response(v03_stream_resp.result)
    async for item in self._handle_stream(context, _handler):
        yield item
```

</details>

### `CompatGrpcHandler.TaskSubscription._handler`

Source lines 215–226; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `AsyncIterable[a2a_v0_3_pb2.StreamResponse]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `types_v03.TaskResubscriptionRequest(id=0, params=proto_utils.FromProto.task_id_params(request))`; output construction/calls here execute immediately when this method runs.
2. Asynchronously iterates `self.handler03.on_subscribe_to_task(req_v03, server_context)` into `v03_stream_resp`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `proto_utils.ToProto.stream_response(v03_stream_resp.result)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.TaskResubscriptionRequest`, `self.handler03.on_subscribe_to_task`, `proto_utils.FromProto.task_id_params`, `proto_utils.ToProto.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> AsyncIterable[a2a_v0_3_pb2.StreamResponse]:
    req_v03 = types_v03.TaskResubscriptionRequest(id=0, params=proto_utils.FromProto.task_id_params(request))
    async for v03_stream_resp in self.handler03.on_subscribe_to_task(req_v03, server_context):
        yield proto_utils.ToProto.stream_response(v03_stream_resp.result)
```

</details>

### `CompatGrpcHandler.CreateTaskPushNotificationConfig`

Source lines 231–256; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext)`. Output annotation: `a2a_v0_3_pb2.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Handles the 'CreateTaskPushNotificationConfig' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, a2a_v0_3_pb2.TaskPushNotificationConfig())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.SetTaskPushNotificationConfigRequest`, `proto_utils.ToProto.task_push_notification_config`, `self._handle_unary`, `self.handler03.on_create_task_push_notification_config`, `a2a_v0_3_pb2.TaskPushNotificationConfig`, `proto_utils.FromProto.task_push_notification_config_request`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def CreateTaskPushNotificationConfig(self, request: a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext) -> a2a_v0_3_pb2.TaskPushNotificationConfig:

    async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.TaskPushNotificationConfig:
        req_v03 = types_v03.SetTaskPushNotificationConfigRequest(id=0, params=proto_utils.FromProto.task_push_notification_config_request(request))
        res_v03 = await self.handler03.on_create_task_push_notification_config(req_v03, server_context)
        return proto_utils.ToProto.task_push_notification_config(res_v03)
    return await self._handle_unary(context, _handler, a2a_v0_3_pb2.TaskPushNotificationConfig())
```

</details>

### `CompatGrpcHandler.CreateTaskPushNotificationConfig._handler`

Source lines 238–252; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `a2a_v0_3_pb2.TaskPushNotificationConfig`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `types_v03.SetTaskPushNotificationConfigRequest(id=0, params=proto_utils.FromProto.task_push_notification_config_request(request))`; output construction/calls here execute immediately when this method runs.
2. Assigns `res_v03` from `await self.handler03.on_create_task_push_notification_config(req_v03, server_context)`; output construction/calls here execute immediately when this method runs.
3. Returns `proto_utils.ToProto.task_push_notification_config(res_v03)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.SetTaskPushNotificationConfigRequest`, `proto_utils.ToProto.task_push_notification_config`, `self.handler03.on_create_task_push_notification_config`, `proto_utils.FromProto.task_push_notification_config_request`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.TaskPushNotificationConfig:
    req_v03 = types_v03.SetTaskPushNotificationConfigRequest(id=0, params=proto_utils.FromProto.task_push_notification_config_request(request))
    res_v03 = await self.handler03.on_create_task_push_notification_config(req_v03, server_context)
    return proto_utils.ToProto.task_push_notification_config(res_v03)
```

</details>

### `CompatGrpcHandler.GetTaskPushNotificationConfig`

Source lines 258–282; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.GetTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext)`. Output annotation: `a2a_v0_3_pb2.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Handles the 'GetTaskPushNotificationConfig' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, a2a_v0_3_pb2.TaskPushNotificationConfig())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._extract_task_and_config_id`, `types_v03.GetTaskPushNotificationConfigRequest`, `proto_utils.ToProto.task_push_notification_config`, `self._handle_unary`, `self.handler03.on_get_task_push_notification_config`, `a2a_v0_3_pb2.TaskPushNotificationConfig`, `types_v03.GetTaskPushNotificationConfigParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def GetTaskPushNotificationConfig(self, request: a2a_v0_3_pb2.GetTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext) -> a2a_v0_3_pb2.TaskPushNotificationConfig:

    async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.TaskPushNotificationConfig:
        task_id, config_id = self._extract_task_and_config_id(request.name)
        req_v03 = types_v03.GetTaskPushNotificationConfigRequest(id=0, params=types_v03.GetTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=config_id))
        res_v03 = await self.handler03.on_get_task_push_notification_config(req_v03, server_context)
        return proto_utils.ToProto.task_push_notification_config(res_v03)
    return await self._handle_unary(context, _handler, a2a_v0_3_pb2.TaskPushNotificationConfig())
```

</details>

### `CompatGrpcHandler.GetTaskPushNotificationConfig._handler`

Source lines 265–278; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `a2a_v0_3_pb2.TaskPushNotificationConfig`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `(task_id, config_id)` from `self._extract_task_and_config_id(request.name)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_v03` from `types_v03.GetTaskPushNotificationConfigRequest(id=0, params=types_v03.GetTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=config_id))`; output construction/calls here execute immediately when this method runs.
3. Assigns `res_v03` from `await self.handler03.on_get_task_push_notification_config(req_v03, server_context)`; output construction/calls here execute immediately when this method runs.
4. Returns `proto_utils.ToProto.task_push_notification_config(res_v03)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._extract_task_and_config_id`, `types_v03.GetTaskPushNotificationConfigRequest`, `proto_utils.ToProto.task_push_notification_config`, `self.handler03.on_get_task_push_notification_config`, `types_v03.GetTaskPushNotificationConfigParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.TaskPushNotificationConfig:
    task_id, config_id = self._extract_task_and_config_id(request.name)
    req_v03 = types_v03.GetTaskPushNotificationConfigRequest(id=0, params=types_v03.GetTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=config_id))
    res_v03 = await self.handler03.on_get_task_push_notification_config(req_v03, server_context)
    return proto_utils.ToProto.task_push_notification_config(res_v03)
```

</details>

### `CompatGrpcHandler.ListTaskPushNotificationConfig`

Source lines 284–318; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.ListTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext)`. Output annotation: `a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse`. Decorators: `none`.

Source intent: Handles the 'ListTaskPushNotificationConfig' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._extract_task_id`, `types_v03.ListTaskPushNotificationConfigRequest`, `a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse`, `self._handle_unary`, `self.handler03.on_list_task_push_notification_configs`, `types_v03.ListTaskPushNotificationConfigParams`, `proto_utils.ToProto.task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def ListTaskPushNotificationConfig(self, request: a2a_v0_3_pb2.ListTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext) -> a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse:

    async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse:
        task_id = self._extract_task_id(request.parent)
        req_v03 = types_v03.ListTaskPushNotificationConfigRequest(id=0, params=types_v03.ListTaskPushNotificationConfigParams(id=task_id))
        res_v03 = await self.handler03.on_list_task_push_notification_configs(req_v03, server_context)
        return a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse(configs=[proto_utils.ToProto.task_push_notification_config(c) for c in res_v03])
    return await self._handle_unary(context, _handler, a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse())
```

</details>

### `CompatGrpcHandler.ListTaskPushNotificationConfig._handler`

Source lines 291–312; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `task_id` from `self._extract_task_id(request.parent)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_v03` from `types_v03.ListTaskPushNotificationConfigRequest(id=0, params=types_v03.ListTaskPushNotificationConfigParams(id=task_id))`; output construction/calls here execute immediately when this method runs.
3. Assigns `res_v03` from `await self.handler03.on_list_task_push_notification_configs(req_v03, server_context)`; output construction/calls here execute immediately when this method runs.
4. Returns `a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse(configs=[proto_utils.ToProto.task_push_notification_config(c) for c in res_v03])`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._extract_task_id`, `types_v03.ListTaskPushNotificationConfigRequest`, `a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse`, `self.handler03.on_list_task_push_notification_configs`, `types_v03.ListTaskPushNotificationConfigParams`, `proto_utils.ToProto.task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse:
    task_id = self._extract_task_id(request.parent)
    req_v03 = types_v03.ListTaskPushNotificationConfigRequest(id=0, params=types_v03.ListTaskPushNotificationConfigParams(id=task_id))
    res_v03 = await self.handler03.on_list_task_push_notification_configs(req_v03, server_context)
    return a2a_v0_3_pb2.ListTaskPushNotificationConfigResponse(configs=[proto_utils.ToProto.task_push_notification_config(c) for c in res_v03])
```

</details>

### `CompatGrpcHandler.GetAgentCard`

Source lines 320–338; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.GetAgentCardRequest, context: grpc.aio.ServicerContext)`. Output annotation: `a2a_v0_3_pb2.AgentCard`. Decorators: `none`.

Source intent: Get the extended agent card for the agent served (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, a2a_v0_3_pb2.AgentCard())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.GetAuthenticatedExtendedCardRequest`, `proto_utils.ToProto.agent_card`, `self._handle_unary`, `self.handler03.on_get_extended_agent_card`, `a2a_v0_3_pb2.AgentCard`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def GetAgentCard(self, request: a2a_v0_3_pb2.GetAgentCardRequest, context: grpc.aio.ServicerContext) -> a2a_v0_3_pb2.AgentCard:

    async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.AgentCard:
        req_v03 = types_v03.GetAuthenticatedExtendedCardRequest(id=0)
        res_v03 = await self.handler03.on_get_extended_agent_card(req_v03, server_context)
        return proto_utils.ToProto.agent_card(res_v03)
    return await self._handle_unary(context, _handler, a2a_v0_3_pb2.AgentCard())
```

</details>

### `CompatGrpcHandler.GetAgentCard._handler`

Source lines 327–334; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `a2a_v0_3_pb2.AgentCard`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `types_v03.GetAuthenticatedExtendedCardRequest(id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `res_v03` from `await self.handler03.on_get_extended_agent_card(req_v03, server_context)`; output construction/calls here execute immediately when this method runs.
3. Returns `proto_utils.ToProto.agent_card(res_v03)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.GetAuthenticatedExtendedCardRequest`, `proto_utils.ToProto.agent_card`, `self.handler03.on_get_extended_agent_card`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> a2a_v0_3_pb2.AgentCard:
    req_v03 = types_v03.GetAuthenticatedExtendedCardRequest(id=0)
    res_v03 = await self.handler03.on_get_extended_agent_card(req_v03, server_context)
    return proto_utils.ToProto.agent_card(res_v03)
```

</details>

### `CompatGrpcHandler.DeleteTaskPushNotificationConfig`

Source lines 340–362; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_v0_3_pb2.DeleteTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext)`. Output annotation: `empty_pb2.Empty`. Decorators: `none`.

Source intent: Handles the 'DeleteTaskPushNotificationConfig' gRPC method (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `_handler` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `await self._handle_unary(context, _handler, empty_pb2.Empty())`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._extract_task_and_config_id`, `types_v03.DeleteTaskPushNotificationConfigRequest`, `empty_pb2.Empty`, `self._handle_unary`, `self.handler03.on_delete_task_push_notification_config`, `types_v03.DeleteTaskPushNotificationConfigParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def DeleteTaskPushNotificationConfig(self, request: a2a_v0_3_pb2.DeleteTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext) -> empty_pb2.Empty:

    async def _handler(server_context: ServerCallContext) -> empty_pb2.Empty:
        task_id, config_id = self._extract_task_and_config_id(request.name)
        req_v03 = types_v03.DeleteTaskPushNotificationConfigRequest(id=0, params=types_v03.DeleteTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=config_id))
        await self.handler03.on_delete_task_push_notification_config(req_v03, server_context)
        return empty_pb2.Empty()
    return await self._handle_unary(context, _handler, empty_pb2.Empty())
```

</details>

### `CompatGrpcHandler.DeleteTaskPushNotificationConfig._handler`

Source lines 347–360; declaration kind `AsyncFunctionDef`.

Inputs: `(server_context: ServerCallContext)`. Output annotation: `empty_pb2.Empty`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `(task_id, config_id)` from `self._extract_task_and_config_id(request.name)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_v03` from `types_v03.DeleteTaskPushNotificationConfigRequest(id=0, params=types_v03.DeleteTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=config_id))`; output construction/calls here execute immediately when this method runs.
3. Executes `await self.handler03.on_delete_task_push_notification_config(req_v03, server_context)`; awaits completion before continuing.
4. Returns `empty_pb2.Empty()`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._extract_task_and_config_id`, `types_v03.DeleteTaskPushNotificationConfigRequest`, `empty_pb2.Empty`, `self.handler03.on_delete_task_push_notification_config`, `types_v03.DeleteTaskPushNotificationConfigParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _handler(server_context: ServerCallContext) -> empty_pb2.Empty:
    task_id, config_id = self._extract_task_and_config_id(request.name)
    req_v03 = types_v03.DeleteTaskPushNotificationConfigRequest(id=0, params=types_v03.DeleteTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=config_id))
    await self.handler03.on_delete_task_push_notification_config(req_v03, server_context)
    return empty_pb2.Empty()
```

</details>
