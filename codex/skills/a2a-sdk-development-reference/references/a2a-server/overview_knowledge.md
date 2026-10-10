# A2A server: start here

Inspected **a2a-sdk 1.1.4**, Python 3.11, on **2026-10-07**. Source: `../.venv/lib/python3.11/site-packages/a2a/server/` relative to this folder. This is a reference for the installed implementation, not a guarantee about other SDK versions. The unrelated `a2a` distribution is absent. Inspection did not modify installed code or contact external services.

## Reading map

| Reference | Scope |
|---|---|
| [Root initializer](init_knowledge.md) | Import surface, optional dependencies |
| [Call context](context_knowledge.md) | Caller identity, tenant, extensions, state |
| [IDs](id_generator_knowledge.md) | Generation contracts and UUID defaults |
| [JSON-RPC models](jsonrpc_models_knowledge.md) | Error payload models |
| [Database models](models_knowledge.md) | Tables, keys, factories, ownership constraints |
| [Owner resolver](owner_resolver_knowledge.md) | Storage ownership boundary |
| [Agent execution](agent_execution_knowledge.md) | Context construction, producer/consumer lifecycle, cancellation |
| [Events](events_knowledge.md) | Legacy and V2 queues, fan-out, backpressure, closure |
| [Request handlers](request_handlers_knowledge.md) | Protocol operations, validation, V2/legacy differences, gRPC |
| [Routes](routes_knowledge.md) | REST, JSON-RPC, SSE, Agent Cards, FastAPI schemas |
| [Tasks](tasks_knowledge.md) | State aggregation, stores, pagination, push delivery |
| [Supporting dependencies](dependencies_knowledge.md) | Wire models, validation, errors, telemetry, v0.3 integration |
| [Usage and practices](usage_knowledge.md) | Working example, deployment choices, troubleshooting |
| [Callable index](callable_index_knowledge.md) | Every declared class/function/method, including private and nested helpers |
| [Coverage](coverage_knowledge.md) | Inventory, source hashes, checks, known validation limits |

Every one of the 48 server Python files has a source section in the corresponding guide. Root files each have a separate guide; the five folders each have a guide covering every nested source file. `__pycache__` contains interpreter caches, not additional implementation; it is excluded. The inventory found no other non-cache files under `server`.

## Definitions and resource hierarchy

**Agent Card:** discovery document advertising interfaces, protocol versions, skills, capabilities, and security requirements. Advertising security does not install authentication middleware.

**ServerCallContext:** one transport call's caller identity and auxiliary state. **RequestContext:** the executor-facing view of one message or cancellation, with IDs, configuration, current task, and related tasks.

**Message:** one user/agent communication containing typed `Part` values. **Task:** a persisted snapshot with ID, conversation/context ID, status, history, metadata, and artifacts. **Artifact:** task output identified by `artifact_id`, potentially delivered in chunks.

**ActiveTask:** V2's process-local coordination object containing the producer, consumer, queues, task manager, and subscriber references. **TaskManager:** mutable cached snapshot plus persistence operations. **TaskStore:** snapshot storage; it does not run agents. **TaskUpdater:** constructs and enqueues events; it does not save snapshots directly.

```text
Agent Card → transport endpoint → ServerCallContext → RequestHandler
                                                  ↓
                                        RequestContext / ActiveTask
                                                  ↓
                                            AgentExecutor
                                                  ↓
                                              event queue
                                                  ↓
                                     TaskManager → TaskStore
                                                  ↓
                              unary result / subscribers / push sender
```

Conceptually, owner → context/conversation → tasks → history/artifacts/configs. Physically, database task IDs are globally primary-keyed, the V2 registry is keyed only by task ID, and push dispatch queries all owners by task ID. Owner and tenant are distinct: default ownership is `context.user.user_name`, not `context.tenant`. Use globally unique IDs and explicitly incorporate a trusted tenant into ownership where required.

## Objects and lifetime

| Object | Created when | Lifetime / durable state |
|---|---|---|
| Executor, handler, stores | Application startup | Shared objects; executor may run different tasks concurrently |
| ServerCallContext | Every request | Call-scoped, may be retained by live execution |
| RequestContext | Send setup or cancellation | One executor invocation; request protobuf may be mutated to insert IDs |
| ActiveTask and TaskManager | V2 registry miss | Process-local; task snapshots separately persisted |
| Agent queue and subscriber source | ActiveTask construction | Start dispatcher background tasks immediately; need a running event loop |
| Subscriber sink | Subscription starts | Closed on generator exit; no durable replay log |
| Task snapshot | Initial Task, implicit TaskManager creation, or store read | Memory or database according to chosen store |
| Push configuration | Explicit registration or inline send configuration | Separate store; task deletion does not automatically delete configs |

## Core paths

1. **Send:** parse protobuf-compatible request → validate required fields → verify existing task ownership if continuing → construct IDs/context → optionally store inline push config → get/create ActiveTask → tap subscription before enqueuing request → serialized executor call → persist/fan out emitted events → select unary result.
2. **Stream:** same execution, but yields individual events in `StreamResponse` envelopes. V2 history trimming applies to emitted full Tasks, not every status/artifact event. SSE transport eagerly obtains the first event before starting the response.
3. **Get/list:** use owner-scoped snapshot storage directly, without running the executor. Get can trim history; list also omits artifacts unless requested. Cursor pagination is not a frozen snapshot.
4. **Subscribe:** V2 obtains or starts a coordinator for an owned nonterminal persisted task, emits initial state, and listens to future local events. A coordinator created from storage does not restart prior execution or replay history.
5. **Cancel:** locate/start coordinator → await executor cancellation hook → cancel producer → wait for consumer completion → return snapshot, forcing canceled if still nonterminal. This order differs from the executor docstring.
6. **Push:** persist event → retrieve configs across owners for task ID → concurrent HTTP POSTs of protobuf stream envelopes. No built-in retry, outbox, delivery receipt, or exactly-once guarantee.

## State and consistency

Terminal states: `COMPLETED`, `CANCELED`, `FAILED`, `REJECTED`. Interrupted states: `INPUT_REQUIRED`, `AUTH_REQUIRED`. They are prefixed with `TASK_STATE_` in protobuf enums. `UNSPECIFIED` is not terminal in V2, but the legacy consumer treats it as a stopping event.

The V2 request lock serializes execution and event processing for one ActiveTask; other tasks can run concurrently on the same executor instance. Store operations are individually scoped/transactional where implemented, not an atomic transaction covering execution, persistence, and HTTP notification. Cached TaskManager state can diverge from external writes. Source contains no request deduplication or executor retry system.

## Version-sensitive cautions

- `DefaultRequestHandler` aliases V2; passing a distributed `queue_manager` does nothing except warn.
- The consumer requires a first Task before a first **status** update, but the artifact-first path can implicitly create a Task. Publish a Task first for predictable semantics.
- General event processing has no comprehensive terminal-state transition validator. TaskUpdater prevents later status updates only for that updater instance; artifact publishing has no such guard.
- V2 continuation setup checks an existing task but builds RequestContext with `task=None`. It does not automatically derive the persisted context ID when a continuation omits it. Send the original context ID.
- Missing first output can leave `get_task()` waiting indefinitely. Always emit a Message or initial Task.
- FastAPI, gRPC, and SQLAlchemy are absent in this `.venv`; their code was inspected, but integrations could not be exercised without installing dependencies.
