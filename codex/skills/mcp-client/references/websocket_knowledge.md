# `mcp.client.websocket`

Source inspected: MCP 1.30.0. `websocket_client(url)` is deprecated and non-spec; use Streamable HTTP. It connects with subprotocol `mcp`, creates unbuffered streams, and runs nested `ws_reader`/`ws_writer` tasks. Reader validates every received text frame as JSON-RPC and emits a `SessionMessage` or `ValidationError`; writer serializes outgoing message bodies with aliases and omitted `None`. Context exit cancels both tasks and closes WebSocket.

Callable index: `websocket_client`, nested `ws_reader`, `ws_writer`.
