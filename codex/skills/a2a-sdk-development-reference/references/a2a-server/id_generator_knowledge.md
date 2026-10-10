# ID generation

Source: [`server/id_generator.py`](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/id_generator.py).

- `IDGeneratorContext`: Pydantic value containing optional `task_id` and `context_id`, both defaulting to None. Gives generators related identifiers; no identity or persistence.
- `IDGenerator.generate(context) -> str`: abstract synchronous contract. An implementation supplies an identifier; errors propagate to context/updater construction.
- `UUIDGenerator.generate(context) -> str`: returns `str(uuid.uuid4())`; ignores context; no network, store lookup, or collision retry.

RequestContext defaults missing task/context IDs to UUIDGenerator. It generates the task ID first, then the context ID with the task ID supplied in generator context. TaskUpdater separately defaults artifact/message generators; those receive both IDs.

A custom generator must return a valid nonempty string, fit database column sizes where used, and preserve global uniqueness across owners/replicas. Context-dependent IDs should not encode secrets or imply that a conversation ID authorizes access. Generation does not persist a task or reserve an ID. Passing existing IDs avoids generation; send continuation context IDs explicitly.
