# Coverage and validation

Inspected a2a-sdk **1.1.4**, **2026-10-07**, source `.venv/lib/python3.11/site-packages/a2a/helpers`. Scope: **3 non-cache files and 29 AST declarations**, including private/nested/property definitions. Every source file maps to a behavioral guide; non-Python files are included in hashes and prose. Installed source remains unchanged.

[source_inventory.json](source_inventory.json) binds paths, SHA-256 hashes, guide mappings and declaration identity (lexical name, original line, AST kind). [callable_index_knowledge.md](callable_index_knowledge.md) includes signatures/source links; prose explains behavior rather than relying on name coverage or source docstrings alone.

Run from workspace root:

```sh
.venv/bin/python a2a-reference/validate_small_packages.py
```

Validator checks inventory/hash drift, exact declarations, per-file source sections, declaration mention in meaningful narrative, index entries, Markdown links/whitespace/fences. It does not import migration/CLI code or run external operations. Presence checks supplement manual source inspection, not replace semantic review.

Runtime evidence: local identity, extension parsing/card lookup, model aliases, and helper construction/extraction branches were checked without network services. Migration/Alembic/SQL integration was source-inspected only because Alembic/SQLAlchemy are absent; no DDL, engine connection or migration command was executed. Generated template callables are documented as template signatures, not runtime AST declarations. External service guarantees are not inferred from local code.
