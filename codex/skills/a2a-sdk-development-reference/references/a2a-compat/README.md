# A2A compat execution reference

Entire installed `a2a/compat`, **a2a-sdk 1.1.4**, inspected **2026-10-07**. Source root: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat`.

Compatibility translates old wire shapes into the current SDK's core protobuf objects. It does not replace the core request handler, task stores, executor, auth policy or client transport runtime. Start with [execution boundaries](execution_boundaries_knowledge.md), then the relevant flow/modules below. Claims derive from inspected bodies; protocol intent in source comments is identified separately.

## Navigation

| Source/module family | Guide |
|---|---|
| Root empty initializer | [compat namespace](compat_init_knowledge.md) |
| Nested empty initializer / representation map | [v0.3 package](v0_3_init_knowledge.md) |
| Current protobuf ↔ legacy Pydantic | [conversions](v0_3_conversions_knowledge.md) |
| Legacy protobuf ↔ legacy Pydantic, integer helpers | [proto utilities](v0_3_proto_utils_knowledge.md) |
| Every Pydantic class, field/default/schema meaning/enum | [types](v0_3_types_knowledge.md) |
| Generated Python, every PYI declaration, complete runtime descriptors | [protobuf family](v0_3_a2a_v0_3_pb2_knowledge.md) |
| Generated stub, servicer defaults, registration, experimental wrappers | [gRPC wrappers](v0_3_a2a_v0_3_pb2_grpc_knowledge.md) |
| Protocol-independent server delegate | [RequestHandler03](v0_3_request_handler_knowledge.md) |
| JSON-RPC server routing, envelopes, SSE | [JSON-RPC adapter](v0_3_jsonrpc_adapter_knowledge.md) |
| REST route map and response management | [REST adapter](v0_3_rest_adapter_knowledge.md) |
| REST body/path/query parsing and serialization | [REST handler](v0_3_rest_handler_knowledge.md) |
| Legacy gRPC server execution and error aborts | [gRPC handler](v0_3_grpc_handler_knowledge.md) |
| JSON-RPC client, HTTP/SSE helpers, errors | [JSON-RPC transport](v0_3_jsonrpc_transport_knowledge.md) |
| REST client and subscribe fallback state | [REST transport](v0_3_rest_transport_knowledge.md) |
| gRPC client, metadata, errors and EOF streams | [gRPC transport](v0_3_grpc_transport_knowledge.md) |
| Extension header mutation | [extension headers](v0_3_extension_headers_knowledge.md) |
| Context identity and legacy/current extension union | [context builders](v0_3_context_builders_knowledge.md) |
| Version interval detection | [versions](v0_3_versions_knowledge.md) |
| Database format/encryption helpers | [model conversions](v0_3_model_conversions_knowledge.md) |
| Entire proto/comments, README, buf YAML/lock | [protocol assets](v0_3_protocol_assets_knowledge.md) |
| Direct external/sibling execution boundaries | [boundaries](execution_boundaries_knowledge.md) |

[Callable index](callable_index.md) / [machine index](callable_index.json) account for classes, public methods, private helpers, nested closures, generated experimental wrappers and PYI constructors. [Source manifest](source_manifest.json) hashes every source/support/cache file. Bytecode files are inventoried as generated runtime caches, not treated as additional implementation source. No separate JSON schema or buf generation YAML exists under this source folder.

## Identity and resource hierarchy

AgentCard advertises interfaces, app version, skills, capabilities and security descriptions. Legacy card exposes primary URL plus additional interfaces; core card exposes supported_interfaces with protocol binding/version. Python distribution version 1.1.4, wire version 0.3 or 1.0, proto generator version 5.29.3 and AgentCard.version are independent.

Message.message_id identifies a message, Task.id identifies a task, context_id groups conversation/work context, reference_task_ids links tasks in Pydantic/core but is absent in legacy protobuf. JSON-RPC envelope id correlates request/response and never substitutes for business IDs. Legacy gRPC resources use `tasks/{id}` and `tasks/{task}/pushNotificationConfigs/{config}`; core config flattens task_id and id, legacy pivot nests push_notification_config. User identity comes from ServerCallContext builder/middleware; owner supplied to DB constructors is not authenticated by those helpers.

## End-to-end flows

### Current client → legacy JSON-RPC peer

1. Caller creates core SendMessageRequest and optional ClientCallContext.
2. CompatJsonRpcTransport converts message/configuration/metadata to legacy pivot params, creates JSON-RPC method envelope with new UUID, dumps camel aliases excluding None.
3. Request-local HTTP headers include version 0.3 and optional mirrored legacy extension header; injected httpx client handles actual peer connection/auth/TLS. Context timeout applies here.
4. Shared helper awaits send, checks status, parses JSON; compat validates response envelope, maps error code or classifies task/message result and converts back to core.
5. Streaming creates one HTTP SSE connection and converts each recognized envelope result. Unknown kinds can be skipped, errors raised, EOF ends iteration. No cursor/replay/retry; logical task cancellation requires separate cancel call.

### Legacy JSON-RPC client → current server core

1. Outer application/router parses body/method/id and calls JSONRPC03Adapter.
2. Adapter selects legacy Pydantic model, validates body and builds HTTP context plus legacy extension union; stores method/request ID in context.state.
3. Expected-version decorator checks context headers (actual source compares major only).
4. RequestHandler03 converts to core and awaits/iterates the same current RequestHandler using the same context. Core handler decides task/auth/store/executor policy.
5. Unary result gets typed legacy success envelope; JSON aliases emitted. Generic downstream errors become internal-error envelopes. SSE iteration failure becomes an internal-error SSE data item. Delete's None result is excluded from server output; compat client repairs it for envelope parsing.

### Current client ↔ legacy REST or gRPC

1. Current request goes through conversions to pivot, then ToProto to old protobuf. REST serializes protobuf JSON and sends route-specific HTTP; gRPC calls legacy stub path `/a2a.v1.A2AService/...`.
2. Legacy server adapter uses protobuf body/request → FromProto → pivot → RequestHandler03 → current handler.
3. Result takes reverse steps; REST uses MessageToDict/SSE JSON, gRPC encodes generated response type. HTTP server extended-card is a notable exception using Pydantic JSON dump.
4. Both directions cross an extra legacy-protobuf stage, losing fields even when direct pivot/core conversion preserves them. File bytes become UTF-8 base64 text at this stage; timestamp/reference IDs disappear, skill security/card icon/OAuth metadata omitted by utilities.
5. gRPC abort details map by class name on client; HTTP REST expects an older top-level type/message shape while current server decorator emits nested error payload. Neither representation translates storage/auth ownership policy.

### Core data ↔ legacy storage format

1. Task helper converts core to Pydantic JSON and constructs TaskModel with protocol_version 0.3 and explicit owner.
2. Push helper serializes inner config bytes, optionally encrypts with caller Fernet, constructs row keyed by explicit task_id/config.id.
3. External store/session persists row and enforces owner/transactions; helpers perform no SQL.
4. Reader validates stored legacy task fields or decrypted config JSON, then converts core. Push reader does not decrypt or verify protocol label; caller must route format/decrypt first.

## Operational support matrix

| Operation/policy | JSON-RPC client / server | REST client / server | gRPC client / server |
|---|---|---|---|
| Send, stream, get, cancel, subscribe | Implemented | Implemented | Implemented |
| ListTasks | Client rejects; no server method | Client rejects; no route | Client rejects; no proto RPC |
| Push create/get | Implemented | Implemented | Implemented |
| Push list | Implemented; paging lost | Client rejects; server GET route exists | Implemented; paging lost |
| Push delete | Implemented; result None omitted server-side | Client rejects; no route | Implemented; Empty response |
| Extended card cache shortcut | Client skips when flag false | Client skips when flag false | Client always requests |
| ClientCallContext timeout | Applied to httpx | Applied to httpx | Ignored by compat stub calls |
| Retry / automatic reconnect | None in compat | Subscribe 405 verb fallback only | None in compat; runtime channel options outside scope |
| Server version decorator | Applied to processors | Applied to handler methods | None in CompatGrpcHandler |

Cancel means requesting a core/remote cancellation transition; local compat code cannot guarantee executor termination or absence of future updates. Delete only delegates callback-config deletion and does not delete a task. Stream disconnect closes transport iteration/resource, not necessarily the agent's logical task.

## Common pitfalls and safe usage

- Set explicit legacy blocking behavior when using REST/gRPC. Absent protobuf configuration becomes blocking false after FromProto, unlike absent direct Pydantic configuration.
- Verify conversions with representative bytes, timestamps, null/empty metadata, zero history length, references, multiple OAuth flows and credentials; round trips are intentionally lossy.
- Card conversion requires at least one missing/legacy protocol-version interface; current-only core cards fail reverse conversion. Copied signatures are not re-signed.
- Supply canonical-case A2A-Extensions in call parameters for mirroring. Header helper uses exact-case dict keys.
- Supply authenticated context builders. Default gRPC identity is unauthenticated; HTTP relies on middleware. Compat itself performs no credential acquisition/owner checks.
- Decide ownership of shared injected clients/channels before using async context manager/close; transport closes them.
- Add caller retry/idempotency/deadline/replay policy only with understood remote guarantees; compat does not supply them. Especially gRPC context timeout is not forwarded.
- Keep callback credentials separate from A2A peer authorization, and choose Fernet encryption explicitly for persistence. No expiry/rotation/decrypt behavior is inferred.

## Reproducibility and validation

Generate module drafts/index/hash inventory locally:

```sh
.venv/bin/python -B a2a-compat/build_reference.py
```

Validate inventory, declaration headings/body narratives, field/descriptor coverage, file hashes, local links/format and pure/mock examples:

```sh
.venv/bin/python -B a2a-compat/validate_reference.py
```

[Validation results](validation_report.json) records actual counts/checks. Coverage checks establish names/fields/body presence; they do not prove every narrative claim semantically. Body tracing and local behavior fixtures supplement them. gRPC and SQLAlchemy are absent: corresponding implementation reviewed statically, no gRPC/DB import/run. No external HTTP, cloud API, installs, commits, server startup or destructive actions performed. Only this directory was written.
