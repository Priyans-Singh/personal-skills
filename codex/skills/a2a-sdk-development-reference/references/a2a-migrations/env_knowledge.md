# `env.py`: Alembic setup and engine lifecycle

Source: [env.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/env.py), a2a-sdk 1.1.4, 2026-10-07.

## Import-time execution

Imports SQLAlchemy, async engine creation, server.models.Base, then Alembic context. Optional dependencies can fail before the friendly Alembic ImportError message because SQLAlchemy/server models import first. Requires active Alembic context; ordinary application import is not a side-effect-free config read.

Module body takes context.config, reads DATABASE_URL, raises RuntimeError if absent, puts it in sqlalchemy.url, loads logging via fileConfig when config file exists and ends .ini, optionally raises sqlalchemy.engine logger to INFO, sets target_metadata=Base.metadata and VERSION_TABLE='a2a_alembic_version'. It immediately chooses offline or online function based on context.is_offline_mode().

Connection URL is consumed by SQLAlchemy to reach the configured database, not A2A message transport. Online engine lifetime is one command. No token refresh, secret-manager lookup or masking implementation lives here. Verbose SQL logs may expose application data; use controlled logs and avoid echoing URLs.

## Every callable

`run_migrations_offline() -> None`: reads configured URL; context.configure(url, target_metadata, literal_binds=True, dialect_opts paramstyle='named', dedicated version_table); begins Alembic transaction and runs revisions. Does not create an Engine/connect to target. Existence helpers synthesize assumptions rather than inspect database, so emitted SQL is not proof target objects exist.

`do_run_migrations(connection: Connection) -> None`: synchronous callback passed to AsyncConnection.run_sync. Configures Alembic with actual sync connection, metadata and dedicated version table; begins transaction and runs migrations. Does not create/dispose connection. Revision/helper exceptions propagate.

`run_async_migrations() -> None`: builds AsyncEngine from config section, prefix sqlalchemy., poolclass NullPool; opens connection in async context; awaits connection.run_sync(do_run_migrations), then engine.dispose. Disposal occurs after successful context exit, not inside finally; a failure before that line can skip explicit disposal. Connection context still handles its normal close semantics. No retry, parallelism or long-lived pool.

`run_migrations_online() -> None`: asyncio.run(run_async_migrations()). It owns an event loop and is unsuitable for direct invocation in an already running loop; programmatic integrations should follow their own async orchestration rather than import env.py into an agent callback.

## Consistency and integration

Alembic transaction scope surrounds revisions, but transactional DDL/rollback behavior depends on database/dialect and cannot be guaranteed by this local code. NullPool avoids retained connection pool between CLI operations. Online inspector calls use Alembic op.get_bind on this migration connection. Base.metadata enables autogeneration but installed revision functions determine actual changes. Custom table names are supplied through config; changing table flags alone does not make metadata factories/autogeneration magically target custom models.

Practices: run from a dedicated administration process, explicitly select tested driver/URL, set controlled logging, verify revision plus resulting schema, and handle failure/resource disposal in any custom runner. No live database call was performed during inspection.
