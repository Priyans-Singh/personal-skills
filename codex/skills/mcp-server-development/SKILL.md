---
name: mcp-server-development
description: "Build, modify, debug, or review Python MCP servers using the installed MCP SDK. Use for FastMCP tools, resources, prompts, transports, sessions, and server authentication; not MCP client-only work."
---

# MCP Server Development

Build server-side MCP functionality using `mcp.server.fastmcp.FastMCP` by default. Use the low-level `mcp.server.lowlevel.Server` only when the task needs raw protocol handler registration, lifecycle ownership, or custom transport/session control.

## Normal server work

- Register tools with `@mcp.tool()`, resources with `@mcp.resource()`, and prompts with `@mcp.prompt()`; do not use bare decorator forms.
- Treat Python type hints as the tool schema contract and docstrings as the client-facing description. Preserve a `Context` parameter when the tool needs progress, client logging, resource reads, elicitation, or session access.
- Use stdio by default unless the user asks for a web deployment. Prefer streamable HTTP for new HTTP servers; SSE is legacy and WebSocket is deprecated.
- Keep registration in process memory unless the user asks for persistence. Be deliberate about duplicate names: tools/resources/prompts retain an existing registration; templates replace one.

Read [FastMCP reference](references/fastmcp_knowledge.md) for tools, schemas, resources, prompts, and application mounting. Read [core server reference](references/core_server_knowledge.md) when changing lifecycle, low-level handlers, sessions, transports, protocol validation, or transport security.

## Security-sensitive work

Read [auth and experimental reference](references/auth_experimental_knowledge.md) before adding OAuth, bearer auth, authorization, protected-resource metadata, session binding, or experimental tasks.

- Do not assume FastMCP custom routes inherit MCP endpoint authentication; protect them explicitly when needed.
- Do not invent token persistence, audience/resource validation, or OAuth callback behavior: provider implementation owns those guarantees.
- Treat absolute-path file/directory resources and HTTP resources as explicit data-access/network boundaries; add application-level restrictions only when requested or warranted by the task.
- Do not introduce experimental task APIs unless the user explicitly accepts their deprecated/unstable status.

## Reference scope

The references are source-grounded to MCP Python SDK 1.30.0, the installed v1 maintenance line. Confirm installed source/version before relying on version-specific behavior; do not silently apply these v1 details to MCP v2.
