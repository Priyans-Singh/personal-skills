# Core client and root import surface

Source: `a2a/client/{__init__,client,base_client}.py`, a2a-sdk 1.1.4. See [index](index_knowledge.md) for snapshot and scope.

## `__init__.py`: public imports

Re-exports `A2ACardResolver`, `A2AClientError`, `A2AClientTimeoutError`, `AgentCardResolutionError`, `AuthInterceptor`, `BaseClient`, `Client`, `ClientCallContext`, `ClientCallInterceptor`, `ClientConfig`, `ClientFactory`, `CredentialService`, `InMemoryContextCredentialStore`, `create_client`, and `minimal_agent_card`. No functions/classes are declared here. Importing this package loads its factory/auth/core dependencies; optional gRPC imports are guarded.

`BeforeArgs`/`AfterArgs` are imported from `a2a.client.interceptors`; service-parameter helpers from `a2a.client.service_parameters`; transport classes from `a2a.client.transports`; wire models from `a2a.types.a2a_pb2`. These are not all root re-exports.

## Resource and identity hierarchy

| Object/identifier | Lifetime and meaning |
|---|---|
| Agent Card | Local protobuf describing remote interfaces/capabilities/security; held by BaseClient and transport |
| Factory | Registry, configuration and shared HTTPX resource; can create several clients |
| Client | One selected transport with card/config/interceptor state |
| Tenant | Request routing identifier; interface default applies only to empty request tenant |
| Message | Typed request content; may start or continue remote work through task/context identifiers |
| Task ID | Remote work identifier used by get/cancel/subscribe and push-config operations |
| Context ID | Conversation/work grouping carried in protocol values; distinct from credential-store `sessionId` |
| Push configuration ID | Remote callback configuration subordinate to a task |
| Call context | Local mutable state, timeout and transport headers/metadata; `state` is not automatically serialized |

The client retains configuration/card/transport references, not independent snapshots. It has no task store, response cache or locks around shared state.

## `client.py`: contracts and configuration

`ClientConfig` is a dataclass, not a validating Pydantic model:

| Field | Default | Runtime effect |
|---|---|---|
| `streaming` | `True` | Enables streaming when card also supports it |
| `polling` | `False` | ORs into send configuration's `return_immediately`; caller polls |
| `httpx_client` | `None` | Factory creates AsyncClient if absent; otherwise uses injected resource |
| `grpc_channel_factory` | `None` | Required to construct a gRPC transport |
| `supported_protocol_bindings` | Empty list | Empty implies JSONRPC; explicit list enables matching registered bindings |
| `use_client_preference` | `False` | Default favors card binding order; true favors configured binding order |
| `accepted_output_modes` | Empty list | Fills empty send-request modes |
| `push_notification_config` | `None` | Copies into send request only if request config lacks it |

`ClientCallContext` is a Pydantic model with independent default `state` mapping, optional float `timeout`, and optional `dict[str,str]` `service_parameters`. State can pass values between hooks; timeout becomes HTTPX timeout or current gRPC deadline; service parameters become HTTP headers or lower-cased gRPC metadata.

`Client` is abstract. `__init__` retains a provided nonempty interceptor list or creates an empty one. `add_interceptor` asynchronously appends without I/O. `__aenter__` returns self; `__aexit__` awaits `close`, including when the body raises. It does not suppress the exception; a close failure may itself propagate.

The abstract operations define these inputs/outputs; every operation accepts optional keyword `context`:

| Method | Protobuf input | Output |
|---|---|---|
| `send_message` | `SendMessageRequest` | Async iterator of `StreamResponse` |
| `get_task` | `GetTaskRequest` | `Task` |
| `list_tasks` | `ListTasksRequest` | `ListTasksResponse` (caller handles pagination) |
| `cancel_task` | `CancelTaskRequest` | `Task` |
| `create_task_push_notification_config` | `TaskPushNotificationConfig` | `TaskPushNotificationConfig` |
| `get_task_push_notification_config` | `GetTaskPushNotificationConfigRequest` | `TaskPushNotificationConfig` |
| `list_task_push_notification_configs` | `ListTaskPushNotificationConfigsRequest` | `ListTaskPushNotificationConfigsResponse` |
| `delete_task_push_notification_config` | `DeleteTaskPushNotificationConfigRequest` | Contract: `None` |
| `subscribe` | `SubscribeToTaskRequest` | Async iterator of `StreamResponse` |
| `get_extended_agent_card` | `GetExtendedAgentCardRequest` | `AgentCard` |
| `close` | None | `None`; releases transport |

## `base_client.py`: implementation

`BaseClient.__init__` stores card, config, transport and interceptor list. It resets `_interceptors` to the supplied list after the superclass initialization.

### Send execution

1. Iterating `send_message(request)` runs `_apply_client_config`; constructing the async generator alone sends nothing.
2. `_apply_client_config` mutates the protobuf in place: ORs polling into `return_immediately`, copies default push config only when absent, and extends output modes only when empty. It cannot turn an already-true request flag off.
3. If config or card disallows streaming, `_execute_with_interceptors` invokes transport `send_message`; hooks see method `send_message` and its `SendMessageResponse`.
4. The resulting response must contain `task` or `message`. That field is copied into a new `StreamResponse`, yielded once. Neither field raises `ValueError('Response has neither task nor message')`. There is no repeated polling or aggregation.
5. Otherwise `_execute_stream_with_interceptors` invokes transport `send_message_streaming`; hooks see method `send_message_streaming` and each `StreamResponse`.
6. `_process_stream` runs reverse after hooks for each event, yields the modified result, then stops if that result has `message`. It does not inspect terminal task status to implement a separate stopping rule.

### Ordinary operation delegates

`get_task`, `list_tasks`, `cancel_task`, `create_task_push_notification_config`, `get_task_push_notification_config`, `list_task_push_notification_configs`, and `delete_task_push_notification_config` pass their protobuf to the same-named transport method through `_execute_with_interceptors`. Each supplies its own method string and preserves the result after hooks. They do not locally validate resource existence, permissions, pagination tokens or callback URL safety. The input/output table above distinguishes their contracts and remote effects.

### Subscription and extended card

`subscribe` first requires both streaming flags; otherwise raises `NotImplementedError`. It delegates through `_execute_stream_with_interceptors` with method `subscribe`. A subscription request does not provide a built-in reconnect loop.

`get_extended_agent_card` uses ordinary interception, then invokes optional synchronous `signature_verifier(card)`, then assigns `_card`. Failure before assignment leaves BaseClient's retained card unchanged. It does not renegotiate/rebuild the transport when the new card advertises other interfaces. Current transports retain their original card; legacy transports can update their own card before this verifier runs. See [dependencies](dependencies_knowledge.md).

`close` awaits transport `close`; no local closed flag or ownership/ref-count check is maintained.

### Interceptor machinery

`_execute_with_interceptors` creates `BeforeArgs`, awaits `_intercept_before`, and either uses its early result or calls the transport with the possibly replaced input/context. It creates `AfterArgs`, runs `_intercept_after`, returns the potentially replaced result. Transport exceptions bypass after hooks; these are result hooks, not finally hooks.

`_execute_stream_with_interceptors` follows the same before stage. A before early result gets reverse after hooks for only the executed hooks, then is yielded once and returns. Otherwise it obtains the transport iterator and passes it to `_process_stream`.

`_intercept_before` calls hooks in list order, records each successfully executed hook, and checks **truthiness** of `args.early_return`. A falsy value such as `0`, `False` or an empty container cannot trigger the short circuit. On a truthy value it returns a dictionary containing the value and executed hook list.

`_intercept_after` reverses the supplied executed list or all interceptors. A truthy `AfterArgs.early_return` stops subsequent after hooks only. It does not itself stop the event stream, cancel the task or undo side effects.

### Concurrency and failures

Hook/verifier errors propagate. Result replacements must satisfy the next consumer's assumptions (`HasField`, protobuf fields, expected return shape); the framework does not enforce hook result types. Concurrent card replacement or interceptor-list mutation has no synchronization. Copy request/context objects before concurrent reuse. Closing one shared HTTP-backed client can interrupt other clients using the same resource. No client-level retry or transaction guarantee exists.
