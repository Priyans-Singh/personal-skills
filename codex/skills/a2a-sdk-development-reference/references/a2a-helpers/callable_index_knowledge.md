# Complete source and callable index

AST inventory includes classes, functions, properties, methods, conditional definitions and nested helpers. Signature/source-docstring summaries are supplementary evidence: manually written behavioral guides explain actual execution. Non-Python files are inventoried and linked even though they have no runtime AST callables.

## `__init__.py`

Behavior: [init_knowledge.md](init_knowledge.md). Source: [__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/__init__.py).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

## `agent_card.py`

Behavior: [agent_card_knowledge.md](agent_card_knowledge.md). Source: [agent_card.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/agent_card.py).

<!-- declaration:agent_card.py:6:display_agent_card -->
### `display_agent_card`

```python
def display_agent_card(card: AgentCard) -> None
```

Source: [display_agent_card](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/agent_card.py:6). Source-docstring summary: Print a human-readable summary of an AgentCard to stdout.

## `proto_helpers.py`

Behavior: [proto_helpers_knowledge.md](proto_helpers_knowledge.md). Source: [proto_helpers.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py).

<!-- declaration:proto_helpers.py:28:new_message -->
### `new_message`

```python
def new_message(parts: list[Part], context_id: str | None=None, task_id: str | None=None, role: Role=Role.ROLE_AGENT) -> Message
```

Source: [new_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:28). Source-docstring summary: Creates a new message containing a list of Parts.

<!-- declaration:proto_helpers.py:44:new_text_message -->
### `new_text_message`

```python
def new_text_message(text: str, media_type: str | None=None, context_id: str | None=None, task_id: str | None=None, role: Role=Role.ROLE_AGENT) -> Message
```

Source: [new_text_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:44). Source-docstring summary: Creates a new message containing a single text Part.

<!-- declaration:proto_helpers.py:60:get_message_text -->
### `get_message_text`

```python
def get_message_text(message: Message, delimiter: str='\n') -> str
```

Source: [get_message_text](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:60). Source-docstring summary: Extracts and joins all text content from a Message's parts.

<!-- declaration:proto_helpers.py:65:new_data_message -->
### `new_data_message`

```python
def new_data_message(data: Any, media_type: str | None=None, context_id: str | None=None, task_id: str | None=None, role: Role=Role.ROLE_AGENT) -> Message
```

Source: [new_data_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:65). Source-docstring summary: Creates a new message containing a single data Part.

<!-- declaration:proto_helpers.py:92:new_raw_message -->
### `new_raw_message`

```python
def new_raw_message(raw: bytes, media_type: str | None=None, filename: str | None=None, context_id: str | None=None, task_id: str | None=None, role: Role=Role.ROLE_AGENT) -> Message
```

Source: [new_raw_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:92). Source-docstring summary: Creates a new message containing a single raw bytes Part.

<!-- declaration:proto_helpers.py:121:new_url_message -->
### `new_url_message`

```python
def new_url_message(url: str, media_type: str | None=None, filename: str | None=None, context_id: str | None=None, task_id: str | None=None, role: Role=Role.ROLE_AGENT) -> Message
```

Source: [new_url_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:121). Source-docstring summary: Creates a new message containing a single URL Part.

<!-- declaration:proto_helpers.py:153:new_artifact -->
### `new_artifact`

```python
def new_artifact(parts: list[Part], name: str, description: str | None=None, artifact_id: str | None=None) -> Artifact
```

Source: [new_artifact](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:153). Source-docstring summary: Creates a new Artifact object.

<!-- declaration:proto_helpers.py:168:new_text_artifact -->
### `new_text_artifact`

```python
def new_text_artifact(name: str, text: str, media_type: str | None=None, description: str | None=None, artifact_id: str | None=None) -> Artifact
```

Source: [new_text_artifact](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:168). Source-docstring summary: Creates a new Artifact object containing only a single text Part.

<!-- declaration:proto_helpers.py:184:new_data_artifact -->
### `new_data_artifact`

```python
def new_data_artifact(name: str, data: Any, media_type: str | None=None, description: str | None=None, artifact_id: str | None=None) -> Artifact
```

Source: [new_data_artifact](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:184). Source-docstring summary: Creates a new Artifact object containing only a single data Part.

<!-- declaration:proto_helpers.py:211:new_raw_artifact -->
### `new_raw_artifact`

```python
def new_raw_artifact(name: str, raw: bytes, media_type: str | None=None, filename: str | None=None, description: str | None=None, artifact_id: str | None=None) -> Artifact
```

Source: [new_raw_artifact](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:211). Source-docstring summary: Creates a new Artifact object containing only a single raw bytes Part.

<!-- declaration:proto_helpers.py:240:new_url_artifact -->
### `new_url_artifact`

```python
def new_url_artifact(name: str, url: str, media_type: str | None=None, filename: str | None=None, description: str | None=None, artifact_id: str | None=None) -> Artifact
```

Source: [new_url_artifact](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:240). Source-docstring summary: Creates a new Artifact object containing only a single URL Part.

<!-- declaration:proto_helpers.py:269:get_artifact_text -->
### `get_artifact_text`

```python
def get_artifact_text(artifact: Artifact, delimiter: str='\n') -> str
```

Source: [get_artifact_text](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:269). Source-docstring summary: Extracts and joins all text content from an Artifact's parts.

<!-- declaration:proto_helpers.py:277:new_task_from_user_message -->
### `new_task_from_user_message`

```python
def new_task_from_user_message(user_message: Message) -> Task
```

Source: [new_task_from_user_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:277). Source-docstring summary: Creates a new Task object from an initial user message.

<!-- declaration:proto_helpers.py:295:new_task -->
### `new_task`

```python
def new_task(task_id: str, context_id: str, state: TaskState, artifacts: list[Artifact] | None=None, history: list[Message] | None=None) -> Task
```

Source: [new_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:295). Source-docstring summary: Creates a Task object with a specified status.

<!-- declaration:proto_helpers.py:320:new_text_part -->
### `new_text_part`

```python
def new_text_part(text: str, media_type: str | None=None) -> Part
```

Source: [new_text_part](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:320). Source-docstring summary: Creates a Part with text content.

<!-- declaration:proto_helpers.py:336:new_data_part -->
### `new_data_part`

```python
def new_data_part(data: Any, media_type: str | None=None) -> Part
```

Source: [new_data_part](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:336). Source-docstring summary: Creates a Part with structured data (google.protobuf.Value).

<!-- declaration:proto_helpers.py:355:new_raw_part -->
### `new_raw_part`

```python
def new_raw_part(raw: bytes, media_type: str | None=None, filename: str | None=None) -> Part
```

Source: [new_raw_part](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:355). Source-docstring summary: Creates a Part with raw bytes content.

<!-- declaration:proto_helpers.py:377:new_url_part -->
### `new_url_part`

```python
def new_url_part(url: str, media_type: str | None=None, filename: str | None=None) -> Part
```

Source: [new_url_part](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:377). Source-docstring summary: Creates a Part with a URL pointing to file content.

<!-- declaration:proto_helpers.py:399:get_text_parts -->
### `get_text_parts`

```python
def get_text_parts(parts: Sequence[Part]) -> list[str]
```

Source: [get_text_parts](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:399). Source-docstring summary: Extracts text content from all text Parts.

<!-- declaration:proto_helpers.py:404:get_data_parts -->
### `get_data_parts`

```python
def get_data_parts(parts: Sequence[Part]) -> list[Any]
```

Source: [get_data_parts](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:404). Source-docstring summary: Extracts structured data from all data Parts.

<!-- declaration:proto_helpers.py:419:get_raw_parts -->
### `get_raw_parts`

```python
def get_raw_parts(parts: Sequence[Part]) -> list[bytes]
```

Source: [get_raw_parts](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:419). Source-docstring summary: Extracts raw bytes content from all raw Parts.

<!-- declaration:proto_helpers.py:431:get_url_parts -->
### `get_url_parts`

```python
def get_url_parts(parts: Sequence[Part]) -> list[str]
```

Source: [get_url_parts](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:431). Source-docstring summary: Extracts URL strings from all URL Parts.

<!-- declaration:proto_helpers.py:446:new_text_status_update_event -->
### `new_text_status_update_event`

```python
def new_text_status_update_event(task_id: str, context_id: str, state: TaskState, text: str) -> TaskStatusUpdateEvent
```

Source: [new_text_status_update_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:446). Source-docstring summary: Creates a TaskStatusUpdateEvent with a single text message.

<!-- declaration:proto_helpers.py:468:new_text_artifact_update_event -->
### `new_text_artifact_update_event`

```python
def new_text_artifact_update_event(task_id: str, context_id: str, name: str, text: str, append: bool=False, last_chunk: bool=False, artifact_id: str | None=None) -> TaskArtifactUpdateEvent
```

Source: [new_text_artifact_update_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:468). Source-docstring summary: Creates a TaskArtifactUpdateEvent with a single text artifact.

<!-- declaration:proto_helpers.py:489:new_data_artifact_update_event -->
### `new_data_artifact_update_event`

```python
def new_data_artifact_update_event(task_id: str, context_id: str, name: str, data: Any, media_type: str | None=None, append: bool=False, last_chunk: bool=False, artifact_id: str | None=None) -> TaskArtifactUpdateEvent
```

Source: [new_data_artifact_update_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:489). Source-docstring summary: Creates a TaskArtifactUpdateEvent with a single data artifact.

<!-- declaration:proto_helpers.py:528:new_raw_artifact_update_event -->
### `new_raw_artifact_update_event`

```python
def new_raw_artifact_update_event(task_id: str, context_id: str, name: str, raw: bytes, media_type: str | None=None, filename: str | None=None, append: bool=False, last_chunk: bool=False, artifact_id: str | None=None) -> TaskArtifactUpdateEvent
```

Source: [new_raw_artifact_update_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:528). Source-docstring summary: Creates a TaskArtifactUpdateEvent with a single raw bytes artifact.

<!-- declaration:proto_helpers.py:570:new_url_artifact_update_event -->
### `new_url_artifact_update_event`

```python
def new_url_artifact_update_event(task_id: str, context_id: str, name: str, url: str, media_type: str | None=None, filename: str | None=None, append: bool=False, last_chunk: bool=False, artifact_id: str | None=None) -> TaskArtifactUpdateEvent
```

Source: [new_url_artifact_update_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:570). Source-docstring summary: Creates a TaskArtifactUpdateEvent with a single URL artifact.

<!-- declaration:proto_helpers.py:612:get_stream_response_text -->
### `get_stream_response_text`

```python
def get_stream_response_text(response: StreamResponse, delimiter: str='\n') -> str
```

Source: [get_stream_response_text](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/proto_helpers.py:612). Source-docstring summary: Extracts text content from a StreamResponse.

