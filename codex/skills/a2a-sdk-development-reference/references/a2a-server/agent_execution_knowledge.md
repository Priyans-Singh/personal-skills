# Agent execution and active-task lifecycle

Sources: `server/agent_execution/`, a2a-sdk 1.1.4. Exact signatures and line links are in the [callable index](callable_index_knowledge.md). This chapter describes every file and the meaningful behavior of its methods.

## `__init__.py`

Re-exports AgentExecutor, RequestContext, RequestContextBuilder, SimpleRequestContextBuilder. No lifecycle logic. ActiveTask/registry require defining-module imports.

## `agent_executor.py`

`AgentExecutor` is an abstract interface, not an LLM framework. Implement async `execute(context, event_queue) -> None` and `cancel(context, event_queue) -> None`. Read RequestContext and enqueue protocol events; returning a Python string does not return a protocol reply. A normal immediate response is one Message; a task workflow starts with Task then status/artifact updates. Finish or yield control with an appropriate state. Do not continue using the context/queue after execution returns.

Concurrency is per active task, not per executor instance: different tasks can call the same executor concurrently. Keep per-task mutable state keyed by globally unique IDs or outside the shared executor. Cancellation should stop application work and publish canceled state; clean resource handles in finally clauses.

Implementation overrides docstring assumptions: V2 awaits `cancel()` **before** canceling the producer. If your cancel hook waits for execute to receive cancellation, deadlock is possible. Executor docstring mentions `TASK_STATE_ERROR`; actual enum and failure implementation use `TASK_STATE_FAILED`. The hook should finish promptly and avoid depending on transport disconnect to stop business work.

## `context.py`

`RequestContext.__init__` accepts call context, optional SendMessageRequest, explicit IDs, existing Task/related tasks, and generator overrides. It stores mutable references, not an immutable snapshot. With a request, explicit IDs overwrite message IDs; a supplied Task with a conflicting explicit ID raises InvalidParamsError. Otherwise `_check_or_generate_task_id` and `_check_or_generate_context_id` fill missing fields and set internal IDs. Construction can mutate the request protobuf before executor entry.

| Member | Inputs / result / effects |
|---|---|
| `get_user_input(delimiter='\n')` | Concatenates only text Parts via get_message_text; no request returns empty string. Raw/URL/data Parts are not fetched or decoded |
| `attach_related_task(task)` | Appends the supplied Task object to the mutable related list |
| `message` | Request message or None |
| `related_tasks` | Stored mutable list, not a defensive copy |
| `current_task` getter/setter | Cached current Task; producer refreshes before each execute |
| `task_id`, `context_id` | Internal IDs, possibly None for context constructed without request/IDs |
| `configuration` | Request configuration submessage or None; protobuf absent-submessage access is not a Pydantic None check |
| `call_context` | Original ServerCallContext |
| `metadata` | New dict made from request metadata protobuf; empty dict without request |
| `tenant`, `requested_extensions` | Delegate to call context; extension set remains mutable |
| `_check_or_generate_task_id` | UUID/custom generation only when neither internal nor message task ID exists; generator receives available context ID |
| `_check_or_generate_context_id` | Same for context ID; generator receives current task ID |

No owner authorization here; the handler/store establish access. The context does not independently load the task or verify that arbitrary request IDs identify the persisted conversation.

## `request_context_builder.py`

`RequestContextBuilder.build(context, params=None, task_id=None, context_id=None, task=None)` is async abstract construction. Replace it to derive context consistently or load approved application state. Do not replace transport authentication with trust in message metadata.

## `simple_request_context_builder.py`

`SimpleRequestContextBuilder.__init__` records referred-task population flag (False by default), store, and ID generators. `build` optionally gathers store.get calls concurrently for message.reference_task_ids using caller context, drops missing Tasks, then constructs RequestContext. asyncio.gather errors propagate; missing related tasks are silently omitted. No automatic reference deduplication or recursive graph traversal. With default handler wiring, related tasks are not loaded.

## `active_task_registry.py`

`ActiveTaskRegistry.__init__` holds executor, store, optional sender, ID-keyed map, threading.RLock, cleanup-task set, and closed flag. Locks guard map operations, not asynchronous database operations.

`get_or_create(task_id, call_context, context_id=None, create_task_if_missing=False, initial_message=None)` rejects a closed registry. Under map lock it finds an object or creates TaskManager + ActiveTask and inserts it. Outside the lock it starts a new object. On a cache hit with create_task_if_missing=False it rechecks store ownership and raises TaskNotFoundError if unreadable. With True it skips that cache-hit check; send setup separately validates an explicitly supplied continuation ID. Globally unique generated IDs are essential.

`get` simply returns a map entry; it has no owner parameter/check. `get_or_create` is the handler path. Creation inserts before awaiting start; setup failures arrange cleanup, so races/cleanup timing must be considered if extending this code.

`_on_active_task_cleanup` schedules `_remove_task` and tracks its asyncio task; the callback discards it from the cleanup set when done. `_remove_task` pops by ID under lock; no durable Task deletion. `aclose` marks registry closed, closes live tasks concurrently with exceptions collected/logged, awaits cleanup tasks, then clears map. It is not a database shutdown or an application recovery checkpoint.

## `active_task.py`: architecture and constructor

`_RequestStarted.__init__` carries an internal UUID plus RequestContext; `_RequestCompleted.__init__` carries request UUID. They are lifecycle sentinels, never protocol output. The local `EventConsumer` is different from the legacy class in `events/event_consumer.py`.

`ActiveTask.__init__` creates:

- Agent EventQueueSource with default consumer sink.
- Subscriber EventQueueSource without a default sink; each subscriber taps it.
- Async lifecycle lock and request-processing lock.
- Task-created and finished events.
- Request queue, producer/consumer handles, reference count, optional push sender and cleanup callback.

EventQueueSource construction schedules dispatcher tasks immediately. Instantiate this path inside a running loop. `task_id` returns fixed ID. `enqueue_request` puts `(RequestContext, new internal UUID)` into the request queue; it does not itself execute the agent.

## Start → produce → consume

`start(call_context, create_task_if_missing=False)` locks setup, rejects finished objects, ignores duplicate successful starts, updates manager call context, and loads snapshot. Existing terminal state is InvalidParamsError; missing state is TaskNotFoundError unless creation allowed. Successful existing load sets task-created. Failure sets finished and requests cleanup when unreferenced; successful setup adds one background-execution reference and creates producer/consumer asyncio tasks.

`_run_producer` waits for queued requests, acquires request lock, switches manager context to request caller, refreshes request.current_task, and enqueues started sentinel. It awaits executor.execute then enqueues completed sentinel. The consumer releases the lock only after processing completed, preventing the next invocation from overtaking prior event persistence. Request queue.task_done runs in finally.

Producer cancellation/queue shutdown ends the loop. Other executor errors are logged, ensure/create a Task, mark nonterminal state failed, save it, set task-created, and enqueue the exception. Finally it shuts request queue and gracefully closes event/subscriber queues. A store error while marking failure can interrupt this path; there is no retry or universally guaranteed persisted failure.

`EventConsumer.__init__` starts undecided response mode and no pending message. `run` dequeues events until shutdown. On ordinary failure it logs, attempts a FAILED status if current Task is nonterminal, and fans out the exception with a snapshot. Errors during the recovery save/delivery can themselves escape. It does not catch all BaseException types.

| Consumer helper | Behavior |
|---|---|
| `_process_event` | Started remembers request message; completed releases lock; BaseException is raised; Message validates mode; task-family events mutate state; updated state sets created and is sent to subscribers; task_done follows delivery |
| `_handle_message_event` | First Message establishes message mode; second Message or Message in task mode raises InvalidAgentResponseError |
| `_handle_task_event` | Rejects task events after message mode; delegates initial/modification processing; establishes task mode; requires manager snapshot to exist |
| `_handle_initial_task` | Saves first Task; if already stored, logs and ignores Task replacement; clears pending request message |
| `_handle_task_modification_event` | First status update needs existing Task; ensures Task, saves pending request message once by message_id, adopts event context ID, delegates manager.process |
| `_update_task_state` | Marks terminal lifecycle and synchronously awaits sender for Task/status/artifact events when configured |
| `_handle_terminal_state` | Sets finished and immediately shuts queued requests; does not itself delete persisted task |
| `_enqueue_to_subscribers` | Copies updated Task via protobuf CopyFrom, emits `(event, snapshot)`, then acknowledges agent event; status/artifact event object is not universally deep-copied |

Non-obvious boundaries: initial Task should carry initial history; Consumer clears its pending message when accepting an initial Task rather than injecting history itself. Artifact-first modifications can create a submitted task through TaskManager even though status-first is rejected. Context is set from modification event before TaskManager.process; therefore this path is not a complete independent context-mismatch guard. No general state-machine guard rejects all post-terminal buffered events.

`_run_consumer` ensures finished state, shuts request/agent queues, awaits producer completion, releases the background reference, and calls `_maybe_cleanup`. Graceful producer closure, subscriber draining, and an executor that never returns can affect how long this takes.

## Subscribe and disconnect

`subscribe(request=None, include_initial_task=False, replace_status_update_with_task=False)` rejects finished state and adds a reference; taps an evict-on-full sink, then optionally enqueues the request. This order avoids missing initial output. With include_initial_task it awaits `get_task` and yields the snapshot. For live events it raises exception events, optionally replaces status updates with copied snapshots, hides lifecycle sentinels, and ends at the matching completed sentinel for request-bound subscriptions. Independent observers have no matching request sentinel.

A yielded event is acknowledged in a finally block. Queue shutdown/cancellation breaks the loop. Final cleanup closes sink immediately, releases reference, and checks registry cleanup. Generator closure detaches observation; it does not by itself stop the executor. Subscribe has no cursor/replay buffer. Eviction means a slow client can lose remaining events and must read current snapshot/reconnect.

`get_task` waits for task-created then reads manager snapshot; absent snapshot raises RuntimeError. There is no timeout. A Message-only task never sets task-created, but normal message-return flow avoids this method. An executor emitting nothing can leave unary fallback waiting indefinitely.

## Cancellation, failure, shutdown

`cancel(call_context)` refreshes manager caller context and builds a cancellation RequestContext. Under lifecycle lock, if running it awaits executor.cancel. Hook errors log, call `_mark_task_as_failed`, and re-raise; finally cancels producer. It waits for finished, gets persisted snapshot, and if still nonterminal saves a copy in CANCELED state. An already terminal failure/completion is returned unchanged by this method; higher handler rejects terminal persisted state during registry start when necessary.

`_mark_task_as_failed` enqueues FAILED only if task-created is set and snapshot exists; suppresses QueueShutDown; otherwise store errors propagate. It returns the Task it read, not a guaranteed persisted failed result. `_maybe_cleanup` invokes callback only when finished and reference count is zero. `aclose` immediately shuts all queues, sets finished, cancels producer/consumer, gathers/logs exceptions. It does not invoke executor.cancel, mark each task canceled, or close sender's HTTP client/store engine.

## Practices

Publish an initial Task with context.message in history, retain context IDs on continuation, use TaskUpdater consistently, emit terminal/interrupted status before normal return, and keep cancel hooks bounded. Apply application execution deadlines and bounded shutdown. Integrate handler.aclose into application lifespan. Durable storage plus multiple web replicas still needs execution ownership/routing; ActiveTaskRegistry is not distributed coordination.
