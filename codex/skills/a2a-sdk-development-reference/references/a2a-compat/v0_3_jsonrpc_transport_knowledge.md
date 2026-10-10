# v0_3/jsonrpc_transport.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/jsonrpc_transport.py`. SHA-256: `4a94707a77a206055030fbe3a15b0e1b82e1b4025e3179f7fffcbc1f10ab8bb6`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Client wire flow and ownership

CompatJsonRpcTransport retains injected httpx.AsyncClient, current AgentCard and exact URL. Each unary request converts current protobuf to pivot params, dumps aliases/excludes None, creates JSONRPC20Request with a new UUID string ID (conversion's request_id=0 is discarded), and POSTs to the same URL. `_send_request` derives request-local HTTP kwargs, forces lowercase a2a-version=0.3, mirrors extension header and builds request. Shared HTTP helper sends, checks status and parses JSON. No local response-ID correlation check is visible; JSONRPC20Response validation is delegated to jsonrpc library.

Send classifies `result.kind` task/message; if omitted, messageId wins before id. Nondict/unrecognized kind returns empty core SendMessageResponse rather than raising. Get/cancel validate Task. Create/get push validate nested config; list requires a list or returns empty response, loops each config and drops pagination. Delete inserts result=None when neither result nor error was returned. ListTasks always raises NotImplementedError before I/O. Extended-card returns cached card immediately when its extended_agent_card bool is false; otherwise requests `agent/getAuthenticatedExtendedCard`, converts and replaces cache. Request tenant and metadata unsupported by converters are not transferred.

## Streams, errors, and failure visibility

Send-stream/resubscribe build message/stream or tasks/resubscribe envelopes and iterate `_send_stream_request`. It parses each SSE data with json.loads, raises for error key, skips nondict results, selects task/message/status-update/artifact-update. Missing kind fallback recognizes taskId+final as status first, then messageId, then id; missing-kind artifact updates are silently skipped. Unknown kinds are skipped. No retry, resume Last-Event-ID, cursor, deduplication or final-based termination; helper reads until stream EOF/exception/cancel.

`_create_jsonrpc_error` returns an exception (despite docstring saying raises): known integer code maps to current A2A error class, otherwise A2AClientError; error.data is discarded. `_handle_http_error` always raises A2AClientError containing status only. Shared helper maps timeout/network/JSON decode errors. Pydantic errors are not normalized here. close awaits injected client's aclose, affecting other users of that shared client.

## Credentials and async policy

Call-context service_parameters become headers to the configured A2A peer URL; context timeout becomes httpx.Timeout for that call. Neither this transport nor its helpers fetch/refresh/expire credentials. Injected client auth/cookies/TLS configuration lives for client's lifetime. Push callback credentials are payload fields destined for future callback configuration, never automatically copied into peer headers. Cache is per transport instance without lock or TTL; concurrent extended-card calls may both execute. Early closing generators should be explicit; no executor-task cancellation RPC is sent on stream close.

```python
import httpx
from a2a.compat.v0_3.jsonrpc_transport import CompatJsonRpcTransport
from a2a.client.client import ClientCallContext
transport = CompatJsonRpcTransport(httpx.AsyncClient(), None, 'https://example.invalid/a2a')
context = ClientCallContext(timeout=5, service_parameters={'A2A-Extensions': 'urn:example'})
# await transport.send_message(core_request, context=context)
# await transport.close()  # closes the injected client
```

This is setup-only; no request is executed. Use caller-owned test doubles for local integration. Avoid blind retries for send/create/cancel/delete: compat has no idempotency guarantee.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import json
import logging
from collections.abc import AsyncGenerator
from typing import Any, NoReturn
from uuid import uuid4
import httpx
from jsonrpc.jsonrpc2 import JSONRPC20Request, JSONRPC20Response
from a2a.client.client import ClientCallContext
from a2a.client.errors import A2AClientError
from a2a.client.transports.base import ClientTransport
from a2a.client.transports.http_helpers import get_http_args, send_http_request, send_http_stream_request
from a2a.compat.v0_3 import conversions
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.extension_headers import add_legacy_extension_header
from a2a.types.a2a_pb2 import AgentCard, CancelTaskRequest, DeleteTaskPushNotificationConfigRequest, GetExtendedAgentCardRequest, GetTaskPushNotificationConfigRequest, GetTaskRequest, ListTaskPushNotificationConfigsRequest, ListTaskPushNotificationConfigsResponse, ListTasksRequest, ListTasksResponse, SendMessageRequest, SendMessageResponse, StreamResponse, SubscribeToTaskRequest, Task, TaskPushNotificationConfig
from a2a.utils.constants import PROTOCOL_VERSION_0_3, VERSION_HEADER
from a2a.utils.errors import JSON_RPC_ERROR_CODE_MAP
from a2a.utils.telemetry import SpanKind, trace_class
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
_JSON_RPC_ERROR_CODE_TO_A2A_ERROR = {code: error_type for error_type, code in JSON_RPC_ERROR_CODE_MAP.items()}
```

## Declaration-by-declaration execution reference

### `CompatJsonRpcTransport`

Source lines 54–498; declaration kind `ClassDef`.

Bases: `ClientTransport`. Decorators: `trace_class(kind=SpanKind.CLIENT)`.

Source definition/intent (executed behavior is determined by fields and methods): A backward compatible JSON-RPC transport for A2A v0.3.

Declared operations: `__init__`, `send_message`, `send_message_streaming`, `get_task`, `list_tasks`, `cancel_task`, `create_task_push_notification_config`, `get_task_push_notification_config`, `list_task_push_notification_configs`, `delete_task_push_notification_config`, `subscribe`, `get_extended_agent_card`, `close`, `_create_jsonrpc_error`, `_handle_http_error`, `_send_stream_request`, `_send_request`. Each method is traced below; constructor determines retained state.

### `CompatJsonRpcTransport.__init__`

Source lines 57–66; declaration kind `FunctionDef`.

Inputs: `(self, httpx_client: httpx.AsyncClient, agent_card: AgentCard | None, url: str)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Initializes the CompatJsonRpcTransport.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.url` from `url`; output construction/calls here execute immediately when this method runs.
2. Assigns `self.httpx_client` from `httpx_client`; output construction/calls here execute immediately when this method runs.
3. Assigns `self.agent_card` from `agent_card`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, httpx_client: httpx.AsyncClient, agent_card: AgentCard | None, url: str):
    self.url = url
    self.httpx_client = httpx_client
    self.agent_card = agent_card
```

</details>

### `CompatJsonRpcTransport.send_message`

Source lines 68–119; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: SendMessageRequest, *, context: ClientCallContext | None=None)`. Output annotation: `SendMessageResponse`. Decorators: `none`.

Source intent: Sends a non-streaming message request to the agent.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_send_message_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='message/send', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
5. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Assigns `result_dict` from `json_rpc_response.result`; output construction/calls here execute immediately when this method runs.
7. Branches on `not isinstance(result_dict, dict)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
8. Assigns `kind` from `result_dict.get('kind')`; output construction/calls here execute immediately when this method runs.
9. Branches on `not kind`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
10. Branches on `kind == 'task'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
11. Branches on `kind == 'message'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
12. Returns `SendMessageResponse()`; this is the output/delegation boundary for this path.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_send_message_request`, `JSONRPC20Request`, `JSONRPC20Response`, `result_dict.get`, `SendMessageResponse`, `self._send_request`, `self._create_jsonrpc_error`, `isinstance`, `req_v03.params.model_dump`, `str`, `dict`, `uuid4`, `conversions.to_core_task`, `conversions.to_core_message`, `types_v03.Task.model_validate`, `types_v03.Message.model_validate`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def send_message(self, request: SendMessageRequest, *, context: ClientCallContext | None=None) -> SendMessageResponse:
    req_v03 = conversions.to_compat_send_message_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='message/send', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
    result_dict = json_rpc_response.result
    if not isinstance(result_dict, dict):
        return SendMessageResponse()
    kind = result_dict.get('kind')
    if not kind:
        if 'messageId' in result_dict:
            kind = 'message'
        elif 'id' in result_dict:
            kind = 'task'
    if kind == 'task':
        return SendMessageResponse(task=conversions.to_core_task(types_v03.Task.model_validate(result_dict)))
    if kind == 'message':
        return SendMessageResponse(message=conversions.to_core_message(types_v03.Message.model_validate(result_dict)))
    return SendMessageResponse()
```

</details>

### `CompatJsonRpcTransport.send_message_streaming`

Source lines 121–143; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: SendMessageRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AsyncGenerator[StreamResponse]`. Decorators: `none`.

Source intent: Sends a streaming message request to the agent and yields responses as they arrive.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_send_message_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='message/stream', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Asynchronously iterates `self._send_stream_request(dict(rpc_request.data), context)` into `event`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `event`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_send_message_request`, `JSONRPC20Request`, `self._send_stream_request`, `dict`, `req_v03.params.model_dump`, `str`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def send_message_streaming(self, request: SendMessageRequest, *, context: ClientCallContext | None=None) -> AsyncGenerator[StreamResponse]:
    req_v03 = conversions.to_compat_send_message_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='message/stream', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    async for event in self._send_stream_request(dict(rpc_request.data), context):
        yield event
```

</details>

### `CompatJsonRpcTransport.get_task`

Source lines 145–169; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: GetTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `Task`. Decorators: `none`.

Source intent: Retrieves the current state and history of a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_get_task_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='tasks/get', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
5. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `conversions.to_core_task(types_v03.Task.model_validate(json_rpc_response.result))`; this is the output/delegation boundary for this path.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_get_task_request`, `JSONRPC20Request`, `JSONRPC20Response`, `conversions.to_core_task`, `self._send_request`, `self._create_jsonrpc_error`, `types_v03.Task.model_validate`, `req_v03.params.model_dump`, `str`, `dict`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def get_task(self, request: GetTaskRequest, *, context: ClientCallContext | None=None) -> Task:
    req_v03 = conversions.to_compat_get_task_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='tasks/get', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
    return conversions.to_core_task(types_v03.Task.model_validate(json_rpc_response.result))
```

</details>

### `CompatJsonRpcTransport.list_tasks`

Source lines 171–180; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: ListTasksRequest, *, context: ClientCallContext | None=None)`. Output annotation: `ListTasksResponse`. Decorators: `none`.

Source intent: Retrieves tasks for an agent.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Raises `NotImplementedError('ListTasks is not supported in A2A v0.3 JSONRPC.')`.

Explicit errors: `NotImplementedError('ListTasks is not supported in A2A v0.3 JSONRPC.')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def list_tasks(self, request: ListTasksRequest, *, context: ClientCallContext | None=None) -> ListTasksResponse:
    raise NotImplementedError('ListTasks is not supported in A2A v0.3 JSONRPC.')
```

</details>

### `CompatJsonRpcTransport.cancel_task`

Source lines 182–209; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: CancelTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `Task`. Decorators: `none`.

Source intent: Requests the agent to cancel a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_cancel_task_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='tasks/cancel', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
5. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `conversions.to_core_task(types_v03.Task.model_validate(json_rpc_response.result))`; this is the output/delegation boundary for this path.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_cancel_task_request`, `JSONRPC20Request`, `JSONRPC20Response`, `conversions.to_core_task`, `self._send_request`, `self._create_jsonrpc_error`, `types_v03.Task.model_validate`, `req_v03.params.model_dump`, `str`, `dict`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def cancel_task(self, request: CancelTaskRequest, *, context: ClientCallContext | None=None) -> Task:
    req_v03 = conversions.to_compat_cancel_task_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='tasks/cancel', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
    return conversions.to_core_task(types_v03.Task.model_validate(json_rpc_response.result))
```

</details>

### `CompatJsonRpcTransport.create_task_push_notification_config`

Source lines 211–241; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: TaskPushNotificationConfig, *, context: ClientCallContext | None=None)`. Output annotation: `TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Sets or updates the push notification configuration for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_create_task_push_notification_config_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='tasks/pushNotificationConfig/set', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
5. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `conversions.to_core_task_push_notification_config(types_v03.TaskPushNotificationConfig.model_validate(json_rpc_response.result))`; this is the output/delegation boundary for this path.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_create_task_push_notification_config_request`, `JSONRPC20Request`, `JSONRPC20Response`, `conversions.to_core_task_push_notification_config`, `self._send_request`, `self._create_jsonrpc_error`, `types_v03.TaskPushNotificationConfig.model_validate`, `req_v03.params.model_dump`, `str`, `dict`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def create_task_push_notification_config(self, request: TaskPushNotificationConfig, *, context: ClientCallContext | None=None) -> TaskPushNotificationConfig:
    req_v03 = conversions.to_compat_create_task_push_notification_config_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='tasks/pushNotificationConfig/set', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
    return conversions.to_core_task_push_notification_config(types_v03.TaskPushNotificationConfig.model_validate(json_rpc_response.result))
```

</details>

### `CompatJsonRpcTransport.get_task_push_notification_config`

Source lines 243–273; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: GetTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None)`. Output annotation: `TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Retrieves the push notification configuration for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_get_task_push_notification_config_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='tasks/pushNotificationConfig/get', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
5. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `conversions.to_core_task_push_notification_config(types_v03.TaskPushNotificationConfig.model_validate(json_rpc_response.result))`; this is the output/delegation boundary for this path.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_get_task_push_notification_config_request`, `JSONRPC20Request`, `JSONRPC20Response`, `conversions.to_core_task_push_notification_config`, `self._send_request`, `self._create_jsonrpc_error`, `types_v03.TaskPushNotificationConfig.model_validate`, `req_v03.params.model_dump`, `str`, `dict`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def get_task_push_notification_config(self, request: GetTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None) -> TaskPushNotificationConfig:
    req_v03 = conversions.to_compat_get_task_push_notification_config_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='tasks/pushNotificationConfig/get', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
    return conversions.to_core_task_push_notification_config(types_v03.TaskPushNotificationConfig.model_validate(json_rpc_response.result))
```

</details>

### `CompatJsonRpcTransport.list_task_push_notification_configs`

Source lines 275–314; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: ListTaskPushNotificationConfigsRequest, *, context: ClientCallContext | None=None)`. Output annotation: `ListTaskPushNotificationConfigsResponse`. Decorators: `none`.

Source intent: Lists push notification configurations for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_list_task_push_notification_config_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='tasks/pushNotificationConfig/list', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
4. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
5. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Assigns `configs_data` from `json_rpc_response.result`; output construction/calls here execute immediately when this method runs.
7. Branches on `not isinstance(configs_data, list)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
8. Assigns `response` from `ListTaskPushNotificationConfigsResponse()`; output construction/calls here execute immediately when this method runs.
9. Iterates `configs_data` into `config_data`; each iteration performs the shown conversion/delegation, preserving iteration order.
10. Returns `response`; this is the output/delegation boundary for this path.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_list_task_push_notification_config_request`, `JSONRPC20Request`, `JSONRPC20Response`, `ListTaskPushNotificationConfigsResponse`, `self._send_request`, `self._create_jsonrpc_error`, `isinstance`, `response.configs.append`, `req_v03.params.model_dump`, `str`, `dict`, `conversions.to_core_task_push_notification_config`, `uuid4`, `types_v03.TaskPushNotificationConfig.model_validate`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def list_task_push_notification_configs(self, request: ListTaskPushNotificationConfigsRequest, *, context: ClientCallContext | None=None) -> ListTaskPushNotificationConfigsResponse:
    req_v03 = conversions.to_compat_list_task_push_notification_config_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='tasks/pushNotificationConfig/list', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
    configs_data = json_rpc_response.result
    if not isinstance(configs_data, list):
        return ListTaskPushNotificationConfigsResponse()
    response = ListTaskPushNotificationConfigsResponse()
    for config_data in configs_data:
        response.configs.append(conversions.to_core_task_push_notification_config(types_v03.TaskPushNotificationConfig.model_validate(config_data)))
    return response
```

</details>

### `CompatJsonRpcTransport.delete_task_push_notification_config`

Source lines 316–343; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: DeleteTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None)`. Output annotation: `None`. Decorators: `none`.

Source intent: Deletes the push notification configuration for a specific task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_delete_task_push_notification_config_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='tasks/pushNotificationConfig/delete', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
4. Branches on `'result' not in response_data and 'error' not in response_data`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
6. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_delete_task_push_notification_config_request`, `JSONRPC20Request`, `JSONRPC20Response`, `self._send_request`, `self._create_jsonrpc_error`, `req_v03.params.model_dump`, `str`, `dict`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def delete_task_push_notification_config(self, request: DeleteTaskPushNotificationConfigRequest, *, context: ClientCallContext | None=None) -> None:
    req_v03 = conversions.to_compat_delete_task_push_notification_config_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='tasks/pushNotificationConfig/delete', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    if 'result' not in response_data and 'error' not in response_data:
        response_data['result'] = None
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
```

</details>

### `CompatJsonRpcTransport.subscribe`

Source lines 345–366; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: SubscribeToTaskRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AsyncGenerator[StreamResponse]`. Decorators: `none`.

Source intent: Reconnects to get task updates.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `req_v03` from `conversions.to_compat_subscribe_to_task_request(request, request_id=0)`; output construction/calls here execute immediately when this method runs.
2. Assigns `rpc_request` from `JSONRPC20Request(method='tasks/resubscribe', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
3. Asynchronously iterates `self._send_stream_request(dict(rpc_request.data), context)` into `event`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `event`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_compat_subscribe_to_task_request`, `JSONRPC20Request`, `self._send_stream_request`, `dict`, `req_v03.params.model_dump`, `str`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def subscribe(self, request: SubscribeToTaskRequest, *, context: ClientCallContext | None=None) -> AsyncGenerator[StreamResponse]:
    req_v03 = conversions.to_compat_subscribe_to_task_request(request, request_id=0)
    rpc_request = JSONRPC20Request(method='tasks/resubscribe', params=req_v03.params.model_dump(by_alias=True, exclude_none=True, mode='json'), _id=str(uuid4()))
    async for event in self._send_stream_request(dict(rpc_request.data), context):
        yield event
```

</details>

### `CompatJsonRpcTransport.get_extended_agent_card`

Source lines 368–395; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: GetExtendedAgentCardRequest, *, context: ClientCallContext | None=None)`. Output annotation: `AgentCard`. Decorators: `none`.

Source intent: Retrieves the Extended AgentCard.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `card` from `self.agent_card`; output construction/calls here execute immediately when this method runs.
2. Branches on `card and (not card.capabilities.extended_agent_card)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Assigns `rpc_request` from `JSONRPC20Request(method='agent/getAuthenticatedExtendedCard', params={}, _id=str(uuid4()))`; output construction/calls here execute immediately when this method runs.
4. Assigns `response_data` from `await self._send_request(dict(rpc_request.data), context)`; output construction/calls here execute immediately when this method runs.
5. Assigns `json_rpc_response` from `JSONRPC20Response(**response_data)`; output construction/calls here execute immediately when this method runs.
6. Branches on `json_rpc_response.error`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
7. Assigns `card` from `conversions.to_core_agent_card(types_v03.AgentCard.model_validate(json_rpc_response.result))`; output construction/calls here execute immediately when this method runs.
8. Assigns `self.agent_card` from `card`; output construction/calls here execute immediately when this method runs.
9. Returns `card`; this is the output/delegation boundary for this path.

Explicit errors: `self._create_jsonrpc_error(json_rpc_response.error)`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `JSONRPC20Request`, `JSONRPC20Response`, `conversions.to_core_agent_card`, `self._send_request`, `self._create_jsonrpc_error`, `types_v03.AgentCard.model_validate`, `str`, `dict`, `uuid4`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def get_extended_agent_card(self, request: GetExtendedAgentCardRequest, *, context: ClientCallContext | None=None) -> AgentCard:
    card = self.agent_card
    if card and (not card.capabilities.extended_agent_card):
        return card
    rpc_request = JSONRPC20Request(method='agent/getAuthenticatedExtendedCard', params={}, _id=str(uuid4()))
    response_data = await self._send_request(dict(rpc_request.data), context)
    json_rpc_response = JSONRPC20Response(**response_data)
    if json_rpc_response.error:
        raise self._create_jsonrpc_error(json_rpc_response.error)
    card = conversions.to_core_agent_card(types_v03.AgentCard.model_validate(json_rpc_response.result))
    self.agent_card = card
    return card
```

</details>

### `CompatJsonRpcTransport.close`

Source lines 397–399; declaration kind `AsyncFunctionDef`.

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

### `CompatJsonRpcTransport._create_jsonrpc_error`

Source lines 401–411; declaration kind `FunctionDef`.

Inputs: `(self, error_dict: dict[str, Any])`. Output annotation: `Exception`. Decorators: `none`.

Source intent: Raises a specific error based on jsonrpc error code.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `code` from `error_dict.get('code')`; output construction/calls here execute immediately when this method runs.
2. Assigns `message` from `error_dict.get('message', 'Unknown Error')`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(code, int)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `A2AClientError(message)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `error_dict.get`, `isinstance`, `A2AClientError`, `_JSON_RPC_ERROR_CODE_TO_A2A_ERROR.get`, `error_class`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _create_jsonrpc_error(self, error_dict: dict[str, Any]) -> Exception:
    code = error_dict.get('code')
    message = error_dict.get('message', 'Unknown Error')
    if isinstance(code, int):
        error_class = _JSON_RPC_ERROR_CODE_TO_A2A_ERROR.get(code)
        if error_class:
            return error_class(message)
    return A2AClientError(message)
```

</details>

### `CompatJsonRpcTransport._handle_http_error`

Source lines 413–415; declaration kind `FunctionDef`.

Inputs: `(self, e: httpx.HTTPStatusError)`. Output annotation: `NoReturn`. Decorators: `none`.

Source intent: Handles HTTP errors for standard requests.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Raises `A2AClientError(f'HTTP Error: {e.response.status_code}')`, chained from `e`.

Explicit errors: `A2AClientError(f'HTTP Error: {e.response.status_code}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `A2AClientError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _handle_http_error(self, e: httpx.HTTPStatusError) -> NoReturn:
    raise A2AClientError(f'HTTP Error: {e.response.status_code}') from e
```

</details>

### `CompatJsonRpcTransport._send_stream_request`

Source lines 417–477; declaration kind `AsyncFunctionDef`.

Inputs: `(self, json_data: dict[str, Any], context: ClientCallContext | None=None)`. Output annotation: `AsyncGenerator[StreamResponse]`. Decorators: `none`.

Source intent: Sends an HTTP stream request.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `http_kwargs` from `get_http_args(context)`; output construction/calls here execute immediately when this method runs.
2. Executes `http_kwargs.setdefault('headers', {})`.
3. Assigns `http_kwargs['headers'][VERSION_HEADER.lower()]` from `PROTOCOL_VERSION_0_3`; output construction/calls here execute immediately when this method runs.
4. Executes `add_legacy_extension_header(http_kwargs['headers'])`.
5. Asynchronously iterates `send_http_stream_request(self.httpx_client, 'POST', self.url, self._handle_http_error, json=json_data, **http_kwargs)` into `sse_data`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=result))`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: `self._create_jsonrpc_error(data['error'])`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `get_http_args`, `http_kwargs.setdefault`, `add_legacy_extension_header`, `send_http_stream_request`, `VERSION_HEADER.lower`, `json.loads`, `data.get`, `result_dict.get`, `self._create_jsonrpc_error`, `isinstance`, `types_v03.Task.model_validate`, `conversions.to_core_stream_response`, `types_v03.Message.model_validate`, `types_v03.SendStreamingMessageSuccessResponse`, `types_v03.TaskStatusUpdateEvent.model_validate`, `types_v03.TaskArtifactUpdateEvent.model_validate`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _send_stream_request(self, json_data: dict[str, Any], context: ClientCallContext | None=None) -> AsyncGenerator[StreamResponse]:
    http_kwargs = get_http_args(context)
    http_kwargs.setdefault('headers', {})
    http_kwargs['headers'][VERSION_HEADER.lower()] = PROTOCOL_VERSION_0_3
    add_legacy_extension_header(http_kwargs['headers'])
    async for sse_data in send_http_stream_request(self.httpx_client, 'POST', self.url, self._handle_http_error, json=json_data, **http_kwargs):
        data = json.loads(sse_data)
        if 'error' in data:
            raise self._create_jsonrpc_error(data['error'])
        result_dict = data.get('result', {})
        if not isinstance(result_dict, dict):
            continue
        kind = result_dict.get('kind')
        if not kind:
            if 'taskId' in result_dict and 'final' in result_dict:
                kind = 'status-update'
            elif 'messageId' in result_dict:
                kind = 'message'
            elif 'id' in result_dict:
                kind = 'task'
        result: types_v03.Task | types_v03.Message | types_v03.TaskStatusUpdateEvent | types_v03.TaskArtifactUpdateEvent
        if kind == 'task':
            result = types_v03.Task.model_validate(result_dict)
        elif kind == 'message':
            result = types_v03.Message.model_validate(result_dict)
        elif kind == 'status-update':
            result = types_v03.TaskStatusUpdateEvent.model_validate(result_dict)
        elif kind == 'artifact-update':
            result = types_v03.TaskArtifactUpdateEvent.model_validate(result_dict)
        else:
            continue
        yield conversions.to_core_stream_response(types_v03.SendStreamingMessageSuccessResponse(result=result))
```

</details>

### `CompatJsonRpcTransport._send_request`

Source lines 479–498; declaration kind `AsyncFunctionDef`.

Inputs: `(self, json_data: dict[str, Any], context: ClientCallContext | None=None)`. Output annotation: `dict[str, Any]`. Decorators: `none`.

Source intent: Sends an HTTP request.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `http_kwargs` from `get_http_args(context)`; output construction/calls here execute immediately when this method runs.
2. Executes `http_kwargs.setdefault('headers', {})`.
3. Assigns `http_kwargs['headers'][VERSION_HEADER.lower()]` from `PROTOCOL_VERSION_0_3`; output construction/calls here execute immediately when this method runs.
4. Executes `add_legacy_extension_header(http_kwargs['headers'])`.
5. Assigns `request` from `self.httpx_client.build_request('POST', self.url, json=json_data, **http_kwargs)`; output construction/calls here execute immediately when this method runs.
6. Returns `await send_http_request(self.httpx_client, request, self._handle_http_error)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `get_http_args`, `http_kwargs.setdefault`, `add_legacy_extension_header`, `self.httpx_client.build_request`, `VERSION_HEADER.lower`, `send_http_request`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def _send_request(self, json_data: dict[str, Any], context: ClientCallContext | None=None) -> dict[str, Any]:
    http_kwargs = get_http_args(context)
    http_kwargs.setdefault('headers', {})
    http_kwargs['headers'][VERSION_HEADER.lower()] = PROTOCOL_VERSION_0_3
    add_legacy_extension_header(http_kwargs['headers'])
    request = self.httpx_client.build_request('POST', self.url, json=json_data, **http_kwargs)
    return await send_http_request(self.httpx_client, request, self._handle_http_error)
```

</details>
