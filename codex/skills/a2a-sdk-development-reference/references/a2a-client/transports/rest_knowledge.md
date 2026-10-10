# `rest.py`: current HTTP+JSON transport

Source: a2a-sdk 1.1.4. `RestTransport` is CLIENT trace-decorated. `__init__` retains HTTPX/card and removes one trailing slash from URL. `_get_path(base_path,tenant)` prefixes `/{tenant}` when tenant is nonempty. IDs and tenant are interpolated; no explicit component quoting/validation is performed here beyond HTTPX URL processing.

## Operation encoding

All inputs/results are current protobuf values. `MessageToDict` uses protobuf JSON names; `ParseDict`/`Parse` parse responses without opting into unknown-field tolerance.

| Method | Request behavior | Parsed output |
|---|---|---|
| `send_message` | POST send path; full request JSON, including tenant when present | `SendMessageResponse` |
| `send_message_streaming` | POST stream path; full request JSON | Each `StreamResponse` |
| `get_task` | GET task path; removes `id`, `tenant` from converted query params | `Task` |
| `list_tasks` | GET tasks; removes `tenant`; other request fields become query params | `ListTasksResponse` |
| `cancel_task` | POST cancel path; full request JSON | `Task` |
| `create_task_push_notification_config` | POST task push collection; full config JSON | `TaskPushNotificationConfig` |
| `get_task_push_notification_config` | GET push item; strips `id`, `taskId`, `tenant` from query | `TaskPushNotificationConfig` |
| `list_task_push_notification_configs` | GET push collection; strips `taskId`, `tenant` from query | `ListTaskPushNotificationConfigsResponse` |
| `delete_task_push_notification_config` | DELETE push item; strips `id`, `taskId`, `tenant` from query; awaits helper but discards parsed data | `None` |
| `subscribe` | POST subscribe path; no request body fields forwarded by this method | Each `StreamResponse` |
| `get_extended_agent_card` | Stored card if capability false; otherwise GET `/extendedAgentCard` | `AgentCard` |

Exact URL paths are in [wire map](transport_knowledge.md). Query/body dictionaries are new serialized objects, so removing keys does not mutate source protobuf. Tenant decoration and BaseClient defaulting can still mutate the protobuf earlier.

`subscribe` forwards request ID and tenant through the path; other fields such as request metadata are not serialized by this implementation. The extended-card fetch does not update transport's `agent_card`; BaseClient updates its separate reference after verification. No pagination accumulation or capability check for push APIs is done locally.

## HTTP helpers

`_execute_request(method,target,tenant,context,json=None,params=None)` builds URL with `_get_path`, obtains copied context headers/timeout, builds HTTPX request and awaits `_send_request`. `_send_request` calls shared `send_http_request` with `_handle_http_error`.

`_send_stream_request(method,target,tenant,context,json=None)` builds the same URL/context, calls shared SSE helper with both `_handle_http_error` and `_handle_sse_error`, and uses `Parse(raw_string,StreamResponse())` for each data event.

The ordinary helper always invokes `response.json`, including for DELETE. A successful empty-body/204 delete can therefore raise a JSON decoding client error after the remote deletion has happened. No rollback is performed. Callers should distinguish transport/parse outcome from remote mutation outcome.

## Error helpers

`_parse_rest_error(error_payload,fallback_message)` reads `error.message` and `error.details`. Non-list details return None. Finds first Google `ErrorInfo`; a known string `reason` maps through `A2A_REASON_TO_ERROR`, creates that exception, and attaches nonempty metadata as `.data`. It stops at the first ErrorInfo even if unrecognized. ErrorInfo domain is not checked here. Invalid container shapes can propagate Python errors.

`_handle_http_error(status_error)` attempts to JSON-decode response and raise a mapped error, chaining status cause. JSONDecodeError/ValueError are swallowed for fallback. Unmapped 404 becomes `MethodNotFoundError` with resource URL, regardless of whether the missing resource was actually a task. Other statuses become generic `A2AClientError`. Errors mapped by reason win before the 404 fallback.

`_handle_sse_error(sse_data)` runs `json.loads`, maps with `_parse_rest_error`, raises mapped or generic `A2AClientError`. Shared stream exception context translates JSONDecodeError; other structure/protobuf errors may propagate.

`close` closes HTTPX client. No request retries, POST/GET fallback, local credential refresh or durable subscriptions exist in this current transport; the fallback belongs to legacy REST only.
