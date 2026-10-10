# Complete source and callable index

AST inventory includes classes, functions, properties, methods, conditional definitions and nested helpers. Signature/source-docstring summaries are supplementary evidence: manually written behavioral guides explain actual execution. Non-Python files are inventoried and linked even though they have no runtime AST callables.

## `__init__.py`

Behavior: [init_knowledge.md](init_knowledge.md). Source: [__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/extensions/__init__.py).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

## `common.py`

Behavior: [common_knowledge.md](common_knowledge.md). Source: [common.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/extensions/common.py).

<!-- declaration:common.py:7:get_requested_extensions -->
### `get_requested_extensions`

```python
def get_requested_extensions(values: list[str]) -> set[str]
```

Source: [get_requested_extensions](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/extensions/common.py:7). Source-docstring summary: Get the set of requested extensions from an input list.

<!-- declaration:common.py:21:find_extension_by_uri -->
### `find_extension_by_uri`

```python
def find_extension_by_uri(card: AgentCard, uri: str) -> AgentExtension | None
```

Source: [find_extension_by_uri](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/extensions/common.py:21). Source-docstring summary: Find an AgentExtension in an AgentCard given a uri.

