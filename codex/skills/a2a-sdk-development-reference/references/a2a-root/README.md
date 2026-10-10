# Loose A2A package-root files

Inspected a2a-sdk **1.1.4**, package `.venv/lib/python3.11/site-packages/a2a`, 2026-10-07. This complements per-folder guides; excludes existing server/client work.

- [_base.py model configuration](base_knowledge.md).
- [a2a_db_cli.py command control plane](a2a_db_cli_knowledge.md).
- [alembic.ini and py.typed](support_files_knowledge.md).
- [Callable index](callable_index_knowledge.md), [coverage](coverage_knowledge.md).

No root __init__.py exists in this installation: a2a is a namespace package, with actual APIs in subpackages. Bytecode cache is interpreter output, not a separate library module. See [all-package navigation](../a2a-reference/README.md).
