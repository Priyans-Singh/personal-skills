# Migration package and bundled README

Sources: [__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/__init__.py), [README.md](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/README.md). a2a-sdk 1.1.4, 2026-10-07.

Initializer contains only a package docstring, no callable/export/engine. Importing this initializer is different from executing env.py, whose module body starts migration dispatch.

Bundled README documents CLI extras, DATABASE_URL/custom table/default-owner options, SQL generation, upgrade/downgrade/current and contributor autogeneration. Read it as usage context, then follow implementation: installed revisions **modify existing tables**, they do not create the baseline Task/config tables. README prose mainly describes owner/last_updated revision; installed second revision also adds protocol_version.

Revision hierarchy:

```text
base → 6419d2d130f6 (owner / timestamp / indexes)
     → 38ce57e08137 (protocol_version on both tables) → head
```

Database history uses dedicated a2a_alembic_version table. Schema state and revision stamp are separate: conditional skipping of missing target tables can still allow Alembic revision advancement. A successful upgrade/log is not proof every target table received changes. Determine the correct baseline and table names before execution.

Use async-compatible URLs/drivers for online path. CLI `[db-cli]` supplies Alembic, not necessarily your selected SQL async driver. The bundled generic URL snippets are illustrative; e.g. SQLite requires its own file URL shape rather than user/host credentials. Do not put real connection credentials in committed docs or logs. Offline SQL generation avoids target DB access but still imports SQLAlchemy/server models and requires a DATABASE_URL.
