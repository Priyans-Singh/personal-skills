# Complete source and callable index

AST inventory includes classes, functions, properties, methods, conditional definitions and nested helpers. Signature/source-docstring summaries are supplementary evidence: manually written behavioral guides explain actual execution. Non-Python files are inventoried and linked even though they have no runtime AST callables.

## `README.md`

Behavior: [init_knowledge.md](init_knowledge.md). Source: [README.md](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/README.md).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

## `__init__.py`

Behavior: [init_knowledge.md](init_knowledge.md). Source: [__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/__init__.py).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

## `env.py`

Behavior: [env_knowledge.md](env_knowledge.md). Source: [env.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/env.py).

<!-- declaration:env.py:54:run_migrations_offline -->
### `run_migrations_offline`

```python
def run_migrations_offline() -> None
```

Source: [run_migrations_offline](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/env.py:54). Source-docstring summary: Run migrations in 'offline' mode.

<!-- declaration:env.py:79:do_run_migrations -->
### `do_run_migrations`

```python
def do_run_migrations(connection: Connection) -> None
```

Source: [do_run_migrations](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/env.py:79). Source-docstring summary: Run migrations in 'online' mode.

<!-- declaration:env.py:99:run_async_migrations -->
### `run_async_migrations`

```python
async def run_async_migrations() -> None
```

Source: [run_async_migrations](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/env.py:99). Source-docstring summary: Run migrations using an Engine.

<!-- declaration:env.py:117:run_migrations_online -->
### `run_migrations_online`

```python
def run_migrations_online() -> None
```

Source: [run_migrations_online](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/env.py:117). Source-docstring summary: Run migrations in 'online' mode.

## `migration_utils.py`

Behavior: [migration_utils_knowledge.md](migration_utils_knowledge.md). Source: [migration_utils.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py).

<!-- declaration:migration_utils.py:16:_get_inspector -->
### `_get_inspector`

```python
def _get_inspector() -> sa.engine.reflection.Inspector
```

Source: [_get_inspector](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:16). Source-docstring summary: Get the current database inspector.

<!-- declaration:migration_utils.py:23:table_exists -->
### `table_exists`

```python
def table_exists(table_name: str) -> bool
```

Source: [table_exists](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:23). Source-docstring summary: Check if a table exists in the database.

<!-- declaration:migration_utils.py:31:column_exists -->
### `column_exists`

```python
def column_exists(table_name: str, column_name: str, downgrade_mode: bool=False) -> bool
```

Source: [column_exists](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:31). Source-docstring summary: Check if a column exists in a table.

<!-- declaration:migration_utils.py:43:index_exists -->
### `index_exists`

```python
def index_exists(table_name: str, index_name: str, downgrade_mode: bool=False) -> bool
```

Source: [index_exists](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:43). Source-docstring summary: Check if an index exists on a table.

<!-- declaration:migration_utils.py:55:add_column -->
### `add_column`

```python
def add_column(table: str, column_name: str, nullable: bool, type_: sa.types.TypeEngine, default: Any | None=None) -> None
```

Source: [add_column](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:55). Source-docstring summary: Add a column to a table if it doesn't already exist.

<!-- declaration:migration_utils.py:79:drop_column -->
### `drop_column`

```python
def drop_column(table: str, column_name: str) -> None
```

Source: [drop_column](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:79). Source-docstring summary: Drop a column from a table if it exists.

<!-- declaration:migration_utils.py:89:add_index -->
### `add_index`

```python
def add_index(table: str, index_name: str, columns: list[str]) -> None
```

Source: [add_index](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:89). Source-docstring summary: Create an index on a table if it doesn't already exist.

<!-- declaration:migration_utils.py:103:drop_index -->
### `drop_index`

```python
def drop_index(table: str, index_name: str) -> None
```

Source: [drop_index](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/migration_utils.py:103). Source-docstring summary: Drop an index from a table if it exists.

## `script.py.mako`

Behavior: [script_template_knowledge.md](script_template_knowledge.md). Source: [script.py.mako](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/script.py.mako).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

## `versions/38ce57e08137_add_column_protocol_version.py`

Behavior: [versions_knowledge.md](versions_knowledge.md). Source: [versions/38ce57e08137_add_column_protocol_version.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/38ce57e08137_add_column_protocol_version.py).

<!-- declaration:versions/38ce57e08137_add_column_protocol_version.py:32:upgrade -->
### `upgrade`

```python
def upgrade() -> None
```

Source: [upgrade](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/38ce57e08137_add_column_protocol_version.py:32). Source-docstring summary: Upgrade schema.

<!-- declaration:versions/38ce57e08137_add_column_protocol_version.py:59:downgrade -->
### `downgrade`

```python
def downgrade() -> None
```

Source: [downgrade](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/38ce57e08137_add_column_protocol_version.py:59). Source-docstring summary: Downgrade schema.

## `versions/6419d2d130f6_add_columns_owner_last_updated.py`

Behavior: [versions_knowledge.md](versions_knowledge.md). Source: [versions/6419d2d130f6_add_columns_owner_last_updated.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/6419d2d130f6_add_columns_owner_last_updated.py).

<!-- declaration:versions/6419d2d130f6_add_columns_owner_last_updated.py:37:upgrade -->
### `upgrade`

```python
def upgrade() -> None
```

Source: [upgrade](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/6419d2d130f6_add_columns_owner_last_updated.py:37). Source-docstring summary: Upgrade schema.

<!-- declaration:versions/6419d2d130f6_add_columns_owner_last_updated.py:81:downgrade -->
### `downgrade`

```python
def downgrade() -> None
```

Source: [downgrade](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/6419d2d130f6_add_columns_owner_last_updated.py:81). Source-docstring summary: Downgrade schema.

## `versions/__init__.py`

Behavior: [versions_knowledge.md](versions_knowledge.md). Source: [versions/__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/migrations/versions/__init__.py).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

