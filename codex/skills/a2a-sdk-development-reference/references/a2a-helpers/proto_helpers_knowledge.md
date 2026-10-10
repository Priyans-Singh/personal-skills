# Protobuf helper factories and extraction

Source: [proto_helpers.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py), a2a-sdk 1.1.4, 2026-10-07. Exact signatures are in [callable index](callable_index_knowledge.md).

## Mental model and shared rules

Part → Message/Artifact → Task or update event → StreamResponse. These are value objects; factories return newly constructed protobuf messages, not transport responses. UUIDs are fresh uuid4 strings, not reserved store IDs. Role defaults to ROLE_AGENT for message helpers. Protobuf constructors copy nested message content into containers; subsequent input edits do not automatically mutate returned values. Returned protobuf values themselves remain mutable.

Optional None values passed to protobuf constructors generally mean unset; fields without explicit presence still read their scalar default. Factories do not run the SDK's required-field validator or enforce every business invariant. Incorrect types/JSON values can raise protobuf/ParseDict errors; no retry/catching here. No helper populates authentication/metadata indiscriminately or forwards caller credentials.

## Parts: lowest layer

| Function | Result / defaulting / delegation |
|---|---|
| `new_text_part(text, media_type=None)` | Part(text=...), media_type defaults to empty string; empty text accepted here |
| `new_data_part(data, media_type=None)` | ParseDict(data, google.protobuf.Value()) → Part.data; accepts JSON object/list/scalar/null shapes, not arbitrary Python objects |
| `new_raw_part(raw, media_type=None, filename=None)` | Part.raw bytes with media type/filename empty defaults; no encoding/read/download |
| `new_url_part(url, media_type=None, filename=None)` | Part.url string and labels; no validation, DNS resolution or fetching |

Part content is a protobuf oneof: each factory sets exactly one content member; replacing another content field clears the prior one. MIME defaults are blank, not automatic text/plain/application/json. Set media_type when protocol consumers need it. Raw bytes become base64 under protobuf JSON serialization; URI content remains a string. `new_data_part` uses a floating-number-capable protobuf Value representation, so do not assume exact arbitrary-size integer preservation; use an explicit string schema for precision-sensitive values.

## Messages

`new_message(parts, context_id=None, task_id=None, role=ROLE_AGENT)` creates Message with UUID message_id, supplied parts and routing IDs/role. It does not derive IDs, set metadata/extensions/references, validate nonempty parts, or enqueue anything.

`new_text_message(text, media_type=None, context_id=None, task_id=None, role=ROLE_AGENT)` calls new_text_part then new_message. `new_data_message(data, media_type=None, context_id=None, task_id=None, role=...)` delegates data conversion. `new_raw_message(raw, media_type=None, filename=None, context_id=None, task_id=None, role=...)` and `new_url_message(url, media_type=None, filename=None, context_id=None, task_id=None, role=...)` preserve content labels. These wrappers share routing/ID semantics but differ in content conversion and accepted input shape.

`get_message_text(message, delimiter='\n')` joins get_text_parts(message.parts) in original order. It skips data/raw/url and does not interpret multimodal content. Empty input/no text returns empty string. Empty text Parts remain included, so delimiters can produce blank segments.

## Artifacts

`new_artifact(parts, name, description=None, artifact_id=None)` constructs Artifact; a falsy ID (None or empty string) generates uuid4. Name and description are stored, not validated for meaningful contents. Does not set metadata/extensions.

`new_text_artifact(name, text, media_type=None, description=None, artifact_id=None)` calls new_text_part/new_artifact. `new_data_artifact` converts arbitrary JSON Value; `new_raw_artifact` includes bytes/media_type/filename; `new_url_artifact` includes URI/media_type/filename. Each result contains exactly one Part. `get_artifact_text` joins only text Parts like get_message_text.

Artifacts are task output, not agent messages. Task association lives on an enclosing Task/update, not the Artifact itself. Reuse artifact_id for successive chunks; omitting it on every call creates distinct outputs.

## Tasks and validation difference

`new_task_from_user_message(user_message)` specifically checks:

1. role equals ROLE_USER, else ValueError.
2. parts nonempty, else ValueError.
3. Every Part with text presence has nonempty text, else ValueError ('Message.text cannot be empty'). It does not require a text Part; data/raw/url-only messages pass this check.

Returns Task with SUBMITTED status, ID/context ID from message if truthy else independently generated uuid4, and history containing copied user message. Crucially, generated task/context IDs are **not inserted back into the original message** or its copied history entry by this function. If an executor receives IDs already inserted by RequestContext, use those; if using helper standalone, assign your own IDs deliberately when routing later events. No timestamp is populated.

`new_task(task_id, context_id, state, artifacts=None, history=None)` supplies empty fresh lists for None inputs and constructs Task with explicit state. It does not validate user role, task-ID uniqueness, nonempty IDs, terminal transitions or timestamp. Constructor type failures propagate. No persistence, event queue, state manager or background execution is created.

## Extraction helpers

`get_text_parts(parts)` returns text strings for HasField('text'); `get_data_parts(parts)` converts present Part.data through MessageToDict to ordinary Python JSON-shaped values; `get_raw_parts(parts)` returns bytes; `get_url_parts(parts)` returns strings. Each accepts a Sequence, preserves matching order, excludes other content, returns a new list, and does no I/O. Data extraction can return scalars/null/lists as well as dictionaries. These functions do not validate MIME type or automatically fetch data referenced by a URL.

## Event factories

`new_text_status_update_event(task_id, context_id, state, text)` constructs TaskStatusUpdateEvent with TaskStatus(state, message=new_text_message(... ROLE_AGENT and same IDs)). Inner message receives UUID. Neither status timestamp nor event metadata is set; no transition guard or publication occurs.

| Factory | Part conversion | Shared update behavior |
|---|---|---|
| `new_text_artifact_update_event` | new_text_artifact(name,text) | task/context IDs, optional artifact ID, append=False and last_chunk=False defaults |
| `new_data_artifact_update_event` | data Value with optional media type | same flags; JSON parse errors can propagate |
| `new_raw_artifact_update_event` | bytes/media type/filename | same flags; no read/encode step |
| `new_url_artifact_update_event` | URL/media type/filename | same flags; no destination screening |

Flags are emitted, not enacted. Server TaskManager decides replacement/append; append=True to a missing artifact is rejected there. First chunk should have append=False with fixed artifact_id, subsequent chunks append=True with that same ID. last_chunk is delivered in the event, but does not automatically create a durable completion bit on the stored Artifact. These factories do not support generic event metadata parameters; edit protobuf deliberately or use another publisher when needed.

`get_stream_response_text(response, delimiter='\n')` checks payload presence in order: Message→message text; Task→artifact texts (drops empty artifact text, joins nonempty); status_update→status.message text if present; artifact_update→artifact text; empty/unrecognized envelope→empty string. For Task it does **not** include Task.status.message or history, and for nontext payload it returns no substitute. Oneof normally ensures only one branch.

## Example: prepare values, then let integration publish

```python
from a2a.helpers import (
    new_text_message, new_task_from_user_message,
    new_text_artifact_update_event, get_stream_response_text,
)
from a2a.types import Role, StreamResponse

message = new_text_message("hello", task_id="task-1", context_id="context-1",
                           role=Role.ROLE_USER)
task = new_task_from_user_message(message)
first = new_text_artifact_update_event(
    task.id, task.context_id, "answer", "hello ", artifact_id="answer-1"
)
next_chunk = new_text_artifact_update_event(
    task.id, task.context_id, "answer", "world", artifact_id="answer-1",
    append=True, last_chunk=True,
)
assert get_stream_response_text(StreamResponse(artifact_update=next_chunk)) == "world"
# In execute(), await event_queue.enqueue_event(task), then enqueue the updates.
```

Do not emit a bare Message after entering Task workflow; attach agent text to TaskStatus.message or Artifact. To publish timestamps/guarded states, server TaskUpdater is often more suitable. Construct values using current helpers, preserve selected interface/version at transport boundaries, and keep URL/file handling explicit.

## Supporting dependencies and operational semantics

uuid supplies IDs; protobuf supplies messages/oneofs and JSON parse/serialization. There are no external calls, retries, persisted records, credential material, resource disposal or synchronization primitives in this module. Concurrent construction is independent; sharing/mutating returned messages is an application concurrency concern. Runtime errors arise from explicit task checks, invalid protobuf values or JSON conversion, not translated A2A exceptions. Local validation covers all helper calls and value distinctions, not a remote protocol deployment.
