# `script.py.mako`: generation template

Source: [script.py.mako](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/script.py.mako). Not importable Python until Alembic/Mako substitutes placeholders.

Template produces revision docstring with message/IDs/date; imports Sequence/Union, sqlalchemy and guarded alembic.op; emits additional generated imports; fills revision/down_revision/branch_labels/depends_on; creates upgrade and downgrade functions containing generated bodies or `pass`. These two function declarations are template signatures, not callable implementations in the installed runtime; generated revisions are covered separately by AST index.

The template changes no schema by being present. Autogeneration compares configured metadata/database through Alembic, renders candidate code using this template, and writes a revision. Review candidate DDL manually: no automatic correctness check, data migration plan, safe downgrade validation, retry or provider guarantee comes from placeholders. Imported metadata and custom table mappings must match intended schema. The CLI bundled here exposes upgrade/downgrade/current, not revision generation; contributor autogeneration uses Alembic tooling separately. No revision was generated during this task.
