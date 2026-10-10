# `jsonrpc.py`: current JSON-RPC transport

Source: a2a-sdk 1.1.4. Current protocol methods use PascalCase names; legacy slash names are a separate compatibility implementation.

`JsonRpcTransport` has `trace_class(kind=SpanKind.CLIENT)` decoration. `__init__(httpx_client,agent_card,url)` retains those values unchanged. URL normalization is not done here. [Dependencies](../dependencies_knowledge.md) explains tracing limitations and serialization boundaries.

## Unary operation family

`send_message`, `get_task`, `list_tasks`, `cancel_task`, `create_task_push_notification_config`, `get_task_push_notification_config`, and `list_task_push_notification_configs` all:

1. Convert protobuf input with `json_format.MessageToDict`.
2. Create `JSONRPC20Request` with the exact operation name in [wire map](transport_knowledge.md), fresh `str(uuid4())` request ID, and converted params.
3. Await `_send_request(dict(rpc_request.data),context)`.
4. Construct `JSONRPC20Response(**response_data)`; error truthiness raises `_create_jsonrpc_error`.
5. Parse result with `ParseDict` into `SendMessageResponse`, `Task`, `ListTasksResponse`, `Task`, `TaskPushNotificationConfig`, `TaskPushNotificationConfig`, or `ListTaskPushNotificationConfigsResponse`, respectively.

Current result parsing does not set `ignore_unknown_fields=True`. There is no custom response-ID correlation check in this transport; any JSON-RPC library checks are outside this implementation. Fresh request IDs are correlation values, not an SDK retry/deduplication mechanism.

`delete_task_push_notification_config` builds/sends/parses the envelope identically and checks errors, but does not parse a result protobuf and returns `None`.

## Stream and card paths

`send_message_streaming` builds method `SendStreamingMessage`; `subscribe` builds `SubscribeToTask`. Both protobuf-convert params, allocate UUID, then forward events from `_send_stream_request`.

`_send_stream_request(payload,context)` uses copied HTTP args, POSTs to `self.url` through `send_http_stream_request`, and supplies `_handle_sse_error`. Each yielded string is parsed by `JSONRPC20Response.from_json`; envelope errors are mapped, otherwise result becomes `StreamResponse` via `ParseDict`. A non-SSE response is still processed through this envelope path. No events are accumulated into a task snapshot.

`get_extended_agent_card` returns the stored original card without I/O if its extended-card capability is false. Otherwise sends `GetExtendedAgentCard`, checks envelope errors, requires result to be a dictionary (else `A2AClientError`), parses `AgentCard`, and returns it. It does not update `self.agent_card`. BaseClient separately verifies and updates its own retained card.

## Helpers, errors and closure

`_send_request(payload,context)` builds HTTP POST JSON with `get_http_args`, then uses `send_http_request`. No special HTTP-status domain mapper is supplied: status failures are generic client errors, even if body contains domain information.

`_create_jsonrpc_error(error_dict)` reads code/message/raw data. If data is a list, finds first dictionary with `@type=type.googleapis.com/google.rpc.ErrorInfo`, takes `metadata` or None, and uses that as mapped exception data. Known integer code maps through reversed `JSON_RPC_ERROR_CODE_MAP`; **the code selects the exception**, not ErrorInfo reason. Unknown codes return generic `A2AClientError('JSON-RPC Error ...')`. Non-list raw data is not preserved as mapped data.

`_handle_sse_error(sse_data)` parses JSON-RPC envelope, raises mapped error if present, otherwise raises generic SSE error. Malformed envelope exceptions may propagate; no error swallowing or retries.

`close` awaits retained HTTPX client's `aclose`, including an injected/shared client. Current transport owns no independent card cache refresh, request queue or durable state. Remote methods and protobuf parse failures surface through the boundaries above.
