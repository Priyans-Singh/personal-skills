# v0_3/rest_transport.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/rest_transport.py`. SHA-256: `7d5ccce6199665c6b3372ac871cbfa7995028df6a0be8c71733eecda08ab37c0`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Client REST state and wire translation

CompatRestTransport retains HTTP client/card, removes one trailing slash from URL, and tracks subscribe method preference. `_execute_request` builds full URL by direct concatenation, optional JSON/query, request-local version/extension headers; `_send_request` delegates to shared helper. IDs are interpolated without explicit escaping, so inputs containing slash/query syntax can alter URLs. Use opaque URL-safe IDs from your own protocol policy.

Send/stream translate current → pivot → legacy protobuf and MessageToDict(preserving_proto_field_name=True), producing snake_case wire fields. Responses ParseDict(ignore_unknown_fields=True) into legacy protobuf → pivot → current. Send returns empty response for unset payload. Get preserves current history_length presence in historyLength query; server protobuf hop can still lose zero. Cancel POSTs task :cancel; create POSTs full CreateTaskPushNotificationConfigRequest with parent, config_id, nested config. Get config GETs nested resource. ListTasks, list_task_push_notification_configs and delete_task_push_notification_config raise NotImplementedError locally; server adapter does expose config-list despite this client gap.

Extended-card GETs `/v1/card` unless cached card says extended-card false, parses legacy protobuf card, converts and replaces cache. close closes injected httpx client. All caches/preferences are instance mutable state without locks or TTL; concurrent subscription/card operations can race, though no corruption guarantee is established by source.

## Exact subscribe fallback state machine

`subscribe` starts override or POST. It streams task :subscribe, catches only A2AClientError whose __cause__ is HTTPStatusError status 405. If no override, stores GET and recursively subscribes once. Successful GET persists for later calls. If an override exists and automatic flag is true, another 405 sets auto false and override POST, then re-raises; later calls use POST with no further fallback. Explicit override initializes auto false and never retries. Once GET was remembered, a later GET 405 resets to POST and raises rather than retrying in the same call. Other errors and domain MethodNotFoundError do not trigger fallback. The docstring's wording 'official method' is not an external guarantee; this is installed implementation behavior.

## Error compatibility boundary

`_handle_http_error` tries to read/decode response and expects **top-level** type/message matching A2A class names. It suppresses StreamClosed during read and certain JSON/value failures. Known type raises mapped domain error. Otherwise 404 becomes MethodNotFoundError with URL; all others become A2AClientError with status. The same SDK's current REST error decorator emits `{'error': {'code','status','message','details'}}`, so its structured domain reason is **not** recognized by this legacy client; generic status fallback applies. Non-dict response JSON can raise AttributeError because .get is assumed. Shared helper reads streaming error bodies before invoking this callback.

`_send_stream_request` parses every data as legacy protobuf JSON and unknown fields are ignored. Unset/unrecognized StreamResponse then raises ValueError in FromProto. Standard SSE `event:error` is already rejected by shared helper; there is no retry except verb fallback. EOF ends stream; no final-state stop or task cancellation call is issued. Call-context timeout goes to HTTP; request-local headers go to A2A peer. Callback token/auth credentials travel only in nested payload. This module does not sign, expire, persist or refresh either category.

```python
import httpx
from a2a.compat.v0_3.rest_transport import CompatRestTransport
transport = CompatRestTransport(httpx.AsyncClient(), None, 'https://example.invalid')
# choose subscribe_method_override='GET' for a known GET-only peer
# await transport.get_task(core_get_request)
```

Setup-only example. Explicitly configure blocking and test file/metadata/card round trips before choosing this legacy protobuf route.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import contextlib
import json
import logging
from collections.abc import AsyncGenerator
from typing import Any, NoReturn
import httpx
from google.protobuf.json_format import MessageToDict, Parse, ParseDict
from a2a.client.client import ClientCallContext
from a2a.client.errors import A2AClientError
from a2a.client.transports.base import ClientTransport
from a2a.client.transports.http_helpers import get_http_args, send_http_request, send_http_stream_request
from a2a.compat.v0_3 import a2a_v0_3_pb2, conversions, proto_utils
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.extension_headers import add_legacy_extension_header
from a2a.types.a2a_pb2 import AgentCard, CancelTaskRequest, DeleteTaskPushNotificationConfigRequest, GetExtendedAgentCardRequest, GetTaskPushNotificationConfigRequest, GetTaskRequest, ListTaskPushNotificationConfigsRequest, ListTaskPushNotificationConfigsResponse, ListTasksRequest, ListTasksResponse, SendMessageRequest, SendMessageResponse, StreamResponse, SubscribeToTaskRequest, Task, TaskPushNotificationConfig
from a2a.utils.constants import PROTOCOL_VERSION_0_3, VERSION_HEADER
from a2a.utils.errors import JSON_RPC_ERROR_CODE_MAP, MethodNotFoundError
from a2a.utils.telemetry import SpanKind, trace_class
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
_A2A_ERROR_NAME_TO_CLS = {error_type.__name__: error_type for error_type in JSON_RPC_ERROR_CODE_MAP}
```

## Declaration-by-declaration execution reference

### `CompatRestTransport`

Source lines 60–428; declaration kind `ClassDef`.

Bases: `ClientTransport`. Decorators: `trace_class(kind=SpanKind.CLIENT)`.

Source definition/intent (executed behavior is determined by fields and methods): A backward compatible REST transport for A2A v0.3.

Declared operations: `__init__`, `send_message`, `send_message_streaming`, `get_task`, `list_tasks`, `cancel_task`, `create_task_push_notification_config`, `get_task_push_notification_config`, `list_task_push_notification_configs`, `delete_task_push_notification_config`, `subscribe`, `get_extended_agent_card`, `close`, `_handle_http_error`, `_send_stream_request`, `_send_request`, `_execute_request`. Each method is traced below; constructor determines retained state.

### `CompatRestTransport.__init__`

Source lines 63–75; declaration kind `FunctionDef`.

Inputs: `(self, httpx_client: httpx.AsyncClient, agent_card: AgentCard | None, url: str, subscribe_method_override: str | None=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Initializes the CompatRestTransport.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.url` from `url.removesuffix('/')`; output construction/calls here execute immediately when this method runs.
2. Assigns `self.httpx_client` from `httpx_client`; output construction/calls here execute immediately when this method runs.
3. Assigns `self.agent_card` from `agent_card`; output construction/calls here execute immediately when this method runs.
4. Assigns `self._subscribe_method_override` from `subscribe_method_override`; output construction/calls here execute immediately when this method runs.
5. Assigns `self._subscribe_auto_method_override` from `subscribe_method_override is None`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `url.removesuffix`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, httpx_client: httpx.AsyncClient, agent_card: AgentCard | None, url: str, subscribe_method_override: str | None=None):
    self.url = url.removesuffix('/')
    self.httpx_client = httpx_client
    self.agent_card = agent_card
    self._subscribe_method_override = subscribe_method_override
    self._subscribe_auto_method_override = subscribe_method_override is None
```

</details>

### `CompatRestTransport.send_message`

Source lines 77–120; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: SendMessageRequest, *, context: ClientCallContext | None=None)`. Output annotation: `SendMessageResponse`. Decorators: `none`.

Source intent: Sends a non-streaming message request to the agent.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_send_message_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_proto` from `a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._execute_request('POST', '/v1/message:send', context=context, json=MessageToDict(req_proto, preserving_proto_field_name=True))`; output construction/calls here execute immediately when this method runs.
4. Assigns `resp_proto` from `ParseDict(response_data, a2a_v0_3_pb2.SendMessageResponse(), ignore_unknown_fields=True)`; output construction/calls here execute immediately when this method runs.
5. Assigns `which` from `resp_proto.WhichOneof('payload')`; output construction/calls here execute immediately when this method runs.
6. Branches on `which == 'task'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
7. Branches on `which == 'msg'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
8. Returns `SendMessageResponse()`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_send_message_request`, `a2a_v0_3_pb2.SendMessageRequest`, `ParseDict`, `resp_proto.WhichOneof`, `SendMessageResponse`, `self._execute_request`, `a2a_v0_3_pb2.SendMessageResponse`, `proto_utils.ToProto.message`, `proto_utils.ToProto.message_send_configuration`, `proto_utils.ToProto.metadata`, `MessageToDict`, `conversions.to_core_task`, `conversions.to_core_message`, `proto_utils.FromProto.task`, `proto_utils.FromProto.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def send_message(self, request: SendMessageRequest, *, context: ClientCallContext | None=None) -> SendMessageResponse:
    req_v03 = conversions.to_compat_send_message_request(request, request_id=0)
    req_proto = a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))
    response_data = await self._execute_request('POST', '/v1/message:send', context=context, json=MessageToDict(req_proto, preserving_proto_field_name=True))
    resp_proto = ParseDict(response_data, a2a_v0_3_pb2.SendMessageResponse(), ignore_unknown_fields=True)
    which = resp_proto.WhichOneof('payload')
    if which == 'task':
        return SendMessageResponse(task=conversions.to_core_task(proto_utils.FromProto.task(resp_proto.task)))
    if which == 'msg':
        return SendMessageResponse(message=conversions.to_core_message(proto_utils.FromProto.message(resp_proto.msg)))
    return SendMessageResponse()
```

</details>

### `CompatRestTransport.send_message_streaming`

Source lines 122–146; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: SendMessageRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AsyncGenerator[StreamResponse]`. Decorators: `none`.

Source intent: Sends a streaming message request to the agent and yields responses as they arrive.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_send_message_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_proto` from `a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))`; output construction/calls here execute immediately when this method runs.
3. Asynchronously iterates `self._send_stream_request('POST', '/v1/message:stream', context=context, json=MessageToDict(req_proto, preserving_proto_field_name=True))` into `event`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `event`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_send_message_request`, `a2a_v0_3_pb2.SendMessageRequest`, `self._send_stream_request`, `proto_utils.ToProto.message`, `proto_utils.ToProto.message_send_configuration`, `proto_utils.ToProto.metadata`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def send_message_streaming(self, request: SendMessageRequest, *, context: ClientCallContext | None=None) -> AsyncGenerator[StreamResponse]:
    req_v03 = conversions.to_compat_send_message_request(request, request_id=0)
    req_proto = a2a_v0_3_pb2.SendMessageRequest(request=proto_utils.ToProto.message(req_v03.params.message), configuration=proto_utils.ToProto.message_send_configuration(req_v03.params.configuration), metadata=proto_utils.ToProto.metadata(req_v03.params.metadata))
    async for event in self._send_stream_request('POST', '/v1/message:stream', context=context, json=MessageToDict(req_proto, preserving_proto_field_name=True)):
        yield event
```

</details>

### `CompatRestTransport.get_task`

Source lines 148–168; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: GetTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `Task`. Decorators: `none`.

Source intent: Retrieves the current state and history of a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `params` from `{}`; output construction/calls here execute immediately when this method runs.
2. Branches on `request.HasField('history_length')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Assigns `response_data` from `await self._execute_request('GET', f'/v1/tasks/{request.id}', context=context, params=params)`; output construction/calls here execute immediately when this method runs.
4. Assigns `resp_proto` from `ParseDict(response_data, a2a_v0_3_pb2.Task(), ignore_unknown_fields=True)`; output construction/calls here execute immediately when this method runs.
5. Returns `conversions.to_core_task(proto_utils.FromProto.task(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `request.HasField`, `ParseDict`, `conversions.to_core_task`, `self._execute_request`, `a2a_v0_3_pb2.Task`, `proto_utils.FromProto.task`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def get_task(self, request: GetTaskRequest, *, context: ClientCallContext | None=None) -> Task:
    params = {}
    if request.HasField('history_length'):
        params['historyLength'] = request.history_length
    response_data = await self._execute_request('GET', f'/v1/tasks/{request.id}', context=context, params=params)
    resp_proto = ParseDict(response_data, a2a_v0_3_pb2.Task(), ignore_unknown_fields=True)
    return conversions.to_core_task(proto_utils.FromProto.task(resp_proto))
```

</details>

### `CompatRestTransport.list_tasks`

Source lines 170–179; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: ListTasksRequest, *, context: ClientCallContext | None=None)`. Output annotation: `ListTasksResponse`. Decorators: `none`.

Source intent: Retrieves tasks for an agent.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Raises `NotImplementedError('ListTasks is not supported in A2A v0.3 REST.')`.

Explicit errors: `NotImplementedError('ListTasks is not supported in A2A v0.3 REST.')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def list_tasks(self, request: ListTasksRequest, *, context: ClientCallContext | None=None) -> ListTasksResponse:
    raise NotImplementedError('ListTasks is not supported in A2A v0.3 REST.')
```

</details>

### `CompatRestTransport.cancel_task`

Source lines 181–196; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: CancelTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `Task`. Decorators: `none`.

Source intent: Requests the agent to cancel a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `response_data` from `await self._execute_request('POST', f'/v1/tasks/{request.id}:cancel', context=context)`; output construction/calls here execute immediately when this method runs.
2. Assigns `resp_proto` from `ParseDict(response_data, a2a_v0_3_pb2.Task(), ignore_unknown_fields=True)`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_core_task(proto_utils.FromProto.task(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `ParseDict`, `conversions.to_core_task`, `self._execute_request`, `a2a_v0_3_pb2.Task`, `proto_utils.FromProto.task`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def cancel_task(self, request: CancelTaskRequest, *, context: ClientCallContext | None=None) -> Task:
    response_data = await self._execute_request('POST', f'/v1/tasks/{request.id}:cancel', context=context)
    resp_proto = ParseDict(response_data, a2a_v0_3_pb2.Task(), ignore_unknown_fields=True)
    return conversions.to_core_task(proto_utils.FromProto.task(resp_proto))
```

</details>

### `CompatRestTransport.create_task_push_notification_config`

Source lines 198–230; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: TaskPushNotificationConfig, *, context: ClientCallContext | None=None)`. Output annotation: `TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Sets or updates the push notification configuration for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_create_task_push_notification_config_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `req_proto` from `a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest(parent=f'tasks/{request.task_id}', config_id=req_v03.params.push_notification_config.id, config=proto_utils.ToProto.task_push_notification_config(req_v03.params))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._execute_request('POST', f'/v1/tasks/{request.task_id}/pushNotificationConfigs', context=context, json=MessageToDict(req_proto, preserving_proto_field_name=True))`; output construction/calls here execute immediately when this method runs.
4. Assigns `resp_proto` from `ParseDict(response_data, a2a_v0_3_pb2.TaskPushNotificationConfig(), ignore_unknown_fields=True)`; output construction/calls here execute immediately when this method runs.
5. Returns `conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_create_task_push_notification_config_request`, `a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest`, `ParseDict`, `conversions.to_core_task_push_notification_config`, `self._execute_request`, `a2a_v0_3_pb2.TaskPushNotificationConfig`, `proto_utils.FromProto.task_push_notification_config`, `proto_utils.ToProto.task_push_notification_config`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def create_task_push_notification_config(self, request: TaskPushNotificationConfig, *, context: ClientCallContext | None=None) -> TaskPushNotificationConfig:
    req_v03 = conversions.to_compat_create_task_push_notification_config_request(request, request_id=0)
    req_proto = a2a_v0_3_pb2.CreateTaskPushNotificationConfigRequest(parent=f'tasks/{request.task_id}', config_id=req_v03.params.push_notification_config.id, config=proto_utils.ToProto.task_push_notification_config(req_v03.params))
    response_data = await self._execute_request('POST', f'/v1/tasks/{request.task_id}/pushNotificationConfigs', context=context, json=MessageToDict(req_proto, preserving_proto_field_name=True))
    resp_proto = ParseDict(response_data, a2a_v0_3_pb2.TaskPushNotificationConfig(), ignore_unknown_fields=True)
    return conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))
```

</details>

### `CompatRestTransport.get_task_push_notification_config`

Source lines 232–251; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: GetTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None)`. Output annotation: `TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Retrieves the push notification configuration for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `response_data` from `await self._execute_request('GET', f'/v1/tasks/{request.task_id}/pushNotificationConfigs/{request.id}', context=context)`; output construction/calls here execute immediately when this method runs.
2. Assigns `resp_proto` from `ParseDict(response_data, a2a_v0_3_pb2.TaskPushNotificationConfig(), ignore_unknown_fields=True)`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `ParseDict`, `conversions.to_core_task_push_notification_config`, `self._execute_request`, `a2a_v0_3_pb2.TaskPushNotificationConfig`, `proto_utils.FromProto.task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def get_task_push_notification_config(self, request: GetTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None) -> TaskPushNotificationConfig:
    response_data = await self._execute_request('GET', f'/v1/tasks/{request.task_id}/pushNotificationConfigs/{request.id}', context=context)
    resp_proto = ParseDict(response_data, a2a_v0_3_pb2.TaskPushNotificationConfig(), ignore_unknown_fields=True)
    return conversions.to_core_task_push_notification_config(proto_utils.FromProto.task_push_notification_config(resp_proto))
```

</details>

### `CompatRestTransport.list_task_push_notification_configs`

Source lines 253–262; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: ListTaskPushNotificationConfigsRequest, *, context: ClientCallContext | None=None)`. Output annotation: `ListTaskPushNotificationConfigsResponse`. Decorators: `none`.

Source intent: Lists push notification configurations for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Raises `NotImplementedError('list_task_push_notification_configs not supported in v0.3 REST')`.

Explicit errors: `NotImplementedError('list_task_push_notification_configs not supported in v0.3 REST')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def list_task_push_notification_configs(self, request: ListTaskPushNotificationConfigsRequest, *, context: ClientCallContext | None=None) -> ListTaskPushNotificationConfigsResponse:
    raise NotImplementedError('list_task_push_notification_configs not supported in v0.3 REST')
```

</details>

### `CompatRestTransport.delete_task_push_notification_config`

Source lines 264–273; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: DeleteTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None)`. Output annotation: `None`. Decorators: `none`.

Source intent: Deletes the push notification configuration for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Raises `NotImplementedError('delete_task_push_notification_config not supported in v0.3 REST')`.

Explicit errors: `NotImplementedError('delete_task_push_notification_config not supported in v0.3 REST')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def delete_task_push_notification_config(self, request: DeleteTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None) -> None:
    raise NotImplementedError('delete_task_push_notification_config not supported in v0.3 REST')
```

</details>

### `CompatRestTransport.subscribe`

Source lines 275–315; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: SubscribeToTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AsyncGenerator[StreamResponse]`. Decorators: `none`.

Source intent: Reconnects to get task updates. This method implements backward compatibility logic for the subscribe endpoint. It first attempts to use POST, which is the official method for A2A subscribe endpoint. If the server returns 405 Method Not Allowed, it falls back to GET and remembers this preference for future calls on this transport instance. If both fail with 405, it will default back to POST for next calls but will not retry again.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `subscribe_method` from `self._subscribe_method_override or 'POST'`; output construction/calls here execute immediately when this method runs.
2. Runs guarded operations; catches `A2AClientError` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.

Yielded output expressions: `event`, `event`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self._send_stream_request`, `isinstance`, `self.subscribe`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def subscribe(self, request: SubscribeToTaskRequest, *, context: ClientCallContext | None=None) -> AsyncGenerator[StreamResponse]:
    subscribe_method = self._subscribe_method_override or 'POST'
    try:
        async for event in self._send_stream_request(subscribe_method, f'/v1/tasks/{request.id}:subscribe', context=context):
            yield event
    except A2AClientError as e:
        cause = e.__cause__
        if isinstance(cause, httpx.HTTPStatusError) and cause.response.status_code == httpx.codes.METHOD_NOT_ALLOWED:
            if self._subscribe_method_override:
                if self._subscribe_auto_method_override:
                    self._subscribe_auto_method_override = False
                    self._subscribe_method_override = 'POST'
                raise
            else:
                self._subscribe_method_override = 'GET'
                async for event in self.subscribe(request, context=context):
                    yield event
        else:
            raise
```

</details>

### `CompatRestTransport.get_extended_agent_card`

Source lines 317–338; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: GetExtendedAgentCardRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AgentCard`. Decorators: `none`.

Source intent: Retrieves the Extended AgentCard.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `card` from `self.agent_card`; output construction/calls here execute immediately when this method runs.
2. Branches on `card and (not card.capabilities.extended_agent_card)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Assigns `response_data` from `await self._execute_request('GET', '/v1/card', context=context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `resp_proto` from `ParseDict(response_data, a2a_v0_3_pb2.AgentCard(), ignore_unknown_fields=True)`; output construction/calls here execute immediately when this method runs.
5. Assigns `card` from `conversions.to_core_agent_card(proto_utils.FromProto.agent_card(resp_proto))`; output construction/calls here execute immediately when this method runs.
6. Assigns `self.agent_card` from `card`; output construction/calls here execute immediately when this method runs.
7. Returns `card`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `ParseDict`, `conversions.to_core_agent_card`, `self._execute_request`, `a2a_v0_3_pb2.AgentCard`, `proto_utils.FromProto.agent_card`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def get_extended_agent_card(self, request: GetExtendedAgentCardRequest, *, context: ClientCallContext | None=None) -> AgentCard:
    card = self.agent_card
    if card and (not card.capabilities.extended_agent_card):
        return card
    response_data = await self._execute_request('GET', '/v1/card', context=context)
    resp_proto = ParseDict(response_data, a2a_v0_3_pb2.AgentCard(), ignore_unknown_fields=True)
    card = conversions.to_core_agent_card(proto_utils.FromProto.agent_card(resp_proto))
    self.agent_card = card
    return card
```

</details>

### `CompatRestTransport.close`

Source lines 340–342; declaration kind `AsyncFunctionDef`.

Inputs: `(self)`. Output annotation: `None`. Decorators: `none`.

Source intent: Closes the httpx client.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `await self.httpx_client.aclose()`; awaits completion before continuing.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `self.httpx_client.aclose`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def close(self) -> None:
    await self.httpx_client.aclose()
```

</details>

### `CompatRestTransport._handle_http_error`

Source lines 344–371; declaration kind `FunctionDef`.

Inputs: `(self, e: httpx.HTTPStatusError)`. Output annotation: `NoReturn`. Decorators: `none`.

Source intent: Handles HTTP status errors and raises the appropriate A2AError.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Runs guarded operations; catches `(json.JSONDecodeError, ValueError)` only. Else/finally clauses, when present, run as shown below; exceptions outside these catches propagate.
2. Assigns `status_code` from `e.response.status_code`; output construction/calls here execute immediately when this method runs.
3. Branches on `status_code == httpx.codes.NOT_FOUND`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Raises `A2AClientError(f'HTTP Error {status_code}: {e}')`, chained from `e`.

Explicit errors: `A2AClientError(f'HTTP Error {status_code}: {e}')`; `MethodNotFoundError(f'Resource not found: {e.request.url}')`; `exception_cls(message)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `A2AClientError`, `error_data.get`, `isinstance`, `MethodNotFoundError`, `contextlib.suppress`, `e.response.read`, `e.response.json`, `str`, `_A2A_ERROR_NAME_TO_CLS.get`, `exception_cls`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _handle_http_error(self, e: httpx.HTTPStatusError) -> NoReturn:
    try:
        with contextlib.suppress(httpx.StreamClosed):
            e.response.read()
        try:
            error_data = e.response.json()
        except (json.JSONDecodeError, ValueError, httpx.ResponseNotRead):
            error_data = {}
        error_type = error_data.get('type')
        message = error_data.get('message', str(e))
        if isinstance(error_type, str):
            exception_cls = _A2A_ERROR_NAME_TO_CLS.get(error_type)
            if exception_cls:
                raise exception_cls(message) from e
    except (json.JSONDecodeError, ValueError):
        pass
    status_code = e.response.status_code
    if status_code == httpx.codes.NOT_FOUND:
        raise MethodNotFoundError(f'Resource not found: {e.request.url}') from e
    raise A2AClientError(f'HTTP Error {status_code}: {e}') from e
```

</details>

### `CompatRestTransport._send_stream_request`

Source lines 373–400; declaration kind `AsyncFunctionDef`.

Inputs: `(self, method: str, path: str, context: ClientCallContext | None=None, *, json: dict[str, Any] | None=None)`. Output annotation: `AsyncGenerator[StreamResponse]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `http_kwargs` from `get_http_args(context)`; output construction/calls here execute immediately when this method runs.
2. Executes `http_kwargs.setdefault('headers', {})`.
3. Assigns `http_kwargs['headers'][VERSION_HEADER.lower()]` from `PROTOCOL_VERSION_0_3`; output construction/calls here execute immediately when this method runs.
4. Executes `add_legacy_extension_header(http_kwargs['headers'])`.
5. Asynchronously iterates `send_http_stream_request(self.httpx_client, method, f'{self.url}{path}', self._handle_http_error, json=json, **http_kwargs)` into `sse_data`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=proto_utils.FromProto.stream_response(event_proto)))`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `get_http_args`, `http_kwargs.setdefault`, `add_legacy_extension_header`, `send_http_stream_request`, `VERSION_HEADER.lower`, `a2a_v0_3_pb2.StreamResponse`, `Parse`, `conversions.to_core_stream_response`, `types_v03.SendStreamingMessageSuccessResponse`, `proto_utils.FromProto.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _send_stream_request(self, method: str, path: str, context: ClientCallContext | None=None, *, json: dict[str, Any] | None=None) -> AsyncGenerator[StreamResponse]:
    http_kwargs = get_http_args(context)
    http_kwargs.setdefault('headers', {})
    http_kwargs['headers'][VERSION_HEADER.lower()] = PROTOCOL_VERSION_0_3
    add_legacy_extension_header(http_kwargs['headers'])
    async for sse_data in send_http_stream_request(self.httpx_client, method, f'{self.url}{path}', self._handle_http_error, json=json, **http_kwargs):
        event_proto = a2a_v0_3_pb2.StreamResponse()
        Parse(sse_data, event_proto, ignore_unknown_fields=True)
        yield conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=proto_utils.FromProto.stream_response(event_proto)))
```

</details>

### `CompatRestTransport._send_request`

Source lines 402–405; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: httpx.Request)`. Output annotation: `dict[str, Any]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `await send_http_request(self.httpx_client, request, self._handle_http_error)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `send_http_request`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _send_request(self, request: httpx.Request) -> dict[str, Any]:
    return await send_http_request(self.httpx_client, request, self._handle_http_error)
```

</details>

### `CompatRestTransport._execute_request`

Source lines 407–428; declaration kind `AsyncFunctionDef`.

Inputs: `(self, method: str, path: str, context: ClientCallContext | None=None, *, json: dict[str, Any] | None=None, params: dict[str, Any] | None=None)`. Output annotation: `dict[str, Any]`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `http_kwargs` from `get_http_args(context)`; output construction/calls here execute immediately when this method runs.
2. Executes `http_kwargs.setdefault('headers', {})`.
3. Assigns `http_kwargs['headers'][VERSION_HEADER.lower()]` from `PROTOCOL_VERSION_0_3`; output construction/calls here execute immediately when this method runs.
4. Executes `add_legacy_extension_header(http_kwargs['headers'])`.
5. Assigns `request` from `self.httpx_client.build_request(method, f'{self.url}{path}', json=json, params=params, **http_kwargs)`; output construction/calls here execute immediately when this method runs.
6. Returns `await self._send_request(request)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `get_http_args`, `http_kwargs.setdefault`, `add_legacy_extension_header`, `self.httpx_client.build_request`, `VERSION_HEADER.lower`, `self._send_request`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _execute_request(self, method: str, path: str, context: ClientCallContext | None=None, *, json: dict[str, Any] | None=None, params: dict[str, Any] | None=None) -> dict[str, Any]:
    http_kwargs = get_http_args(context)
    http_kwargs.setdefault('headers', {})
    http_kwargs['headers'][VERSION_HEADER.lower()] = PROTOCOL_VERSION_0_3
    add_legacy_extension_header(http_kwargs['headers'])
    request = self.httpx_client.build_request(method, f'{self.url}{path}', json=json, params=params, **http_kwargs)
    return await self._send_request(request)
```

</details>
