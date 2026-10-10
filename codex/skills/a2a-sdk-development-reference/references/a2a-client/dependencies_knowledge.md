# Direct implementation dependencies

Source: a2a-sdk 1.1.4. Paths here are relative to installed `a2a/`. These files participate directly in client execution; coverage outside `client/` is limited to those execution paths. This is not a second guide to the whole SDK.

## Current protocol models and integrations

`types/a2a_pb2.py` contains generated protobuf descriptors and dynamically built message classes. Client inputs/outputs are these classes, not the older Pydantic v0.3 models. Presence uses `HasField` for singular message/optional/oneof fields; repeated fields/maps use truthiness (HasField would raise). `CopyFrom` copies same-type protobuf values; it does not perform arbitrary type conversion.

| Model | Relevant fields |
|---|---|
| `AgentCard` | Name/version, supported interfaces, capabilities, skills, security requirements/schemes, signatures |
| `AgentInterface` | URL, binding, protocol version, tenant |
| `Message` | Message ID, context ID, task ID, role, parts, metadata, extensions, reference task IDs |
| `Task` | ID, context ID, status, artifacts, history, metadata |
| `SendMessageRequest` | Tenant, message, configuration, metadata |
| `SendMessageConfiguration` | Accepted modes, task push configuration, optional history length, return immediately |
| `SendMessageResponse` | Task or message payload |
| `StreamResponse` | Task, message, status update or artifact update |
| `TaskPushNotificationConfig` | Tenant, task ID, config ID, callback URL, token, callback authentication |
| `ListTasksRequest` | Tenant/context/status, page size/token, history length, timestamp filter, include artifacts |

Push callback token/authentication are destination-specific configuration delivered to the remote agent in protobuf request fields; they are separate from credentials used to authenticate this client request. Local client does not expire/store them independently or validate callback addresses.

Google protobuf `MessageToDict` uses JSON names such as `taskId`, `supportedInterfaces`, `returnImmediately` and omits unset/default fields according to protobuf JSON rules. Bytes/timestamps/enums use protobuf JSON representation. `ParseDict` and `Parse` reconstruct protobuf values; current transports generally reject unknown fields, while discovery and legacy REST explicitly tolerate them. Metadata uses protobuf Struct/Value, which has its own numeric representation constraints.

`types/a2a_pb2_grpc.py`: `A2AServiceStub.__init__` binds channel unary-unary/unary-stream callables to `/lf.a2a.v1.A2AService/<method>`, request SerializeToString and response FromString. Delete response is Google Empty. Stub has no retry/polling/validation logic of its own in this generated constructor. Server servicer and server registration helpers are unrelated to client dispatch and excluded.

External integrations: HTTPX handles connection pooling, default headers and timeout enforcement; `jsonrpc.jsonrpc2` builds/parses JSON-RPC envelopes; Google protobuf handles serialization; grpc.aio handles channel/stub calls; packaging.Version performs version comparison; Pydantic validates call context and legacy values; optional OpenTelemetry decorates operations. No FastAPI/framework server adapter exists under this client package.

## Constants, errors, extension parameters

`utils/constants.py`: `TransportProtocol` labels JSONRPC, HTTP+JSON, GRPC; discovery path `/.well-known/agent-card.json`; header `A2A-Version`; current version `1.0`; legacy lower bound `0.3`. Page-size constants exist but these client methods do not enforce a local page-size policy.

`utils/errors.py`: `A2AError.__init__(message=None,data=None)` preserves class default message unless supplied message is truthy, retains data and initializes Exception. Subclasses supply domain messages. `JSON_RPC_ERROR_CODE_MAP` drives JSON-RPC mapping; `A2A_REASON_TO_ERROR` reverses REST/gRPC reason mapping.

| Error class | JSON-RPC code | REST/gRPC reason |
|---|---|---|
| TaskNotFoundError | -32001 | TASK_NOT_FOUND |
| TaskNotCancelableError | -32002 | TASK_NOT_CANCELABLE |
| PushNotificationNotSupportedError | -32003 | PUSH_NOTIFICATION_NOT_SUPPORTED |
| UnsupportedOperationError | -32004 | UNSUPPORTED_OPERATION |
| ContentTypeNotSupportedError | -32005 | CONTENT_TYPE_NOT_SUPPORTED |
| InvalidAgentResponseError | -32006 | INVALID_AGENT_RESPONSE |
| ExtendedAgentCardNotConfiguredError | -32007 | EXTENDED_AGENT_CARD_NOT_CONFIGURED |
| ExtensionSupportRequiredError | -32008 | EXTENSION_SUPPORT_REQUIRED |
| VersionNotSupportedError | -32009 | VERSION_NOT_SUPPORTED |
| InvalidParamsError | -32602 | INVALID_PARAMS |
| InvalidRequestError | -32600 | INVALID_REQUEST |
| MethodNotFoundError | -32601 | METHOD_NOT_FOUND |
| InternalError | -32603 | INTERNAL_ERROR |
| JSONParseError | -32700 | No corresponding entry in reason map |

`extensions/common.py.get_requested_extensions(values)` splits each string on commas, strips whitespace, returns nonempty entries as a set. It is the direct helper used by service-parameter extension merging. Other extension discovery APIs are outside this path.

`utils/grpc_status.py.status_from_call(call)` returns None if trailing metadata API/value/details entry absent; parses `grpc-status-details-bin` into Google Status, verifies code and message match original call, returns status. Mismatch ValueErrors and binary parse errors propagate. This is called only by current gRPC error mapping.

`utils/proto_utils.py.bad_request_to_validation_errors` maps each BadRequest violation into `ValidationDetail(field,message)` from field/description. It does not validate outgoing client messages. Server-oriented required-field validation helpers in that module are not invoked by BaseClient/transports.

## Optional tracing

`utils/telemetry.py` imports OpenTelemetry if present and checks `OTEL_INSTRUMENTATION_A2A_SDK_ENABLED` (default `true`, case-insensitive exact true). Without dependency/enabling, `_NoOp` supplies call/context/attribute behavior; `_NoOp.__call__`, `__enter__`, `__getattr__` return self and `__exit__` does nothing.

`trace_class` returns nested `decorator(cls)` which enumerates Python functions, skips dunder names, applies optional include/exclude rules, wraps methods using `trace_function`, and mutates class attributes. Client transports use CLIENT span kind and default inclusion. Private helper calls can create their own spans.

`trace_function` supports direct or configured decoration via partial, selects `async_wrapper` only for coroutine functions, otherwise `sync_wrapper`. Wrappers open span, set static attributes, call original, mark success, record exceptions and re-raise. Async cancellation/QueueShutDown are recorded without treating them as ordinary errors. Optional attribute-extractor errors are logged and swallowed in finally. The transport decorators do not pass extractors themselves. Synchronous wrapper does not await returned objects.

Async generators are not coroutine functions: tracing their creation via the synchronous wrapper does **not** mean a span encloses all subsequent stream iteration. Installed source supports this distinction; full stream telemetry depends on integration beyond these wrappers. No exporter/backend is configured by the client.

## v0.3 compatibility transports selected by the factory

`compat/v0_3/versions.py.is_legacy_version(version)` returns true only for parseable >=0.3,<1.0; missing/invalid strings return false. The compatibility transports still implement the current `ClientTransport` interface and return current protobufs. They adapt older wire formats, not arbitrary older protocol versions.

### `jsonrpc_transport.py`

`CompatJsonRpcTransport.__init__` retains HTTPX/card/URL. Operation names change as follows:

| Current Python operation | Legacy JSON-RPC method |
|---|---|
| send / streaming | message/send / message/stream |
| get / cancel task | tasks/get / tasks/cancel |
| create / get / list / delete push config | tasks/pushNotificationConfig/set / get / list / delete (same prefix) |
| subscribe | tasks/resubscribe |
| extended card | agent/getAuthenticatedExtendedCard |

Requests use `conversions.to_compat_*` to construct Pydantic params, dump by alias excluding None, then create UUID JSON-RPC envelopes. Send recognizes `kind` or infers message/task from messageId/id; unrecognized or non-dictionary result returns empty SendMessageResponse, which BaseClient rejects. Get/cancel parse legacy Task then convert. Push create/get parse legacy config; list requires list result, otherwise returns empty collection; delete inserts result None if both result and error are absent. `list_tasks` raises NotImplementedError.

`_send_request` and `_send_stream_request` override A2A-Version to `0.3` and add legacy extension header. Streaming recognizes task/message/status-update/artifact-update; some missing kinds are inferred; non-dictionary/unrecognized events are silently skipped. `_create_jsonrpc_error` maps recognized integer codes without preserving data, otherwise generic error. `_handle_http_error` creates generic status error. `close` closes HTTPX.

Extended-card retrieval returns stored card if unsupported; otherwise parses/converts legacy AgentCard, **updates transport card before returning**, then BaseClient's verifier runs. A verifier rejection therefore leaves BaseClient unchanged but can leave the compatibility transport holding the fetched card.

### `rest_transport.py`

`CompatRestTransport.__init__` retains HTTPX/card/normalized URL and subscription-method override/auto-fallback flags. Send/stream convert current request to legacy Pydantic then legacy protobuf; paths are `/v1/message:send` and `/v1/message:stream`; JSON preserves protobuf field names. Results ignore unknown fields, convert legacy proto -> legacy values -> current proto. Get path `/v1/tasks/{id}` forwards optional historyLength; cancel POSTs `/v1/tasks/{id}:cancel`. Push create/get use `/v1/tasks/{task_id}/pushNotificationConfigs[/{id}]`. ListTasks, list push configs and delete push configs raise NotImplementedError.

`subscribe` starts POST unless overridden. If generic A2AClientError has HTTPStatusError cause 405 and there is no existing override, sets GET and recursively tries once; success remembers GET. If GET also fails 405, automatic fallback resets future preference to POST, disables further auto-switch and re-raises. Explicit overrides do not auto-switch. Other failures propagate. This narrow method fallback is the exception to absence of retry behavior; it is not a message retry/backoff layer.

Extended card GETs `/v1/card`, parses/converts and updates transport card. `_execute_request` and `_send_stream_request` set version 0.3 and legacy extensions; `_send_request` uses shared HTTP helper. `_handle_http_error` maps legacy `type` class names, then 404/fallback; it attempts to read the response, suppresses StreamClosed, and swallows selected decode/ValueErrors. Stream responses use legacy protobuf and `FromProto.stream_response` conversion. `close` closes HTTPX. Tenant-prefixed current routing is not implemented by this transport.

### `grpc_transport.py`

`CompatGrpcTransport.__init__` builds legacy stub; `create` requires caller channel factory. Send/stream convert through legacy values/protobuf; get/cancel build resource names `tasks/{id}`; push get/delete use `tasks/{task_id}/pushNotificationConfigs/{id}`; push create uses parent `tasks/{task_id}`. Subscribe calls legacy `TaskSubscription`, not current SubscribeToTask. Extended card calls GetAgentCard and updates transport state without a capability short circuit. ListTasks raises NotImplementedError. Stream loops read to EOF and convert legacy events. `close` closes channel.

`_get_grpc_metadata` lower-cases parameters, sends 0.3 header and mirrors extension header. **Legacy calls do not forward `context.timeout` to stub methods**, unlike current gRPC. `_handle_grpc_exception` and `_handle_grpc_stream_exception` return wrapping ordinary/stream callables catching AioRpcError. `_map_grpc_error` maps deadline first, then parses error details string `ExceptionClass: message`, then generic fallback; it does not use current Google ErrorInfo/BadRequest mapping.

### Conversion and generated support chain

`compat/v0_3/extension_headers.py.add_legacy_extension_header(parameters)` mutates mapping to mirror exact `A2A-Extensions` key as `X-A2A-Extensions` only if legacy key absent. Current value remains. Case-sensitive dictionary lookup means alternate key capitalization is not mirrored by this helper.

`compat/v0_3/conversions.py` is used directly by every compatibility transport. `to_compat_send_message_request` converts message/config/metadata into legacy envelope; config maps `return_immediately` to inverse `blocking`. Get/cancel/subscribe conversion inserts task ID; push get/delete distinguish task ID versus push config ID; push create flattens current config into legacy task/config hierarchy; list returns current `configs` collection. Modern tenant is not represented in those converted requests.

`to_compat_message`/`to_core_message` copy identifiers, roles, parts, metadata, extensions and reference task IDs. Part helpers preserve text, URL or base64 raw file content, media type/name; scalar/list data uses a metadata `data_part_compat` marker because legacy DataPart expects an object. Unknown outgoing part content raises ValueError. Task helpers recursively convert status/history/artifacts and metadata; state mapping falls back to unspecified/unknown; timestamps use protobuf JSON conversion. Stream conversion maps legacy message/task/status/artifact event to current StreamResponse oneof. Push conversion copies URL/token/authentication and associates task ID; it does not acquire credentials or send callbacks.

`to_core_agent_card` constructs primary interface from legacy URL/preferred transport/version, extends additional interfaces, and recursively converts capabilities, schemes/requirements, provider, skills, signatures and modes. This is model conversion, not signature verification. Additional-interface conversion has no separate legacy version field to preserve.

REST/gRPC additionally use `compat/v0_3/proto_utils.py` `ToProto` and `FromProto` classmethod conversions for message/config/metadata/task/push/card/stream values. Those recursively adapt legacy Pydantic models and legacy protobuf oneofs, timestamps and JSON metadata. `ToProto.message` converts parts into legacy `content`, role into enum, optional IDs to empty strings, metadata through `dict_to_struct`; it does not preserve reference task IDs. `dict_to_struct` recursively inserts dictionary values into Google Struct, without automatically calling the module's separate generic normalization helpers. `FromProto.metadata` returns `{}` for empty fields or MessageToDict otherwise. `FromProto.stream_response` chooses msg/task/status/artifact presence and raises ValueError for an unsupported/empty payload. `FromProto.task_push_notification_config` extracts task ID from regex-matched resource name and raises InvalidParamsError when absent; malformed remote names can therefore fail during response adaptation. These helpers do not perform client authentication or persistence.

`compat/v0_3/types.py` supplies the Pydantic schemas and discriminators, and imports SDK `_base.py` for alias-aware base behavior. `_base.to_camel_custom` removes trailing underscores then uses Pydantic's camel-case conversion. `A2ABaseModel.model_config` enables validation by Python name or alias, serialization by alias, and that alias generator. Its docstring mentions lazy alias attribute warnings, but this installed implementation defines no attribute-access override or warning machinery. `a2a_v0_3_pb2.py`/`a2a_v0_3_pb2_grpc.py` supply generated legacy models/stub serialization. These are included as the direct support chain; unrelated compatibility server adapters and reverse conversions unused by client calls are outside this guide's callable index.

Conversions can be lossy for fields absent in older models. Local source cannot promise full current-protocol behavior through a legacy interface. A type-compatible Client object can still raise NotImplementedError for unsupported legacy operations.
