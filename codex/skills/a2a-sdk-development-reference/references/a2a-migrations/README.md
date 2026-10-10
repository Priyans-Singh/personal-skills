# A2A migrations reference

Inspected a2a-sdk **1.1.4**, `.venv/lib/python3.11/site-packages/a2a/migrations`, 2026-10-07. This is the database **control plane**: schema DDL/revision administration, separate from runtime TaskStore CRUD.

- [Package and README](init_knowledge.md).
- [Environment and engine lifecycle](env_knowledge.md).
- [Every schema helper](migration_utils_knowledge.md).
- [Both revisions and nested initializer](versions_knowledge.md).
- [Revision generation template](script_template_knowledge.md).
- [Callable index](callable_index_knowledge.md), [coverage](coverage_knowledge.md).

CLI/parser/configuration are covered in [a2a-root](../a2a-root/README.md). No migrations were executed for this documentation; Alembic and SQLAlchemy are absent locally. Inspect target schema and test on a disposable copy before applying changes. Downgrades remove columns/indexes and can destroy data.
