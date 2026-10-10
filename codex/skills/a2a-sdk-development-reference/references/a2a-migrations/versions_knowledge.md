# Every revision under `versions/`

Sources: [versions/__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/__init__.py), [6419d2d130f6_add_columns_owner_last_updated.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/6419d2d130f6_add_columns_owner_last_updated.py), [38ce57e08137_add_column_protocol_version.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/38ce57e08137_add_column_protocol_version.py). Inspected 1.1.4, 2026-10-07.

Initializer is docstring-only, no callables or runtime dispatch. Alembic loads revision modules from script location and follows revision/down_revision values. Both revisions set branch_labels and depends_on to None. Their upgrade/downgrade functions take no arguments/return no result; they use active context configuration and helper DDL. They are not automatically run by runtime TaskStore saves.

## `6419d2d130f6_add_columns_owner_last_updated.py`

Base revision, down_revision=None. `upgrade` reads custom default owner (config key add_columns_owner_last_updated_default_owner; default legacy_v03_no_user_info), task table name (tasks) and config table name (push_notification_configs).

For existing Task table: add nullable owner String(255) with server default owner, nullable last_updated DateTime, index idx_<table>_owner_last_updated over [owner,last_updated]. For existing config table: add nullable owner String(255) with same default, index ix_<table>_owner over owner. Missing tables log warning and skip independently. Name-based helpers skip existing columns/indexes without checking compatible definitions.

`downgrade` reads same table names, drops Task composite index then owner and last_updated columns; drops config owner index then owner. Missing tables warn/skip. Owner/timestamp data is removed; no export/archive/backfill reversal. No foreign-key/primary-key changes occur.

The default legacy owner is **not** the default runtime anonymous owner (empty string). Inference from runtime owner filters: migrated legacy rows can become unreadable through default user scope unless the application intentionally maps/migrates ownership. It is not automatic per-user authorization repair. Empty timestamps remain empty; migration does not reconstruct status timestamps. Validate visibility and ownership policy separately.

## `38ce57e08137_add_column_protocol_version.py`

down_revision='6419d2d130f6'. `upgrade` resolves table names, adds nullable protocol_version String(16) to each existing table. No server default, row backfill, conversion of JSON payloads, or version inference. Missing tables warn/skip.

`downgrade` resolves same names and drops protocol_version where table exists. Data removed from that column; task/config JSON remains in its old representation. Default stores use protocol_version to choose parsing (`1.0` current protobuf JSON; other/null treated by legacy conversion), so removing marker from current-format rows can make later reads misinterpret data. Plan application compatibility around downgrade instead of assuming DDL rollback equals wire-data rollback.

## Safe command pattern (documentation only)

Use CLI `current` to inspect history, compare actual table schema, generate/review offline SQL when useful, then apply chosen upgrade against a disposable copy before production administration. Revision table can advance even when target tables were absent/skipped; explicitly verify columns/indexes after migration. Never use revision history alone as schema conformance proof. See root CLI guide for flag precedence and default action.
