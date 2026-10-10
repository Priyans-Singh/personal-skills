# A2A auth reference

Inspected a2a-sdk **1.1.4** in `.venv/lib/python3.11/site-packages/a2a/auth`, 2026-10-07. This tiny package defines an identity interface; it does not implement OAuth, credential validation, or an authentication server.

- [Initializer](init_knowledge.md): import surface.
- [Identity objects and usage](user_knowledge.md): every class/property, integration and ownership implications.
- [Callable index](callable_index_knowledge.md) and [coverage](coverage_knowledge.md): source inventory and verification.

See [server call context](../a2a-server/context_knowledge.md) for where identity enters execution; server/client guides are existing references, not new inspection scope.
