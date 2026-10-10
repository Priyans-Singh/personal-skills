# Core protocol server and transports

This guide covers the non-auth, non-FastMCP source at `mcp/server` in MCP 1.30.0: root package files, `lowlevel/`, session, elicitation, transports, HTTP manager, security and validation.

## Low-level request lifecycle

```text
transport parses JSON-RPC → ServerSession enforces initialize state
→ session.incoming_messages → Server.run starts handler task
→ Server installs request ContextVar → registered handler
→ result/error races safely back through session → transport serializes it
```

`__init__.py` re-exports `Server`, `FastMCP`, `NotificationOptions`, and `InitializationOptions`. `models.py` defines `InitializationOptions(server_name, server_version, capabilities, instructions?, website_url?, icons?)`. `__main__.py` is a diagnostic stdio listener: it logs incoming messages with AnyIO/Trio and does not implement application handlers.

## `lowlevel/`

`lowlevel/__init__.py` exports `Server` and `NotificationOptions`. `helper_types.py` provides `ReadResourceContents(content: str|bytes, mime_type?, meta?)`, the preferred resource-reader return value.

### `server.py — Server`

`NotificationOptions` advertises list-change flags for prompts/resources/tools. Default `lifespan` is an async context manager yielding `{}`. `Server(name, version?, instructions?, website_url?, icons?, lifespan=...)` holds exact request-type → async-handler maps, notification handlers, a tool definition cache, and lazy experimental handlers. `request_context` reads a ContextVar and raises `LookupError` outside a dispatched request.

`create_initialization_options` gets the installed MCP version unless supplied. `get_capabilities` infers capabilities from registered handlers: list prompts/resources/tools, logging level and completions. Resources advertise `subscribe=False`; experimental handlers may amend capabilities.

Decorator registration APIs are `list_prompts`, `get_prompt`, `list_resources`, `list_resource_templates`, `read_resource`, `set_logging_level`, `subscribe_resource`, `unsubscribe_resource`, `list_tools`, `call_tool`, `progress_notification`, and `completion`. List decorators accept zero-arg legacy handlers or typed request handlers; `func_inspection.create_call_wrapper` chooses compatible calling convention. `read_resource` accepts content objects or `ReadResourceContents`; raw strings/bytes are legacy/deprecated and normalized to text/blob content. Completion turns `None` into empty completion.

`call_tool(validate_input=True)` caches definitions from `list_tools`, JSON-Schema-validates inputs when enabled, calls the user handler, and accepts an existing `CallToolResult`, a task result, `(content, structured_dict)`, dict, or iterable blocks. Dict becomes pretty JSON text plus structured content. If tool has output schema, structured content is required and schema-validated. Validation/application errors become `CallToolResult(isError=True)`; `UrlElicitationRequiredError` remains a protocol error.

`run(read_stream, write_stream, initialization_options, raise_exceptions=False, stateless=False)` enters lifespan then `ServerSession`, configures experimental tasks if enabled, and starts one AnyIO task per incoming message. Transport end cancels outstanding handler work. `_handle_message` distinguishes request, notification and stream failures. `_handle_request` installs `RequestContext`, maps `McpError` to its error data and unexpected errors to code 0, avoids responding after cancellation, and tolerates closed-stream response races. Unknown methods yield `METHOD_NOT_FOUND`. `_handle_notification` invokes matching handler. `_ping_handler` returns `EmptyResult`.

`func_inspection.py — create_call_wrapper` introspects legacy callable signatures: it supplies a correctly typed required request parameter positional or named, otherwise invokes no arguments; introspection failure defaults to zero arguments. `experimental.py — ExperimentalHandlers` lazily enables deprecated task support, changes capabilities, owns per-session scope checks, and registers default task list/get/result/cancel handlers.

## `session.py`, elicitation, validation

`InitializationState` is `NotInitialized`, `Initializing`, `Initialized`. `ServerSession` extends shared `BaseSession`; it uses unbuffered AnyIO streams and exposes `incoming_messages`. Stateful sessions allow only initialize/ping until initialization notification; stateless sessions begin initialized. On initialization it chooses the requested supported protocol version or newest, returns server info/capabilities, then waits for initialized notification.

Server-to-client notifications: log, resource updated/list changed, tool/prompt list changed, progress, elicitation complete, and experimental raw `send_message`. Server-to-client requests: sampling `create_message`, `list_roots`, `elicit`/`elicit_form`, `elicit_url`, and ping. Capability checks cover roots, sampling/tools, elicitation and experimental entries. Sampling tool messages are validated; task-aware builders add related-task metadata and task IDs.

`elicitation.py` adds typed wrappers. `AcceptedElicitation[T]`, `DeclinedElicitation`, `CancelledElicitation`, and `AcceptedUrlElicitation` represent actions. `_validate_elicitation_schema` permits primitives, string sequences and optionals/unions—not nested models. `elicit_with_validation` generates schema, calls form elicitation and Pydantic-parses accepted data. `elicit_url` maps URL action; applications must later notify completion.

`validation.py`: `check_sampling_tools_capability` requires sampling plus tools; `validate_sampling_tools` raises `INVALID_PARAMS` if unsupported; `validate_tool_use_result_messages` ensures final tool-result blocks follow matching tool-use IDs.

## Transport modules

### `stdio.py`

`stdio_server` is an async context manager. It rewraps binary stdin/stdout as UTF-8 without closing OS handles, runs reader/writer tasks over unbuffered memory streams, parses one newline-delimited JSON-RPC message per line, forwards parse/model errors as stream values, writes aliases/non-null JSON one line at a time and flushes.

### `sse.py` — legacy SSE

`SseServerTransport(endpoint, security_settings?, max_request_body_size=4MiB)` accepts only a safe relative endpoint and positive size. It tracks UUID session writers and authenticated owners. `connect_sse` validates Host/Origin, creates stream pairs, emits an SSE `endpoint` event with encoded POST URL plus session ID, serializes server messages as SSE `message` events, and cleans state on close. `handle_post_message` uses a body-limited app; its private handler checks security, session ID, parsed JSON-RPC and owner identity. Missing/unknown/mismatched session returns 404 (no disclosure); malformed JSON 400; accepted input is queued. `websocket.py — websocket_server` is deprecated because WebSocket was never MCP spec: validates security, accepts `mcp` subprotocol, maps text JSON-RPC to streams and closes on errors.

### `streamable_http.py`

`EventMessage` holds output and optional event ID. `EventStore` is an abstract persistence boundary: store a stream event and replay after an ID. `StreamableHTTPServerTransport` owns state/session streams, request-specific response queues, SSE writers, optional store and idle state. IDs must be visible ASCII; timeout must be positive/finite.

`connect` routes output to a matching related-request stream, standalone GET stream, or event store. POST requests get distinct response streams to prevent a slow SSE writer from blocking others. `_mint_priming_event` persists an empty cursor only with an event store and protocol >= `2025-11-25`; `_run_sse_writer` sends it, then message events, stopping on JSON-RPC response/error. Per-request close enables replay; standalone reconnect is not implemented.

`handle_request` tracks in-flight work for idle timeout. Private dispatch validates security/termination and routes POST/GET/DELETE. POST requires valid Accept and JSON content, parses/validates body, creates session only on initialize, requires matching ID/protocol afterward, immediately 202-accepts notifications/client responses, returns per-request JSON in JSON mode or SSE in streaming mode. GET supports standalone SSE/replay with `Last-Event-ID`. DELETE terminates and closes all streams. Invalid sessions return 404; parse/schema failures return 400.

### `streamable_http_manager.py`

`StreamableHTTPSessionManager` is the ASGI host for a low-level app. It bounds request body, owns task group/transports/session principals, and `run()` may be entered once; teardown cancels and clears all. Stateless mode makes a transport and server run per request then shield-terminates it. Stateful mode binds a session to the creating authorization principal, returns 404 for mismatched/unknown IDs, protects admission with a lock, limits to `max_sessions` (503), and retains a new session only after opening status <400. Server task handles idle expiration and always discards before awaiting terminate. `_error_response` is JSON-RPC error; `_send_and_report_status` observes opening response status.

### `transport_security.py`

`TransportSecuritySettings` defaults DNS rebinding protection on; `TransportSecurityMiddleware(None)` defaults it off for compatibility. With protection, `validate_request` accepts allowed exact/wildcard-port Host and Origin, allows absent Origin, sends 421 invalid host / 403 invalid origin, and always requires JSON Content-Type for POST. `RequestBodyLimitMiddleware` rejects declared or aggregate bodies over limit with 413, buffers/replays permitted HTTP bodies, and passes non-HTTP scopes through.

## Failure and concurrency properties

There is no message retry. Stream errors can become log notifications; output write races are swallowed only when transport is closed/broken. AnyIO cancellation is the primary shutdown control. Event resumption exists only when the caller supplies an `EventStore`. Never depend on legacy SSE/WebSocket for new deployments; use stdio or streamable HTTP.

