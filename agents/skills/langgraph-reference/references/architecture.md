# LangGraph 1.2.2: Architecture and execution

Inspected source: local package tree `langgraph/`, version `1.2.2`, on 2026-09-20. This is an implementation guide for that package snapshot, not every LangGraph release.

## Mental model

LangGraph runs a directed stateful workflow. A node reads a snapshot of channels/state and returns writes. Channel reducers merge writes; the Pregel engine schedules eligible nodes in supersteps. A compiled graph can checkpoint a snapshot, stream events, retry a task, pause through an interrupt, and resume from saved thread state.

```text
StateGraph / Pregel definition
  -> compile(checkpointer, store, cache, ...)
  -> CompiledStateGraph / Pregel runnable
  -> run identified by configurable.thread_id and checkpoint namespace/id
  -> supersteps containing Pregel tasks
  -> node reads channels and emits channel writes
  -> checkpoint snapshots + optional store/cache side effects
```

## Primary execution paths

### Custom state graph

1. Define state, normally a `TypedDict`, Pydantic model, or dataclass. Annotated fields can declare reducers, for example `Annotated[list, operator.add]`.
2. Build `StateGraph(schema)`, add nodes and `START`/`END` or conditional edges, then call `compile()`.
3. `graph/state.py` turns schema fields into channels and nodes into runnable wrappers.
4. `pregel/main.py` starts a sync or async Pregel loop. `pregel/_algo.py` prepares tasks from channel versions/triggers.
5. Tasks read (`pregel/_read.py`), run under retry/timeout policy (`pregel/_retry.py`), and write updates (`pregel/_write.py`). `channels/` validates and merges updates.
6. The loop applies writes, creates/updates a checkpoint when configured, schedules dependent nodes, then returns output or streams it.

### Tool-calling agent

`prebuilt.create_react_agent()` constructs a state graph around a chat model and tools. The model node produces an AI message; `tools_condition()` routes to `ToolNode` only for tool calls. `ToolNode` injects graph state/store/runtime arguments where requested, executes tools, translates results/errors into tool messages, then routes back to the model. The prebuilt layer validates chat history and model/tool compatibility first.

### Pause and resume

`interrupt(value)` raises graph-control flow from a node/tool. A checkpointer persists task/snapshot state under the run's thread/checkpoint configuration. A later `Command(resume=...)` supplies the resume value; the saved task is replayed from its durable boundary. `callbacks.py` emits interrupt/resume lifecycle events. Do not use an interrupt for ordinary recoverable errors.

### Persistence, memory, and cache

- A **checkpointer** saves execution snapshots for a thread: continuation, replay, interrupts, and history. `InMemorySaver` is process-local.
- A **store** holds application data independent of one graph run/thread: namespaced items, optional indexing/embedding search, and TTL behavior. `InMemoryStore` is process-local.
- A **cache** memoizes node/work results according to `CachePolicy`. `InMemoryCache` is local; `RedisCache` is Redis-backed.

These are separate planes. A checkpointer is not user long-term memory; a store is not a resume mechanism; a cache should not be the sole durable business record.

## Boundaries and safety

LangGraph delegates models/tools to LangChain Core/provider integrations; it is not an LLM service. `pregel/remote.py` and `runtime.py` integrate with the LangGraph SDK/server runtime. Database/cloud checkpoint/store adapters may be separate packages.

- Sync and async are distinct: use `ainvoke`/`astream` for async nodes/models/tools.
- `RetryPolicy` and `TimeoutPolicy` operate per task. Retry/timeout cancellation is surfaced, not turned into success.
- Invalid/conflicting state writes surface as `InvalidUpdateError`; graph recursion is bounded by `GraphRecursionError`.
- `EncryptedSerializer` can encrypt checkpoint bytes; serializer allowlists constrain type reconstruction. Persisted Python objects are not automatically a trust boundary.

## Module choice

- Custom workflow: `langgraph.graph` (`StateGraph`, `START`, `END`).
- Chat-message state: `langgraph.graph.message` (`add_messages`, `MessagesState`).
- Standard chat-and-tools loop: `langgraph.prebuilt` (`create_react_agent`, `ToolNode`).
- Conversation thread/resume: `langgraph.checkpoint` at compile time.
- Cross-conversation data: `langgraph.store` and `Runtime`/`get_store()`.
- Events: compiled graph `stream`/`astream` and `langgraph.stream` internals.
