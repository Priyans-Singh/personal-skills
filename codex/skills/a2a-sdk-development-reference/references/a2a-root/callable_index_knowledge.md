# Complete source and callable index

AST inventory includes classes, functions, properties, methods, conditional definitions and nested helpers. Signature/source-docstring summaries are supplementary evidence: manually written behavioral guides explain actual execution. Non-Python files are inventoried and linked even though they have no runtime AST callables.

## `_base.py`

Behavior: [base_knowledge.md](base_knowledge.md). Source: [_base.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/_base.py).

<!-- declaration:_base.py:5:to_camel_custom -->
### `to_camel_custom`

```python
def to_camel_custom(snake: str) -> str
```

Source: [to_camel_custom](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/_base.py:5). Source-docstring summary: Convert a snake_case string to camelCase.

<!-- declaration:_base.py:21:A2ABaseModel -->
### `A2ABaseModel`

```python
class A2ABaseModel(BaseModel)
```

Source: [A2ABaseModel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/_base.py:21). Source-docstring summary: Base class for shared behavior across A2A data models.

## `a2a_db_cli.py`

Behavior: [a2a_db_cli_knowledge.md](a2a_db_cli_knowledge.md). Source: [a2a_db_cli.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/a2a_db_cli.py).

<!-- declaration:a2a_db_cli.py:18:_add_shared_args -->
### `_add_shared_args`

```python
def _add_shared_args(parser: argparse.ArgumentParser, is_sub: bool=False) -> None
```

Source: [_add_shared_args](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/a2a_db_cli.py:18). Source-docstring summary: Add common arguments to the given parser.

<!-- declaration:a2a_db_cli.py:53:create_parser -->
### `create_parser`

```python
def create_parser() -> argparse.ArgumentParser
```

Source: [create_parser](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/a2a_db_cli.py:53). Source-docstring summary: Create the argument parser for the migration tool.

<!-- declaration:a2a_db_cli.py:105:run_migrations -->
### `run_migrations`

```python
def run_migrations() -> None
```

Source: [run_migrations](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/a2a_db_cli.py:105). Source-docstring summary: CLI tool to manage database migrations.

## `alembic.ini`

Behavior: [support_files_knowledge.md](support_files_knowledge.md). Source: [alembic.ini](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/alembic.ini).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

## `py.typed`

Behavior: [support_files_knowledge.md](support_files_knowledge.md). Source: [py.typed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/py.typed).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

