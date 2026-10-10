# v0_3/grpc_transport.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/grpc_transport.py`. SHA-256: `5cad8190163be751ea6c818b843f3d2c62567a8c29d47661c1e29d943c2a397f`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## gRPC client boundary and identity

CompatGrpcTransport retains injected Channel/card and creates legacy A2AServiceStub; create(card,url,config) requires grpc_channel_factory or raises ValueError, then passes URL unchanged to factory. Channel creation, TLS/channel credentials, call credentials/interceptors and target naming policy are factory/runtime boundaries. close awaits channel.close and affects all sharing callers. grpcio is absent locally; source validation covers this module but no gRPC live/import smoke test was performed.

Send/stream convert core → pivot → legacy protobuf request. Stub SendMessage returns task/msg oneof, converted back; unset returns empty response. SendStreamingMessage and TaskSubscription repeatedly await stream.read until grpc.aio.EOF, converting each event; no explicit stream.cancel/final-based stop or reconnect occurs. GetTask builds tasks/{id} and unconditionally assigns request.history_length, losing core optional absence at protobuf wire. Cancel similarly builds resource. Push create constructs parent/config_id/config; get/delete use tasks/{task_id}/pushNotificationConfigs/{id}; list only task parent and ignores request paging, drops response next-page-token. Delete waits for RPC and returns None. GetAgentCard always calls RPC (no capability shortcut), converts and replaces cached card. ListTasks raises NotImplementedError.

`_get_grpc_metadata` begins lowercase a2a-version=0.3; it copies context service_parameters, mirrors legacy extension header then appends each lowercased key/value. User-provided version key becomes an additional duplicate rather than replacing first one. CallContext.timeout is **ignored**: compat stub calls pass metadata only, no timeout argument. Context state is also ignored. Credentials in service_parameters go to the gRPC peer on that call; channel credentials last as long as caller channel. Callback credentials are payload only. No local refresh, expiry, retry, persistence or authorization enforcement.

## Errors and wrappers

`_map_grpc_error` maps DEADLINE_EXCEEDED to A2AClientTimeoutError. Otherwise details `ClassName: message` maps by names of classes in current JSON_RPC_ERROR_CODE_MAP; unknown string/name/status becomes A2AClientError with status/details. Server abort text and current class names must match; structured rich status is not decoded and error data is not preserved. `_handle_grpc_exception` returns nested wraps-preserving async wrapper that awaits one method and catches only AioRpcError. Stream decorator's nested wrapper async-iterates/yields and catches that same type during iteration. Other exceptions, cancellation and conversion errors pass through.

Underlying gRPC may implement retry configured in channel options; compat adds none. No local consistency/cache guarantees beyond storing last fetched card. Caller should set deadlines in channel/interceptors when using this transport, since ClientCallContext timeout is not applied here. Do not assume stream disconnect cancels the agent's logical task.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import logging
from collections.abc import AsyncGenerator, Callable
from functools import wraps
from typing import Any, NoReturn
from a2a.client.errors import A2AClientError, A2AClientTimeoutError
from a2a.utils.errors import JSON_RPC_ERROR_CODE_MAP
from a2a.client.client import ClientCallContext, ClientConfig
from a2a.client.optionals import Channel
from a2a.client.transports.base import ClientTransport
from a2a.compat.v0_3 import a2a_v0_3_pb2, a2a_v0_3_pb2_grpc, conversions, proto_utils
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.extension_headers import add_legacy_extension_header
from a2a.types import a2a_pb2
from a2a.utils.constants import PROTOCOL_VERSION_0_3, VERSION_HEADER
from a2a.utils.telemetry import SpanKind, trace_class
import grpc
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
_A2A_ERROR_NAME_TO_CLS = {error_type.__name__: error_type for error_type in JSON_RPC_ERROR_CODE_MAP}
```

## Declaration-by-declaration execution reference

### `_map_grpc_error`

Source lines 46–56; declaration kind `FunctionDef`.

Inputs: `(e: grpc.aio.AioRpcError)`. Output annotation: `NoReturn`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `e.code() == grpc.StatusCode.DEADLINE_EXCEEDED`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Assigns `details` from `e.details()`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(details, str) and ': ' in details`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Raises `A2AClientError(f'gRPC Error {e.code().name}: {e.details()}')`, chained from `e`.

Explicit errors: `A2AClientError(f'gRPC Error {e.code().name}: {e.details()}')`; `A2AClientTimeoutError('Client Request timed out')`; `exception_cls(error_message)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `e.details`, `A2AClientError`, `e.code`, `A2AClientTimeoutError`, `isinstance`, `details.split`, `_A2A_ERROR_NAME_TO_CLS.get`, `exception_cls`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _map_grpc_error(e: grpc.aio.AioRpcError) -> NoReturn:
    if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        raise A2AClientTimeoutError('Client Request timed out') from e
    details = e.details()
    if isinstance(details, str) and ': ' in details:
        error_type_name, error_message = details.split(': ', 1)
        exception_cls = _A2A_ERROR_NAME_TO_CLS.get(error_type_name)
        if exception_cls:
            raise exception_cls(error_message) from e
    raise A2AClientError(f'gRPC Error {e.code().name}: {e.details()}') from e
```

</details>

### `_handle_grpc_exception`

Source lines 59–67; declaration kind `FunctionDef`.

Inputs: `(func: Callable[..., Any])`. Output annotation: `Callable[..., Any]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `wrapper` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `wrapper`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `wraps`, `func`, `_map_grpc_error`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _handle_grpc_exception(func: Callable[..., Any]) -> Callable[..., Any]:

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except grpc.aio.AioRpcError as e:
            _map_grpc_error(e)
    return wrapper
```

</details>

### `_handle_grpc_exception.wrapper`

Source lines 61–65; declaration kind `AsyncFunctionDef`.

Inputs: `(*args: Any, **kwargs: Any)`. Output annotation: `Any`. Decorators: `wraps(func)`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `grpc.aio.AioRpcError` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `wraps`, `func`, `_map_grpc_error`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@wraps(func)
async def wrapper(*args: Any, **kwargs: Any) -> Any:
    try:
        return await func(*args, **kwargs)
    except grpc.aio.AioRpcError as e:
        _map_grpc_error(e)
```

</details>

### `_handle_grpc_stream_exception`

Source lines 70–81; declaration kind `FunctionDef`.

Inputs: `(func: Callable[..., Any])`. Output annotation: `Callable[..., Any]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Defines closure `wrapper` capturing enclosing locals; its separate entry below documents deferred execution.
2. Returns `wrapper`; this is the output/delegation boundary for this path.

Yielded output expressions: `item`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `wraps`, `func`, `_map_grpc_error`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _handle_grpc_stream_exception(func: Callable[..., Any]) -> Callable[..., Any]:

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            async for item in func(*args, **kwargs):
                yield item
        except grpc.aio.AioRpcError as e:
            _map_grpc_error(e)
    return wrapper
```

</details>

### `_handle_grpc_stream_exception.wrapper`

Source lines 74–79; declaration kind `AsyncFunctionDef`.

Inputs: `(*args: Any, **kwargs: Any)`. Output annotation: `Any`. Decorators: `wraps(func)`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `grpc.aio.AioRpcError` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.

Yielded output expressions: `item`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `wraps`, `func`, `_map_grpc_error`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@wraps(func)
async def wrapper(*args: Any, **kwargs: Any) -> Any:
    try:
        async for item in func(*args, **kwargs):
            yield item
    except grpc.aio.AioRpcError as e:
        _map_grpc_error(e)
```

</details>

### `CompatGrpcTransport`

Source lines 85–372; declaration kind `ClassDef`.

Bases: `ClientTransport`. Decorators: `trace_class(kind=SpanKind.CLIENT)`.

Source definition/intent (executed behavior is determined by fields and methods): A backward compatible gRPC transport for A2A v0.3.

Declared operations: `__init__`, `create`, `send_message`, `send_message_streaming`, `subscribe`, `get_task`, `list_tasks`, `cancel_task`, `create_task_push_notification_config`, `get_task_push_notification_config`, `list_task_push_notification_configs`, `delete_task_push_notification_config`, `get_extended_agent_card`, `close`, `_get_grpc_metadata`. Each method is traced below; constructor determines retained state.

### `CompatGrpcTransport.__init__`

Source lines 88–92; declaration kind `FunctionDef`.

Inputs: `(self, channel: Channel, agent_card: a2a_pb2.AgentCard | None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Initializes the CompatGrpcTransport.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.agent_card` from `agent_card`; output construction/calls here execute immediately when this method runs.
2. Assigns `self.channel` from `channel`; output construction/calls here execute immediately when this method runs.
3. Assigns `self.stub` from `a2a_v0_3_pb2_grpc.A2AServiceStub(channel)`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2_grpc.A2AServiceStub`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, channel: Channel, agent_card: a2a_pb2.AgentCard | None):
    self.agent_card = agent_card
    self.channel = channel
    self.stub = a2a_v0_3_pb2_grpc.A2AServiceStub(channel)
```

</details>

### `CompatGrpcTransport.create`

Source lines 95–104; declaration kind `FunctionDef`.

Inputs: `(cls, card: a2a_pb2.AgentCard, url: str, config: ClientConfig)`. Output annotation: `'CompatGrpcTransport'`. Decorators: `classmethod`.

Source intent: Creates a gRPC transport for the A2A client.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `config.grpc_channel_factory is None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `cls(config.grpc_channel_factory(url), card)`; this is the output/delegation boundary for this path.

Explicit errors: `ValueError('grpc_channel_factory is required when using gRPC')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `cls`, `ValueError`, `config.grpc_channel_factory`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def create(cls, card: a2a_pb2.AgentCard, url: str, config: ClientConfig) -> 'CompatGrpcTransport':
    if config.grpc_channel_factory is None:
        raise ValueError('grpc_channel_factory is required when using gRPC')
    return cls(config.grpc_channel_factory(url), card)
```

</details>

### `CompatGrpcTransport.send_message`

Source lines 107–143; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.SendMessageRequest, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.SendMessageResponse`. Decorators: `_handle_grpc_exception`.

Source intent: Sends a non-streaming message request to the agent (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_send_message_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_proto` from `a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))`; output construction/calls here execute immediately when this method runs.
3. Assigns `resp_proto` from `await self.stub.SendMessage(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
4. Assigns `which` from `resp_proto.WhichOneof('payload')`; output construction/calls here execute immediately when this method runs.
5. Branches on `which == 'task'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Branches on `which == 'msg'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
7. Returns `a2a_pb2.SendMessageResponse()`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_send_message_request`, `a2a_v0_3_pb2.SendMessageRequest`, `resp_proto.WhichOneof`, `a2a_pb2.SendMessageResponse`, `self.stub.SendMessage`, `proto_utils.ToProto.message`, `proto_utils.ToProto.message_send_configuration`, `proto_utils.ToProto.metadata`, `self._get_grpc_metadata`, `conversions.to_core_task`, `conversions.to_core_message`, `proto_utils.FromProto.task`, `proto_utils.FromProto.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def send_message(self, request: a2a_pb2.SendMessageRequest, *, context: ClientCallContext | None=None) -> a2a_pb2.SendMessageResponse:
    req_v03 = conversions.to_compat_send_message_request(request, request_id=0)
    req_proto = a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))
    resp_proto = await self.stub.SendMessage(req_proto, metadata=self._get_grpc_metadata(context))
    which = resp_proto.WhichOneof('payload')
    if which == 'task':
        return a2a_pb2.SendMessageResponse(task=conversions.to_core_task(proto_utils.FromProto.task(resp_proto.task)))
    if which == 'msg':
        return a2a_pb2.SendMessageResponse(message=conversions.to_core_message(proto_utils.FromProto.message(resp_proto.msg)))
    return a2a_pb2.SendMessageResponse()
```

</details>

### `CompatGrpcTransport.send_message_streaming`

Source lines 146–176; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.SendMessageRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AsyncGenerator[a2a_pb2.StreamResponse]`. Decorators: `_handle_grpc_stream_exception`.

Source intent: Sends a streaming message request to the agent (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_send_message_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_proto` from `a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))`; output construction/calls here execute immediately when this method runs.
3. Assigns `stream` from `self.stub.SendStreamingMessage(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
4. Repeats while `True`; termination/break conditions and per-item output are explicit in the body below.

Yielded output expressions: `conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=proto_utils.FromProto.stream_response(response)))`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_send_message_request`, `a2a_v0_3_pb2.SendMessageRequest`, `self.stub.SendStreamingMessage`, `proto_utils.ToProto.message`, `proto_utils.ToProto.message_send_configuration`, `proto_utils.ToProto.metadata`, `self._get_grpc_metadata`, `stream.read`, `conversions.to_core_stream_response`, `types_v03.SendStreamingMessageSuccessResponse`, `proto_utils.FromProto.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_stream_exception
async def send_message_streaming(self, request: a2a_pb2.SendMessageRequest, *, context: ClientCallContext | None=None) -> AsyncGenerator[a2a_pb2.StreamResponse]:
    req_v03 = conversions.to_compat_send_message_request(request, request_id=0)
    req_proto = a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))
    stream = self.stub.SendStreamingMessage(req_proto, metadata=self._get_grpc_metadata(context))
    while True:
        response = await stream.read()
        if response == grpc.aio.EOF:
            break
        yield conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=proto_utils.FromProto.stream_response(response)))
```

</details>

### `CompatGrpcTransport.subscribe`

Source lines 179–202; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.SubscribeToTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AsyncGenerator[a2a_pb2.StreamResponse]`. Decorators: `_handle_grpc_stream_exception`.

Source intent: Reconnects to get task updates (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_proto` from `a2a_v0_3_pb2.TaskSubscriptionRequest(name=f'tasks/{request.id}')`; output construction/calls here execute immediately when this method runs.
2. Assigns `stream` from `self.stub.TaskSubscription(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
3. Repeats while `True`; termination/break conditions and per-item output are explicit in the body below.

Yielded output expressions: `conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=proto_utils.FromProto.stream_response(response)))`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2.TaskSubscriptionRequest`, `self.stub.TaskSubscription`, `self._get_grpc_metadata`, `stream.read`, `conversions.to_core_stream_response`, `types_v03.SendStreamingMessageSuccessResponse`, `proto_utils.FromProto.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_stream_exception
async def subscribe(self, request: a2a_pb2.SubscribeToTaskRequest, *, context: ClientCallContext | None=None) -> AsyncGenerator[a2a_pb2.StreamResponse]:
    req_proto = a2a_v0_3_pb2.TaskSubscriptionRequest(name=f'tasks/{request.id}')
    stream = self.stub.TaskSubscription(req_proto, metadata=self._get_grpc_metadata(context))
    while True:
        response = await stream.read()
        if response == grpc.aio.EOF:
            break
        yield conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=proto_utils.FromProto.stream_response(response)))
```

</details>

### `CompatGrpcTransport.get_task`

Source lines 205–220; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.GetTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.Task`. Decorators: `_handle_grpc_exception`.

Source intent: Retrieves the current state and history of a specific task (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_proto` from `a2a_v0_3_pb2.GetTaskRequest(name=f'tasks/{request.id}', history_length=request.history_length)`; output construction/calls here execute immediately when this method runs.
2. Assigns `resp_proto` from `await self.stub.GetTask(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_core_task(proto_utils.FromProto.task(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2.GetTaskRequest`, `conversions.to_core_task`, `self.stub.GetTask`, `proto_utils.FromProto.task`, `self._get_grpc_metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def get_task(self, request: a2a_pb2.GetTaskRequest, *, context: ClientCallContext | None=None) -> a2a_pb2.Task:
    req_proto = a2a_v0_3_pb2.GetTaskRequest(name=f'tasks/{request.id}', history_length=request.history_length)
    resp_proto = await self.stub.GetTask(req_proto, metadata=self._get_grpc_metadata(context))
    return conversions.to_core_task(proto_utils.FromProto.task(resp_proto))
```

</details>

### `CompatGrpcTransport.list_tasks`

Source lines 223–233; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.ListTasksRequest, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.ListTasksResponse`. Decorators: `_handle_grpc_exception`.

Source intent: Retrieves tasks for an agent (v0.3 - NOT SUPPORTED in v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Raises `NotImplementedError('ListTasks is not supported in A2A v0.3 gRPC.')`.

Explicit errors: `NotImplementedError('ListTasks is not supported in A2A v0.3 gRPC.')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def list_tasks(self, request: a2a_pb2.ListTasksRequest, *, context: ClientCallContext | None=None) -> a2a_pb2.ListTasksResponse:
    raise NotImplementedError('ListTasks is not supported in A2A v0.3 gRPC.')
```

</details>

### `CompatGrpcTransport.cancel_task`

Source lines 236–248; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.CancelTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.Task`. Decorators: `_handle_grpc_exception`.

Source intent: Requests the agent to cancel a specific task (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_proto` from `a2a_v0_3_pb2.CancelTaskRequest(name=f'tasks/{request.id}')`; output construction/calls here execute immediately when this method runs.
2. Assigns `resp_proto` from `await self.stub.CancelTask(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_core_task(proto_utils.FromProto.task(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2.CancelTaskRequest`, `conversions.to_core_task`, `self.stub.CancelTask`, `proto_utils.FromProto.task`, `self._get_grpc_metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def cancel_task(self, request: a2a_pb2.CancelTaskRequest, *, context: ClientCallContext | None=None) -> a2a_pb2.Task:
    req_proto = a2a_v0_3_pb2.CancelTaskRequest(name=f'tasks/{request.id}')
    resp_proto = await self.stub.CancelTask(req_proto, metadata=self._get_grpc_metadata(context))
    return conversions.to_core_task(proto_utils.FromProto.task(resp_proto))
```

</details>

### `CompatGrpcTransport.create_task_push_notification_config`

Source lines 251–276; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.TaskPushNotificationConfig, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.TaskPushNotificationConfig`. Decorators: `_handle_grpc_exception`.

Source intent: Sets or updates the push notification configuration (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_create_task_push_notification_config_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_proto` from `a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest(parent=f'tasks/{request.task_id}', config_id=req_v03.params.push_notification_config.id, config=proto_utils.ToProto.task_push_notification_config(req_v03.params))`; output construction/calls here execute immediately when this method runs.
3. Assigns `resp_proto` from `await self.stub.CreateTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
4. Returns `conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_create_task_push_notification_config_request`, `a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest`, `conversions.to_core_task_push_notification_config`, `self.stub.CreateTaskPushNotificationConfig`, `proto_utils.FromProto.task_push_notification_config`, `proto_utils.ToProto.task_push_notification_config`, `self._get_grpc_metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def create_task_push_notification_config(self, request: a2a_pb2.TaskPushNotificationConfig, *, context: ClientCallContext | None=None) -> a2a_pb2.TaskPushNotificationConfig:
    req_v03 = conversions.to_compat_create_task_push_notification_config_request(request, request_id=0)
    req_proto = a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest(parent=f'tasks/{request.task_id}', config_id=req_v03.params.push_notification_config.id, config=proto_utils.ToProto.task_push_notification_config(req_v03.params))
    resp_proto = await self.stub.CreateTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))
    return conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))
```

</details>

### `CompatGrpcTransport.get_task_push_notification_config`

Source lines 279–295; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.GetTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.TaskPushNotificationConfig`. Decorators: `_handle_grpc_exception`.

Source intent: Retrieves the push notification configuration (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_proto` from `a2a_v0_3_pb2.GetTaskPushNotificationConfigRequest(name=f'tasks/{request.task_id}/pushNotificationConfigs/{request.id}')`; output construction/calls here execute immediately when this method runs.
2. Assigns `resp_proto` from `await self.stub.GetTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2.GetTaskPushNotificationConfigRequest`, `conversions.to_core_task_push_notification_config`, `self.stub.GetTaskPushNotificationConfig`, `proto_utils.FromProto.task_push_notification_config`, `self._get_grpc_metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def get_task_push_notification_config(self, request: a2a_pb2.GetTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None) -> a2a_pb2.TaskPushNotificationConfig:
    req_proto = a2a_v0_3_pb2.GetTaskPushNotificationConfigRequest(name=f'tasks/{request.task_id}/pushNotificationConfigs/{request.id}')
    resp_proto = await self.stub.GetTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))
    return conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))
```

</details>

### `CompatGrpcTransport.list_task_push_notification_configs`

Source lines 298–316; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.ListTaskPushNotificationConfigsRequest, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.ListTaskPushNotificationConfigsResponse`. Decorators: `_handle_grpc_exception`.

Source intent: Lists push notification configurations for a specific task (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_proto` from `a2a_v0_3_pb2.ListTaskPushNotificationConfigRequest(parent=f'tasks/{request.task_id}')`; output construction/calls here execute immediately when this method runs.
2. Assigns `resp_proto` from `await self.stub.ListTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_core_list_task_push_notification_config_response(proto_utils.FromProto.list_task_push_notification_config_response(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2.ListTaskPushNotificationConfigRequest`, `conversions.to_core_list_task_push_notification_config_response`, `self.stub.ListTaskPushNotificationConfig`, `proto_utils.FromProto.list_task_push_notification_config_response`, `self._get_grpc_metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def list_task_push_notification_configs(self, request: a2a_pb2.ListTaskPushNotificationConfigsRequest, *, context: ClientCallContext | None=None) -> a2a_pb2.ListTaskPushNotificationConfigsResponse:
    req_proto = a2a_v0_3_pb2.ListTaskPushNotificationConfigRequest(parent=f'tasks/{request.task_id}')
    resp_proto = await self.stub.ListTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))
    return conversions.to_core_list_task_push_notification_config_response(proto_utils.FromProto.list_task_push_notification_config_response(resp_proto))
```

</details>

### `CompatGrpcTransport.delete_task_push_notification_config`

Source lines 319–332; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.DeleteTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None)`. Output annotation: `None`. Decorators: `_handle_grpc_exception`.

Source intent: Deletes the push notification configuration (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_proto` from `a2a_v0_3_pb2.DeleteTaskPushNotificationConfigRequest(name=f'tasks/{request.task_id}/pushNotificationConfigs/{request.id}')`; output construction/calls here execute immediately when this method runs.
2. Executes `await self.stub.DeleteTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))`; awaits completion before continuing.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2.DeleteTaskPushNotificationConfigRequest`, `self.stub.DeleteTaskPushNotificationConfig`, `self._get_grpc_metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def delete_task_push_notification_config(self, request: a2a_pb2.DeleteTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None) -> None:
    req_proto = a2a_v0_3_pb2.DeleteTaskPushNotificationConfigRequest(name=f'tasks/{request.task_id}/pushNotificationConfigs/{request.id}')
    await self.stub.DeleteTaskPushNotificationConfig(req_proto, metadata=self._get_grpc_metadata(context))
```

</details>

### `CompatGrpcTransport.get_extended_agent_card`

Source lines 335–352; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: a2a_pb2.GetExtendedAgentCardRequest, *, context: ClientCallContext | None=None)`. Output annotation: `a2a_pb2.AgentCard`. Decorators: `_handle_grpc_exception`.

Source intent: Retrieves the agent's card (v0.3).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_proto` from `a2a_v0_3_pb2.GetAgentCardRequest()`; output construction/calls here execute immediately when this method runs.
2. Assigns `resp_proto` from `await self.stub.GetAgentCard(req_proto, metadata=self._get_grpc_metadata(context))`; output construction/calls here execute immediately when this method runs.
3. Assigns `card` from `conversions.to_core_agent_card(proto_utils.FromProto.agent_card(resp_proto))`; output construction/calls here execute immediately when this method runs.
4. Assigns `self.agent_card` from `card`; output construction/calls here execute immediately when this method runs.
5. Returns `card`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_v0_3_pb2.GetAgentCardRequest`, `conversions.to_core_agent_card`, `self.stub.GetAgentCard`, `proto_utils.FromProto.agent_card`, `self._get_grpc_metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@_handle_grpc_exception
async def get_extended_agent_card(self, request: a2a_pb2.GetExtendedAgentCardRequest, *, context: ClientCallContext | None=None) -> a2a_pb2.AgentCard:
    req_proto = a2a_v0_3_pb2.GetAgentCardRequest()
    resp_proto = await self.stub.GetAgentCard(req_proto, metadata=self._get_grpc_metadata(context))
    card = conversions.to_core_agent_card(proto_utils.FromProto.agent_card(resp_proto))
    self.agent_card = card
    return card
```

</details>

### `CompatGrpcTransport.close`

Source lines 354–356; declaration kind `AsyncFunctionDef`.

Inputs: `(self)`. Output annotation: `None`. Decorators: `none`.

Source intent: Closes the gRPC channel.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `await self.channel.close()`; awaits completion before continuing.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self.channel.close`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def close(self) -> None:
    await self.channel.close()
```

</details>

### `CompatGrpcTransport._get_grpc_metadata`

Source lines 358–372; declaration kind `FunctionDef`.

Inputs: `(self, context: ClientCallContext | None=None)`. Output annotation: `list[tuple[str, str]]`. Decorators: `none`.

Source intent: Creates gRPC metadata for extensions.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Declares `metadata: list[tuple[str, str]]` and initializes from `[(VERSION_HEADER.lower(), PROTOCOL_VERSION_0_3)]`.
2. Branches on `context and context.service_parameters`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `metadata`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `dict`, `add_legacy_extension_header`, `params.items`, `VERSION_HEADER.lower`, `metadata.append`, `key.lower`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _get_grpc_metadata(self, context: ClientCallContext | None=None) -> list[tuple[str, str]]:
    metadata: list[tuple[str, str]] = [(VERSION_HEADER.lower(), PROTOCOL_VERSION_0_3)]
    if context and context.service_parameters:
        params = dict(context.service_parameters)
        add_legacy_extension_header(params)
        for key, value in params.items():
            metadata.append((key.lower(), value))
    return metadata
```

</details>
