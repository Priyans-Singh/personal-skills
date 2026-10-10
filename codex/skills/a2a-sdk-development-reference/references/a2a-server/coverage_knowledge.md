# Coverage and validation record

Inspected 2026-10-07: a2a-sdk 1.1.4, Python 3.11, source `../.venv/lib/python3.11/site-packages/a2a/server/`. The unrelated legacy PyPI a2a distribution is not installed. Primary inventory: **48 Python files, 9,123 source lines, 422 AST declarations** including classes, functions, methods, properties/setters, conditional definitions and nested callbacks/wrappers. Bytecode cache is excluded; no other non-cache files were found in server.

## Evidence artifacts

- [source_inventory.json](source_inventory.json) contains every primary file, SHA-256, mapped narrative guide, and declaration's lexical name, original line, AST kind. Hashes bind claims to this inspected installation.
- [callable_index_knowledge.md](callable_index_knowledge.md) records each declaration with exact signature, source line link, source-docstring summary where available, and linked behavioral chapter. No-callable files remain included.
- [validate_reference.py](validate_reference.py) checks source-file set/hashes, declaration set, per-file narrative source sections, exact declaration markers, local Markdown links, whitespace, balanced fences, and example syntax. It does not overwrite source or regenerate evidence.

All primary implementation files were inspected through actual function bodies; source docstrings were separately available. Narrative chapters trace distinct operations and non-obvious behavior rather than relying on the generated index. The index exposes potentially misleading source docstrings without treating them as verified facts; narrative explicitly records cancellation order, TASK_STATE_FAILED, ignored queue_manager, and other implementation differences.

## Primary source map

| Directory | Python files | Behavioral chapter |
|---|---:|---|
| Root | 6 | init/context/id_generator/jsonrpc_models/models/owner_resolver guides |
| agent_execution | 7 | agent_execution_knowledge.md |
| events | 6 | events_knowledge.md |
| request_handlers | 6 | request_handlers_knowledge.md |
| routes | 10 | routes_knowledge.md |
| tasks | 13 | tasks_knowledge.md |

Each chapter identifies every contained file, including __init__.py and private schema helpers. Direct supporting package imports and their execution roles are documented in [dependencies_knowledge.md](dependencies_knowledge.md): auth user, extension parsing, protobuf helpers/types/generated service, queue compatibility, validation, errors, JSON, telemetry, protocol versions, and v0.3 adapters/converters. Supporting scope is deliberately the server-facing integration boundary; it is not a second complete guide to all sibling client/compatibility packages. Optional push URL validator is additionally included for usage guidance.

## Runtime checks completed

The local example was executed through httpx.ASGITransport, with app lifespan entered/exited. No socket server, external HTTP call, DNS resolution, database/cloud resource, or package installation was needed.

Passed:

1. Public Agent Card discovery.
2. REST send returns COMPLETED Task with matching Unicode echo artifact.
3. Explicit historyLength=0 trims response; subsequent untrimmed read preserves stored history.
4. ListTasks returns owned task count.
5. JSON-RPC SendMessage returns task result envelope.
6. SSE stream includes artifactUpdate and raw UTF-8 output.
7. Current REST request without version header rejects legacy default version with HTTP400.
8. Different owner cannot read anonymous owner's Task through handler.
9. Handler lifecycle shutdown completes.

These are focused example checks, not a comprehensive SDK conformance, race, cancellation, or distributed deployment test suite. Structural coverage validation supplements manual inspection; presence of a name does not prove that every possible behavior was tested.

## Known runtime limits

FastAPI, grpcio and SQLAlchemy are absent in this .venv. Their source was inspected; OpenAPI generation, gRPC transport, SQL driver/database behavior and encryption-at-rest database integration were not executed. Webhook behavior was traced in source, without posting to any destination. No claim of external database isolation/durability, credential validity, DNS safety over time, proxy SSE behavior, or remote delivery reliability follows from these checks.

When upgrading the SDK, run validate_reference.py. A failed source hash/declaration check means this reference may need reinspection, not that your application is broken. Preserve the stable architecture concepts but retrace changed implementations and verify optional integration paths in their target environment.
