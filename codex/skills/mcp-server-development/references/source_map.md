# MCP server package — source map

This is a source-grounded reference to the installed `mcp` Python package, version **1.30.0**, inspected on 2026-09-30. The source analysed is `.venv/lib/python3.11/site-packages/mcp/server` (59 Python files). This is the v1 maintenance line; do not treat details here as v2 behaviour. The package metadata says an unpinned `pip install mcp` now selects v2.

## Which API to begin with

Use `from mcp.server.fastmcp import FastMCP` for ordinary servers. It turns decorated Python functions into MCP tools, resources, and prompts, derives Pydantic schemas, runs transports, and delegates protocol handling to the low-level server.

Use `from mcp.server.lowlevel import Server` when you need to register raw protocol request handlers or own the initialization/runtime wiring. `mcp.server` re-exports `FastMCP`, `Server`, `NotificationOptions`, and `InitializationOptions`.

## Runtime hierarchy

```text
FastMCP
├─ lowlevel.Server ── ServerSession ── MCP JSON-RPC messages
├─ ToolManager     ── Tool ── callable + Pydantic metadata
├─ ResourceManager ── Resource / ResourceTemplate
├─ PromptManager   ── Prompt
└─ transport app
   ├─ stdio_server (stdin/stdout)
   ├─ SseServerTransport (GET SSE + POST messages)
   └─ StreamableHTTPSessionManager / StreamableHTTPServerTransport
      └─ optional Bearer auth, OAuth routes, request security middleware
```

## Files, grouped by responsibility

| Guide | Every source file covered |
|---|---|
| [FastMCP](fastmcp_knowledge.md) | `fastmcp/**` (17 files) |
| [Protocol and transports](core_server_knowledge.md) | package root, `lowlevel/**`, `session.py`, stdio/SSE/WebSocket/streamable HTTP, models, elicitation, validation, security (19 files) |
| [Authentication and experiments](auth_experimental_knowledge.md) | `auth/**` and `experimental/**` (23 files) |

Empty `__init__.py` files are recorded in their owning guide as namespace-only. No client, CLI, OS, or shared sibling package has been duplicated. The references do name direct imports from `mcp.types` and `mcp.shared`, because they supply wire models/session primitives, but they are outside this requested source root.

## Important execution boundaries

- **Registration vs serving:** FastMCP registrations are in-memory objects. Listing is metadata-only; tool/resource/prompt functions execute only at invocation/read/render time.
- **Protocol vs application validation:** the low-level server validates raw tool arguments by JSON Schema by default. FastMCP disables that specific check and performs richer Pydantic argument handling itself.
- **Transport vs session:** stdio gets one stream session; legacy SSE binds one POST message endpoint to a stream; streamable HTTP validates headers and can run stateful, resumable or stateless request handling.
- **Auth vs custom routes:** FastMCP protects MCP endpoints when configured, but `custom_route()` routes bypass its auth wrapper. Secure those routes yourself.

## Coverage method

The callable inventories in the three guides were mechanically extracted from the 59 parsed Python files, then checked against the explanations. Private functions are included where they change control flow, validation, serialization, or security.

