# Callable index

This compact source-coverage index retains the concrete entry points and every private implementation family. Start at the named source file for method-level behavior.

| Source | Callables / classes |
|---|---|
| `graph/state.py` | `StateGraph`, `CompiledStateGraph`, schema/channel/control-routing helpers |
| `graph/message.py` | `add_messages`, `MessagesState`, `MessageGraph`, `push_message`, reducer/formatter helpers |
| `graph/ui.py` | `UIMessage`, `RemoveUIMessage`, `push_ui_message`, `delete_ui_message`, reducer |
| `prebuilt/chat_agent_executor.py` | agent state models, `create_react_agent`, model/prompt/history helpers |
| `prebuilt/tool_node.py` | `ToolNode`, `tools_condition`, `ToolRuntime`, request/injection/error helpers |
| `prebuilt/tool_validator.py` | `ValidationNode`, formatting helper |
| `func/__init__.py` | `_TaskFunction`, `task`, `entrypoint` |
| `checkpoint/base/__init__.py` | `BaseCheckpointSaver`, checkpoint records, copy/id/metadata/snapshot helpers |
| `checkpoint/memory/__init__.py` | `InMemorySaver`, `PersistentDict` |
| `checkpoint/serde/*.py` | serializer/cipher protocols, compatibility, `EncryptedSerializer`, serde events, `JsonPlusSerializer`, msgpack/allowlist helpers |
| `store/base/*.py`, `store/memory/__init__.py` | `BaseStore`, store value/operation records, batching, embedding/path helpers, `InMemoryStore`, matching/similarity helpers |
| `cache/*` | `BaseCache`, `InMemoryCache`, `RedisCache` |
| `config.py`, `runtime.py`, `callbacks.py`, `types.py`, `errors.py` | config/store/writer accessors; `Runtime`/metadata/control; callback events/handlers; `Command`, `Send`, `interrupt`, policies/snapshots/tasks; graph exception types |
| `_internal/_cache.py` | `_freeze`, `default_cache_key` |
| `_internal/_config.py` | checkpoint namespace/map and runnable config patch/merge/normalization, callback/tracing helpers |
| `_internal/_fields.py` | schema optional/required/readonly/default/hint/update/reducer helpers |
| `_internal/_future.py` | event-loop/future conversion/chaining/coroutine scheduling helpers |
| `_internal/_pydantic.py` | fields/model creation and version compatibility |
| `_internal/_queue.py` | `AsyncQueue`, `Semaphore`, `SyncQueue` |
| `_internal/_replay.py`, `_retry.py`, `_scratchpad.py`, `_timeout.py` | replay state, retry predicate, task scratchpad, timeout coercion/check |
| `_internal/_runnable.py` | context/injection wrappers, `RunnableCallable`, `RunnableSeq`, coercion/async/iterator helpers |
| `_internal/_serde.py` | serializer allowlist construction and type traversal |
| `channels/*.py` | `BaseChannel`, `AnyValue`, `BinaryOperatorAggregate`, `DeltaChannel`, `EphemeralValue`, `LastValue`, `LastValueAfterFinish`, `NamedBarrierValue`, `NamedBarrierValueAfterFinish`, `Topic`, `UntrackedValue` |
| `managed/*.py` | `ManagedValue`, managed-value probe, last/remaining step managers |
| `pregel/_algo.py` | writes/tasks, interruption/local reads, apply writes, task preparation, task-id/path/scratchpad helpers |
| `pregel/_call.py`, `_checkpoint.py` | functional task invocation/identifiers/futures; snapshot/channel restore/replay helpers |
| `pregel/_draw.py`, `_executor.py`, `_io.py` | graph edge drawing; executors/gating; input/command/output mapping |
| `pregel/_loop.py`, `_read.py`, `_write.py` | sync/async loops; `ChannelRead`, `PregelNode`; channel-write records/runner |
| `pregel/_messages.py`, `_tools.py` | message-ID and model/tool stream handlers |
| `pregel/_retry.py`, `_runner.py` | attempts/watchdog, sync/async retry, `PregelRunner`, error/cancellation helpers |
| `pregel/_utils.py`, `_validate.py`, `debug.py` | graph/async/timeout/closure helpers; validation; debug mapping |
| `pregel/main.py`, `remote.py` | `NodeBuilder`, `Pregel`, runtime coercion; `RemoteGraph`, remote exception/config/header helpers |
| `stream/*.py` | protocol conversion, `StreamMux`, transformer types, run/subgraph streams, `StreamChannel`, event transformers |

Files containing only exports, constants, protocols, annotations, logging, or metadata have no independent executable callable: package `__init__.py` modules, `_constants.py`, `_typing.py`, `pregel/_config.py`, `pregel/_log.py`, `pregel/protocol.py`, `pregel/types.py`, `typing.py`, `version.py`, and `warnings.py`.
