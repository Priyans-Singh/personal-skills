# `mcp.client.streamable_http`: current remote transport

Source inspected: MCP 1.30.0. Use `async with streamable_http_client(url, http_client=None, terminate_on_close=True) as (read, write, get_session_id)`. Pass a preconfigured `httpx.AsyncClient` for authentication, headers, TLS/proxy, and timeout policy; otherwise this module owns a client with 30s general and 300s read timeout.

`StreamableHTTPTransport(url)` stores endpoint, MCP session ID, and negotiated protocol version. Deprecated constructor headers/timeout/SSE/auth inputs warn and are ignored. `_prepare_headers` sends JSON/SSE Accept, JSON Content-Type, and after handshake session/protocol headers. The initialization POST extracts `mcp-session-id`; JSON or SSE response is parsed and initialization response records protocol version. On `notifications/initialized`, `start_get_stream` opens GET SSE for server-initiated traffic.

`post_writer` handles requests concurrently, notifications serially. `_handle_post_request` treats 202 as no result; a request 404 becomes a synthetic session-terminated JSON-RPC error; request JSON goes to `_handle_json_response`, SSE to `_handle_sse_response`, other content type places `ValueError` on read stream. SSE tracks event IDs/retry intervals, processes messages in `_handle_sse_event`, and reconnects twice at server retry or 1 second. Resumption metadata selects `_handle_resumption_request`, GETs with `Last-Event-ID`, and maps returned response ID back to original request. Missing token raises `ResumptionError`.

Same-origin redirect policy accepts same origin/default-port HTTP→HTTPS, preserving POST only for 307/308; cross-origin, method-changing, or HTTPS downgrade redirects produce descriptive `HTTPStatusError`. `terminate_session` DELETEs on context exit when configured; 405 and failures are only logged. Deprecated `streamablehttp_client` converts older parameters then delegates.

Callable index: `StreamableHTTPError`, `ResumptionError`, `_unfollowed_redirect`, `_raise_for_unfollowed_redirect`, `RequestContext`, every `StreamableHTTPTransport` constructor/header/handshake/SSE/GET/resumption/POST/reconnection/writer/termination method, `streamable_http_client`, `streamablehttp_client`.

Internal callable names: `__init__`, `_is_initialization_request`, `_is_initialized_notification`, `_maybe_extract_session_id_from_response`, `_maybe_extract_protocol_version_from_message`, `handle_get_stream`, `_handle_reconnection`, `_handle_unexpected_content_type`, `_send_session_terminated_error`; nested `handle_request_async`.
