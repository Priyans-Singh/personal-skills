# `a2a_db_cli.py`: database migration CLI

Source: [a2a_db_cli.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/a2a_db_cli.py), a2a-sdk 1.1.4, inspected 2026-10-07. Distribution entry_points declares `a2a-db = a2a.a2a_db_cli:run_migrations`.

## Control flow

```text
console entrypoint → run_migrations → create_parser / parse_args
 → bundled alembic.ini + migrations script location
 → consolidate global/subcommand arguments
 → Config values / DATABASE_URL environment
 → alembic.command upgrade | downgrade | current
 → migrations/env.py → revision functions → database schema
```

No server request invokes this automatically. Import requires Alembic and raises installation guidance if absent; it does not run migration function at import. File has no `if __name__ == '__main__'` invocation, so executing `python -m a2a.a2a_db_cli` is not equivalent to installed console entrypoint.

## Every callable and arguments

`_add_shared_args(parser, is_sub=False) -> None` mutates ArgumentParser with --database-url, --tasks-table, --push-notification-configs-table, -v/--verbose store_true, --sql store_true. Subparser destinations prefix sub_; global ones do not. No database access occurs.

`create_parser() -> ArgumentParser`: top-level custom-owner flag `--add_columns_owner_last_updated-default-owner` dest owner; common arguments; optional subcommands: upgrade with revision default head plus its own sub_owner flag/common args; downgrade revision default base/common args; current/common args. Downgrade/current lack sub_owner. No cmd supplied is accepted. Revision syntax validation is delegated to Alembic later, not parser.

`run_migrations() -> None`: configures logging basicConfig(INFO), parses process arguments; absent cmd explicitly becomes upgrade/head, **a mutating default**. Finds bundled ini/scripts using importlib.resources.files('a2a'), sets script_location; consolidates owner/db URL/table flags as global_value OR sub_value, verbose/sql via logical OR. If same option is supplied both before/after subcommand, nonempty global value wins, not last occurrence across positions. Falsy explicit empty string is ignored by this consolidation.

Owner option becomes add_columns_owner_last_updated_default_owner Config key; database URL updates process os.environ['DATABASE_URL']; table names become Config keys; verbose becomes Config verbose='true'. Calls command.upgrade(cfg, revision, sql=sql), command.downgrade(...), or command.current(cfg, verbose=verbose), then logs Done. Errors propagate; there is no rollback/retry wrapper. --sql on current is parsed but not passed; current still uses Alembic's current operation, not SQL generation.

Config/server administration sees URL credentials for target DB; env mutation persists for subsequent calls within same process. No secret masking or credential refresh; do not log real command strings or store URLs in repo examples. importlib resource paths assume access usable by Alembic as filesystem paths; this source does not implement resource extraction for every exotic packaging mode.

## Usage (not executed)

After optional dependencies/driver and a deliberate baseline/schema review, console examples are `a2a-db current`, `a2a-db upgrade head --sql`, or targeted revision operation. No subcommand defaults to upgrade head. **Do not run bare CLI merely to discover help/status.** Use --help for parser-only output, current for deliberate read-only DB revision inspection.

Online operations use async-compatible SQLAlchemy URLs/drivers through env.py. `[db-cli]` alone does not install every selected DB driver. Existing tables only are modified by bundled revisions; absent target tables may be skipped while revision advances. Custom table names must agree with actual store configuration. Offline SQL requires DATABASE_URL and SQLAlchemy even though no target DB connection occurs.

Downgrade default base removes both bundled revisions; lost columns/data are not recreated by later upgrade. Use explicit revision range and validated backup/test environment for real administration. See [migrations reference](../a2a-migrations/README.md) for exact DDL and nullable defaults. Local validation used AST inspection, never imported or invoked Alembic commands because optional dependencies are absent.
