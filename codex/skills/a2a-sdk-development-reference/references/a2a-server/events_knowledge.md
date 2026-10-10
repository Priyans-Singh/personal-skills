# Event queues, fan-out, and consumption

Sources: `server/events/`. All queues are asynchronous, bounded by default at **1024 events**; size <=0 is rejected for public event queues. Queue APIs use the Python-version compatibility backend described in [dependencies](dependencies_knowledge.md).

## `__init__.py`

Re-exports Event, EventConsumer (legacy), EventQueue/Legacy, queue-manager interfaces/implementation and errors. V2 Source/Sink are imported from `event_queue_v2` explicitly.

## `event_queue.py`

`Event` is the union Message | Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent. V2 internally sends sentinels, exceptions, and `(event, Task)` pairs using casts; static union does not describe every internal queue payload.

`EventQueue.__new__` redirects direct construction to EventQueueLegacy with DeprecationWarning; other subclasses construct normally. `enqueue_event` is its only abstract requirement. Avoid direct `EventQueue()` in new code.

`EventQueueLegacy.__init__` constructs a queue, child list, closed flag, and asyncio lock. `queue` exposes backend queue. `__aenter__` returns self; `__aexit__` awaits graceful close. `enqueue_event` checks closed under lock, puts into own queue, then forwards sequentially to children. If shutdown races insertion it logs/drops output. `dequeue_event` raises QueueShutDown once closed/empty; otherwise blocks awaiting get. `task_done` acknowledges one dequeued event.

`tap(max_queue_size=1024)` creates a new child queue observing future events only. It does not replay buffered events. Children remain listed, even if closed. A slow live child can backpressure siblings because forwarding is sequential. `close(immediate=False)` marks closed, shuts backend, closes children concurrently, and on graceful closure joins own queue. Repeated graceful close returns; immediate close can upgrade closure and drop work. `is_closed` returns flag.

Every dequeue needs task_done; abandoned queues can make graceful close hang. Legacy drops enqueue attempts after close rather than raising to producer.

## `event_queue_v2.py`: EventQueueSource

`__init__(max_queue_size=1024, create_default_sink=True)` creates bounded incoming queue, sink set, lock, flag, optional default sink, and dispatcher task. Requires a running loop. Default sink supports source.dequeue_event; no-default mode is suitable for broadcast-only subscribers.

| Method/property | Behavior / errors |
|---|---|
| `queue` | Returns default sink backend; ValueError without default sink |
| `enqueue_event` | Puts into incoming queue; shutdown logs/drops event |
| `_dispatch_loop` | Takes incoming events, snapshots sinks under lock, delivers concurrently with gather(return_exceptions=True), logs sink errors, acknowledges incoming queue |
| `_deliver_to_sink` | Skips closed sink; if evict_on_full and full, logs and force-closes it; otherwise awaits sink insertion |
| `tap` | New future-events-only sink; rejects closed source with QueueShutDown; accepts custom size/eviction flag |
| `remove_sink` | Discards membership under lock; idempotent |
| `dequeue_event`, `task_done` | Delegate to default sink; ValueError without one |
| `_join_incoming_queue` | Races incoming.join against dispatcher completion; stops waiting if dispatcher dies, logs possible event loss, cancels join helper |
| `test_only_join_incoming_queue` | Calls incoming-drain helper; delivery completed is not subscriber processing completed |
| `close` | Shuts incoming queue, drains when graceful, cancels dispatcher, closes every snapshot sink, suppresses dispatcher cancellation/errors while awaiting it |
| `is_closed` | Flag lookup |
| `__aenter__`, `__aexit__` | Return self / graceful close |

Fan-out gives each sink the same event object; generic queues do not defensively copy every payload. ActiveTask copies Task snapshots separately. Mutating received protobuf events may affect other readers; treat events as immutable.

Default `evict_on_full=False` means any sink can slow the source and therefore producers. `True` sacrifices that observer's undelivered data to let dispatch continue. ActiveTask subscribers use True. Incoming queue remains bounded, so excessive production also backpressures execution.

Dispatcher cancellation not initiated by close marks source closed, shuts incoming queue immediately, closes sinks, and re-raises cancellation. Unexpected dispatch errors log and escape; `_join_incoming_queue` notices dispatcher completion rather than waiting forever on incoming join. This does not resolve a live but stalled sink.

Graceful close waits for incoming delivery, cancels dispatcher, then graceful-closes sinks, waiting for their task_done acknowledgements. It can still wait indefinitely on consumers that disappeared. Immediate close drops pending work, closes sinks, and cancels dispatcher. Bound graceful shutdown externally.

## `event_queue_v2.py`: EventQueueSink

`__init__` records parent, eviction policy, bounded queue, closed flag and lock; constructor rejects nonpositive size. `queue` exposes backend.

`_put_internal` inserts while suppressing QueueShutDown races. Public `enqueue_event` raises RuntimeError: sink is consumer-only. `dequeue_event` awaits backend.get and propagates shutdown; `task_done` acknowledges it. `tap` creates a sibling through parent, not a cascade child. `close` marks closed, shuts backend, removes itself from parent, and on graceful closure joins its queue. `is_closed` reports flag; async context manager closes gracefully.

## `queue_manager.py`

`QueueManager` is the legacy replaceable abstraction: `add(task_id, queue)`, `get(task_id)`, `tap(task_id)`, `close(task_id)`, `create_or_tap(task_id)`. Abstract methods do no work. `TaskQueueExists` / `NoTaskQueue` are marker exceptions. This interface alone supplies no owner scope, distributed lease, delivery guarantee, retry, or durable log.

## `in_memory_queue_manager.py`

`InMemoryQueueManager.__init__` creates task-ID dictionary and threading.RLock. `add` rejects duplicate key with TaskQueueExists. `get` returns queue or None. `tap` looks up under lock then awaits queue.tap outside lock, or returns None. `close` removes mapping first, raises NoTaskQueue if missing, then graceful-closes queue. Failed/hanging closure does not restore mapping. `create_or_tap` atomically inserts new legacy queue under map lock or taps existing queue outside lock.

All queue state is process-local; IDs are not owner-namespaced. V2 ignores this manager. A custom legacy distributed implementation must define remote fan-out, routing, state cleanup, cancellation, and failure semantics itself.

## `event_consumer.py`: legacy consumer

`EventConsumer.__init__` records queue, 0.5-second dequeue polling timeout, and exception slot. `consume_all` repeatedly checks saved exception, awaits dequeue with timeout, calls task_done **before** yielding, and closes immediately on a stopping event.

Stopping events: Message, or Task/status update whose state is COMPLETED, CANCELED, FAILED, REJECTED, UNSPECIFIED, or INPUT_REQUIRED. AUTH_REQUIRED is not in this list; legacy aggregation handles early unary return for it separately. Timeouts continue polling. Shutdown/QueueEmpty end only when queue reports closed. Pydantic ValidationError is logged and skipped. Other exceptions are logged/stored, then raised at next loop check.

`agent_task_callback` captures a completed, noncancelled producer's exception so a waiting consumer sees executor failure. Producer cancellation does not populate this slot. Unlike V2, this consumer does not persist Tasks or validate message/task mode itself; ResultAggregator/TaskManager do aggregation.

## Usage rules

Enqueue protocol events on the queue supplied to execute; do not own/close that queue from executor code. Use sink taps as subscriptions, not as producer destinations. Acknowledge events exactly once when using queues directly. Avoid sharing mutable protobuf values across application consumers. Monitor slow-subscriber eviction and use snapshot reads to recover; there is no built-in replay cursor.
