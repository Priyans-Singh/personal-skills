# `mcp.client.__main__`

Source inspected: MCP 1.30.0. This is the `python -m mcp.client` connectivity CLI, not a general interactive MCP shell.

`cli()` parses `COMMAND_OR_URL [ARGS…]` plus repeatable `-e/--env KEY VALUE`, then calls `anyio.run(partial(main, ...), backend="trio")`. `main(command_or_url, args, env)` treats only `http`/`https` URLs as legacy `sse_client` endpoints; every other value becomes `StdioServerParameters(command=…, args=…, env=dict(env))`. It opens that transport and passes its streams to `run_session`.

`run_session(read_stream, write_stream, client_info=None)` context-manages `ClientSession`, installs `message_handler`, then only calls `initialize()`. `message_handler(message)` logs exceptions as errors and all other server messages as info. No tool listing/calling occurs. Warnings are suppressed when Python was not configured with warning options.

Use it for a quick handshake: `python -m mcp.client python server.py -e API_KEY value`. The environment applies only to stdio; URL arguments after the URL are not HTTP configuration. Invalid CLI syntax exits through argparse; transport/session failures propagate through AnyIO.

Callable index: `message_handler`, `run_session`, `main`, `cli`.
