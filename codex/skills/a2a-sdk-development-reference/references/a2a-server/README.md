# A2A server reference

Source-grounded deep dive into the installed **a2a-sdk 1.1.4** server, inspected **2026-10-07**.

Start with [overview_knowledge.md](overview_knowledge.md). It links one guide per root file and per server folder. Read [usage_knowledge.md](usage_knowledge.md) for examples and best practices, [callable_index_knowledge.md](callable_index_knowledge.md) for every declaration, and [coverage_knowledge.md](coverage_knowledge.md) for validation and limits.

The primary source has **48 Python files and 422 declarations** (classes, functions, methods, properties/setters, conditional definitions, and nested helpers). Documentation covers execution, transport adapters, persistence, authorization, queues, cancellation, notifications, errors, and direct implementation dependencies.

Run the reference checks from the workspace root:

```sh
.venv/bin/python a2a-server/validate_reference.py
```

[Starlette example](examples/starlette_server.py) is locally checked through in-process ASGI requests. FastAPI, SQL and gRPC code was inspected but cannot be runtime-tested in this environment without its absent optional dependencies. No installed library files were changed.
