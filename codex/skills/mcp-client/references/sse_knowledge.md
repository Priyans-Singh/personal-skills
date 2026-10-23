# `mcp.client.sse`: legacy SSE transport

Source inspected: MCP 1.30.0. `sse_client(url, headers=None, timeout=5, sse_read_timeout=300, httpx_client_factory=create_mcp_http_client, auth=None, on_session_created=None)` is an async context manager yielding streams for `ClientSession`.

It GETs an SSE endpoint, waits for an `endpoint` event, resolves its URL against the original and rejects a different scheme/netloc, then POSTs outgoing serialized JSON-RPC to that endpoint. `message` events become `SessionMessage`; blank data is a keepalive; invalid JSON is put on read stream as an exception and later events continue. `on_session_created` receives query `sessionId`/`session_id` when available. HTTP status failures raise; post-writer failures log then close the write side.

SSE read timeout limits idle event wait; regular request operations use `timeout`. HTTP redirect handling follows only safe same-origin paths via shared helpers. Prefer streamable HTTP for new code—this transport requires the old endpoint-event convention.

`remove_request_params` produces a path-only log URL; `_extract_session_id_from_endpoint` parses accepted query spellings. Callable index: both helpers, `sse_client`, nested `sse_reader`, `post_writer`.
