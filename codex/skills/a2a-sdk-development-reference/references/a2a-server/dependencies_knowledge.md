# Direct supporting dependencies

This chapter follows server implementation dependencies outside `a2a/server`. It documents their server-facing behavior; unrelated client, authentication clients, signing utilities, and migration administration are not duplicated. Every server source is inventoried separately; these supporting modules are included because the server actually calls their models/helpers/adapters. All observations refer to installed a2a-sdk 1.1.4.

## Protocol models: `a2a/types/__init__.py`, `a2a_pb2.py`, `a2a_pb2_grpc.py`

Current protocol values are **generated protobuf messages**, not the legacy Pydantic API. `types/__init__.py` re-exports generated models and selected domain exceptions. Its A2ARequest union is a convenience alias, not the full dispatcher operation set (for example ListTasksRequest is exported but not in that union).

| Model | Fields relevant to server execution |
|---|---|
| Message | message_id, task_id, context_id, role, parts, metadata, extensions, reference_task_ids |
| Part | content oneof: text/data/raw/url; media_type, filename, metadata |
| Task | id, context_id, status, artifacts, history, metadata |
| TaskStatus | state, timestamp, optional message |
| TaskStatusUpdateEvent | task_id, context_id, status, metadata |
| TaskArtifactUpdateEvent | task_id, context_id, artifact, append, last_chunk, metadata |
| SendMessageRequest | message, configuration, metadata, tenant where declared by protocol |
| SendMessageConfiguration | accepted_output_modes, task_push_notification_config, optional history_length, return_immediately |
| SendMessageResponse | Task or Message payload |
| StreamResponse | Task, Message, status_update, artifact_update oneof |
| TaskPushNotificationConfig | tenant, id, task_id, url, token, authentication |
| AgentCard | supported_interfaces, capabilities, skills, input/output modes, security declarations and descriptive fields |
| AgentInterface | URL, protocol_binding, protocol_version, tenant |

Use `HasField` for presence-aware fields; absent scalar values and absent optional fields are not interchangeable. Python names are snake_case; MessageToDict normally outputs camelCase, enum names as strings, timestamps as RFC3339, bytes as base64, and omits default fields. CopyFrom/MergeFrom/repeated-container behavior differs from replacing Python dicts. Struct metadata is JSON-shaped, not arbitrary Python objects. These distinctions explain history trimming, required validation, persistence, and OpenAPI differences.

Generated gRPC code declares service methods, client stub wiring, default unimplemented servicer methods, registration helper `add_A2AServiceServicer_to_server`, and experimental static service calls. Server GrpcHandler subclasses the generated servicer and supplies actual implementations; generated registration does not start a server, add credentials, or manage lifespan. grpcio must be installed. Generated descriptors establish model fields and REQUIRED annotations; runtime validation remains in SDK helpers.

## Identity and extension helpers

`a2a/auth/user.py`: User's abstract is_authenticated/user_name contract; UnauthenticatedUser returns False/empty string. No credential validation or claims parsing. Server builders choose identity.

`a2a/extensions/common.py`: get_requested_extensions(values) splits all header strings by comma, strips whitespace, drops blanks, returns unique set. HTTP_EXTENSION_HEADER='A2A-Extensions'. find_extension_by_uri(card, uri) scans declarations and returns matching extension/None. Collection does not enforce extension support or a required extension.

## `a2a/helpers/proto_helpers.py`

The server directly uses get_message_text, which joins only get_text_parts results. Helpers in the usage example are also inspected:

- new_message creates Message with UUID message_id, parts, role (agent default), optional task/context IDs.
- new_text/data/raw/url_message wrap corresponding typed Part factories. Data uses protobuf Value/ParseDict; bytes remain bytes until JSON conversion; URLs are values, not fetched.
- new_artifact and typed artifact factories assign UUID unless supplied and attach name/description/parts. get_artifact_text extracts only text.
- new_task_from_user_message requires user role, nonempty parts, and nonempty any text part; returns SUBMITTED Task with message IDs or generated UUIDs and initial history. It does not enqueue or save. new_task constructs a Task from explicit IDs/state/history/artifacts.
- new_text/data/raw/url_part construct Part oneof; get_text/data/raw/url_parts filter matching presence and extract values.
- typed status/artifact update factories build events; they do not publish. Artifact append/last_chunk flags need coherent IDs across calls.
- get_stream_response_text chooses present payload, extracting message text, task artifact texts, status-message text, or artifact-update text. No file retrieval or multimodal inference.

## Validation and wire utilities

`a2a/utils/proto_utils.py`:

- to_stream_response copies a recognized event into matching oneof. Unknown input produces an empty envelope instead of raising; validate outputs in application code.
- parse_params accepts protobuf camelCase query keys, ignores unknown keys, uses final scalar occurrence, splits repeated comma-separated/repeated values, converts bool strings by equality to 'true', then ParseDict(ignore_unknown_fields=True). Unsupported shapes/values can raise parse errors. A typo query can be silently ignored.
- validate_proto_required_fields walks descriptor REQUIRED annotations. `_check_required_field_violation` handles empty repeated, missing presence, default scalar. `_recurse_validation` visits present singular/repeated/map message values; `_append_nested_errors` prefixes paths; `_validate_proto_required_fields_internal` accumulates them. Errors→InvalidParamsError(data={'errors': field/message dictionaries}). It is not full business validation or outgoing event validation.
- validation_errors_to_bad_request / bad_request_to_validation_errors convert paths/messages to/from Google RPC BadRequest details.
- make_dict_serializable recursively handles basic scalars/dicts/lists/tuples and stringifies other objects; normalize_large_integers_to_strings recursively converts integers exceeding 15 digits; parse_string_integers_in_dict reverses sufficiently long numeric strings. These utilities are not automatically applied to every server response.

`a2a/utils/task.py`: validate_history_length rejects negative; apply_history_length leaves original Task unless trimming needed, then copies and keeps last N or clears history for explicit zero. Missing field means untrimmed. validate_page_size accepts 1–100. encode_page_token/decode_page_token use base64 task ID, restoring missing padding, turning decode errors into InvalidParamsError. Cursor is neither signed nor owner authorization; store validates existence/scope.

`a2a/utils/constants.py`: card path `/.well-known/agent-card.json`, default RPC `/`, list page size 50/max 100, current protocol 1.0/legacy 0.3, VERSION_HEADER='A2A-Version', TransportProtocol values JSONRPC/HTTP+JSON/GRPC. SDK version 1.1.4 and protocol version 1.0 are different concepts.

`a2a/utils/version_validator.py`: validate_version parses expected version once. Nested decorator locates ServerCallContext from keyword/context positional args; `_get_actual_version` reads headers, defaults to legacy 0.3 when context exists but header absent, or expected version when no context. `_is_version_compatible` accepts exact match or same parsed major. Invalid version/mismatched major→VersionNotSupportedError. Coroutine and generator wrappers preserve delegation shape; checks happen before execution, not protocol negotiation.

`a2a/utils/json_utils.py`: dumps uses json.dumps(ensure_ascii=False), preserving non-ASCII SSE characters. Does not make nonserializable values serializable.

## Error conversion

`a2a/utils/errors.py`: A2AError carries message and optional data, with concrete domain subclasses. Exact class maps specify JSON-RPC codes, HTTP code, gRPC status and ErrorInfo reason. For example TaskNotFound→JSON-RPC -32001/HTTP404/NOT_FOUND; InvalidParams→-32602/HTTP400/INVALID_ARGUMENT; InvalidAgentResponse→-32006/HTTP500/INTERNAL. Unknown subclasses generally fall back to internal/unknown because adapters use exact type lookup.

`a2a/utils/error_handlers.py`: `_error_info`, build_error_details and `_build_error_payload` construct Google RPC-shaped details/error wrappers. InvalidParams nested errors add BadRequest fieldViolations. build_rest_error_payload maps A2AError; protobuf ParseError→400 INVALID_ARGUMENT; unknown exceptions→500 with generic 'unknown exception'. `_create_error_response` logs then JSONResponse with mapped status. rest_error_handler catches ordinary exceptions around endpoint execution. rest_stream_error_handler catches setup errors; nested iterator catches/logs/re-raises errors after response starts. The dispatcher itself emits SSE error payloads in its iterator. These wrappers do not catch every BaseException or retry failed operations.

`a2a/utils/grpc_status.py`: GrpcStatus holds code/details/trailing metadata. status_to_grpc maps integer code to grpc.StatusCode, packs serialized Status under grpc-status-details-bin, rejects invalid status and missing grpc. status_from_call parses those trailers and verifies status code/message matches call; it is a supporting decoding API, not server execution.

## Queues and telemetry

`a2a/utils/_async_queue_compat.py`: Python >=3.13 uses asyncio.Queue/QueueShutDown; earlier versions use culsans.Queue(...).async_q and AsyncQueueShutDown. create_async_queue is selected by import-time Python version. Shutdown/join semantics used throughout server must be checked against selected backend; this environment uses culsans.

`a2a/utils/telemetry.py`: optional OpenTelemetry with no-op objects when absent or OTEL_INSTRUMENTATION_A2A_SDK_ENABLED is not 'true' (case-insensitive). trace_function wraps coroutine or sync function, starts span, records result status/exceptions, runs optional attribute_extractor whose errors are logged/swallowed. Cancellation/queue shutdown are not marked error in coroutine wrapper. trace_class wraps inspect-discovered nondunder methods subject to include/exclude lists. It does not configure exporters. Async generators are treated as sync function calls, so span coverage can end at generator creation rather than include iteration. Hardcoded instrumentation version '1.0.0' is not installed SDK version.

## Optional URL screening

`a2a/utils/push_url_validator.py` is a recommended explicit dependency, not automatically used by server constructors. validate_push_notification_url requires HTTP(S), hostname, valid port and successful async DNS resolution. `_ip_is_blocked` rejects invalid/private/loopback/link-local/multicast/reserved/unspecified addresses; any blocked resolved address rejects host. False rejects URL; OS resolution error fails closed. No live DNS call was made for this documentation.

Inference from code: checking DNS before a separate HTTP request does not pin resolved addresses or validate redirect destinations. Use constrained egress/allowlisted destinations when those boundaries matter. Set client follow_redirects=False and explicit timeout; pass validator at both config registration and delivery. Validator exceptions outside sender's HTTP try can propagate.

## v0.3 compatibility implementation

The server imports compatibility modules directly even when feature flags are disabled. Compatibility is **representation adaptation around the same core handler**, not a second executor/task store.

- `compat/v0_3/jsonrpc_adapter.py`: JSONRPC03Adapter supports legacy slash methods. Parses Pydantic request envelope, builds wrapped context, dispatches to RequestHandler03, returns Pydantic success/error envelopes. Streaming maps errors to legacy internal-error payloads. Only enable when actually advertising legacy interfaces.
- `compat/v0_3/rest_adapter.py`: REST03Adapter returns `/v1/...` paths via partial-bound methods; pre-reads streaming body; wraps REST03Handler output into JSON/SSE. Legacy routes include card `/v1/card`; default map lacks config DELETE. Source method presence elsewhere does not imply mounted endpoint.
- `compat/v0_3/request_handler.py`: RequestHandler03 converts legacy request→current protobuf, calls core RequestHandler, converts current result back. Send discriminates Task/Message; get/cancel require non-None; streams wrap current events then map old result; configs use old nested structure; list maps response to legacy config list. No independent authorization/cache/retry.
- `compat/v0_3/rest_handler.py`: REST03Handler parses legacy protobuf body ignoring unknown fields, uses legacy FromProto→Pydantic→RequestHandler03→legacy ToProto, serializes result. Path IDs override config body; historyLength converted with int; metadata is not uniformly accepted for path-only operations. Version 0.3 validation wraps methods.
- `compat/v0_3/context_builders.py` and extension_headers.py: V03 HTTP/gRPC builders delegate inner builder then union legacy X-A2A-Extensions values with current extension set; preserve identity. No authentication is added. `_get_legacy_grpc_extensions` decodes matching metadata strings/bytes.
- `compat/v0_3/conversions.py`: maps old Pydantic values↔current protobuf models. Parts convert text, object data, base64 file bytes/URI; nonobject data uses data_part_compat metadata marker. Messages preserve IDs/references/metadata/roles. Task/status/artifact conversion maps states/history/timestamps/parts. Old blocking inverts current return_immediately. Config conversion flattens/unflattens nested push configuration and preserves authentication/token. Security requirements convert maps/scopes; OAuth/security oneofs select schemes (old multiple flows cannot all coexist in current flow oneof). Cards move primary/additional interfaces into supported_interfaces; reverse conversion selects only legacy-compatible interfaces and raises VersionNotSupportedError if none. Core-only fields may not survive legacy conversion; do not assume arbitrary lossless roundtrip.
- `compat/v0_3/model_conversions.py`: converts old ORM JSON task/config rows to current models; custom core_to_compat_* hooks can persist legacy representations with protocol_version='0.3'. Task hook does not automatically populate timestamp-derived last_updated like current store converter. Config conversion can Fernet-encrypt bytes.
- `compat/v0_3/proto_utils.py`, legacy generated protobuf/types.py and versions.py: backing representations for REST03Handler. ToProto/FromProto translate old Pydantic data, file/content/state/security/card/config objects to old protobuf, using Struct conversion/large-number normalization, enum mappings and old oneofs. They do not operate current models directly; conversions.py bridges to current models. Legacy version predicate controls reverse card interface filtering. These are supporting translation layers, not a reason to duplicate all legacy client/server packages in this server guide.

## Third-party boundaries

Starlette routes/auth/users and sse-starlette response classes serve HTTP; FastAPI helper adds OpenAPI exposure. httpx executes webhook I/O; SQLAlchemy and an async driver perform database transactions; protobuf parses/serializes wire values; json-rpc validates/builds envelopes; Pydantic validates context/legacy models; packaging parses versions; cryptography encrypts stored config. Local server source cannot establish database durability, remote webhook behavior, reverse-proxy streaming, or external authentication guarantees.
