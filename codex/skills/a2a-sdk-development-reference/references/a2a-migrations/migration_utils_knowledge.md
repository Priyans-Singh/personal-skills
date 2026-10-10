# `migration_utils.py`: conditional schema operations

Source: [migration_utils.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py), a2a-sdk 1.1.4, 2026-10-07.

Helpers run inside Alembic context. SQLAlchemy import is unconditional; guarded Alembic import gives installation guidance if absent. They neither establish their own transaction nor create a database engine. Exceptions from reflection/DDL propagate; no retry/backoff or error swallowing.

| Callable | Online behavior | Offline behavior |
|---|---|---|
| `_get_inspector()` | op.get_bind → sa.inspect(bind) | Not normally called by existence helpers |
| `table_exists(table_name)` | Reflect table names, exact membership | Always True |
| `column_exists(table_name,column_name,downgrade_mode=False)` | Reflect column names, exact membership | Returns downgrade_mode |
| `index_exists(table_name,index_name,downgrade_mode=False)` | Reflect index names, exact membership | Returns downgrade_mode |
| `add_column(table,column_name,nullable,type_,default=None)` | If absent, op.add_column(sa.Column(... server_default=default)); else info log | Assumes absent, emits addition |
| `drop_column(table,column_name)` | If present, op.drop_column; else info log | Uses downgrade_mode=True, emits drop |
| `add_index(table,index_name,columns)` | If absent, op.create_index; else info log | Assumes absent, emits creation |
| `drop_index(table,index_name)` | If present, op.drop_index(index_name,table_name=table); else info log | Uses downgrade_mode=True, emits drop |

Existence is checked by **name only**, not type/nullability/default/index column compatibility. Existing incompatible column/index is skipped, not repaired. Repeated helpers create fresh inspectors; no cache. Reflection can fail for nonexistent table if called without table_exists gating; revisions supply that gate. Concurrent administrators can race check-then-DDL; no lock or atomic “if absent” guarantee is supplied.

default is a SQL server_default supplied to Column, not an application-only Python default. Backend behavior determines existing-row values and default persistence. Source leaves server defaults installed; there is no subsequent removal/backfill validation. Column nullable flags and SQLAlchemy type inputs are forwarded unchanged. These helpers don't sanitize custom identifiers independently; delegate identifier quoting/DDL compilation to SQLAlchemy/Alembic.

Use these for controlled revision functions, not user-facing task requests. Offline output must be reviewed against actual schema because all tables are assumed to exist. Downgrade removes data-bearing columns; inspect rollback scope and backup first. The source cannot establish that a transaction will undo each DDL statement on your database.
