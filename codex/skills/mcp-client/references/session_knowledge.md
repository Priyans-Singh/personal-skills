# `mcp.client.session`: application session

Source inspected: MCP 1.30.0. `ClientSession` sits over transport-provided AnyIO memory streams. `BaseSession` assigns JSON-RPC IDs, routes responses, supports progress/cancellation, and runs a receive task when context-entered. Always `async with ClientSession(read, write)` then `await initialize()`.

## Construction and handshake

`ClientSession(read_stream, write_stream, read_timeout_seconds=None, sampling_callback=None, elicitation_callback=None, list_roots_callback=None, logging_callback=None, message_handler=None, client_info=None, *, sampling_capabilities=None, experimental_task_handlers=None)` stores callbacks and delegates stream machinery to BaseSession. Default client info is `mcp/0.1.0`; default sampling, elicitation, and roots callbacks return `ErrorData(INVALID_REQUEST)`; logging ignores; generic message handling checkpoints. Callback presence advertises matching capability during `initialize`. Supplying experimental handlers emits a deprecation warning.

`initialize()` sends `initialize` with latest protocol/version/capabilities, rejects an unsupported server version with `RuntimeError`, caches server capabilities, then sends `notifications/initialized`. `get_server_capabilities()` is `None` before that. Server requests become `RequestContext`; callback results are Pydantic-validated before responding. Exceptions from application callbacks are not converted to friendly results—return `ErrorData` for expected failures.

## Outbound API

Every request can raise `McpError` for JSON-RPC errors, Pydantic validation failures, or connection/timeout errors. Per-call `read_timeout_seconds` (`timedelta`) overrides the session timeout.

- `send_ping()` and `set_logging_level(level)` return `EmptyResult`.
- `send_progress_notification(token, progress, total=None, message=None)` is one-way.
- `list_resources`, `list_resource_templates`, `list_prompts`, and `list_tools` accept deprecated positional `cursor` or `params=PaginatedRequestParams`, never both (`ValueError`); no auto-pagination. `list_tools` caches output schemas.
- `read_resource(uri)`, `subscribe_resource(uri)`, `unsubscribe_resource(uri)` use validated `AnyUrl`.
- `call_tool(name, arguments=None, read_timeout_seconds=None, progress_callback=None, *, meta=None)` sends JSON mapping arguments. A progress callback injects `_meta.progressToken`; successful structured output is locally JSON-Schema validated when the tool was listed with `outputSchema`. Missing required structured content or invalid schema/content raises `RuntimeError`.
- `get_prompt(name, arguments: dict[str,str]|None)`, `complete(ref, argument, context_arguments=None)`, and `send_roots_list_changed()` map directly to their MCP methods.

Incoming sampling/elicitation with task metadata is diverted to experimental task handlers; otherwise `_received_request` calls the regular callback. `_received_notification` calls logging callback for logging notifications; `_handle_incoming` passes remaining requests, notifications, and exceptions to `message_handler`.

`experimental` lazily returns a cached deprecated `ExperimentalClientFeatures` facade.

Callable index: protocols `SamplingFnT`, `ElicitationFnT`, `ListRootsFnT`, `LoggingFnT`, `MessageHandlerFnT`; five `_default_*` callbacks; `ClientSession.__init__`, `initialize`, `get_server_capabilities`, `experimental`, `send_ping`, `send_progress_notification`, `set_logging_level`, list/read/subscribe/unsubscribe methods, `call_tool`, `_validate_tool_result`, `get_prompt`, `complete`, `send_roots_list_changed`, `_received_request`, `_received_notification`, `_handle_incoming`.

Literal callback names: each protocol defines `__call__`; defaults are `_default_message_handler`, `_default_sampling_callback`, `_default_elicitation_callback`, `_default_list_roots_callback`, and `_default_logging_callback`.
