# `http_helpers.py`: HTTP dispatch and SSE lifetime

Source: a2a-sdk 1.1.4. Shared by current and compatibility HTTP transports.

## Ordinary requests and errors

`get_http_args(context)` returns a new kwargs dictionary. Nonempty service parameters are shallow-copied to `headers`; non-None timeout becomes `httpx.Timeout(value)`, including zero. Missing fields leave HTTPX defaults active. State is not serialized.

`send_http_request(httpx_client,request,status_error_handler=None)` runs `client.send(request)`, `raise_for_status`, `response.json` inside `handle_http_exceptions`. Despite dictionary annotation, response shape is not explicitly checked here.

Synchronous context manager `handle_http_exceptions(status_error_handler=None)` yields once and catches:

| Exception | Raised result |
|---|---|
| HTTPX timeout | `A2AClientTimeoutError` |
| HTTP status | Calls optional handler, expected to raise; if it returns, raises generic `A2AClientError` |
| HTTPX request/network | `A2AClientError` |
| JSON decode | `A2AClientError` |

Each generic translation chains its cause. Protobuf parsing, shape errors and Unicode decoding are not covered by these catches. Request construction can occur outside this context. No retry is installed.

## SSE parser

Async generator `parse_sse_stream(response)` reads `response.aiter_lines()`, defaults event name to `message`, accumulates `data:` values, and yields `(event_name,newline_joined_data)` on blank lines. It removes one optional leading space after the colon, splits only the first colon, ignores comment lines beginning `:`, and ignores unknown keys including `id` and `retry`.

After each blank delimiter it resets event name/chunks. No payload yields for a block with no data lines. **There is no final flush on EOF**, so data without a trailing blank delimiter is dropped. It does not store Last-Event-ID or implement reconnect delays. Parser memory grows with the current event block, not the full stream; no local maximum event-size bound is imposed.

## Streaming dispatch

`send_http_stream_request(client,method,url,status_error_handler=None,sse_error_handler=_default_sse_error_handler,**kwargs)` is an async generator. Iteration opens `_SSEEventSource` within the exception context. It checks status; on upfront status failure it first awaits `response.aread()` so error handlers can inspect the body.

If Content-Type lacks the literal substring `text/event-stream`, it reads the whole body, decodes UTF-8 and yields one string. Otherwise it parses event blocks, ignores empty data, calls the error handler for event name exactly `error`, and yields the raw data strings. If a custom error handler unexpectedly returns, the same data is yielded. Transport code then performs JSON/protobuf parsing.

`_default_sse_error_handler(sse_data)` always raises `A2AClientError` containing the error event. REST and current JSON-RPC override it with their domain parsing. Legacy HTTP transports use the default for SSE error events.

## `_SSEEventSource`

`__init__(client,method,url,**kwargs)` converts supplied headers to `httpx.Headers`, uses `setdefault` for `Accept: text/event-stream` and `Cache-Control: no-store`, builds the request, retains client and starts with no response. Explicit caller values are preserved.

`__aenter__` calls `client.send(request,stream=True)`, stores and returns response. `__aexit__` closes a stored response with `aclose`; it does not close the shared client. Its class-based async context manager avoids an async-generator context manager finalization collision described in source. It does not make abandoned outer generators synchronously close themselves.

Consume streams with deliberate lifetime management, explicitly close iterators when abandoning them, and close the high-level client at application shutdown. Breaking iteration or losing a connection is not a remote task cancellation. There is no HTTP/SSE reconnect or delivery replay layer.
