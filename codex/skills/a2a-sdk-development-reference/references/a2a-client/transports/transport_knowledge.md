# `transports/`: contract, operations and tenant decoration

Source: a2a-sdk 1.1.4. Every file in this folder has a guide linked from [index](../index_knowledge.md).

## `__init__.py` and `base.py`

`__init__.py` re-exports `ClientTransport`, `JsonRpcTransport`, `RestTransport`, `GrpcTransport`. Guarded gRPC import assigns `GrpcTransport=None` on ImportError; the name remains in `__all__`.

`ClientTransport` is an abstract wire contract. `__aenter__` returns self; `__aexit__` awaits `close`. Ordinary `send_message` returns `SendMessageResponse`, unlike high-level Client's uniform async iterator. `send_message_streaming` and `subscribe` yield `StreamResponse`; their abstract bodies contain a yield solely to define generator shape. Abstract task, push-config, extended-card and close operations otherwise match [core's input/output table](../core_knowledge.md). No buffering, validation, retry or persistence is implemented by the abstract base.

## Current wire-operation map

All JSON-RPC operations POST to the selected interface URL. gRPC unary methods have these names under service `/lf.a2a.v1.A2AService/`; SendStreamingMessage and SubscribeToTask are unary-stream. REST paths below are optionally prefixed by `/{tenant}`.

| Python method | JSON-RPC / gRPC name | REST |
|---|---|---|
| `send_message` | `SendMessage` | POST `/message:send` |
| `send_message_streaming` | `SendStreamingMessage` | POST `/message:stream` |
| `get_task` | `GetTask` | GET `/tasks/{id}` |
| `list_tasks` | `ListTasks` | GET `/tasks` |
| `cancel_task` | `CancelTask` | POST `/tasks/{id}:cancel` |
| `create_task_push_notification_config` | `CreateTaskPushNotificationConfig` | POST `/tasks/{task_id}/pushNotificationConfigs` |
| `get_task_push_notification_config` | `GetTaskPushNotificationConfig` | GET `/tasks/{task_id}/pushNotificationConfigs/{id}` |
| `list_task_push_notification_configs` | `ListTaskPushNotificationConfigs` | GET `/tasks/{task_id}/pushNotificationConfigs` |
| `delete_task_push_notification_config` | `DeleteTaskPushNotificationConfig` | DELETE `/tasks/{task_id}/pushNotificationConfigs/{id}` |
| `subscribe` | `SubscribeToTask` | POST `/tasks/{id}:subscribe` |
| `get_extended_agent_card` | `GetExtendedAgentCard` | GET `/extendedAgentCard` |

These methods transmit requests and parse responses; they do not prove remote completion or durability. Push methods manage remote callback configuration; the client does not host a webhook receiver. Cancellation is an explicit remote request, not a guarantee of interruption.

## `tenant_decorator.py`

`TenantTransportDecorator.__init__(base,tenant)` retains wrapped transport and default. `_resolve_tenant(tenant)` returns nonempty explicit tenant or default; no policy validation occurs.

The following methods are mechanically identical mutation/delegation wrappers: `send_message`, `get_task`, `list_tasks`, `cancel_task`, `create_task_push_notification_config`, `get_task_push_notification_config`, `list_task_push_notification_configs`, `delete_task_push_notification_config`, `get_extended_agent_card`. Each assigns `request.tenant = _resolve_tenant(request.tenant)`, then awaits same-named base method with unchanged context and returns its result. Input/output types and wire effects differ as shown above and in core. Delete returns whatever wrapped method returns despite its `None` annotation.

`send_message_streaming` and `subscribe` assign tenant then async-iterate their matching base method, forwarding each event without aggregation. `close` simply awaits base `close`. Exceptions propagate; no after-call restoration of the original request tenant occurs.

BaseClient interceptors run before this decorator: a before hook can set/replace tenant and thereby override the default. An interface tenant is a routing convenience, not an enforced authorization boundary. Current JSON-RPC includes tenant in protobuf JSON; current REST uses it in URL paths and sometimes payload; current gRPC transmits the protobuf. Legacy transports do not preserve all modern fields, including tenant routing. See [dependencies](../dependencies_knowledge.md).
