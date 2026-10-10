# Ownership resolution

Source: [`server/owner_resolver.py`](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/owner_resolver.py).

`OwnerResolver = Callable[[ServerCallContext], str]`. `resolve_user_scope(context)` returns `context.user.user_name` unchanged. It has no I/O, normalization, authentication check, or tenant concatenation; missing/invalid identity attributes propagate their exceptions.

Built-in task/config stores call the resolver for scoped operations. UnauthenticatedUser returns an empty name, so all anonymous requests share one default owner scope. StarletteUser uses `display_name`, which may not be a unique immutable account identifier. The resolver is an authorization boundary only when its input comes from trusted authentication.

Recommended custom resolver: derive a stable subject ID and, where relevant, a validated tenant ID from authenticated context. Reject unauthenticated access according to application policy. Do not treat a caller-controlled tenant path or task ID as proof of ownership.

Memory stores nest dictionaries by owner; SQL task/config primary keys omit owner. Read/delete filters include owner, but `merge` writes identify rows by the primary key and can overwrite a colliding ID across owners. V2 caches and webhook dispatch also key by task ID. Generate globally unique task/config IDs; a custom schema/runtime is needed for true owner-relative ID reuse.

Push dispatch intentionally uses `get_info_for_dispatch(task_id)` without caller context so background delivery can reach all registered configs. Keep registration owner-scoped and ensure IDs cannot collide between unrelated tasks. See [tasks](tasks_knowledge.md).
