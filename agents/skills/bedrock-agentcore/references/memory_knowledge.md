# Bedrock AgentCore Memory: Internal Working Reference

Last inspected: 2026-09-19
Source: the installed `bedrock_agentcore.memory` package in this repository's `.venv`.

This is an implementation-oriented guide, not merely an API list. It follows what happens from an agent turn through AgentCore Memory, and then maps every module and callable in the installed package. The SDK's preferred application API is `MemorySessionManager`; `MemoryClient` remains supported as a higher-level but legacy-compatible client.

## The Mental Model

AgentCore Memory has two different stores built from the same input stream:

```text
application messages
  -> create_event(memoryId, actorId, sessionId, payload, metadata)
  -> short-term memory (STM): ordered event history and branches
  -> asynchronous strategy extraction
  -> long-term memory (LTM): memory records in strategy namespaces
  -> retrieve_memory_records(search query + namespace/namespacePath)
  -> agent prompt context
```

An **event** is the durable input unit. Its payload can contain several conversational messages or blobs. An event belongs to exactly one `(memory_id, actor_id, session_id)` stream, optionally with a branch. It is not itself an LTM record.

An LTM **memory record** is output created later by a configured strategy. Therefore `create_event()` succeeding proves STM was accepted; it does **not** prove that semantic, preference, summary, or episodic extraction has completed. Retrieval is eventually consistent.

### The identity hierarchy

```text
Memory resource
├─ Actor: a person, customer, or other durable identity
│  ├─ Session: one conversation for that actor
│  │  ├─ Event: one persisted group of messages
│  │  └─ Branch: alternate history rooted at a prior event
│  └─ LTM records: retrieved through strategy namespace(s)
└─ Strategies: server-side extraction definitions
   └─ Namespace templates resolve with actor/session/strategy identity
```

Use an actor-only namespace (for example `/preferences/{actorId}/`) when a fact should be recalled in later sessions. A namespace containing `{sessionId}` intentionally limits recall to that session.

## Package Map and Import Surface

```python
from bedrock_agentcore.memory import (
    Actor, MemoryClient, MemoryControlPlaneClient,
    MemorySession, MemorySessionManager,
)
```

| File | Role |
|---|---|
| `client.py` | Compatibility/high-level client; creates resources, events, strategies, and hides old/new API shape differences. |
| `session.py` | Recommended session-first data-plane API. |
| `controlplane.py` | Explicit resource/strategy lifecycle client. |
| `constants.py` | Strategy, role, status, message, and retrieval value objects. |
| `models/` | Lightweight response wrappers and typed metadata filter builders. |
| `integrations/strands/` | Adapter that makes AgentCore back Strands sessions and long-term `MemoryStore`s. |

There are two AWS service clients:

| Plane | boto3 service | Changes / reads |
|---|---|---|
| Control plane | `bedrock-agentcore-control` | Memory resources and strategy configuration. |
| Data plane | `bedrock-agentcore` | Events, branches, records, actors, sessions, extraction jobs. |

`MemoryClient` constructs both. `MemorySessionManager` only constructs the data-plane client because it consumes an existing `memory_id`.

## A Complete Turn, Step by Step

`MemorySession.process_turn_with_llm()` is the clearest core execution path:

```python
from bedrock_agentcore.memory import MemorySessionManager
from bedrock_agentcore.memory.constants import RetrievalConfig

manager = MemorySessionManager(memory_id="mem-123", region_name="us-east-1")
session = manager.create_memory_session("user-42", "chat-99")

def call_model(user_input, records):
    context = "\n".join(r.get("content", {}).get("text", "") for r in records)
    return my_model(f"<memory>{context}</memory>\n{user_input}")

records, answer, event = session.process_turn_with_llm(
    user_input="What restaurant do I usually prefer?",
    llm_callback=call_model,
    retrieval_config={
        "/preferences/{actorId}/": RetrievalConfig(top_k=5, relevance_score=0.5),
    },
)
```

Execution is strictly sequential:

1. `_retrieve_memories_for_llm` resolves namespace placeholders with the actor, session, and selected strategy ID.
2. For each configured namespace it calls `retrieve_memory_records`; if configured, it filters records below `relevance_score` locally.
3. The synchronous callback receives `(user_input, retrieved_records)` and must return a `str`. The async twin awaits it.
4. `_save_conversation_turn` builds a USER and ASSISTANT `ConversationalMessage`, then `add_turns` serializes them into one `create_event` payload.
5. The data plane returns an event, wrapped as `Event`. Extraction is initiated server-side and finishes independently.

There is no transaction across retrieval, model invocation, and event write. If model execution fails, no event is written. If the event write fails after the model answers, the caller has an answer but no stored turn and must decide whether to retry safely.

## `constants.py`: Values and Defaults

| Type | Values / use |
|---|---|
| `StrategyType` | Wire strategy wrapper names: semantic, summary, preference, episodic, custom. |
| `MemoryStrategyTypeEnum` | API-normalized types: `SEMANTIC`, `SUMMARIZATION`, `USER_PREFERENCE`, `EPISODIC`, `CUSTOM`. |
| `OverrideType` | Custom strategy override kinds used to wrap extraction/consolidation/reflection configuration. |
| `MemoryStatus` | `CREATING`, `ACTIVE`, `FAILED`, `UPDATING`, `DELETING`. Wait helpers poll these. |
| `MemoryStrategyStatus` | Per-strategy `CREATING`, `ACTIVE`, `DELETING`, `FAILED`. |
| `Role` | Narrow `USER` and `ASSISTANT` pair. |
| `MessageRole` | Event conversational roles: `USER`, `ASSISTANT`, `TOOL`, `OTHER`. |
| `ConfigLimits` | Compatibility constants for trigger/context limits; not an active validator. |
| `ConversationalMessage(text, role)` | Dataclass. `__post_init__` rejects a non-string text or non-`MessageRole` role. Serializes to `payload[].conversational`. |
| `BlobMessage(data)` | Dataclass. Serializes arbitrary value to `payload[].blob`; no local shape validation. |
| `RetrievalConfig` | Pydantic model: `top_k` 2–100 (default 10), score 0–1 (default 0), optional `strategy_id` and `retrieval_query`. |

`DEFAULT_NAMESPACES` supplies templates when a built-in strategy is created without one: semantic and preferences are actor scoped; summary and episodic are actor+session scoped. Custom defaults to `custom/{actorId}/{sessionId}/` in the client helper.

## `models/`: Responses and Filters

`DictWrapper` is deliberately thin: `obj.field` means `dict.get("field")` and therefore returns `None` for missing keys; `obj["field"]` preserves ordinary dictionary `KeyError` behavior. `get`, `keys`, `values`, `items`, containment, `__dir__`, `__repr__`, and `__str__` all delegate to its `_data` dictionary. `ActorSummary`, `Branch`, `Event`, `EventMessage`, `MemoryRecord`, and `SessionSummary` add no behavior; they label a wrapped response shape.

### Event metadata filter builders (`models/filters.py`)

`StringValue.build(value)`, `LeftExpression.build(key)`, and `RightExpression.build(value)` construct the nested data-plane shape. `EventMetadataFilter.build_expression(left, operator, right=None)` stores `operator.value` and only includes `right` when supplied.

`OperatorType` accepts `EQUALS_TO`, `EXISTS`, and `NOT_EXISTS`. `EXISTS` and `NOT_EXISTS` must not need a right operand. This filter is passed as `eventMetadata` to `list_events`.

### LTM metadata filter builders

`MemoryRecordLeftExpression.build(key)` chooses an indexed key. `MemoryRecordRightExpression` has `build_string`, `build_number`, `build_datetime`, and `build_string_list`. `MemoryMetadataFilter.build_expression` validates the operator/right pairing locally:

| Operator | Required right builder |
|---|---|
| `EQUALS_TO` | `build_string` |
| `BEFORE`, `AFTER` | `build_datetime` |
| `CONTAINS` | `build_string_list` |
| comparison operators | `build_number` |
| `EXISTS`, `NOT_EXISTS` | none; supplying one raises `ValueError` |

`MetadataValueType` and `IndexedKey.build(key, value_type)` define provisioned indexed fields. An indexed key has a key and `STRING`, `STRINGLIST`, or `NUMBER` type. Indexes are supplied at resource creation; the client documents that they cannot be removed.

## `MemorySessionManager`: Recommended Data-Plane API

### Construction and plumbing

```python
MemorySessionManager(memory_id, region_name=None, boto3_session=None,
                     boto_client_config=None)
```

The constructor records the immutable memory ID, resolves a region in this order: explicit region, supplied boto3 session region, `AWS_REGION`, default boto3 session region, then `us-west-2`. An explicit region that conflicts with the supplied session region raises `ValueError`. `_build_client_config` appends `bedrock-agentcore-sdk` to `user_agent_extra`. `_configure_timestamp_serialization` replaces botocore's timestamp serializer so Python `datetime` values become fractional Unix seconds, preserving milliseconds.

`__getattr__` forwards only an allowlist of raw data-plane methods—record/event CRUD and batch record methods—to its boto3 client, accepting snake_case keyword aliases. It does not turn arbitrary SDK operations into magic methods.

### Manager method map

| Method | What it does / important behavior |
|---|---|
| `process_turn_with_llm` | Retrieve configured LTM, call a synchronous `(input, records) -> str` callback, write one USER+ASSISTANT event, return `(records, response, Event)`. |
| `process_turn_with_llm_async` | Same flow but awaits the callback. Retrieval and save still use synchronous boto3 in this implementation. |
| `_retrieve_memories_for_llm` | Resolves `{actorId}`, `{sessionId}`, `{strategyId}`; joins optional retrieval query with user text; concatenates every namespace's results. |
| `_save_conversation_turn` | Internal two-message `add_turns` call. |
| `add_turns` | Requires nonempty `ConversationalMessage`/`BlobMessage` list; serializes payload; defaults timestamp to UTC now; returns wrapped `Event`. |
| `fork_conversation` | Adds an event with `branch={rootEventId, name}`. The new branch begins from that root event. |
| `list_events` | Paginates (up to 100 per call, hard safety 1,000 loops), supports branch inheritance, event metadata filters and `include_payload`; wraps results as `Event`. |
| `list_branches` | Uses the service event listing to identify branch structure and returns `Branch` objects. |
| `get_last_k_turns` | Reads events then converts payload messages into the last `k` conversational turns. Its unit is turn/message grouping, not LTM records. |
| `get_event` / `delete_event` | Get or delete a concrete STM event for this identity. |
| `search_long_term_memories` | Semantic LTM retrieval. Use exactly one of deprecated `namespace_prefix`, `namespace`, or hierarchical `namespace_path`; supports `strategy_id` and indexed `metadata_filters`. |
| `list_long_term_memory_records` | Lists records without a semantic query, using the same namespace choice rules. |
| `list_actors` | Lists actors that have events in this memory. |
| `get_memory_record` / `delete_memory_record` | Read/delete one LTM record by ID. |
| `list_actor_sessions` | Lists sessions belonging to one actor. |
| `delete_all_long_term_memories_in_namespace` | Pages records in one exact namespace and batch-deletes them. It is destructive and returns its operation result. |
| `create_memory_session` | Generates a UUID session ID when omitted and returns a bound `MemorySession`. |

`MemorySession` is a convenience binding of manager + `(memory_id, actor_id, session_id)`. `_construct_session_dict` is its wrapped identity representation. Every public method delegates to the corresponding manager method while inserting actor/session values: `add_turns`, `fork_conversation`, both LLM methods, history, event and record CRUD, search/list records, `list_actors`, `list_events`, and `list_branches`. `get_actor()` returns a bound `Actor`; `Actor._construct_session_dict` forms its identity wrapper and `list_sessions()` delegates to `list_actor_sessions`.

## `MemoryClient`: High-Level / Compatibility Client

`MemoryClient(region_name=None, integration_source=None, boto3_session=None)` creates both service clients and appends integration telemetry to the user agent. Its `__getattr__` separately allowlists data-plane and control-plane boto3 operations, converting snake-case keyword names.

It intentionally absorbs an API naming migration. Requests use old names such as `memoryStrategies` and `memoryStrategyId`; `_normalize_memory_response` ensures returned objects expose both old and new aliases: `id`/`memoryId`, `strategies`/`memoryStrategies`, `strategyId`/`memoryStrategyId`, `type`/`memoryStrategyType`, and `namespaceTemplates`/deprecated `namespaces`.

### Resource lifecycle

| Method | Behavior |
|---|---|
| `create_memory` | Adds default namespaces, generates `clientToken`, calls control-plane create, normalizes result. Supports description, retention days, execution role, delivery resources, indexes. |
| `create_or_get_memory` | Calls create-and-wait; on an “already exists” validation error, searches listed memories for a name-prefix match. This is convenient, but that prefix fallback deserves care with similarly named resources. |
| `create_memory_and_wait` | Create then poll until `ACTIVE`, or raise failure/timeout. |
| `get_memory_strategies`, `get_memory_status`, `list_memories` | Normalized reads. `list_memories` paginates. |
| `delete_memory` / `delete_memory_and_wait` | Start deletion; the latter polls until removal. |
| `_wait_for_memory_active` | Polls status; returns full normalized memory on `ACTIVE`, raises on `FAILED` or timeout. |

### Events, retrieval, and branches

| Method | Behavior |
|---|---|
| `retrieve_memories` | Calls data-plane retrieval using an exact `namespace` or subtree `namespace_path`; takes query, actor, `top_k`, metadata filters. It catches `ClientError`, logs it, and returns an empty list—use raw boto3 or the Strands store if retrieval failure must propagate. |
| `create_event` | High-level text/role event writer. Converts pairs/objects to conversational payload, supports timestamp, branch, metadata and extraction mode. |
| `create_blob_event` | Writes a blob payload event. |
| `save_conversation` | Deprecated alias; use `create_event`. |
| `process_turn_with_llm` | Legacy counterpart of session manager flow: retrieve, invoke callback, persist pair. |
| `list_events` | Paginated STM listing with branch, parent, metadata and payload controls. |
| `list_branches`, `list_branch_events`, `get_conversation_tree` | Discover the branch graph and retrieve its events. |
| `merge_branch_context` | Flattens branch (and optionally parent) payload into messages for an LLM context. |
| `get_last_k_turns` | Retrieves/reformats the final `k` conversation turns. |
| `fork_conversation` | Creates an event on a named branch rooted at an existing event. |
| `wait_for_memories` | Polls a retrieval query for extraction. Reliable only for an empty, exact namespace; no wildcards; a populated namespace may make it return too early. |

### Strategy helpers

Strategies are control-plane configuration that cause eventual LTM generation from future events. Every `add_*_strategy_and_wait` calls its non-waiting sibling then waits for the memory resource to return to `ACTIVE`.

| Method family | Strategy produced |
|---|---|
| `add_semantic_strategy[_and_wait]` | Extracts durable factual/semantic memory. |
| `add_summary_strategy[_and_wait]` | Consolidates a session summary. |
| `add_user_preference_strategy[_and_wait]` | Extracts actor preferences. |
| `add_episodic_strategy[_and_wait]` | Keeps session episodes plus reflection namespace/templates. |
| `add_custom_semantic_strategy[_and_wait]` | Semantic strategy with caller-supplied extraction/consolidation model/prompt configuration. |
| `add_custom_episodic_strategy[_and_wait]` | Custom extraction, consolidation, and reflection. |
| `modify_strategy` / `delete_strategy` | Thin modify/delete strategy operations. `namespaces` is deprecated in favor of `namespace_templates`. |
| `update_memory_strategies[_and_wait]` | Atomically submits add/modify/delete groups; modifying reads existing strategy type so `_wrap_configuration` can use the correct service wrapper. |
| `add_strategy` | Generic add, but warns because the resource may remain `CREATING`; prefer typed wait helpers. |

Private helpers complete the behavior: `_add_strategy` delegates through grouped update; `_add_default_namespaces` deep-copies and fills missing templates; `_validate_namespace` warns, rather than rejects, unrecognized placeholder usage; `_validate_strategy_config` checks each namespace; `_try_get_override_type` returns `None` for service values the enum does not model; `_wrap_configuration` applies the required nested extraction, consolidation, and reflection configuration wrappers for built-in/custom override forms.

## `MemoryControlPlaneClient`: Explicit Lifecycle API

This older dedicated client uses `BEDROCK_AGENTCORE_CONTROL_SERVICE` to override the service name and `BEDROCK_AGENTCORE_CONTROL_ENDPOINT` to override its endpoint. `environment` is logged only; it is not sent as a service parameter.

| Method | Behavior |
|---|---|
| `create_memory` | Builds raw control-plane request; optional wait for `ACTIVE`. |
| `get_memory`, `list_memories` | Resource inspection; list paginates. |
| `update_memory` | Updates description/expiry/role/delivery and grouped add/modify/delete strategy configuration; can wait. |
| `delete_memory` | Deletes resource, with optional waits for strategies/deletion. |
| `add_strategy` | Adds one raw strategy; can wait. |
| `get_strategy` | Finds one strategy in a resource response. |
| `update_strategy` | Builds a `modifyMemoryStrategies` request; accepts deprecated `namespaces` or preferred templates. |
| `remove_strategy` | Submits strategy deletion; can wait. |
| `_wait_for_memory_active`, `_wait_for_strategy_active` | Specializations over `_wait_for_status`. |
| `_wait_for_status` | Poll loop for a target resource status, optionally checking all strategies; raises on failure/timeout. |

Prefer `MemorySessionManager` for conversations and `MemoryClient` for the SDK's shorthand builders. Use this class when an application intentionally wants near-raw control-plane lifecycle calls and endpoint overrides.

## Strategy and Namespace Design

```python
client.create_memory_and_wait(
    name="support-memory",
    strategies=[
        {"userPreferenceMemoryStrategy": {
            "name": "preferences",
            "namespaceTemplates": ["/preferences/{actorId}/"],
        }},
        {"semanticMemoryStrategy": {
            "name": "facts",
            "namespaceTemplates": ["/facts/{actorId}/"],
        }},
        {"summaryMemoryStrategy": {
            "name": "session-summary",
            "namespaceTemplates": ["/summaries/{actorId}/{sessionId}/"],
        }},
    ],
)
```

Provisioning and retrieval use different stages of placeholder resolution. Strategies retain templates for server-side extraction. A retrieval caller must provide a concrete `namespace` or `namespace_path`; `MemorySessionManager` resolves its known placeholders before calling the data plane. Exact namespace search is a single prefix target; `namespace_path` searches descendants. Do not confuse the two: broad tree search can mix unrelated facts if the hierarchy is weak.

## LangGraph Integration: `langgraph-checkpoint-aws`

This is an application-side adapter, not part of the `bedrock_agentcore.memory` SDK. It is useful when a LangGraph graph needs both its resumable checkpoint state and AgentCore-backed memory. Installed adapter source inspected: `langgraph-checkpoint-aws` 1.2.3 on 2026-09-20. Its complete package guide remains standalone because it also covers unrelated DynamoDB/S3, Valkey, and Bedrock Sessions backends.

| Adapter | Identity and behavior |
|---|---|
| `AgentCoreMemorySaver(memory_id, ...)` | Requires LangGraph `configurable.thread_id` and `configurable.actor_id`. Writes checkpoint state as typed base64 JSON **blob events** under AgentCore `(memory_id, actor_id, session_id)`. Empty checkpoint namespace uses `thread_id` as session id; a nonempty namespace uses deterministic SHA-256 of `thread_id + "_" + namespace` to fit the session-id limit. This is STM event persistence, not LTM extraction. |
| `AgentCoreMemoryStore(memory_id, hierarchical_search=True, ...)` | Implements LangGraph `BaseStore`. A `PutOp` requires namespace exactly `(actor_id, session_id)` and `value["message"]` as a LangChain `BaseMessage`; it sends a conversational event. A `SearchOp` calls `retrieve_memory_records` under `namespacePath` (or exact `namespace` when disabled), so results are strategy-extracted LTM and eventually consistent. |

Checkpoint save flow: `put()` emits one channel-data blob per new channel version plus one checkpoint blob; `put_writes()` appends a writes blob. Values use LangGraph typed serde then base64. Batches are split to at most 100 payload items and 10 MB per `create_event` request. `get_tuple()` pages events, drops undecodable blobs with a warning, groups blobs by checkpoint id, chooses an explicit id or lexical maximum, then rebuilds channel values and pending writes. It patches orphaned AI tool calls with synthetic error `ToolMessage`s unless an interrupt write is present, preventing invalid restored transcripts from reaching Bedrock.

`create_event` retries only `RetryableConflictException`: default maximum three retries, blocking exponential backoff starting at 100 ms and capped at 2 s. Reads/deletes have no equivalent adapter retry. Event append, checkpoint reconstruction, and deletion are multi-call/non-transactional. `delete_thread(thread_id, actor_id)` deletes every event in that derived AgentCore session and is destructive. `list()` supports id/before/limit but ignores its metadata `filter` parameter.

For the store, delete `PutOp` (`value is None`) is intentionally unsupported: it logs a warning and performs no remote deletion. It also returns `[]` for `ListNamespacesOp`. Therefore use the SDK `MemorySessionManager` or raw data-plane client for event/record deletion, branch behavior, or complete STM/LTM operations. The adapter's async methods run sync boto3 work in an executor; they avoid blocking the event loop but are not native async data-plane calls.

## Strands Integration, Path 1: Session Persistence

`integrations/strands/config.py` defines the configuration for `AgentCoreMemorySessionManager`, which implements Strands `RepositorySessionManager` and `SessionRepository`.

| Item | Meaning |
|---|---|
| `normalize_metadata` | Converts plain string values to `{"stringValue": value}`; explicit shaped values survive. |
| `PersistenceMode.FULL` | Default: persist session, agent state, and messages. |
| `PersistenceMode.NONE` | No AgentCore writes, but local state and retrieval injection still operate. |
| Strands `RetrievalConfig` | `top_k` 1–1000, score default .2, optional strategy and initialization query. This differs from core `RetrievalConfig`. |
| `AgentCoreMemoryConfig` | Requires memory/session/actor IDs; controls retrieval, 1–100 message batch size, periodic flush, XML context tag, restored tool filtering, metadata defaults/provider, persistence, and async hooks. |

`AgentCoreMemorySessionManager` serializes Strands session state into AgentCore events. Its constructor initializes clients/buffers/hooks, validates config, and may start a flush timer. `_get_monotonic_timestamp` prevents ordering collisions by moving a desired timestamp forward if needed. `_build_metadata` merges default metadata, dynamic provider, per-call metadata, and internal keys in that order.

| Method group | What occurs |
|---|---|
| `create_session`, `read_session`, `delete_session` | Store/discover/delete session state in AgentCore event history. Deletion deletes the session's associated data. |
| `create_agent`, `read_agent`, `update_agent` | Persist and restore a Strands agent state snapshot. |
| `create_message`, `read_message`, `update_message`, `list_messages` | Event-backed Strands message CRUD/history. Buffered messages can be updated before a flush. |
| `_filter_restored_tool_context` | Optionally removes historical tool-use/result blocks, avoiding stale tool context on restoration. |
| `append_message` | Adds an Agent message using the AgentCore event ID as its message ID. |
| `retrieve_customer_context` | Searches configured LTM and injects it for regular Agent invocations. |
| `register_hooks`, `initialize` | Attach lifecycle callbacks to Strands. In `async_mode`, callbacks use `asyncio.to_thread`; construction-time restoration still blocks because Strands initialization hooks are synchronous. |
| `_flush_messages_only`, `_flush_agent_states_only`, `_flush_messages` | Writes buffered items; batch thresholds and timer determine when these execute. |
| `pending_message_count`, `pending_agent_state_count` | Observability for outstanding buffers. |
| `close`, context-manager methods | Flush, stop timer, and close. Always close a long-lived manager. |
| `_start_flush_timer`, `_interval_flush_callback`, `_stop_flush_timer` | Lifecycle of periodic persistence. |

`bedrock_converter.py`'s `AgentCoreMemoryConverter` implements the session wire translation: `_filter_empty_text` removes text invalid for Bedrock Converse; `message_to_payload` turns a Strands `SessionMessage` into `(role, text)` pairs; `events_to_messages` restores events; `total_length` and `exceeds_conversational_limit` enforce conversational payload limits. `converters/protocol.py` declares this converter contract. `converters/openai.py` offers `OpenAIConverseConverter` with the same three public conversions for OpenAI-format STM payloads.

## Strands Integration, Path 2: Native Long-Term `MemoryStore`

This path is separate from the session manager: it makes AgentCore LTM look like Strands' native `MemoryStore`. The store consumes an already-provisioned resource and never creates strategies.

```python
from strands.memory import MemoryManager
from bedrock_agentcore.memory.integrations.strands.memorystore import AgentCoreMemoryStore

store = AgentCoreMemoryStore(
    memory_id="mem-123", actor_id="user-42", session_id="chat-99",
    namespace="/preferences/{actorId}/", writable=True, extraction=True,
)
agent_memory = MemoryManager(stores=[store])
```

### `memorystore/store.py`

`_create_memory_client` resolves region (explicit, boto session, `AWS_REGION`, default) and creates `MemoryClient(..., integration_source="strands")`.

`AgentCoreMemoryStore.__init__` requires exactly one of exact `namespace` and subtree `namespace_path`, resolves only `{actorId}` and `{sessionId}`, then rejects unexpanded braces. It validates every numeric parameter, clamps future search wire calls to topK 100, builds a sender only for `writable=True`, and warns if extraction was supplied to a read-only store.

| Method | Behavior |
|---|---|
| `search(query, options=None)` | Calls raw data-plane retrieval in a worker thread. Per-call result option overrides default. If `min_score` is set, over-fetches then filters client-side. Errors deliberately propagate so `MemoryManager` can apply partial-failure policy. |
| `add_messages(messages, context=None)` | Requires writable store and delegates role-preserving writes to sender. There is intentionally no flat `add()` because it would discard role/turn semantics. |
| `_to_entry(record)` | Converts a record to `MemoryEntry`; places service identifiers in reserved `_id`, `_score`, `_namespaces`, `_createdAt` metadata. |
| `_format_created_at` | Normalizes datetimes to millisecond UTC ISO-8601; non-datetime values become strings. |

### `memorystore/sender.py`: write mechanics

`AgentCoreEventSender` is the write engine. `_map_role` maps Strands user to `USER` and all supported assistant content to `ASSISTANT`; `_extract_text` joins nonblank text blocks; `_is_user_or_assistant_with_text` rejects tool-only, blank, and unsupported messages.

`send_batch` validates metadata before any network write, groups eligible messages, launches all groups concurrently, and shields the operation from cancellation until every thread-backed boto call settles. `_group_into_events` starts a new event when metadata changes or the turn cap is reached. `_send_event` writes data-plane `create_event` with UTC time, payload, metadata, optional extraction mode, and deterministic token. `_token_for_sequence_numbers` derives idempotency from identity, run ID, and sequence range only when all sequence numbers exist. `_send_all` collapses any group failures into Strands `AggregateMemoryError`.

`_metadata_scalar_string` permits only strings, finite numbers, and booleans; `_to_agentcore_metadata` validates AgentCore's allowed character set and wraps values as `stringValue`. Invalid metadata fails locally rather than partially writing sibling events.

### Multi-namespace factory and types

`create_agentcore_memory_stores` validates a nonempty namespace list, shares one `MemoryClient`, makes the first non-opted-out namespace the writer when extraction is enabled, and calls `_assert_writable_topology`. The topology rule is fundamental: only one store may write for one `(memory, actor, session)` stream, because event creation has no namespace field. Multiple writers would submit duplicate conversation events.

`memorystore/types.py` contains TypedDict contracts, not runtime service calls: connection config; exact/subtree store configs; event sender and namespace configs; extraction config; factory input; metadata provider; extraction mode; and validation/namespace utility functions. It defines defaults (region, result count, over-fetch multiplier, event turn cap), maximum `topK=100`, reserved metadata prefix, `assert_non_empty`, concrete namespace expansion, unresolved-template rejection, and namespace slug creation. `memorystore/__init__.py`, `integrations/__init__.py`, `strands/__init__.py`, and `converters/__init__.py` are re-export boundaries.

## Per-File Callable Index

This index makes the implementation coverage explicit. A method named here is either described above in depth or is a façade/helper whose exact role is stated here.

### `client.py`

| Callable | Use |
|---|---|
| `__init__` | Builds authenticated control/data clients and telemetry user agent. |
| `__getattr__` | Safely forwards only allowlisted raw boto3 APIs to their plane. |
| `create_memory`, `create_or_get_memory`, `create_memory_and_wait` | Create resource; the latter two handle duplicate lookup or `ACTIVE` polling. |
| `retrieve_memories` | High-level LTM exact/subtree semantic query; logs `ClientError` and returns no records. |
| `create_event`, `create_blob_event`, `save_conversation` | Write conversational, blob, or deprecated compatibility events. |
| `process_turn_with_llm` | Legacy retrieve → callback → persist orchestrator. |
| `list_events`, `list_branches`, `list_branch_events` | Paginated event history and branch views. |
| `get_conversation_tree`, `merge_branch_context`, `get_last_k_turns` | Construct a branch graph, flattened LLM context, or tail history from events. |
| `fork_conversation` | Creates a child branch event rooted at a selected event. |
| `get_memory_strategies`, `get_memory_status`, `list_memories` | Normalized control-plane inspection. |
| `delete_memory`, `delete_memory_and_wait` | Delete initiation and deletion-state polling. |
| `add_semantic_strategy`, `add_summary_strategy`, `add_user_preference_strategy`, `add_episodic_strategy` | Create built-in strategy wire dictionaries and submit them. |
| `add_semantic_strategy_and_wait`, `add_summary_strategy_and_wait`, `add_user_preference_strategy_and_wait`, `add_episodic_strategy_and_wait`, `add_custom_semantic_strategy_and_wait`, `add_custom_episodic_strategy_and_wait` | Corresponding add operation followed by resource `ACTIVE` polling. |
| `add_custom_semantic_strategy`, `add_custom_episodic_strategy` | Submit custom prompt/model extraction configurations; episodic includes reflection. |
| `modify_strategy`, `delete_strategy` | Build one modify/delete entry for grouped updates. |
| `update_memory_strategies`, `update_memory_strategies_and_wait` | Submit add/modify/delete group; modify configuration is wrapped based on discovered strategy type. |
| `wait_for_memories` | Best-effort extraction polling with empty-namespace caveat. |
| `add_strategy` | Generic one-strategy API that warns about transient `CREATING`. |
| `_normalize_memory_response` | Mutates/normalizes output aliases for old/new wire names. |
| `_add_strategy`, `_wait_for_memory_active` | Primitive grouped add and status poll. |
| `_add_default_namespaces`, `_validate_namespace`, `_validate_strategy_config` | Copy/fill templates and provide basic warning-only namespace validation. |
| `_try_get_override_type`, `_wrap_configuration` | Convert known override enum and nest extraction/consolidation/reflection payloads as the service requires. |

### `controlplane.py`

| Callable | Use |
|---|---|
| `__init__` | Builds raw configurable control-plane client. |
| `create_memory`, `get_memory`, `list_memories` | Resource create/read/list. |
| `update_memory`, `delete_memory` | Resource property and grouped strategy changes/deletion. |
| `add_strategy`, `get_strategy`, `update_strategy`, `remove_strategy` | Direct individual strategy lifecycle helpers. |
| `_wait_for_memory_active`, `_wait_for_strategy_active`, `_wait_for_status` | Generic/specialized state polling with failure/timeout handling. |

### `session.py`

| Callable | Use |
|---|---|
| `MemorySessionManager.__init__` | Fixes memory identity, resolves region, creates data plane, patches timestamp serialization. |
| `_validate_and_resolve_region`, `_build_client_config`, `_configure_timestamp_serialization`, `serialize_timestamp_as_float`, `__getattr__` | Construction validation, user agent merging, millisecond timestamp preservation (the nested serializer converts a `datetime` to fractional epoch seconds), and allowlisted raw forwarding. |
| `process_turn_with_llm`, `process_turn_with_llm_async`, `_retrieve_memories_for_llm`, `_save_conversation_turn` | The complete synchronous/async callback pipeline and its two phases. |
| `add_turns`, `fork_conversation`, `list_events`, `list_branches`, `get_last_k_turns` | STM write/history/branch operations. |
| `get_event`, `delete_event` | Targeted STM event read/delete. |
| `search_long_term_memories`, `list_long_term_memory_records`, `get_memory_record`, `delete_memory_record`, `delete_all_long_term_memories_in_namespace` | LTM semantic/list/CRUD and namespace cleanup. |
| `list_actors`, `list_actor_sessions`, `create_memory_session` | Identity discovery and bound façade construction. |
| `MemorySession.__init__`, `_construct_session_dict` | Store bound manager/identity and represent it as wrapper data. |
| All other `MemorySession` public methods | One-for-one identity-inserting delegates to manager: no new request semantics. |
| `Actor.__init__`, `_construct_session_dict`, `list_sessions` | Bound actor wrapper and delegated actor-session listing. |

### `constants.py` and `models/`

| Callable | Use |
|---|---|
| `ConversationalMessage.__post_init__` | Runtime guard for text and enum role. |
| `StringValue.build`, `LeftExpression.build`, `RightExpression.build` | Build event metadata filter operands. |
| `EventMetadataFilter.build_expression` | Builds an event metadata filter, omitting optional right side when absent. |
| `MemoryRecordLeftExpression.build` | Builds indexed LTM metadata key operand. |
| `MemoryRecordRightExpression.build_string/build_number/build_datetime/build_string_list` | Builds type-matching LTM right operand. |
| `MemoryMetadataFilter.build_expression` | Enforces right-operand/operator compatibility before a request. |
| `IndexedKey.build` | Creates an index declaration for resource provisioning. |
| `DictWrapper.__getattr__/__getitem__/get/__contains__/keys/values/items/__dir__/__repr__/__str__` | Attribute/dictionary access and introspection over the response dictionary; wrapper subclasses only call this base constructor. |

### `integrations/strands/config.py`, converter files

| Callable | Use |
|---|---|
| `normalize_metadata` | Normalizes only plain strings into AgentCore metadata wrapper shape. |
| `AgentCoreMemoryConfig._normalize_default_metadata` | Pydantic before-validator applying that normalizer to config defaults. |
| `AgentCoreMemoryConverter._filter_empty_text` | Removes empty Bedrock Converse text blocks. |
| `message_to_payload`, `events_to_messages` | Bidirectional Strands-session / AgentCore STM conversion. |
| `total_length`, `exceeds_conversational_limit` | Payload sizing and limit check. |
| `MemoryConverter` protocol methods | Required converter interface, no implementation. |
| `_bedrock_to_openai`, `_openai_to_bedrock` | Internal bidirectional mapping between Strands-native blocks and OpenAI message/tool/reasoning shapes. |
| `OpenAIConverseConverter.message_to_payload/events_to_messages/exceeds_conversational_limit` | Equivalent conversion/limit rules for OpenAI-shaped STM messages. |

### `integrations/strands/session_manager.py`

| Callable | Use |
|---|---|
| `__init__`, `_get_monotonic_timestamp`, `_build_metadata` | Configure adapter, preserve event ordering, and merge metadata. |
| `create_session/read_session/delete_session` | Strands session repository lifecycle. |
| `create_agent/read_agent/update_agent` | Agent-state persistence lifecycle. |
| `create_message/read_message/update_message/list_messages` | Message repository lifecycle, including pagination. |
| `_filter_restored_tool_context` | Removes historical tool blocks if configured. |
| `append_message`, `retrieve_customer_context`, `retrieve_for_namespace` | Hook actions: event append, configured LTM injection, and the nested per-namespace retrieval/threshold helper used by injection. |
| `register_hooks`, `_offload`, `_on_message_added_persist`, `initialize` | Install and initialize lifecycle integration; nested async hooks offload blocking work and persist a newly added message plus agent state. |
| `_update_buffered_message`, `_flush_messages_only`, `_flush_agent_states_only`, `_flush_messages` | Coalesce updates and write the buffers. |
| `pending_message_count`, `pending_agent_state_count` | Buffered-work metrics. |
| `close`, `__enter__`, `__exit__` | Deterministic flush and timer cleanup. |
| `_start_flush_timer`, `_interval_flush_callback`, `_stop_flush_timer` | Timed flush control. |

### `integrations/strands/memorystore/`

| Callable | Use |
|---|---|
| `types.resolve_namespace` | Substitute only actor/session placeholders. |
| `types.assert_resolved_namespace` | Reject remaining/unmatched braces before a read. |
| `types.assert_non_empty` | Enforce required nonblank string identity. |
| `types.slugify_namespace` | Derive deterministic default store name. |
| `store._create_memory_client` | Build integration-tagged `MemoryClient`. |
| `AgentCoreMemoryStore.__init__`, `search`, `add_messages`, `_to_entry` | Validate a read target, retrieve/map LTM, write via sender, map result metadata. |
| `store._format_created_at` | Millisecond UTC result formatting. |
| `AgentCoreEventSender._map_role/_extract_text/_is_user_or_assistant_with_text` | Filter Strands message eligibility and map payload. |
| `AgentCoreEventSender.__init__`, `send_batch`, `_send_all`, `_group_into_events`, `_send_event`, `_token_for_sequence_numbers` | Sender configuration, cancellation-safe group dispatch, concurrent errors, grouping, wire write, idempotency token. |
| `sender._metadata_scalar_string`, `sender._to_agentcore_metadata` | Validate scalar metadata and wrap it for AgentCore. |
| `factory._assert_writable_topology` | Enforces one writer; optionally requires one when extraction enabled. |
| `factory.create_agentcore_memory_stores` | Builds a validated, shared-client, multi-namespace store set. |

## Operational Rules and Failure Modes

| Symptom | Most likely cause / action |
|---|---|
| Event exists, search finds nothing | Extraction has not completed, no matching strategy, or retrieval namespace differs from generated record namespace. Wait/retry; verify the strategy template. |
| Cross-session recall missing | Namespace contains `{sessionId}`. Use actor-scoped strategy namespace for durable user facts/preferences. |
| `ValidationException` after strategy change | Resource is temporarily `CREATING`. Use an `_and_wait` helper or poll to `ACTIVE`. |
| Search too broad/narrow | `namespace` is exact; `namespace_path` is a subtree. Choose deliberately. |
| `MemoryClient.retrieve_memories` hides outage | It logs `ClientError` and returns `[]`. Use a raw vended client/store where error propagation matters. |
| Strands extraction duplicates events | More than one writable store shares an identity stream. Keep exactly one writer. |
| Async server pauses during Strands initialization | `async_mode` helps runtime hooks, not synchronous agent construction; construct the Agent in `asyncio.to_thread` if needed. |
| `flush()` treated as durable write acknowledgement | Strands can retain/log failed batches for retry; it is not proof server-side LTM extraction completed. |

## Safe Baseline

1. Provision an actor-scoped preference/fact namespace and a session-scoped summary namespace.
2. Create a single `MemorySessionManager` per memory resource; create bound `MemorySession`s per active actor/session.
3. Write each completed turn as one event containing its user and assistant messages.
4. Retrieve only the namespaces appropriate to the answer, and explicitly format returned records into the model prompt.
5. Treat strategy updates and extraction as asynchronous state transitions.
6. In Strands native-memory mode, use one shared `MemoryManager` per active identity and at most one writable store.
