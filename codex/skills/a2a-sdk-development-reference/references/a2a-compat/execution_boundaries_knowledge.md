# Direct execution boundaries

Inspected locally: a2a-sdk **1.1.4**, **2026-10-07**. These are direct dependencies of compat behavior, not duplicated client/server references. [Navigation](README.md).

## Representation and dependency boundaries

| Dependency | What compat delegates | Execution consequence |
|---|---|---|
| `a2a.types.a2a_pb2` | Current core protobuf object construction, field presence, enum/oneof behavior | Modern Python SDK inputs/results are protobuf; namespace `lf.a2a.v1`. Current fields unsupported by compat can disappear. No business logic or network call occurs merely from constructing them. |
| `a2a._base.A2ABaseModel`, Pydantic | Alias generation, input parsing, union selection, JSON serialization, validation errors | Snake names and camel aliases accepted; `in_` alias becomes `in`. Types are not custom runtime clients. Default extra fields ignored. Core business exceptions are distinct from legacy schema error models. |
| `google.protobuf` JSON/runtime/descriptor APIs | `Parse`, `ParseDict`, `MessageToDict`, Struct/Value, Timestamp, generated builder | Unknown fields ignored only where caller passes that option. Scalar/default/presence behavior differs from Pydantic optional fields. Large Struct numbers use doubles. `bytes` JSON uses base64. Builder materializes runtime classes absent from AST. |
| `google.api` annotations/client/field-behavior | Descriptor registration and options | Runtime generated import dependency, even for local protobuf serialization. Required field annotations do not themselves execute validation in hand-written compat methods. |
| `packaging.version` | Version ordering/parsing | Invalid versions return false in `is_legacy_version`; decorator boundary raises VersionNotSupportedError for incompatible valid/invalid headers. PEP 440 parsing is not strict semantic-version-only parsing. |
| `a2a.utils.constants` | `A2A-Version`, protocol constants 0.3 / 1.0 | SDK release, wire protocol, application card version and compiled protobuf generator version are separate dimensions. |
| `a2a.utils.errors` / `a2a.server.jsonrpc_models` | Executable exceptions and JSON-RPC error models/code maps | Transports map error codes/names, often losing error data. Server JSON-RPC adapter wraps generic downstream exceptions as InternalError. Exact error class mapping can miss subclasses. |
| `jsonrpc.jsonrpc2.JSONRPC20Request/Response` | Envelope construction/parsing | UUID envelope IDs are transport correlation fields. No explicit response ID comparison is added by compat; library parsing remains an external boundary. |
| `a2a.utils.json_utils.dumps` | REST SSE serialization | Actual body calls `json.dumps(obj, ensure_ascii=False)`. It preserves Unicode in emitted text and raises normal JSON serialization errors; no protocol translation inside. |

## Shared HTTP helper body trace

Source inspected: `a2a/client/transports/http_helpers.py`. Compat HTTP transports call it directly.

`get_http_args(context)` creates a fresh dict; copies `service_parameters` into `headers` and applies `httpx.Timeout(context.timeout)` when timeout is non-None. It ignores `context.state`. It does not fetch credentials or merge a separate interceptor policy. Compat then inserts version/mirrors extensions into that copied header dict.

`send_http_request` enters `handle_http_exceptions`, awaits injected client's `send(request)`, calls `raise_for_status`, then `response.json`. TimeoutException becomes A2AClientTimeoutError; HTTPStatusError calls supplied domain callback; RequestError becomes A2AClientError network error; JSONDecodeError becomes A2AClientError decode error. Other errors propagate. No retry loop is present. Callback raising a domain error preserves that error rather than falling through to generic status.

`send_http_stream_request` creates `_SSEEventSource` with request kwargs, enters it, checks status. On status failure it `await response.aread()` before raising so status handler can read error JSON. If content type does not include `text/event-stream`, it reads entire body, decodes UTF-8, yields one data string, returns. Otherwise it iterates `parse_sse_stream`; empty data skipped; SSE event name `error` invokes default callback raising A2AClientError. Compat sees only data strings after this preprocessing. Consequently JSON-RPC can parse a non-SSE upfront error payload; REST will try protobuf JSON parsing unless status already failed.

`parse_sse_stream` defaults event name to `message`, collects multiple `data:` lines joined with newline, ignores comments, splits fields on first colon and strips one leading value space. Blank line emits only if payload chunks exist, then resets buffers/event name. It ignores id/retry/unknown fields. It has no final EOF flush, so an unterminated last event without a blank line is lost. It buffers one event, not the full stream. There is no reconnect, Last-Event-ID persistence, deduplication or retry-delay application.

`_SSEEventSource.__init__` builds an httpx request, adding default Accept=text/event-stream and Cache-Control=no-store if absent. `__aenter__` awaits client.send(stream=True); `__aexit__` awaits response.aclose if created. Class-based async context management avoids nested asynccontextmanager generator finalization collision; it does not create an independent agent task. Closing transport closes the injected HTTP client, so it is an ownership decision affecting all users of that client. Inherited ClientTransport `__aenter__` returns self and `__aexit__` calls close.

## Server context and error boundaries

Source inspected: `a2a/server/routes/common.py`, `a2a/server/context.py`, `a2a/extensions/common.py`, `a2a/server/request_handlers/grpc_handler.py`.

HTTP default builder copies request headers, conditionally copies middleware auth into state and creates a user adapter from middleware user. With no user it creates UnauthenticatedUser. gRPC default builder stores `grpc_context`, parses current extension metadata and always uses UnauthenticatedUser. Compat wrappers union legacy extensions and preserve the same context. `get_requested_extensions` splits comma lists, trims, removes empty values and produces set. No authentication or extension implementation is added by this parser.

Core RequestHandler is the direct async behavior interface. Task stores, event queues, executor transitions, user/owner checks, callback sending, consistency, logical task cancellation and persistence occur beyond it. RequestHandler03 forwards calls rather than substituting those implementations. Current `to_stream_response` checks four core event classes and wraps them into the corresponding protobuf oneof; unknown event gives empty wrapper, then compat conversion rejects unknown payload.

Source inspected: `a2a/utils/version_validator.py`. Decorator searches kwargs `context`, then positional ServerCallContext; no context uses expected version. Reads exact standard/lowercase version keys from `context.state['headers']`; missing/empty defaults 0.3. `_is_version_compatible` checks actual==expected first, then parsed **major equality**, ignoring both minor and patch. This contradicts its descriptive docstring. Async-generator wrapper validates when called, returns generator; coroutine wrapper validates on await. Compat JSON-RPC processing and REST methods apply it; CompatGrpcHandler does not. Custom HTTP context builders must retain headers in state if they want this validation.

Source inspected: `a2a/utils/error_handlers.py`. REST unary decorator catches Exception and produces JSONResponse; A2AError maps via exact type to HTTP/status/reason plus ErrorInfo metadata; InvalidParamsError validation data can add BadRequest field violations. Protobuf ParseError gives HTTP 400; arbitrary exception yields 500 unknown exception. Payload is nested `error` with code/status/message/details. Configured error.data can be serialized and logged; it is not redacted by this dependency. REST stream decorator converts errors while creating response; if response.body_iterator is async generator, wraps iteration, logs and re-raises late errors. HTTP status cannot be changed after headers by this code. Compat REST client expects top-level legacy type/message, so it generally misses this newer structured reason.

gRPC `_ERROR_CODE_MAP` is exact error-class map: request/params/content errors INVALID_ARGUMENT; missing task/method NOT_FOUND; internal/invalid response INTERNAL; cancellation unsupported/push unsupported/operation unsupported/extended-card/extension/version errors FAILED_PRECONDITION. Compat abort encodes class name and message in details, and client maps names from JSON_RPC_ERROR_CODE_MAP; there is no rich google.rpc status decoding in compat. Transport-level identity and deadline come from grpc runtime/interceptors, not protobuf fields.

## Telemetry and optional persistence

Fresh direct `JSONRPC03Adapter` import was observed to fail through adapter → `server.routes.common` → routes package initializer → jsonrpc_routes → jsonrpc_dispatcher → partially initialized adapter. Source bodies show `server.routes.__init__` eagerly imports route families and dispatcher imports the compat adapter. Initializing `a2a.server.routes` first was locally verified to avoid that cycle. This is an import-order execution boundary; no installed source was changed. Prefer normal route package entry points when integrating rather than assuming direct adapter imports always work.

`trace_class` body enumerates inspect.isfunction members, skips dunder names, applies include/exclude filters, and replaces eligible functions with trace_function span wrappers. Compat HTTP/gRPC transports use CLIENT kind, REST03Handler SERVER. It can also wrap private methods; constructors are excluded. It does not implement retry or storage. Export/provider/network telemetry policy is outside compat; no telemetry exporters or endpoints were configured/invoked during this reference build.

`model_conversions` imports SQLAlchemy model classes. Source `a2a/server/models.py` has a guarded import that raises an explicit ImportError when SQLAlchemy is missing. Task model columns store JSON status/history/artifacts/metadata plus ID/context/owner/protocol label; callback config stores binary bytes with composite task/config key and owner/protocol. Helper constructing an ORM object performs no SQL or commit. Fernet.encrypt, if supplied, encrypts serialized payload; no decryption or key rotation is added by compat. Caller owns store transactions, key lifetime and owner verification.

## Credentials by destination and lifetime

| Value | Destination | Lifetime implemented locally |
|---|---|---|
| CallContext service parameters, including caller auth headers | Configured A2A peer HTTP URL or gRPC channel target | Copied into per-request headers/metadata; transport does not expire/refresh them. Caller context may retain originals. |
| Injected httpx client auth/cookies/TLS settings | HTTP peer | Owned by client until caller/transport closes it; compat does not inspect credential material. |
| Channel/call credentials | gRPC peer | Channel factory/experimental wrapper/runtime control; compat transports do not create a credential provider. |
| Push config token/authentication credentials | Configuration payload for callback URL | Model/core/optional DB row lifetime; plaintext unless caller encrypts via Fernet helper; no delivery/refresh/expiry here. |
| Card security scheme OAuth token URL/scopes | Discovery descriptions | No OAuth request or token acquisition; translated fields only. |
| Card signature/protected/header | Discovery payload | Copied without verification/re-signing; transformations may change signed content. |
| ServerCallContext.user/owner arguments | Core handler/store policy | HTTP/gRPC request context or constructed ORM row; compat does not establish ownership truth. |

## Installed optional dependency status

Local probe found httpx, jsonrpc, packaging, Pydantic, google.api annotations, Starlette, sse-starlette and cryptography present. **grpcio and SQLAlchemy absent**. Therefore gRPC transport/handler/generated-grpc and persistence imports were not executed. All their source bodies were inspected. No dependency installation, external request, server startup, database session or cloud API was used.
