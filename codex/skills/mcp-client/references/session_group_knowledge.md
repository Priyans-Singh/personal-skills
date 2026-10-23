# `mcp.client.session_group`: multi-server aggregation

Source inspected: MCP 1.30.0. `ClientSessionGroup` owns/uses an async exit stack, establishes sessions, then exposes aggregate mutable dictionaries `prompts`, `resources`, `tools`; `sessions` is a list snapshot. Use `component_name_hook(name, server_info)` to namespace before aggregation; duplicate aggregate names raise `McpError(INVALID_PARAMS)`.

Configuration models: `SseServerParameters(url, headers=None, timeout=5, sse_read_timeout=300)`, `StreamableHttpParameters(url, headers=None, timeout=30s, sse_read_timeout=300s, terminate_on_close=True)`, and stdio parameters. `ClientSessionParameters` carries ClientSession timeouts/callbacks/info.

`connect_to_server` selects transport, creates client/session, initializes it, then aggregates. `connect_with_session` aggregates an existing initialized session. `_aggregate_components` lists prompts/resources/tools independently; each `McpError` logs and does not prevent other component families. It builds temporary maps then commits only after collision checks. `call_tool` looks up aggregate name and delegates to owning session; deprecated `args` overrides `arguments`; unknown name is `KeyError`. `disconnect_from_server` removes reverse-indexed components and closes its stack; unmanaged session raises `McpError`.

Callable index: `SseServerParameters`, `StreamableHttpParameters`, `ClientSessionParameters`, `ClientSessionGroup`, `_ComponentNames`, constructor/context lifecycle, properties, `call_tool`, disconnect/connect methods, `_establish_session`, `_aggregate_components`, `_component_name`.

Lifecycle names: `__init__`, `__aenter__`, `__aexit__`.
