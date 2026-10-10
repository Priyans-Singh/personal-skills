# v0_3/request_handler.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/request_handler.py`. SHA-256: `6064d5462465c2c3a4ab28a046b610e68c383074c9bdb11836f6cbf24bc3794e`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Protocol-agnostic execution boundary

`RequestHandler03` retains a current `RequestHandler`. It is the server bridge, not an AgentExecutor, task store, event queue or auth layer. Each method converts legacy request to core, invokes the corresponding underlying handler with the **same ServerCallContext**, then converts output. Every unary method awaits exactly one delegate call. Send selects Task versus Message by runtime core type. Get/cancel raise core TaskNotFoundError when the delegate returns falsy. Configuration methods preserve task/config identity through their dedicated conversions. Delete waits for the delegate and returns None; it performs no deletion independently.

Send-stream and resubscribe are async generators. For each delegated event, current `a2a.utils.proto_utils.to_stream_response` wraps a core Task/Message/status/artifact event, then compat conversion builds a legacy success envelope using request.id. No event buffering, deduplication, replay, completion-state stop, automatic reconnect, background tasks, or cancellation shielding occurs. Backpressure follows sequential iteration. Delegate and conversion exceptions propagate to whichever transport adapter called it.

List-push-config converts the core response to a legacy success envelope then returns its result list; unexpected non-success root gives []. Pagination fields are not preserved. Extended-card delegates identity enforcement to core; the wrapper does not check authenticated status. Request/stream lifetime is owned by adapter/framework and underlying handler. Storage ownership, callback delivery, task consistency, executor cancellation and authorization remain external execution boundaries.

## Integration shape (no network)

```python
from a2a.compat.v0_3.request_handler import RequestHandler03
# core_handler implements a2a.server.request_handlers.request_handler.RequestHandler
bridge = RequestHandler03(core_handler)
# await bridge.on_message_send(legacy_request, server_context)
```

Use the same core handler and context policy for current and legacy endpoints; compatibility should not accidentally create separate task stores or identities.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import logging
from collections.abc import AsyncIterable
from a2a.compat.v0_3 import conversions
from a2a.compat.v0_3 import types as types_v03
from a2a.server.context import ServerCallContext
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.types.a2a_pb2 import Task
from a2a.utils import proto_utils as core_proto_utils
from a2a.utils.errors import TaskNotFoundError
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
```

## Declaration-by-declaration execution reference

### `RequestHandler03`

Source lines 17–178; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): A protocol-agnostic v0.3 RequestHandler that delegates to the v1.0 RequestHandler.

Declared operations: `__init__`, `on_message_send`, `on_message_send_stream`, `on_cancel_task`, `on_subscribe_to_task`, `on_get_task_push_notification_config`, `on_create_task_push_notification_config`, `on_get_task`, `on_list_task_push_notification_configs`, `on_delete_task_push_notification_config`, `on_get_extended_agent_card`. Each method is traced below; constructor determines retained state.

### `RequestHandler03.__init__`

Source lines 20–21; declaration kind `FunctionDef`.

Inputs: `(self, request_handler: RequestHandler)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.request_handler` from `request_handler`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, request_handler: RequestHandler):
    self.request_handler = request_handler
```

</details>

### `RequestHandler03.on_message_send`

Source lines 23–35; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.SendMessageRequest, context: ServerCallContext)`. Output annotation: `types_v03.Task | types_v03.Message`. Decorators: `none`.

Source intent: Sends a message using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_send_message_request(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `task_or_message` from `await self.request_handler.on_message_send(v10_req, context)`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(task_or_message, Task)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `conversions.to_compat_message(task_or_message)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_send_message_request`, `isinstance`, `conversions.to_compat_message`, `self.request_handler.on_message_send`, `conversions.to_compat_task`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_message_send(self, request: types_v03.SendMessageRequest, context: ServerCallContext) -> types_v03.Task | types_v03.Message:
    v10_req = conversions.to_core_send_message_request(request)
    task_or_message = await self.request_handler.on_message_send(v10_req, context)
    if isinstance(task_or_message, Task):
        return conversions.to_compat_task(task_or_message)
    return conversions.to_compat_message(task_or_message)
```

</details>

### `RequestHandler03.on_message_send_stream`

Source lines 37–50; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.SendMessageRequest, context: ServerCallContext)`. Output annotation: `AsyncIterable[types_v03.SendStreamingMessageSuccessResponse]`. Decorators: `none`.

Source intent: Sends a message stream using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_send_message_request(request)`; output construction/calls here execute immediately when this method runs.
2. Asynchronously iterates `self.request_handler.on_message_send_stream(v10_req, context)` into `event`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `conversions.to_compat_stream_response(v10_stream_resp, request.id)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_send_message_request`, `self.request_handler.on_message_send_stream`, `core_proto_utils.to_stream_response`, `conversions.to_compat_stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_message_send_stream(self, request: types_v03.SendMessageRequest, context: ServerCallContext) -> AsyncIterable[types_v03.SendStreamingMessageSuccessResponse]:
    v10_req = conversions.to_core_send_message_request(request)
    async for event in self.request_handler.on_message_send_stream(v10_req, context):
        v10_stream_resp = core_proto_utils.to_stream_response(event)
        yield conversions.to_compat_stream_response(v10_stream_resp, request.id)
```

</details>

### `RequestHandler03.on_cancel_task`

Source lines 52–62; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.CancelTaskRequest, context: ServerCallContext)`. Output annotation: `types_v03.Task`. Decorators: `none`.

Source intent: Cancels a task using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_cancel_task_request(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `v10_task` from `await self.request_handler.on_cancel_task(v10_req, context)`; output construction/calls here execute immediately when this method runs.
3. Branches on `v10_task`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Raises `TaskNotFoundError`.

Explicit errors: `TaskNotFoundError`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_cancel_task_request`, `self.request_handler.on_cancel_task`, `conversions.to_compat_task`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_cancel_task(self, request: types_v03.CancelTaskRequest, context: ServerCallContext) -> types_v03.Task:
    v10_req = conversions.to_core_cancel_task_request(request)
    v10_task = await self.request_handler.on_cancel_task(v10_req, context)
    if v10_task:
        return conversions.to_compat_task(v10_task)
    raise TaskNotFoundError
```

</details>

### `RequestHandler03.on_subscribe_to_task`

Source lines 64–77; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.TaskResubscriptionRequest, context: ServerCallContext)`. Output annotation: `AsyncIterable[types_v03.SendStreamingMessageSuccessResponse]`. Decorators: `none`.

Source intent: Subscribes to a task using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_subscribe_to_task_request(request)`; output construction/calls here execute immediately when this method runs.
2. Asynchronously iterates `self.request_handler.on_subscribe_to_task(v10_req, context)` into `event`; each iteration performs the shown conversion/delegation, preserving iteration order.

Yielded output expressions: `conversions.to_compat_stream_response(v10_stream_resp, request.id)`. Generator work happens on iteration; nested closure yields are included.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_subscribe_to_task_request`, `self.request_handler.on_subscribe_to_task`, `core_proto_utils.to_stream_response`, `conversions.to_compat_stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_subscribe_to_task(self, request: types_v03.TaskResubscriptionRequest, context: ServerCallContext) -> AsyncIterable[types_v03.SendStreamingMessageSuccessResponse]:
    v10_req = conversions.to_core_subscribe_to_task_request(request)
    async for event in self.request_handler.on_subscribe_to_task(v10_req, context):
        v10_stream_resp = core_proto_utils.to_stream_response(event)
        yield conversions.to_compat_stream_response(v10_stream_resp, request.id)
```

</details>

### `RequestHandler03.on_get_task_push_notification_config`

Source lines 79–93; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.GetTaskPushNotificationConfigRequest, context: ServerCallContext)`. Output annotation: `types_v03.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Gets a push notification config using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_get_task_push_notification_config_request(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `v10_config` from `await self.request_handler.on_get_task_push_notification_config(v10_req, context)`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_compat_task_push_notification_config(v10_config)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_get_task_push_notification_config_request`, `conversions.to_compat_task_push_notification_config`, `self.request_handler.on_get_task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_get_task_push_notification_config(self, request: types_v03.GetTaskPushNotificationConfigRequest, context: ServerCallContext) -> types_v03.TaskPushNotificationConfig:
    v10_req = conversions.to_core_get_task_push_notification_config_request(request)
    v10_config = await self.request_handler.on_get_task_push_notification_config(v10_req, context)
    return conversions.to_compat_task_push_notification_config(v10_config)
```

</details>

### `RequestHandler03.on_create_task_push_notification_config`

Source lines 95–111; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.SetTaskPushNotificationConfigRequest, context: ServerCallContext)`. Output annotation: `types_v03.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Creates a push notification config using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_create_task_push_notification_config_request(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `v10_config` from `await self.request_handler.on_create_task_push_notification_config(v10_req, context)`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_compat_task_push_notification_config(v10_config)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_create_task_push_notification_config_request`, `conversions.to_compat_task_push_notification_config`, `self.request_handler.on_create_task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_create_task_push_notification_config(self, request: types_v03.SetTaskPushNotificationConfigRequest, context: ServerCallContext) -> types_v03.TaskPushNotificationConfig:
    v10_req = conversions.to_core_create_task_push_notification_config_request(request)
    v10_config = await self.request_handler.on_create_task_push_notification_config(v10_req, context)
    return conversions.to_compat_task_push_notification_config(v10_config)
```

</details>

### `RequestHandler03.on_get_task`

Source lines 113–123; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.GetTaskRequest, context: ServerCallContext)`. Output annotation: `types_v03.Task`. Decorators: `none`.

Source intent: Gets a task using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_get_task_request(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `v10_task` from `await self.request_handler.on_get_task(v10_req, context)`; output construction/calls here execute immediately when this method runs.
3. Branches on `v10_task`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Raises `TaskNotFoundError`.

Explicit errors: `TaskNotFoundError`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_get_task_request`, `self.request_handler.on_get_task`, `conversions.to_compat_task`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_get_task(self, request: types_v03.GetTaskRequest, context: ServerCallContext) -> types_v03.Task:
    v10_req = conversions.to_core_get_task_request(request)
    v10_task = await self.request_handler.on_get_task(v10_req, context)
    if v10_task:
        return conversions.to_compat_task(v10_task)
    raise TaskNotFoundError
```

</details>

### `RequestHandler03.on_list_task_push_notification_configs`

Source lines 125–151; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.ListTaskPushNotificationConfigRequest, context: ServerCallContext)`. Output annotation: `list[types_v03.TaskPushNotificationConfig]`. Decorators: `none`.

Source intent: Lists push notification configs using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_list_task_push_notification_config_request(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `v10_resp` from `await self.request_handler.on_list_task_push_notification_configs(v10_req, context)`; output construction/calls here execute immediately when this method runs.
3. Assigns `v03_resp` from `conversions.to_compat_list_task_push_notification_config_response(v10_resp, request.id)`; output construction/calls here execute immediately when this method runs.
4. Branches on `isinstance(v03_resp.root, types_v03.ListTaskPushNotificationConfigSuccessResponse)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Returns `[]`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_list_task_push_notification_config_request`, `conversions.to_compat_list_task_push_notification_config_response`, `isinstance`, `self.request_handler.on_list_task_push_notification_configs`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_list_task_push_notification_configs(self, request: types_v03.ListTaskPushNotificationConfigRequest, context: ServerCallContext) -> list[types_v03.TaskPushNotificationConfig]:
    v10_req = conversions.to_core_list_task_push_notification_config_request(request)
    v10_resp = await self.request_handler.on_list_task_push_notification_configs(v10_req, context)
    v03_resp = conversions.to_compat_list_task_push_notification_config_response(v10_resp, request.id)
    if isinstance(v03_resp.root, types_v03.ListTaskPushNotificationConfigSuccessResponse):
        return v03_resp.root.result
    return []
```

</details>

### `RequestHandler03.on_delete_task_push_notification_config`

Source lines 153–166; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.DeleteTaskPushNotificationConfigRequest, context: ServerCallContext)`. Output annotation: `None`. Decorators: `none`.

Source intent: Deletes a push notification config using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_delete_task_push_notification_config_request(request)`; output construction/calls here execute immediately when this method runs.
2. Executes `await self.request_handler.on_delete_task_push_notification_config(v10_req, context)`; awaits completion before continuing.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_delete_task_push_notification_config_request`, `self.request_handler.on_delete_task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_delete_task_push_notification_config(self, request: types_v03.DeleteTaskPushNotificationConfigRequest, context: ServerCallContext) -> None:
    v10_req = conversions.to_core_delete_task_push_notification_config_request(request)
    await self.request_handler.on_delete_task_push_notification_config(v10_req, context)
```

</details>

### `RequestHandler03.on_get_extended_agent_card`

Source lines 168–178; declaration kind `AsyncFunctionDef`.

Inputs: `(self, request: types_v03.GetAuthenticatedExtendedCardRequest, context: ServerCallContext)`. Output annotation: `types_v03.AgentCard`. Decorators: `none`.

Source intent: Gets the authenticated extended agent card using v0.3 protocol types.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `v10_req` from `conversions.to_core_get_extended_agent_card_request(request)`; output construction/calls here execute immediately when this method runs.
2. Assigns `v10_card` from `await self.request_handler.on_get_extended_agent_card(v10_req, context)`; output construction/calls here execute immediately when this method runs.
3. Returns `conversions.to_compat_agent_card(v10_card)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `conversions.to_core_get_extended_agent_card_request`, `conversions.to_compat_agent_card`, `self.request_handler.on_get_extended_agent_card`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
async def on_get_extended_agent_card(self, request: types_v03.GetAuthenticatedExtendedCardRequest, context: ServerCallContext) -> types_v03.AgentCard:
    v10_req = conversions.to_core_get_extended_agent_card_request(request)
    v10_card = await self.request_handler.on_get_extended_agent_card(v10_req, context)
    return conversions.to_compat_agent_card(v10_card)
```

</details>
