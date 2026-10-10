# `mcp.server.fastmcp` deep dive

Source root: `.venv/lib/python3.11/site-packages/mcp/server/fastmcp`; MCP **1.30.0**. This is the high-level server authoring layer, not an independent protocol implementation.

## End-to-end tool call

1. `@mcp.tool()` calls `ToolManager.add_tool`, which builds a `Tool` from the Python callable.
2. `Tool.from_function` validates/warns about the tool name, identifies an annotated `Context` parameter, inspects type hints, and builds a Pydantic argument model plus optional output schema.
3. FastMCP wires `list_tools` / `call_tool` into its owned low-level `Server`. The low-level layer accepts an MCP request; FastMCP creates a `Context` backed by that request context.
4. `Tool.run` pre-parses JSON-shaped string arguments where appropriate, Pydantic-validates them, injects `Context`, invokes or awaits the function, then converts the result to MCP content and optional structured content.
5. Errors other than URL-elicitation-required become `ToolError`; the low-level handler serializes that to the MCP result/error path.

## Package surface and server

`__init__.py` exports `FastMCP`, `Context`, `Image`, `Audio`, and wire-model `Icon`; it derives `__version__` from installed package metadata. `exceptions.py` contains `FastMCPError`, `ValidationError`, `ResourceError`, `ToolError`, plus `InvalidSignature` for callable/schema inspection failures.

`server.py` is the composition root.

- `Settings(BaseSettings)` reads `FASTMCP_` environment values (`__` nests fields), ignores unknown environment keys, and stores host/paths, logging, JSON response, state/session limits, duplicate policies, auth/security configuration and dependencies. Dependencies are merely retained; this module never installs them.
- `lifespan_wrapper` adapts a FastMCP async context manager to the low-level server lifespan signature.
- `FastMCP.__init__` builds `Settings`, a low-level server, the three memory-backed managers, optional auth verifier/provider and transport state. Auth settings require exactly one of authorization provider or token verifier. A provider is wrapped in `ProviderTokenVerifier` for compatibility. Localhost automatically gets DNS-rebinding protection unless explicitly overridden.
- Metadata properties proxy the low-level server. `session_manager` raises `RuntimeError` until `streamable_http_app()` creates it.
- `run` selects `stdio`, legacy `sse`, or `streamable-http` and starts AnyIO. Unknown names raise `ValueError`.
- `_setup_handlers` registers tools, resource/resource-template list/read, and prompt list/get handlers. It deliberately sets low-level tool argument validation aside: FastMCP owns that work.

### Public registration and access methods

`list_tools`, `list_resources`, `list_resource_templates`, and `list_prompts` serialize manager entries into MCP wire models. `call_tool` makes the request `Context` and delegates; `read_resource` resolves resource/template then returns one `ReadResourceContents`; resource exceptions are logged and raised as `ResourceError`. `get_prompt` renders and JSON-normalizes messages; unknown/render failures surface as `ValueError`.

`add_tool` / `remove_tool`, `add_resource`, and `add_prompt` delegate to their managers. `tool()`, `resource()`, and `prompt()` return decorators and reject bare decorator use (`@mcp.tool`, etc.). `completion()` delegates to the low-level completion registration decorator. `resource()` chooses a template when URI placeholders exist or the function takes arguments; for templates its URI field names must exactly equal non-Context parameter names. `custom_route()` stores a raw Starlette route and is intentionally outside FastMCP’s auth protection.

`run_stdio_async` connects `stdio_server()` to low-level `.run`. `run_sse_async` / `run_streamable_http_async` serve generated Starlette applications through Uvicorn. `_normalize_path` combines mount and endpoint path. `sse_app` builds SSE GET and message POST routes; `streamable_http_app` lazily creates the session manager and runs it through app lifespan. Both install body/security middleware and, when configured, bearer auth, OAuth authorization routes, and protected-resource metadata. `StreamableHTTPASGIApp` simply delegates ASGI calls to its manager.

`Context` exposes the current request only while handling a request (`fastmcp` / `request_context` otherwise raise `ValueError`). It provides session access, request/client IDs, progress notification, resource read, elicitation, client logging, and level wrappers. Progress is a no-op without a client progress token. `client_id` is request `_meta`, not an OAuth identity. `close_sse_stream` methods are no-ops without callbacks; standalone reconnection close remains unimplemented. The `extra` accepted by level wrappers is not forwarded by `log`.

## Tools (`tools/`)

`tools/__init__.py` re-exports `Tool` and `ToolManager`.

- `base.py — Tool`: Pydantic record of callable, name/title/description, argument schema, `FuncMetadata`, async flag, context parameter, annotations/icons/meta. `output_schema` is cached. `from_function` rejects unnamed lambdas and derives schema; `run` validates/injects/calls/converts. It preserves `UrlElicitationRequiredError`, wrapping all other exceptions in `ToolError`. `_is_async_callable` unwraps `functools.partial` and recognises coroutine functions or async `__call__`.
- `tool_manager.py — ToolManager`: insertion-ordered name map. Initial duplicate entries overwrite with optional warning; later `add_tool` retains the old registration on a duplicate. `get_tool`, `list_tools`, `remove_tool` (unknown -> `ToolError`) and `call_tool` are straightforward delegates. There is no persistence, lock, transaction, or retry.

## Resources (`resources/`)

`resources/__init__.py` re-exports `Resource`, manager/template and six concrete resources.

- `base.py — Resource`: abstract Pydantic resource with URI, name/title/description, MIME type, icons, annotations and `_meta`; validates MIME syntax, defaults name from URI, and requires async `read -> str | bytes`.
- `types.py — TextResource` / `BinaryResource`: return stored text/bytes. `FunctionResource` lazily calls/awaits a zero-arg function, recursively reads a returned Resource, passes text/bytes, otherwise pretty-JSON serializes; exceptions become `ValueError`. Its factory applies `validate_call`. `FileResource` requires an absolute path and reads in an AnyIO worker thread; non-`text/*` MIME infers binary. `HttpResource` makes a new `httpx.AsyncClient` GET, raises status errors, returns text. `DirectoryResource` requires an absolute directory, `glob`/`rglob`s optional pattern in a worker thread, and returns a formatted JSON list of relative regular files.
- `templates.py — ResourceTemplate`: holds a URI template and callable/schema/context metadata. `from_function` derives Pydantic schema; `matches` turns `{field}` segments into non-slash regex captures. `create_resource` injects context and invokes/awaits the template callable, then captures the resolved value inside a transient `FunctionResource`; conversion happens when that resource is read.
- `resource_manager.py — ResourceManager`: concrete URI map plus template-string map. Exact concrete URI wins; otherwise first matching template creates a transient resource. Duplicate concrete resources keep the original (optional warning); templates overwrite. Unknown URI raises `ValueError`; generated template results are never stored.

## Prompts (`prompts/`)

`prompts/__init__.py` exports `Prompt` and `PromptManager`; `Message`, `UserMessage`, `AssistantMessage`, and `PromptArgument` remain importable from `base.py`.

- `base.py — Message`: user/assistant role plus MCP content; strings become `TextContent`. Role subclasses default their respective roles. `Prompt.from_function` discovers context, turns schema properties/required names into `PromptArgument`s, wraps function with `validate_call`, and uses docstring as default description. `render` checks required names, injects context, invokes/awaits, and normalizes: Message unchanged; dict is validated; string becomes user text; other values pretty-JSON become user text. Any failure is a contextual `ValueError`.
- `manager.py — PromptManager`: in-memory name map; duplicates preserve existing prompt with optional warning. `get_prompt`, `list_prompts`, `add_prompt`, `render_prompt` resolve/delegate; unknown names error.

## Utilities (`utilities/`)

`__init__.py` only documents the namespace.

- `context_injection.py`: `find_context_parameter` resolves type hints and finds a direct/generic/union `Context`; unresolved hints silently mean none. `inject_context` merges context only if a detected name and non-null context exist.
- `func_metadata.py`: `StrictJsonSchema` escalates Pydantic schema warnings. `ArgModelBase.model_dump_one_level` preserves direct model values and aliases. `FuncMetadata` pre-parses suitable JSON strings, validates arguments, calls/awaits, and converts output. Existing `CallToolResult` stays a result but structured content is checked; otherwise content becomes MCP blocks. `func_metadata` dynamically creates argument/output models, rejects unresolved/private signatures, supports BaseModel, TypedDict, annotated classes/dataclasses, scalar/list/union/map returns, and handles `CallToolResult` specially. `_inline_root_ref`, `_try_create_model_and_schema`, and four `_create_*model*` helpers make MCP-compatible output schemas. `_convert_to_content` maps `None`, content blocks, Image/Audio, recursive sequences, strings and JSONable values.
- `types.py`: `Image` and `Audio` require exactly one file path or raw data; MIME is explicit, inferred, or fallback octet-stream. Conversion synchronously reads files, base64 encodes and returns wire content.
- `logging.py`: `get_logger` is stdlib logging. `configure_logging` selects Rich’s stderr handler when installed, otherwise standard stream, then calls global `logging.basicConfig`.

## Safe operating conclusions

Function resources/templates and tools execute arbitrary registered application code. File/directory resources allow any absolute local path; HTTP resources issue outbound GETs with no API-level timeout/headers/auth policy. Registries are process-local. Treat duplicate registration behaviour as a potential configuration bug: tools/resources/prompts keep the first, templates replace.

