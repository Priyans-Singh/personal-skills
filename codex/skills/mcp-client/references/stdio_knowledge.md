# `mcp.client.stdio`: subprocess transport

Source inspected: MCP 1.30.0, `stdio/__init__.py`. It starts a local server and transports newline-delimited JSON-RPC over stdin/stdout; it does not initialize a `ClientSession` itself.

`StdioServerParameters(command, args=[], env=None, cwd=None, encoding="utf-8", encoding_error_handler="strict")` is Pydantic configuration. `command` is executable only—there is no shell—so use tokenized `args`. `env=None` inherits a small safe platform allowlist; an explicit mapping overlays it, it does not replace it. Supply secrets explicitly. `strict` decoding is safest because ignore/replace can corrupt protocol framing.

`stdio_client(server, errlog=sys.stderr)` yields unbuffered `(read_stream, write_stream)`. It launches `[command, *args]` (POSIX new session), runs `stdout_reader` and `stdin_writer` concurrently, and forwards child stderr solely to `errlog`. Writer dumps aliases/excludes None, appends one newline, and sends bytes to stdin. Reader decodes chunks, parses only complete newline-separated JSON lines to `SessionMessage`, and emits parse exceptions but continues. A final frame without newline is dropped; server logs must never be stdout.

Exit closes stdin, waits 2 seconds, then `_terminate_process_tree` kills process groups/tree (POSIX TERM then possible KILL; Windows job object when available). Spawn `OSError` closes channel endpoints and re-raises. `_get_executable_command` does Windows extension lookup; `_create_platform_compatible_process` selects Windows/AnyIO POSIX spawn.

Callable index: `get_default_environment`, `StdioServerParameters`, `stdio_client`, nested `stdout_reader`/`stdin_writer`, `_get_executable_command`, `_create_platform_compatible_process`, `_terminate_process_tree`.
