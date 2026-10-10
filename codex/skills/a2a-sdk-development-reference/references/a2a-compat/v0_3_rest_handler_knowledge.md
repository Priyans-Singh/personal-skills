# v0_3/rest_handler.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/rest_handler.py`. SHA-256: `4432eaa4d41abdac369dab8455597e4985dabd64f3cc2300cab414b9baf19dd9`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## REST protobuf-JSON execution

REST03Handler is decorated with SERVER tracing and wraps RequestHandler03. Each method has expected-version 0.3 validation (external validator compares major only). Send reads raw request body, protobuf Parse into legacy SendMessageRequest with ignore_unknown_fields=True, FromProto into pivot params, inserts JSON-RPC id='', and calls the bridge. Unary result becomes legacy protobuf SendMessageResponse then MessageToDict; streaming each legacy result becomes StreamResponse dict. This wire shape is protobuf JSON, not the Pydantic JSON-RPC dictionary.

Cancel/subscribe/get derive task ID from request.path_params['id']; no URI escaping/validation is added here. Get parses historyLength through int when nonempty, so malformed strings raise ValueError. Subscribe ignores body and supports either HTTP verb through adapter routing. Push get also requires push_id. Create parses full legacy CreateTaskPushNotificationConfigRequest and first validates parent through FromProto; only afterward overwrites extracted task_id with URL path ID. Thus a missing/invalid body parent can fail before path authority applies; top-level config_id is ignored. List returns protobuf configs wrapper, ignores paging query and core paging results.

Extended card constructs id=0 and returns **Pydantic** model_dump(mode='json', exclude_none=True), unlike other REST methods. CompatRestTransport parses this into legacy AgentCard protobuf, so check enum/security JSON compatibility for your card; no schema-level equality guarantee is made. Source method docstring mentions a different path, but actual adapter route is `/v1/card`.

Unknown protobuf body fields are discarded. Parse errors, body read failures, int conversion, model validation and delegate failures propagate to REST adapter's decorators. Context is passed unchanged. This module does no auth, callback delivery, persistence, retry or stream termination based on final. Metadata/bytes/time loss follows both converter stages. Prefer JSON-RPC if you require pivot-only fields that legacy protobuf omits.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any
from google.protobuf.json_format import MessageToDict, Parse
from a2a.compat.v0_3 import a2a_v0_3_pb2 as pb2_v03
from a2a.compat.v0_3 import proto_utils
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.request_handler import RequestHandler03
from a2a.server.context import ServerCallContext
from a2a.utils import constants
from a2a.utils.telemetry import SpanKind, trace_class
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

### `REST03Handler`

Source lines 39–304; declaration kind `ClassDef`.

Bases: `object`. Decorators: `trace_class(kind=SpanKind.SERVER)`.

Source definition/intent (executed behavior is determined by fields and methods): Maps incoming REST-like (JSON+HTTP) requests to the appropriate request handler method and formats responses for v0.3 compatibility.

Declared operations: `__init__`, `on_message_send`, `on_message_send_stream`, `on_cancel_task`, `on_subscribe_to_task`, `get_push_notification`, `set_push_notification`, `on_get_task`, `list_push_notifications`, `on_get_extended_agent_card`. Each method is traced below; constructor determines retained state.

### `REST03Handler.__init__`

Source lines 42–51; declaration kind `FunctionDef`.

Inputs: `(self, request_handler: 'RequestHandler')`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Initializes the REST03Handler. Args: request_handler: The underlying `RequestHandler` instance to delegate requests to (v1.0).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.handler03` from `RequestHandler03(request_handler=request_handler)`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `RequestHandler03`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, request_handler: 'RequestHandler'):
    self.handler03 = RequestHandler03(request_handler=request_handler)
```

</details>

### `REST03Handler.on_message_send`

Source lines 54–77; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `dict[str, Any]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'message/send' REST method. Args: request: The incoming `Request` object. context: Context provided by the server. Returns: A `dict` containing the result (Task or Message) in v0.3 format.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `body` from `await request.body()`; output construction/calls here execute immediately when this method runs.
2. Assigns `v03_pb_msg` from `pb2_v03.SendMessageRequest()`; output construction/calls here execute immediately when this method runs.
3. Executes `Parse(body, v03_pb_msg, ignore_unknown_fields=True)`.
4. Assigns `v03_params_msg` from `proto_utils.FromProto.message_send_params(v03_pb_msg)`; output construction/calls here execute immediately when this method runs.
5. Assigns `rpc_req` from `types_v03.SendMessageRequest(id='', params=v03_params_msg)`; output construction/calls here execute immediately when this method runs.
6. Assigns `v03_resp` from `await self.handler03.on_message_send(rpc_req, context)`; output construction/calls here execute immediately when this method runs.
7. Assigns `pb2_v03_resp` from `proto_utils.ToProto.task_or_message(v03_resp)`; output construction/calls here execute immediately when this method runs.
8. Returns `MessageToDict(pb2_v03_resp)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `pb2_v03.SendMessageRequest`, `Parse`, `proto_utils.FromProto.message_send_params`, `types_v03.SendMessageRequest`, `proto_utils.ToProto.task_or_message`, `MessageToDict`, `request.body`, `self.handler03.on_message_send`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def on_message_send(self, request: Request, context: ServerCallContext) -> dict[str, Any]:
    body = await request.body()
    v03_pb_msg = pb2_v03.SendMessageRequest()
    Parse(body, v03_pb_msg, ignore_unknown_fields=True)
    v03_params_msg = proto_utils.FromProto.message_send_params(v03_pb_msg)
    rpc_req = types_v03.SendMessageRequest(id='', params=v03_params_msg)
    v03_resp = await self.handler03.on_message_send(rpc_req, context)
    pb2_v03_resp = proto_utils.ToProto.task_or_message(v03_resp)
    return MessageToDict(pb2_v03_resp)
```

</details>

### `REST03Handler.on_message_send_stream`

Source lines 80–106; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `AsyncIterator[dict[str, Any]]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'message/stream' REST method. Args: request: The incoming `Request` object. context: Context provided by the server. Yields: JSON serialized objects containing streaming events in v0.3 format.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `body` from `await request.body()`; output construction/calls here execute immediately when this method runs.
2. Assigns `v03_pb_msg` from `pb2_v03.SendMessageRequest()`; output construction/calls here execute immediately when this method runs.
3. Executes `Parse(body, v03_pb_msg, ignore_unknown_fields=True)`.
4. Assigns `v03_params_msg` from `proto_utils.FromProto.message_send_params(v03_pb_msg)`; output construction/calls here execute immediately when this method runs.
5. Assigns `rpc_req` from `types_v03.SendMessageRequest(id='', params=v03_params_msg)`; output construction/calls here execute immediately when this method runs.
6. Asynchronously iterates `self.handler03.on_message_send_stream(rpc_req, context)` into `v03_stream_resp`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `MessageToDict(v03_pb_resp)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `pb2_v03.SendMessageRequest`, `Parse`, `proto_utils.FromProto.message_send_params`, `types_v03.SendMessageRequest`, `self.handler03.on_message_send_stream`, `request.body`, `proto_utils.ToProto.stream_response`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def on_message_send_stream(self, request: Request, context: ServerCallContext) -> AsyncIterator[dict[str, Any]]:
    body = await request.body()
    v03_pb_msg = pb2_v03.SendMessageRequest()
    Parse(body, v03_pb_msg, ignore_unknown_fields=True)
    v03_params_msg = proto_utils.FromProto.message_send_params(v03_pb_msg)
    rpc_req = types_v03.SendMessageRequest(id='', params=v03_params_msg)
    async for v03_stream_resp in self.handler03.on_message_send_stream(rpc_req, context):
        v03_pb_resp = proto_utils.ToProto.stream_response(v03_stream_resp.result)
        yield MessageToDict(v03_pb_resp)
```

</details>

### `REST03Handler.on_cancel_task`

Source lines 109–131; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `dict[str, Any]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'tasks/cancel' REST method. Args: request: The incoming `Request` object. context: Context provided by the server. Returns: A `dict` containing the updated Task in v0.3 format.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `task_id` from `request.path_params['id']`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_req` from `types_v03.CancelTaskRequest(id='', params=types_v03.TaskIdParams(id=task_id))`; output construction/calls here execute immediately when this method runs.
3. Assigns `v03_resp` from `await self.handler03.on_cancel_task(rpc_req, context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `pb2_v03_task` from `proto_utils.ToProto.task(v03_resp)`; output construction/calls here execute immediately when this method runs.
5. Returns `MessageToDict(pb2_v03_task)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `types_v03.CancelTaskRequest`, `proto_utils.ToProto.task`, `MessageToDict`, `self.handler03.on_cancel_task`, `types_v03.TaskIdParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def on_cancel_task(self, request: Request, context: ServerCallContext) -> dict[str, Any]:
    task_id = request.path_params['id']
    rpc_req = types_v03.CancelTaskRequest(id='', params=types_v03.TaskIdParams(id=task_id))
    v03_resp = await self.handler03.on_cancel_task(rpc_req, context)
    pb2_v03_task = proto_utils.ToProto.task(v03_resp)
    return MessageToDict(pb2_v03_task)
```

</details>

### `REST03Handler.on_subscribe_to_task`

Source lines 134–160; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `AsyncIterator[dict[str, Any]]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'tasks/{id}:subscribe' REST method. Args: request: The incoming `Request` object. context: Context provided by the server. Yields: JSON serialized objects containing streaming events in v0.3 format.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `task_id` from `request.path_params['id']`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_req` from `types_v03.TaskResubscriptionRequest(id='', params=types_v03.TaskIdParams(id=task_id))`; output construction/calls here execute immediately when this method runs.
3. Asynchronously iterates `self.handler03.on_subscribe_to_task(rpc_req, context)` into `v03_stream_resp`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `MessageToDict(v03_pb_resp)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `types_v03.TaskResubscriptionRequest`, `self.handler03.on_subscribe_to_task`, `proto_utils.ToProto.stream_response`, `types_v03.TaskIdParams`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def on_subscribe_to_task(self, request: Request, context: ServerCallContext) -> AsyncIterator[dict[str, Any]]:
    task_id = request.path_params['id']
    rpc_req = types_v03.TaskResubscriptionRequest(id='', params=types_v03.TaskIdParams(id=task_id))
    async for v03_stream_resp in self.handler03.on_subscribe_to_task(rpc_req, context):
        v03_pb_resp = proto_utils.ToProto.stream_response(v03_stream_resp.result)
        yield MessageToDict(v03_pb_resp)
```

</details>

### `REST03Handler.get_push_notification`

Source lines 163–193; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `dict[str, Any]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'tasks/pushNotificationConfig/get' REST method. Args: request: The incoming `Request` object. context: Context provided by the server. Returns: A `dict` containing the config in v0.3 format.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `task_id` from `request.path_params['id']`; output construction/calls here execute immediately when this method runs.
2. Assigns `push_id` from `request.path_params['push_id']`; output construction/calls here execute immediately when this method runs.
3. Assigns `rpc_req` from `types_v03.GetTaskPushNotificationConfigRequest(id='', params=types_v03.GetTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=push_id))`; output construction/calls here execute immediately when this method runs.
4. Assigns `v03_resp` from `await self.handler03.on_get_task_push_notification_config(rpc_req, context)`; output construction/calls here execute immediately when this method runs.
5. Assigns `pb2_v03_config` from `proto_utils.ToProto.task_push_notification_config(v03_resp)`; output construction/calls here execute immediately when this method runs.
6. Returns `MessageToDict(pb2_v03_config)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `types_v03.GetTaskPushNotificationConfigRequest`, `proto_utils.ToProto.task_push_notification_config`, `MessageToDict`, `self.handler03.on_get_task_push_notification_config`, `types_v03.GetTaskPushNotificationConfigParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def get_push_notification(self, request: Request, context: ServerCallContext) -> dict[str, Any]:
    task_id = request.path_params['id']
    push_id = request.path_params['push_id']
    rpc_req = types_v03.GetTaskPushNotificationConfigRequest(id='', params=types_v03.GetTaskPushNotificationConfigParams(id=task_id, push_notification_config_id=push_id))
    v03_resp = await self.handler03.on_get_task_push_notification_config(rpc_req, context)
    pb2_v03_config = proto_utils.ToProto.task_push_notification_config(v03_resp)
    return MessageToDict(pb2_v03_config)
```

</details>

### `REST03Handler.set_push_notification`

Source lines 196–234; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `dict[str, Any]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'tasks/pushNotificationConfig/set' REST method. Args: request: The incoming `Request` object. context: Context provided by the server. Returns: A `dict` containing the config object in v0.3 format.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `task_id` from `request.path_params['id']`; output construction/calls here execute immediately when this method runs.
2. Assigns `body` from `await request.body()`; output construction/calls here execute immediately when this method runs.
3. Assigns `v03_pb_push` from `pb2_v03.CreateTaskPushNotificationConfigRequest()`; output construction/calls here execute immediately when this method runs.
4. Executes `Parse(body, v03_pb_push, ignore_unknown_fields=True)`.
5. Assigns `v03_params_push` from `proto_utils.FromProto.task_push_notification_config_request(v03_pb_push)`; output construction/calls here execute immediately when this method runs.
6. Assigns `v03_params_push.task_id` from `task_id`; output construction/calls here execute immediately when this method runs.
7. Assigns `rpc_req_push` from `types_v03.SetTaskPushNotificationConfigRequest(id='', params=v03_params_push)`; output construction/calls here execute immediately when this method runs.
8. Assigns `v03_resp` from `await self.handler03.on_create_task_push_notification_config(rpc_req_push, context)`; output construction/calls here execute immediately when this method runs.
9. Assigns `pb2_v03_config` from `proto_utils.ToProto.task_push_notification_config(v03_resp)`; output construction/calls here execute immediately when this method runs.
10. Returns `MessageToDict(pb2_v03_config)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `pb2_v03.CreateTaskPushNotificationConfigRequest`, `Parse`, `proto_utils.FromProto.task_push_notification_config_request`, `types_v03.SetTaskPushNotificationConfigRequest`, `proto_utils.ToProto.task_push_notification_config`, `MessageToDict`, `request.body`, `self.handler03.on_create_task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def set_push_notification(self, request: Request, context: ServerCallContext) -> dict[str, Any]:
    task_id = request.path_params['id']
    body = await request.body()
    v03_pb_push = pb2_v03.CreateTaskPushNotificationConfigRequest()
    Parse(body, v03_pb_push, ignore_unknown_fields=True)
    v03_params_push = proto_utils.FromProto.task_push_notification_config_request(v03_pb_push)
    v03_params_push.task_id = task_id
    rpc_req_push = types_v03.SetTaskPushNotificationConfigRequest(id='', params=v03_params_push)
    v03_resp = await self.handler03.on_create_task_push_notification_config(rpc_req_push, context)
    pb2_v03_config = proto_utils.ToProto.task_push_notification_config(v03_resp)
    return MessageToDict(pb2_v03_config)
```

</details>

### `REST03Handler.on_get_task`

Source lines 237–264; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `dict[str, Any]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'v1/tasks/{id}' REST method. Args: request: The incoming `Request` object. context: Context provided by the server. Returns: A `Task` object containing the Task in v0.3 format.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `task_id` from `request.path_params['id']`; output construction/calls here execute immediately when this method runs.
2. Assigns `history_length_str` from `request.query_params.get('historyLength')`; output construction/calls here execute immediately when this method runs.
3. Assigns `history_length` from `int(history_length_str) if history_length_str else None`; output construction/calls here execute immediately when this method runs.
4. Assigns `rpc_req` from `types_v03.GetTaskRequest(id='', params=types_v03.TaskQueryParams(id=task_id, history_length=history_length))`; output construction/calls here execute immediately when this method runs.
5. Assigns `v03_resp` from `await self.handler03.on_get_task(rpc_req, context)`; output construction/calls here execute immediately when this method runs.
6. Assigns `pb2_v03_task` from `proto_utils.ToProto.task(v03_resp)`; output construction/calls here execute immediately when this method runs.
7. Returns `MessageToDict(pb2_v03_task)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `request.query_params.get`, `types_v03.GetTaskRequest`, `proto_utils.ToProto.task`, `MessageToDict`, `int`, `self.handler03.on_get_task`, `types_v03.TaskQueryParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def on_get_task(self, request: Request, context: ServerCallContext) -> dict[str, Any]:
    task_id = request.path_params['id']
    history_length_str = request.query_params.get('historyLength')
    history_length = int(history_length_str) if history_length_str else None
    rpc_req = types_v03.GetTaskRequest(id='', params=types_v03.TaskQueryParams(id=task_id, history_length=history_length))
    v03_resp = await self.handler03.on_get_task(rpc_req, context)
    pb2_v03_task = proto_utils.ToProto.task(v03_resp)
    return MessageToDict(pb2_v03_task)
```

</details>

### `REST03Handler.list_push_notifications`

Source lines 267–291; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `dict[str, Any]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'tasks/pushNotificationConfig/list' REST method.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `task_id` from `request.path_params['id']`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_req` from `types_v03.ListTaskPushNotificationConfigRequest(id='', params=types_v03.ListTaskPushNotificationConfigParams(id=task_id))`; output construction/calls here execute immediately when this method runs.
3. Assigns `v03_resp` from `await self.handler03.on_list_task_push_notification_configs(rpc_req, context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `pb2_v03_resp` from `pb2_v03.ListTaskPushNotificationConfigResponse(configs=[proto_utils.ToProto.task_push_notification_config(c) for c in v03_resp])`; output construction/calls here execute immediately when this method runs.
5. Returns `MessageToDict(pb2_v03_resp)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `types_v03.ListTaskPushNotificationConfigRequest`, `pb2_v03.ListTaskPushNotificationConfigResponse`, `MessageToDict`, `self.handler03.on_list_task_push_notification_configs`, `types_v03.ListTaskPushNotificationConfigParams`, `proto_utils.ToProto.task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def list_push_notifications(self, request: Request, context: ServerCallContext) -> dict[str, Any]:
    task_id = request.path_params['id']
    rpc_req = types_v03.ListTaskPushNotificationConfigRequest(id='', params=types_v03.ListTaskPushNotificationConfigParams(id=task_id))
    v03_resp = await self.handler03.on_list_task_push_notification_configs(rpc_req, context)
    pb2_v03_resp = pb2_v03.ListTaskPushNotificationConfigResponse(configs=[proto_utils.ToProto.task_push_notification_config(c) for c in v03_resp])
    return MessageToDict(pb2_v03_resp)
```

</details>

### `REST03Handler.on_get_extended_agent_card`

Source lines 294–304; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: Request, context: ServerCallContext)`. Output annotation: `dict[str, Any]`. Decorators: `validate_version(constants.PROTOCOL_VERSION_0_3)`.

Source intent: Handles the 'v1/agent/authenticatedExtendedAgentCard' REST method.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `rpc_req` from `types_v03.GetAuthenticatedExtendedCardRequest(id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `v03_resp` from `await self.handler03.on_get_extended_agent_card(rpc_req, context)`; output construction/calls here execute immediately when this method runs.
3. Returns `v03_resp.model_dump(mode='json', exclude_none=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `validate_version`, `types_v03.GetAuthenticatedExtendedCardRequest`, `v03_resp.model_dump`, `self.handler03.on_get_extended_agent_card`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@validate_version(constants.PROTOCOL_VERSION_0_3)
async def on_get_extended_agent_card(self, request: Request, context: ServerCallContext) -> dict[str, Any]:
    rpc_req = types_v03.GetAuthenticatedExtendedCardRequest(id=0)
    v03_resp = await self.handler03.on_get_extended_agent_card(rpc_req, context)
    return v03_resp.model_dump(mode='json', exclude_none=True)
```

</details>
