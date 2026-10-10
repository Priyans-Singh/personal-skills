# `langgraph_checkpoint_aws` execution guide

Inspected source: package tree `langgraph_checkpoint_aws/`, distribution **1.2.3**, on 2026-09-20. This guide describes that package snapshot, not a service-level AWS guarantee. The package depends on LangGraph 1.x/checkpoint 3–4, boto3, and, for Valkey support, `valkey` and `orjson`.

## What it is

It supplies LangGraph persistence adapters in three distinct families. They share the `BaseCheckpointSaver` / `BaseStore` interfaces, but their storage models and consistency properties differ.

| Need | Class | Persistent identity / physical representation |
|---|---|---|
| AgentCore event checkpoints | `AgentCoreMemorySaver` | `memory_id` → `actor_id` + derived `session_id` → event blobs |
| Bedrock Agent Runtime Session checkpoints | `BedrockSessionSaver` / `AsyncBedrockSessionSaver` | `thread_id` session → deterministic checkpoint/write invocation → invocation steps |
| DynamoDB checkpoints | `DynamoDBSaver` | `thread_id` → namespace/checkpoint metadata item → payload chunk in DynamoDB or S3 |
| Valkey checkpoints | `ValkeySaver` / `AsyncValkeySaver` | hash-tagged thread keys: checkpoint blob, writes blob, and sorted checkpoint-id list |
| Long-term documents | `AgentCoreMemoryStore`, `DynamoDBStore`, `ValkeyStore` / `AsyncValkeyStore` | LangGraph `(namespace tuple, key)` items |
| Result cache | `ValkeyCache` | prefixed `(namespace, key)` string keys |

All checkpointers expect `config["configurable"]["thread_id"]`; AgentCore Memory additionally requires `actor_id`. A checkpoint has a checkpoint id, optional parent id, serialized state/metadata, channel values/versions, and task writes. `put()` returns a config pointing at the saved id; `get_tuple()` reconstructs `CheckpointTuple` including parent config and pending writes.

## Imports and optional dependency boundary

`__init__.py` exports the primary savers, stores, deferred wrapper, session clients, `SDK_USER_AGENT`, and `__version__`. Valkey imports are guarded: if either optional dependency fails to import, all Valkey public names become a callable placeholder that raises an installation-specific `ImportError`; `valkey_available` is false. The legacy top-level `saver`, `session`, `async_saver`, and `async_session` modules only re-export a Bedrock Sessions class and issue `DeprecationWarning`.

## Checkpoint execution paths

### 1. AgentCore Memory: append-only typed event log

`AgentCoreMemorySaver(memory_id, serde, limit, max_results, retry settings, **boto3_kwargs)` creates a `bedrock-agentcore` boto3 client. User-agent configuration is merged, preserving caller `Config.user_agent_extra`. `BedrockAgentCoreClientWithRetry` dynamically wraps **only** `create_event`; it retries `RetryableConflictException` at most three times by default with blocking exponential delays 0.1, 0.2, 0.4 seconds (capped at 2s). Other service calls are not retried by this wrapper.

```
put(config, checkpoint, metadata, new_versions)
  ├─ validate thread_id + actor_id; session_id = thread_id when namespace empty
  │  otherwise SHA-256(thread_id + "_" + namespace), to stay below service limits
  ├─ emit ChannelDataEvent per new version (missing value becomes `_empty`)
  ├─ emit CheckpointEvent (checkpoint sans channel_values; parent is input checkpoint_id)
  ├─ JSON event fields; arbitrary values = serde.dumps_typed → base64
  └─ batch blobs into CreateEvent payloads ≤100 items and ≤10 MB each
```

`put_writes()` requires a checkpoint id and appends a `WritesEvent`; `put_with_writes()` builds the above events plus one writes event per buffered group, allowing the saver to use a single batch sequence. It is not a transactional service primitive—large batches still split into multiple `create_event` calls.

`get_tuple()` pages `list_events(includePayloads=True)`, drops malformed blobs with a warning, groups events by checkpoint id, and selects an explicit id or `max(id)` as “latest”. It restores channel values by matching `(channel, version)`, builds parent config, and restores writes. If loaded `messages` contains AI tool calls without later `ToolMessage`s and no nonempty `__interrupt__` write exists, it adds synthetic error `ToolMessage`s so downstream Bedrock validation will accept the transcript. `list()` sorts ids descending, supports id/before/limit, but **ignores its `filter` argument**. A positive `limit` on source event parsing can omit older checkpoints; a warning is raised only when a next page exists. `delete_thread(thread_id, actor_id)` enumerates and deletes every service event: destructive and non-atomic.

The async methods run the synchronous implementation in an executor; `alist` first materializes the full sync list. `get_next_version` is a lexically sortable integer prefix plus random suffix, not a distributed clock.

### 2. Bedrock Sessions: typed façade over Session/Invocation APIs

`BedrockAgentRuntimeSessionClient` and its async counterpart turn frozen Pydantic, camelCase request models into boto3 parameters. Constructors accept an injected client or construct `bedrock-agent-runtime` with a supplied boto3 session/profile/region/secret credentials/endpoint/config. `SecretStr` values are unwrapped only while building client parameters. Each wrapper maps the boto response into a matching Pydantic response. Async client calls the sync boto client through an executor, so it is non-blocking to the event loop, not a native async SDK.

The saver maps a namespace to deterministic UUID invocation ids: one checkpoint invocation and one writes invocation. A checkpoint is a JSON `SessionCheckpoint` invocation step; channel values and metadata are base64 typed values in the model. `put()` creates the checkpoint invocation (suppresses only `ConflictException`) then stores a step keyed by checkpoint id. `put_writes()` creates the writes invocation, reads its latest step, merges new writes using LangGraph write indexes, and saves a replacement step only when it has new content. `get_tuple()` finds a requested step or pages steps until it finds a checkpoint marker, retrieves writes, retrieves task sends from the parent’s writes, then calls `construct_checkpoint_tuple()`.

`list()` pages steps, fetches each full step, discards non-checkpoint payloads, performs metadata equality filters locally, and honors `before`/limit. A missing Session resource becomes empty results in get/list; other `ClientError`s surface. Sync and async saver implementations are parallel; the async saver uses the async façade. There is no implemented saver `delete_thread` in this backend’s public method set.

### 3. DynamoDB + optional S3: metadata/reference/payload split

`DynamoDBSaver` creates DynamoDB (and optionally S3) clients with an adaptive botocore retry config (`max_attempts=5`) and an identifying user-agent. The data layout is deliberately indirect:

```
checkpoint base item: PK=checkpoint#{thread}, SK=checkpoint#{ns}#{id}
  └─ ref item/payload: serialized checkpoint + metadata, in DynamoDB chunk or S3 object
writes base/ref/payload: PK=writes#{thread}#{ns}#{checkpoint}, SK=task/index
```

`CheckpointSerializer` obtains a typed serde payload; if enabled, it gzip-compresses only payloads at least 1 KiB whose size shrinks by at least 10%. Decompression failure is raised as `ValueError`. `StorageStrategy` chooses S3 only when configured and bytes exceed 350 KiB; otherwise it stores a DynamoDB chunk. S3 keys can be prefixed. With TTL and S3 enabled, construction mutates bucket lifecycle configuration, adding a scoped lifecycle rule and TTL tag; this is an externally visible control-plane write.

Repository `put_checkpoint()` writes base metadata then stores/replaces payload; writes are serialized independently, deduplicated/conditional where applicable. Reads resolve base → reference → payload, skip invalid/missing payloads while searching for a usable checkpoint, deserialize, and then fetch writes. The saver merges `config["metadata"]` into supplied metadata; `new_versions` is unused. Its async methods use an executor (with lazy async list iteration).

`list()` requires thread id; namespace, `before`, metadata filter, and limit route to the repository. `delete_thread()` finds every checkpoint namespace/id, deletes writes before checkpoints and attempts payload cleanup in DynamoDB/S3 batches. These are multi-request operations: partial failure can leave metadata or payload orphans. S3/DynamoDB batch deletion handles unprocessed/failed items but cannot make the cross-service deletion atomic.

### 4. Valkey checkpoint savers

Base keys include a `{thread_id}` hash tag so related keys stay colocated in a cluster:

```
checkpoint:{thread}:namespace:checkpoint-id    typed checkpoint + base64 metadata
writes:{thread}:namespace:checkpoint-id        JSON list of typed/base64 write records
thread:{thread}:namespace                      sorted checkpoint ids
```

`ValkeySaver.put()` serializes the checkpoint, writes it with optional TTL, and adds the id to the thread sorted set. `get_tuple()` selects a requested id or latest sorted-set member, pipelines checkpoint+writes reads, then deserializes. `list()` walks ids in descending order and filters decoded metadata locally. `delete_thread()` scans namespace thread sets and deletes checkpoint/writes/index keys. The synchronous saver’s `aget_tuple`, `alist`, and `aput` deliberately raise `NotImplementedError`; use `AsyncValkeySaver` for async operations.

Writes use WATCH/MULTI optimistic read-modify-write, retrying `WatchError` up to 100 attempts. Existing positional `(task_id, idx >= 0)` writes are preserved (replay-safe); special negative-index writes overwrite in place. A malformed writes blob is warned about and treated as empty, so a later write replaces it. Optional TTL is applied to values/indexes as implemented, therefore expiry can make a thread history incomplete. AsyncSaver implements the same protocol with async pipelines and refuses sync methods.

`AgentCoreValkeySaver` is a separate compatibility implementation: it preserves AgentCore’s actor/session hierarchy and stores checkpoint, writes, per-channel data, and a session checkpoint index in Valkey. It retries connection/timeout errors with its own sync/async exponential retry helpers, uses `ValkeyCheckpointerConfig` key prefixes, reconstructs AgentCore-style event state, and provides executor-backed async entry points.

## Stores and cache

### AgentCoreMemoryStore

`batch()` dispatches `PutOp`, `GetOp`, `SearchOp`, and returns `[]` for unsupported `ListNamespacesOp`; unknown operations raise `ValueError`. Put requires `value["message"]` to be a LangChain `BaseMessage` and namespace exactly `(actor_id, session_id)`. It converts only unsaved nonempty human/AI/tool/system messages to `USER`/`ASSISTANT`/`TOOL`/`OTHER` conversational events. Delete (`PutOp.value is None`) only logs a warning—no delete occurs.

Get calls `get_memory_record` by key (not namespace); not-found returns `None`. Search requires a query, calls `retrieve_memory_records` with `namespacePath` by default or exact `namespace` if configured, and converts service rows to LangGraph items. Missing/unparseable timestamps are replaced with current UTC time (an inference-friendly safe value, not a source timestamp). `abatch()` is executor-backed.

### DynamoDBStore

This is a separate document table: `PK` is namespace joined by `:`, `SK` is key, with serialized dict `value`, timestamps, optional `expires_at`, and optional embedding. Constructor requires a supplied session/region or AWS region environment. `setup()` creates the table if necessary, creates/validates a vector index when configured, waits for index readiness, and enables table TTL. These are control-plane mutations, unlike normal store construction.

`batch()` routes get, put/delete, semantic/basic search, and list-namespaces. Put validates dict values, computes timestamps/TTL, extracts configured JSON paths for embeddings, then writes item; deletion is a delete. Reads can refresh TTL. Filtering is local recursive equality matching. Vector search uses configured embedding query + DynamoDB vector index and transforms distance to a score; it is explicitly eventually consistent, so immediate post-put searches can miss an item. `abatch()` is executor-backed.

### ValkeyStore / AsyncValkeyStore

Documents are Valkey hashes under namespaced keys; value JSON, timestamps, and optional embedding/index fields are converted by `DocumentProcessor`. `put` validates namespace/value, uses `NotProvided` to distinguish caller TTL from default TTL, generates embeddings only when requested/configured, and writes/deletes hashes. `get`, `search`, and list-namespaces dispatch through LangGraph `batch` operations; direct convenience methods call those paths. TTL may be refreshed on reads/search results according to config.

Search is capability-selected in priority order: RediSearch vector query when index+embedding are available; otherwise full hash scan with text scoring; otherwise key-pattern scan. Strategy managers use adapters to normalize bytes/str, parse documents, filter, namespace-match, and paginate. `setup()` creates a RediSearch index only if configured; a missing module/index falls back rather than pretending semantic search happened. The async store detects whether client methods return awaitables and either awaits them or moves sync work to a thread; its synchronous convenience methods raise guidance errors.

### ValkeyCache

Cache keys are `prefix + '/'.join(namespace) + '/' + key`; prefix is normalized to end in `:` or `/`. Values are `type-tag:binaries` from the LangGraph serde. `get()`/`set()` call `asyncio.run()` over `aget()`/`aset()`—do not call those synchronous methods from a running event loop. Reads use `MGET`; malformed individual entries are logged and omitted, while a general unexpected MGET error returns `{}` (connection/timeout re-raise). Writes pipeline at most 100 entries and apply per-entry TTL or default TTL; invalid TTL entries are skipped. `clear()` uses blocking `KEYS` then deletes in chunks of 1,000: broad prefixes are operationally expensive and destructive; failures in individual delete batches are logged and swallowed.

## Operational semantics and safe choices

- Credentials are passed to boto3 client construction (explicit secret arguments for Bedrock Session clients are unwrapped once). This package does not persist credentials; use standard AWS credential providers/roles where possible.
- None of the multi-call persistence/deletion flows provides distributed transactions. Treat retryable writes as idempotency-sensitive, especially AgentCore event appends and cross DynamoDB/S3 cleanup.
- Use a native async saver/store for high-concurrency code. Executor-backed “async” variants protect the event loop but still consume worker threads and invoke synchronous network clients.
- Call `DynamoDBStore.setup()` and Valkey store `setup()` intentionally; they can create tables/indexes/TTL settings. Do not grant that authority merely to serve read/write requests.
- `DeferredCheckpointSaver` reduces I/O but loses mid-run durability: it retains only the latest checkpoint and all writes in memory until `flush`/`aflush` or the corresponding exit context.

## DeferredCheckpointSaver lifecycle

The wrapper rejects nested wrappers, uses a thread lock, intercepts puts/writes, and serves a matching buffered tuple before consulting the underlying saver. `list` intentionally excludes buffered state. On flush it clears buffers before network I/O to avoid duplicate persistence; failures restore the checkpoint only if no newer checkpoint won the race, and leave failed sequential writes at the queue head for retry. With `batch_writes=True`, a saver implementing `put_with_writes`/`aput_with_writes` receives one checkpoint plus public `PendingWrite` records. `flush_on_exit` and `aflush_on_exit` always flush in `finally`, even if the graph raises; `clear()` explicitly discards buffered state.

## Source coverage

Every Python file was inventoried, including package initializers, compatibility shims, models/constants/exceptions/types, all Valkey search adapters/strategies, and the two bundled backend README files. The mechanically checked callable/class catalogue is in [langgraph_checkpoint_aws_callable_index.md](langgraph_checkpoint_aws_callable_index.md). It distinguishes thin aliases/model declarations from execution-bearing code so helpers were not silently omitted.
