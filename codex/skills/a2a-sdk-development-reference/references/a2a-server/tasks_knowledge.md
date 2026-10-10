# Tasks, persistence, aggregation, and push notifications

Sources: `server/tasks/`, a2a-sdk 1.1.4. Signatures/line links are in the [callable index](callable_index_knowledge.md). Task snapshots and push configurations are separate persistence domains; neither is a live execution object.

## `__init__.py`

Re-exports TaskStore, InMemoryTaskStore, DatabaseTaskStore, TaskManager, TaskUpdater, ResultAggregator, push interfaces/implementations and config stores. SQL imports have placeholders when dependencies are absent; see [initializer](init_knowledge.md). CopyingTaskStoreAdapter requires its module import.

## `task_store.py`

`TaskStore` requires async `save(task, context) -> None`, `get(task_id, context) -> Task | None`, `list(params, context) -> ListTasksResponse`, `delete(task_id, context) -> None`. This is snapshot CRUD, not event storage or orchestration. Implement owner checks on every operation, define copy isolation, and propagate meaningful I/O errors. Handler get maps None to TaskNotFoundError. The interface does not prescribe locking, idempotency, optimistic concurrency, retry, retention, or cascading config deletion.

## `copying_task_store.py`

`CopyingTaskStoreAdapter.__init__` records underlying store. `save` deep-copies Task with CopyFrom before forwarding; `get` copies non-None result; `list` copies the complete protobuf response; `delete` forwards unchanged. Exceptions propagate. It isolates object mutation, not simultaneous save transactions. This adapter is enabled by default on InMemoryTaskStore.

## `inmemory_task_store.py`

`_InMemoryTaskStoreImpl.__init__` creates owner→task-ID→Task dictionaries, RLock, resolver. `_get_owner_tasks` returns existing dictionary or temporary empty dict without insertion. `save` resolves owner and replaces ID entry; `get` returns stored reference or None; `delete` removes entry/empty owner bucket and logs/no-ops when missing. No automatic expiry or process-restart recovery.

`list` snapshots dictionary values under lock then filters/sorts outside it. Filters: nonempty context_id, nonzero status, optional status_timestamp_after inclusive >= comparison of timestamp JSON strings. Tasks without timestamps are excluded by timestamp filter. Ordering is descending `(timestamp-present, timestamp JSON string, task ID)`.

The page token decodes to the **first task to include**, not the last task already returned. It must occur in the filtered list or raises InvalidParamsError. Page size defaults to 50 via truthiness. Next token names the task immediately after this page. total_size is filtered total, before cursor/page slicing. The handler validates explicit size 1–100; direct store calls do not enforce that range. Timestamp string comparison is the literal implementation, not a claim of normalized datetime ordering for every possible timestamp representation.

`InMemoryTaskStore.__init__(owner_resolver=resolve_user_scope, use_copying=True)` wraps the implementation in CopyingTaskStoreAdapter by default. Its save/get/list/delete methods are mechanical forwarding. `use_copying=False` exposes stored object references and can let response trimming or callers mutate saved state without save.

## `database_task_store.py`

`DatabaseTaskStore.__init__` takes application-owned AsyncEngine, create_table flag (True), table name, owner resolver, and optional core↔ORM converters. Creates async_sessionmaker(expire_on_commit=False); selects default TaskModel or table factory. Does not connect until operations/initialize.

`initialize` lazily runs Base.metadata.create_all for mapped tables only, when enabled; sets initialized flag after success. `_ensure_initialized` delegates when flag False. There is no initialization lock/migration engine; start up explicitly to expose schema/driver failures before serving requests. Engine ownership remains application responsibility.

`_to_orm` uses override if supplied, otherwise maps Task ID/context, kind, owner, timestamp-derived last_updated, protobuf JSON status/artifact/history, metadata if nonempty, and protocol_version='1.0'. `_from_orm` uses override or reconstructs protobuf for version 1.0; other versions use compat_task_model_to_core. JSON parse/conversion errors propagate.

`save` ensures initialization, resolves owner, converts, and awaits session.merge in an operation transaction. Primary key is task ID alone; owner is not a merge-key component. `get` selects ID AND owner and returns converted Task or None. `delete` transactionally deletes ID AND owner, logs success or missing row, and does not delete notification configs.

`list` builds owner-qualified SQL, optional context/status/timestamp filters, counts filtered rows, and orders descending coalesced timestamp then ID. Status filter matches JSON enum-name text. Cursor token identifies an owned task; unlike memory, this lookup is not restricted to current filters. It adds inclusive ordering predicates starting at that task's timestamp/ID, fetches size+1 rows, returns size rows, and tokenizes the extra row's ID. Null timestamps come last. It exposes filtered count, not a stable snapshot across independent requests; concurrent task changes/deletions can alter pages. Serialization uses status timestamp, not artifact update time.

Database/network errors are not swallowed or retried. Per-operation transactions do not provide a distributed execution lease or compare-and-swap snapshot updates. Concurrent managers can overwrite each other's full snapshots. Default ORM columns require globally unique IDs; see [models](models_knowledge.md).

## `task_manager.py`

`TaskManager.__init__` records store, caller context, optional IDs/initial message, empty cached Task. Non-None task_id must be nonempty str or ValueError. `get_task` returns None without ID, else cached Task or one owner-scoped store read; a missing result remains reloadable on later calls. Cached state is not refreshed just because call context changes.

`save_task_event` checks task ID and context ID against configured values, fills unset IDs, and:

- For Task: saves snapshot directly.
- For status update: ensures task, appends previous status.message to history, MergeFroms event metadata into task metadata, replaces entire status, saves snapshot.
- For artifact update: ensures task, calls append_artifact_to_task, saves snapshot.

`ensure_task_id` uses cached/store snapshot, otherwise `_init_task_obj` creates SUBMITTED Task with initial-message history and `_save_task` persists it. It does not independently validate supplied IDs against existing cached task; save_task_event provides the normal checks. `ensure_task(event)` delegates using event IDs. `process` saves task-family events and returns the original event; Message passes through without persistence.

`_init_task_obj` does not set a timestamp. `_save_task` awaits store.save then caches Task, initializing manager IDs if absent. `update_with_message` moves current status message into history and clears it, appends supplied message, updates cache, and returns Task **without saving**.

`append_artifact_to_task(task, event)` matches artifact_id. append=False replaces same-ID artifact or appends a new artifact. append=True extends existing parts and updates artifact metadata; missing artifact is InvalidAgentResponseError. It does not append name/description or implement finalization/ordering based on last_chunk. The event's last_chunk survives transport emission but is not a durable artifact-completion flag in this snapshot mutation.

TaskManager has no state-transition table, execution retry, per-method async lock, or distributed concurrency protection. Publish sequentially through normal V2 consumer and use a coherent TaskUpdater. A new Task event can replace state here, while ActiveTask consumer deliberately ignores replacement of already-existing Task.

## `task_updater.py`

`TaskUpdater.__init__` takes agent event queue and IDs, creates status lock/terminal flag, defaults artifact/message UUID generators. It is a publishing convenience tied to an invocation, not a store interface.

`update_status(state, message=None, timestamp=None, metadata=None)` locks, rejects if terminal flag already reached, marks terminal for COMPLETED/CANCELED/FAILED/REJECTED, creates current UTC timestamp or parses provided ISO timestamp, and enqueues TaskStatusUpdateEvent. Parsing/enqueue errors propagate; terminal flag is set **before** parsing and publishing, so failure can leave updater terminal even without delivered final event. Queue enqueue can itself log/drop shutdown output.

`complete`, `failed`, `reject`, `submit`, `start_work`, `cancel`, `requires_input`, `requires_auth` each call update_status with their corresponding enum and optional Message. These are genuinely mechanical wrappers.

`add_artifact(parts, artifact_id=None, name=None, metadata=None, append=None, last_chunk=None, extensions=None)` generates ID if absent and enqueues artifact update. It is not protected by status lock/terminal flag. Reuse artifact ID for later chunks; publish first with append=False before append=True. Explicit terminal discipline is application responsibility.

`new_agent_message(parts, metadata=None)` constructs Message with ROLE_AGENT, task/context IDs and generated message ID. It returns that value; does **not** enqueue it. In task mode include it in a status update rather than emitting a bare Message.

## `result_aggregator.py`: legacy result processing

`ResultAggregator.__init__` records manager and empty final-message slot. `current_result` is an **async property**: use `await aggregator.current_result`; returns stored Message or manager snapshot.

`consume_and_emit` applies manager.process then yields each consumer event. `consume_all` returns Message immediately (remembering it), otherwise processes until consumer ends then returns snapshot. `consume_and_break_on_interrupt(consumer, blocking=True, event_callback=None)` persists each non-Message event then awaits callback. AUTH_REQUIRED always triggers early return with background `_continue_consuming`; blocking=False does so after first non-Message event. INPUT_REQUIRED is normally ended by legacy consumer. Return tuple is `(result, interrupted, background_task_or_None)`; caller must track/clean background task. `_continue_consuming` keeps processing/calling callback. Callback/store errors propagate; no retry. Aggregator does not define durable event replay.

## `push_notification_config_store.py`

`PushNotificationConfigStore` declares owner-scoped `set_info`, `get_info`, `delete_info(task_id, context, config_id=None)`; None config ID means all task configs for owner. `get_info_for_dispatch(task_id)` is a background, context-free query across owners. Base implementation warns and falls back to get_info(task_id, ServerCallContext()), often losing nonanonymous-owner configs. Custom stores should override it.

## `inmemory_push_notification_config_store.py`

`__init__` creates owner→task→config-list map, RLock, resolver. `_get_owner_push_notification_infos` returns owner bucket or empty temporary dict. `set_info` mutates supplied config's empty id to task_id, replaces any same-ID config, and stores original object reference. `get_info` returns a new list but same config objects. `get_info_for_dispatch` builds list across all owner buckets, also without copying objects. No persistence/expiry.

`delete_info` deletes all configs for a task if config_id is None, else removes first matching config, prunes empty buckets, logs/no-ops when absent. Treat config objects as immutable after registration; direct mutation can change future destination/token without another set_info.

## `database_push_notification_config_store.py`

`__init__` takes engine, lazy table settings, owner resolver, optional conversion hooks and encryption_key. Config model is default or table factory. Supplying key loads cryptography.Fernet, converts str key to bytes and validates it during Fernet construction. No key generation, secret manager lookup, or automatic rotation.

`initialize` / `_ensure_initialized` follow TaskStore lazy create_all pattern, without initialization lock. `_to_orm` calls custom converter or stores protobuf JSON bytes, optionally Fernet-encrypted, with version='1.0'. Credentials/token in config are stored in this payload; without encryption they are plaintext JSON bytes.

`_from_orm` calls custom converter or attempts decrypt+parse. InvalidToken logs and falls back to plaintext JSON for migration compatibility. A successful decryption followed by parse failure raises ValueError immediately. Plaintext parse failure (including wrong encrypted key) logs/raises ValueError. `_parse_config` uses protobuf Parse for version 1.0, legacy model conversion otherwise.

`set_info` copies input config, defaults copied id to task_id, converts and merges transactionally; unlike memory it does not update caller's id. `_select_configs` initializes, selects predicates, converts rows; per-row ValueError logs and **skips that config** while SQL/other conversion errors propagate. `get_info` uses task+owner predicates; `get_info_for_dispatch` uses task only. `delete_info` transactionally removes owner/task and optional config ID, logs missing/no-op. Primary key excludes owner and no task FK/cascade is present.

## `push_notification_sender.py`

`PushNotificationEvent` is Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent (a runtime union also used by isinstance). `PushNotificationSender.send_notification(task_id, event)` is abstract async delivery contract. Immediate Messages are not push-notification events.

## `base_push_notification_sender.py`

`BasePushNotificationSender.__init__` takes application-owned httpx.AsyncClient, config store, optional URL validator. Historical context argument is accepted but ignored with warning: dispatch no longer carries caller identity.

`send_notification` loads all dispatch configs, returns immediately if none, concurrently calls `_dispatch_notification` for each, and warns if any return False. Store errors propagate. asyncio.gather is not return_exceptions=True; validator exceptions occur outside dispatch's try block and can propagate.

`_dispatch_notification` optionally validates URL before POST. False means skip/False. It sends `MessageToDict(to_stream_response(event))` JSON. Nonempty config.token becomes **`X-A2A-Notification-Token` sent to the webhook destination**. It does not implement config.authentication schemes, obtain OAuth tokens, or reuse caller authorization headers automatically. Caller-owned HTTP client's configured auth/headers/redirects/timeouts still apply.

Within try, HTTP/serialization/status errors log and return False; successful raise_for_status returns True. No backoff, persistence of receipts, or delivery retry. Log messages include URL, so avoid secrets in URL. V2 awaits sender from its consumer: slow delivery delays processing/acknowledgment and potentially the next request, even though per-config HTTP calls run concurrently.

## Operational practices

Keep task IDs globally unique; use stable ownership; leave copying on for memory; initialize database stores explicitly; do not use list cursors as authorization tokens. Close application-owned HTTP clients/engines separately from handler.aclose. Use the same owner resolver across task/config stores. Separate task/config deletion with explicit retention/cascade policy. Validate webhook URLs at registration and dispatch; set HTTP timeouts, bounded concurrency where needed, and keep caller credentials away from webhook destinations. For reliable delivery, build an outbox/custom sender: base sender is best-effort only.

Exact configuration-store class names are `InMemoryPushNotificationConfigStore` and `DatabasePushNotificationConfigStore`. Both are exported by tasks/__init__.py; the database name becomes an ImportError-raising constructor placeholder without SQLAlchemy. The per-file constructor/conversion/CRUD behavior above refers to these classes, not a generic config-store implementation.
