# v0_3/proto_utils.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/proto_utils.py`. SHA-256: `f64d8e6fc84ef4212a5853958e612c1339c59a6d86964c4c1407129e3fb50a52`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Mental model: legacy protobuf ↔ legacy pivot

`ToProto` and `FromProto` are classmethod namespaces, not stateful converters. They encode/decode legacy types only. JSON-RPC does not need this stage; legacy REST/gRPC do. Detailed callable bodies below show every field assignment and branch. All local exceptions propagate, including Pydantic validation, protobuf field errors, UTF-8 decoding, malformed resource names and unsupported variants.

## Non-obvious representation behavior

`dict_to_struct` recursively converts dictionaries and delegates leaf assignment to protobuf Struct. It does **not** call the normalization helpers. Struct numeric values use protobuf doubles; large integers can lose precision. `make_dict_serializable` recursively preserves scalar/None values, turns tuple/list into list, stringifies other objects. `normalize_large_integers_to_strings` uses a decimal threshold `10**max_safe_digits - 1` (default 15 digits), not exactly 2**53-1; nested `_normalize` recurses. `parse_string_integers_in_dict` reverses digit strings longer than this threshold, including negatives. Its `lstrip('-')` also recognizes malformed repeated-minus strings then `int` raises. These helpers are opt-in; metadata/data conversion does not apply them automatically.

`ToProto.message` maps parts to **content**, role via switch, blank context/task to empty strings and optional extensions to empty list; it omits reference-task IDs because legacy protobuf lacks that field. `FromProto.message` reverses but likewise cannot recreate references. Unknown protobuf role becomes legacy agent; unknown Python role becomes ROLE_UNSPECIFIED.

Legacy file `file_with_bytes` is bytes carrying the UTF-8 encoding of the **base64 string**, not decoded file bytes. Reverse decodes UTF-8. Protobuf JSON adds its own bytes base64 encoding around these bytes, so a REST file payload can have two encoding layers. URI branch uses presence; absent file oneof falls back to empty byte-text model. Text/file/data parts use oneof/presence and unknown part raises ValueError.

`ToProto.task_status` copies state and update only, dropping timestamp. `FromProto.task_status` always converts `status.update` without HasField and also drops timestamp. An absent protobuf update therefore becomes a placeholder legacy Message with blank ID, empty parts and agent role. Core direct converters preserve timestamp; the extra legacy proto hop loses it. Task state maps preserve all defined states; wire enum spells TASK_STATE_CANCELLED while current core spells TASK_STATE_CANCELED.

Metadata `None` becomes absent Struct; FromProto empty fields returns `{}`. Data uses MessageToJson then json.loads. Artifact recursively maps parts and modes/extensions. Status final is copied at this stage; core conversion later recomputes or drops it. Event append/lastChunk absent values collapse to false.

`ToProto.message_send_configuration(None)` returns an empty **present** config object; blocking is `config.blocking or False`. `FromProto.message_send_params` always converts request.configuration, so absent wire config becomes an explicit model with blocking false/historyLength zero. Core bridge then makes return_immediately true. Get-task `task_query_params` treats history_length zero as None, losing explicit zero.

## Resource parsing and precedence

TASK_NAME_MATCH is `tasks/([^/]+)`; TASK_PUSH_CONFIG_NAME_MATCH is `tasks/([^/]+)/pushNotificationConfigs/([^/]+)`. Both use `.match`, not fullmatch: valid prefixes with trailing text are accepted. Bad prefixes raise core InvalidParamsError. `ToProto.task_push_notification_config` composes name with the nested config ID; a None ID becomes literal `None`. FromProto extracts task ID from resource name but uses config **payload** ID rather than the resource's config-ID group. Create config request uses parent task and nested config; top-level config_id is ignored.

## Discovery and security loss

AgentCard conversion does not copy icon_url although schema and descriptors define it. Skills conversion omits security despite a proto field existing. OAuth2SecurityScheme omits oauth2_metadata_url in both directions. Capabilities omit state-transition history. Signatures/header copies do not sign or verify. Security map and each scheme map without acquiring any credentials.

ToProto oauth2_flows takes the **first present** branch authorization-code/client-credentials/implicit/password and raises ValueError if none. FromProto uses the same first-three checks then defaults to password even with no oneof set. API-key invalid location raises ValueError. Unrecognized SecurityScheme input falls through to OIDC; FromProto absent scheme also produces an empty OIDC model.

Send response chooses message if present, otherwise task even when payload absent. Stream response requires one of the four known variants and raises ValueError otherwise. List response builds a legacy success envelope with id=None, ignores next_page_token and converts each config.

## Pure example

```python
from a2a.compat.v0_3 import proto_utils, types
part = types.Part(root=types.FilePart(file=types.FileWithBytes(bytes='aGk=')))
wire = proto_utils.ToProto.part(part)
assert wire.file.file_with_bytes == b'aGk='
assert proto_utils.FromProto.part(wire).root.file.bytes == 'aGk='
```

Preserve explicit configuration when crossing this stage. Normalize large integers deliberately on both sides; converting a callback URL or file URI never downloads it.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import json
import logging
import re
from typing import Any
from google.protobuf import json_format, struct_pb2
from a2a.compat.v0_3 import a2a_v0_3_pb2 as a2a_pb2
from a2a.compat.v0_3 import types
from a2a.utils.errors import InvalidParamsError
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
logger = logging.getLogger(__name__)
TASK_NAME_MATCH = re.compile('tasks/([^/]+)')
TASK_PUSH_CONFIG_NAME_MATCH = re.compile('tasks/([^/]+)/pushNotificationConfigs/([^/]+)')
```

## Declaration-by-declaration execution reference

### `dict_to_struct`

Source lines 30–49; declaration kind `FunctionDef`.

Inputs: `(dictionary: dict[str, Any])`. Output annotation: `struct_pb2.Struct`. Decorators: `none`.

Source intent: Converts a Python dict to a Struct proto. Unfortunately, using `json_format.ParseDict` does not work because this wants the dictionary to be an exact match of the Struct proto with fields and keys and values, not the traditional Python dict structure. Args: dictionary: The Python dict to convert. Returns: The Struct proto.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `struct` from `struct_pb2.Struct()`; output construction/calls here execute immediately when this method runs.
2. Iterates `dictionary.items()` into `(key, val)`; each iteration performs the shown conversion/delegation, preserving iteration order.
3. Returns `struct`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `struct_pb2.Struct`, `dictionary.items`, `isinstance`, `dict_to_struct`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def dict_to_struct(dictionary: dict[str, Any]) -> struct_pb2.Struct:
    struct = struct_pb2.Struct()
    for key, val in dictionary.items():
        if isinstance(val, dict):
            struct[key] = dict_to_struct(val)
        else:
            struct[key] = val
    return struct
```

</details>

### `make_dict_serializable`

Source lines 52–69; declaration kind `FunctionDef`.

Inputs: `(value: Any)`. Output annotation: `Any`. Decorators: `none`.

Source intent: Dict pre-processing utility: converts non-serializable values to serializable form. Use this when you want to normalize a dictionary before dict->Struct conversion. Args: value: The value to convert. Returns: A serializable value.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(value, str | int | float | bool) or value is None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `isinstance(value, dict)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `isinstance(value, list | tuple)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `str(value)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `str`, `make_dict_serializable`, `value.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def make_dict_serializable(value: Any) -> Any:
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    if isinstance(value, dict):
        return {k: make_dict_serializable(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [make_dict_serializable(item) for item in value]
    return str(value)
```

</details>

### `normalize_large_integers_to_strings`

Source lines 72–98; declaration kind `FunctionDef`.

Inputs: `(value: Any, max_safe_digits: int=15)`. Output annotation: `Any`. Decorators: `none`.

Source intent: Integer preprocessing utility: converts large integers to strings. Use this when you want to convert large integers to strings considering JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation. Args: value: The value to convert. max_safe_digits: Maximum safe integer digits (default: 15). Returns: A normalized value.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `max_safe_int` from `10 ** max_safe_digits - 1`; output construction/calls here execute immediately when this method runs.
2. Defines closure `_normalize` capturing enclosing locals; its separate entry below documents deferred execution.
3. Returns `_normalize(value)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `_normalize`, `isinstance`, `str`, `abs`, `item.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def normalize_large_integers_to_strings(value: Any, max_safe_digits: int=15) -> Any:
    max_safe_int = 10 ** max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item
    return _normalize(value)
```

</details>

### `normalize_large_integers_to_strings._normalize`

Source lines 89–96; declaration kind `FunctionDef`.

Inputs: `(item: Any)`. Output annotation: `Any`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(item, int) and abs(item) > max_safe_int`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `isinstance(item, dict)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `isinstance(item, list | tuple)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `item`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `str`, `abs`, `_normalize`, `item.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def _normalize(item: Any) -> Any:
    if isinstance(item, int) and abs(item) > max_safe_int:
        return str(item)
    if isinstance(item, dict):
        return {k: _normalize(v) for k, v in item.items()}
    if isinstance(item, list | tuple):
        return [_normalize(i) for i in item]
    return item
```

</details>

### `parse_string_integers_in_dict`

Source lines 101–129; declaration kind `FunctionDef`.

Inputs: `(value: Any, max_safe_digits: int=15)`. Output annotation: `Any`. Decorators: `none`.

Source intent: String post-processing utility: converts large integer strings back to integers. Use this when you want to restore large integer strings to integers after Struct->dict conversion. Args: value: The value to convert. max_safe_digits: Maximum safe integer digits (default: 15). Returns: A parsed value.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(value, dict)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `isinstance(value, list | tuple)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `isinstance(value, str)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `value`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `value.lstrip`, `parse_string_integers_in_dict`, `stripped_value.isdigit`, `int`, `value.items`, `len`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def parse_string_integers_in_dict(value: Any, max_safe_digits: int=15) -> Any:
    if isinstance(value, dict):
        return {k: parse_string_integers_in_dict(v, max_safe_digits) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [parse_string_integers_in_dict(item, max_safe_digits) for item in value]
    if isinstance(value, str):
        stripped_value = value.lstrip('-')
        if stripped_value.isdigit() and len(stripped_value) > max_safe_digits:
            return int(value)
    return value
```

</details>

### `ToProto`

Source lines 132–590; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Converts Python types to proto types.

Declared operations: `message`, `metadata`, `part`, `data`, `file`, `task`, `task_status`, `task_state`, `artifact`, `authentication_info`, `push_notification_config`, `task_artifact_update_event`, `task_status_update_event`, `message_send_configuration`, `update_event`, `task_or_message`, `stream_response`, `task_push_notification_config`, `agent_card`, `agent_card_signature`, `agent_interface`, `capabilities`, `extension`, `provider`, `security`, `security_schemes`, `security_scheme`, `oauth2_flows`, `skill`, `role`. Each method is traced below; constructor determines retained state.

### `ToProto.message`

Source lines 136–147; declaration kind `FunctionDef`.

Inputs: `(cls, message: types.Message | None)`. Output annotation: `a2a_pb2.Message | None`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `message is None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `a2a_pb2.Message(message_id=message.message_id, content=[cls.part(p) for p in message.parts], context_id=message.context_id or '', task_id=message.task_id or '', role=cls.role(message.role), metadata=cls.metadata(message.metadata), extensions=message.extensions or [])`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.Message`, `cls.role`, `cls.metadata`, `cls.part`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def message(cls, message: types.Message | None) -> a2a_pb2.Message | None:
    if message is None:
        return None
    return a2a_pb2.Message(message_id=message.message_id, content=[cls.part(p) for p in message.parts], context_id=message.context_id or '', task_id=message.task_id or '', role=cls.role(message.role), metadata=cls.metadata(message.metadata), extensions=message.extensions or [])
```

</details>

### `ToProto.metadata`

Source lines 150–155; declaration kind `FunctionDef`.

Inputs: `(cls, metadata: dict[str, Any] | None)`. Output annotation: `struct_pb2.Struct | None`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `metadata is None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `dict_to_struct(metadata)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `dict_to_struct`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def metadata(cls, metadata: dict[str, Any] | None) -> struct_pb2.Struct | None:
    if metadata is None:
        return None
    return dict_to_struct(metadata)
```

</details>

### `ToProto.part`

Source lines 158–173; declaration kind `FunctionDef`.

Inputs: `(cls, part: types.Part)`. Output annotation: `a2a_pb2.Part`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(part.root, types.TextPart)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `isinstance(part.root, types.FilePart)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `isinstance(part.root, types.DataPart)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Raises `ValueError(f'Unsupported part type: {part.root}')`.

Explicit errors: `ValueError(f'Unsupported part type: {part.root}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `ValueError`, `a2a_pb2.Part`, `cls.metadata`, `cls.file`, `cls.data`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def part(cls, part: types.Part) -> a2a_pb2.Part:
    if isinstance(part.root, types.TextPart):
        return a2a_pb2.Part(text=part.root.text, metadata=cls.metadata(part.root.metadata))
    if isinstance(part.root, types.FilePart):
        return a2a_pb2.Part(file=cls.file(part.root.file), metadata=cls.metadata(part.root.metadata))
    if isinstance(part.root, types.DataPart):
        return a2a_pb2.Part(data=cls.data(part.root.data), metadata=cls.metadata(part.root.metadata))
    raise ValueError(f'Unsupported part type: {part.root}')
```

</details>

### `ToProto.data`

Source lines 176–177; declaration kind `FunctionDef`.

Inputs: `(cls, data: dict[str, Any])`. Output annotation: `a2a_pb2.DataPart`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.DataPart(data=dict_to_struct(data))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.DataPart`, `dict_to_struct`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def data(cls, data: dict[str, Any]) -> a2a_pb2.DataPart:
    return a2a_pb2.DataPart(data=dict_to_struct(data))
```

</details>

### `ToProto.file`

Source lines 180–191; declaration kind `FunctionDef`.

Inputs: `(cls, file: types.FileWithUri | types.FileWithBytes)`. Output annotation: `a2a_pb2.FilePart`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(file, types.FileWithUri)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `a2a_pb2.FilePart(file_with_bytes=file.bytes.encode('utf-8'), mime_type=file.mime_type, name=file.name)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `a2a_pb2.FilePart`, `file.bytes.encode`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def file(cls, file: types.FileWithUri | types.FileWithBytes) -> a2a_pb2.FilePart:
    if isinstance(file, types.FileWithUri):
        return a2a_pb2.FilePart(file_with_uri=file.uri, mime_type=file.mime_type, name=file.name)
    return a2a_pb2.FilePart(file_with_bytes=file.bytes.encode('utf-8'), mime_type=file.mime_type, name=file.name)
```

</details>

### `ToProto.task`

Source lines 194–210; declaration kind `FunctionDef`.

Inputs: `(cls, task: types.Task)`. Output annotation: `a2a_pb2.Task`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.Task(id=task.id, context_id=task.context_id, status=cls.task_status(task.status), artifacts=[cls.artifact(a) for a in task.artifacts] if task.artifacts else None, history=[cls.message(h) for h in task.history] if task.history else None, metadata=cls.metadata(task.metadata))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.Task`, `cls.task_status`, `cls.metadata`, `cls.artifact`, `cls.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task(cls, task: types.Task) -> a2a_pb2.Task:
    return a2a_pb2.Task(id=task.id, context_id=task.context_id, status=cls.task_status(task.status), artifacts=[cls.artifact(a) for a in task.artifacts] if task.artifacts else None, history=[cls.message(h) for h in task.history] if task.history else None, metadata=cls.metadata(task.metadata))
```

</details>

### `ToProto.task_status`

Source lines 213–217; declaration kind `FunctionDef`.

Inputs: `(cls, status: types.TaskStatus)`. Output annotation: `a2a_pb2.TaskStatus`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.TaskStatus(state=cls.task_state(status.state), update=cls.message(status.message))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.TaskStatus`, `cls.task_state`, `cls.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_status(cls, status: types.TaskStatus) -> a2a_pb2.TaskStatus:
    return a2a_pb2.TaskStatus(state=cls.task_state(status.state), update=cls.message(status.message))
```

</details>

### `ToProto.task_state`

Source lines 220–239; declaration kind `FunctionDef`.

Inputs: `(cls, state: types.TaskState)`. Output annotation: `a2a_pb2.TaskState`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Dispatches on `state` using the exact case map below; default case controls unsupported/unknown input.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_state(cls, state: types.TaskState) -> a2a_pb2.TaskState:
    match state:
        case types.TaskState.submitted:
            return a2a_pb2.TaskState.TASK_STATE_SUBMITTED
        case types.TaskState.working:
            return a2a_pb2.TaskState.TASK_STATE_WORKING
        case types.TaskState.completed:
            return a2a_pb2.TaskState.TASK_STATE_COMPLETED
        case types.TaskState.canceled:
            return a2a_pb2.TaskState.TASK_STATE_CANCELLED
        case types.TaskState.failed:
            return a2a_pb2.TaskState.TASK_STATE_FAILED
        case types.TaskState.input_required:
            return a2a_pb2.TaskState.TASK_STATE_INPUT_REQUIRED
        case types.TaskState.auth_required:
            return a2a_pb2.TaskState.TASK_STATE_AUTH_REQUIRED
        case types.TaskState.rejected:
            return a2a_pb2.TaskState.TASK_STATE_REJECTED
        case _:
            return a2a_pb2.TaskState.TASK_STATE_UNSPECIFIED
```

</details>

### `ToProto.artifact`

Source lines 242–250; declaration kind `FunctionDef`.

Inputs: `(cls, artifact: types.Artifact)`. Output annotation: `a2a_pb2.Artifact`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.Artifact(artifact_id=artifact.artifact_id, description=artifact.description, metadata=cls.metadata(artifact.metadata), name=artifact.name, parts=[cls.part(p) for p in artifact.parts], extensions=artifact.extensions or [])`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.Artifact`, `cls.metadata`, `cls.part`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def artifact(cls, artifact: types.Artifact) -> a2a_pb2.Artifact:
    return a2a_pb2.Artifact(artifact_id=artifact.artifact_id, description=artifact.description, metadata=cls.metadata(artifact.metadata), name=artifact.name, parts=[cls.part(p) for p in artifact.parts], extensions=artifact.extensions or [])
```

</details>

### `ToProto.authentication_info`

Source lines 253–259; declaration kind `FunctionDef`.

Inputs: `(cls, info: types.PushNotificationAuthenticationInfo)`. Output annotation: `a2a_pb2.AuthenticationInfo`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.AuthenticationInfo(schemes=info.schemes, credentials=info.credentials)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AuthenticationInfo`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def authentication_info(cls, info: types.PushNotificationAuthenticationInfo) -> a2a_pb2.AuthenticationInfo:
    return a2a_pb2.AuthenticationInfo(schemes=info.schemes, credentials=info.credentials)
```

</details>

### `ToProto.push_notification_config`

Source lines 262–275; declaration kind `FunctionDef`.

Inputs: `(cls, config: types.PushNotificationConfig)`. Output annotation: `a2a_pb2.PushNotificationConfig`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `auth_info` from `cls.authentication_info(config.authentication) if config.authentication else None`; output construction/calls here execute immediately when this method runs.
2. Returns `a2a_pb2.PushNotificationConfig(id=config.id or '', url=config.url, token=config.token, authentication=auth_info)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.PushNotificationConfig`, `cls.authentication_info`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def push_notification_config(cls, config: types.PushNotificationConfig) -> a2a_pb2.PushNotificationConfig:
    auth_info = cls.authentication_info(config.authentication) if config.authentication else None
    return a2a_pb2.PushNotificationConfig(id=config.id or '', url=config.url, token=config.token, authentication=auth_info)
```

</details>

### `ToProto.task_artifact_update_event`

Source lines 278–288; declaration kind `FunctionDef`.

Inputs: `(cls, event: types.TaskArtifactUpdateEvent)`. Output annotation: `a2a_pb2.TaskArtifactUpdateEvent`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.TaskArtifactUpdateEvent(task_id=event.task_id, context_id=event.context_id, artifact=cls.artifact(event.artifact), metadata=cls.metadata(event.metadata), append=event.append or False, last_chunk=event.last_chunk or False)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.TaskArtifactUpdateEvent`, `cls.artifact`, `cls.metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_artifact_update_event(cls, event: types.TaskArtifactUpdateEvent) -> a2a_pb2.TaskArtifactUpdateEvent:
    return a2a_pb2.TaskArtifactUpdateEvent(task_id=event.task_id, context_id=event.context_id, artifact=cls.artifact(event.artifact), metadata=cls.metadata(event.metadata), append=event.append or False, last_chunk=event.last_chunk or False)
```

</details>

### `ToProto.task_status_update_event`

Source lines 291–300; declaration kind `FunctionDef`.

Inputs: `(cls, event: types.TaskStatusUpdateEvent)`. Output annotation: `a2a_pb2.TaskStatusUpdateEvent`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.TaskStatusUpdateEvent(task_id=event.task_id, context_id=event.context_id, status=cls.task_status(event.status), metadata=cls.metadata(event.metadata), final=event.final)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.TaskStatusUpdateEvent`, `cls.task_status`, `cls.metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_status_update_event(cls, event: types.TaskStatusUpdateEvent) -> a2a_pb2.TaskStatusUpdateEvent:
    return a2a_pb2.TaskStatusUpdateEvent(task_id=event.task_id, context_id=event.context_id, status=cls.task_status(event.status), metadata=cls.metadata(event.metadata), final=event.final)
```

</details>

### `ToProto.message_send_configuration`

Source lines 303–317; declaration kind `FunctionDef`.

Inputs: `(cls, config: types.MessageSendConfiguration | None)`. Output annotation: `a2a_pb2.SendMessageConfiguration`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not config`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `a2a_pb2.SendMessageConfiguration(accepted_output_modes=config.accepted_output_modes, push_notification=cls.push_notification_config(config.push_notification_config) if config.push_notification_config else None, history_length=config.history_length, blocking=config.blocking or False)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.SendMessageConfiguration`, `cls.push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def message_send_configuration(cls, config: types.MessageSendConfiguration | None) -> a2a_pb2.SendMessageConfiguration:
    if not config:
        return a2a_pb2.SendMessageConfiguration()
    return a2a_pb2.SendMessageConfiguration(accepted_output_modes=config.accepted_output_modes, push_notification=cls.push_notification_config(config.push_notification_config) if config.push_notification_config else None, history_length=config.history_length, blocking=config.blocking or False)
```

</details>

### `ToProto.update_event`

Source lines 320–328; declaration kind `FunctionDef`.

Inputs: `(cls, event: types.Task | types.Message | types.TaskStatusUpdateEvent | types.TaskArtifactUpdateEvent)`. Output annotation: `a2a_pb2.StreamResponse`. Decorators: `classmethod`.

Source intent: Converts a task, message, or task update event to a StreamResponse.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `cls.stream_response(event)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `cls.stream_response`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def update_event(cls, event: types.Task | types.Message | types.TaskStatusUpdateEvent | types.TaskArtifactUpdateEvent) -> a2a_pb2.StreamResponse:
    return cls.stream_response(event)
```

</details>

### `ToProto.task_or_message`

Source lines 331–340; declaration kind `FunctionDef`.

Inputs: `(cls, event: types.Task | types.Message)`. Output annotation: `a2a_pb2.SendMessageResponse`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(event, types.Message)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `a2a_pb2.SendMessageResponse(task=cls.task(event))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `a2a_pb2.SendMessageResponse`, `cls.task`, `cls.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_or_message(cls, event: types.Task | types.Message) -> a2a_pb2.SendMessageResponse:
    if isinstance(event, types.Message):
        return a2a_pb2.SendMessageResponse(msg=cls.message(event))
    return a2a_pb2.SendMessageResponse(task=cls.task(event))
```

</details>

### `ToProto.stream_response`

Source lines 343–364; declaration kind `FunctionDef`.

Inputs: `(cls, event: types.Message | types.Task | types.TaskStatusUpdateEvent | types.TaskArtifactUpdateEvent)`. Output annotation: `a2a_pb2.StreamResponse`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(event, types.Message)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `isinstance(event, types.Task)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `isinstance(event, types.TaskStatusUpdateEvent)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `isinstance(event, types.TaskArtifactUpdateEvent)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Raises `ValueError(f'Unsupported event type: {type(event)}')`.

Explicit errors: `ValueError(f'Unsupported event type: {type(event)}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `ValueError`, `a2a_pb2.StreamResponse`, `cls.message`, `cls.task`, `cls.task_status_update_event`, `cls.task_artifact_update_event`, `type`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def stream_response(cls, event: types.Message | types.Task | types.TaskStatusUpdateEvent | types.TaskArtifactUpdateEvent) -> a2a_pb2.StreamResponse:
    if isinstance(event, types.Message):
        return a2a_pb2.StreamResponse(msg=cls.message(event))
    if isinstance(event, types.Task):
        return a2a_pb2.StreamResponse(task=cls.task(event))
    if isinstance(event, types.TaskStatusUpdateEvent):
        return a2a_pb2.StreamResponse(status_update=cls.task_status_update_event(event))
    if isinstance(event, types.TaskArtifactUpdateEvent):
        return a2a_pb2.StreamResponse(artifact_update=cls.task_artifact_update_event(event))
    raise ValueError(f'Unsupported event type: {type(event)}')
```

</details>

### `ToProto.task_push_notification_config`

Source lines 367–375; declaration kind `FunctionDef`.

Inputs: `(cls, config: types.TaskPushNotificationConfig)`. Output annotation: `a2a_pb2.TaskPushNotificationConfig`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.TaskPushNotificationConfig(name=f'tasks/{config.task_id}/pushNotificationConfigs/{config.push_notification_config.id}', push_notification_config=cls.push_notification_config(config.push_notification_config))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.TaskPushNotificationConfig`, `cls.push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_push_notification_config(cls, config: types.TaskPushNotificationConfig) -> a2a_pb2.TaskPushNotificationConfig:
    return a2a_pb2.TaskPushNotificationConfig(name=f'tasks/{config.task_id}/pushNotificationConfigs/{config.push_notification_config.id}', push_notification_config=cls.push_notification_config(config.push_notification_config))
```

</details>

### `ToProto.agent_card`

Source lines 378–408; declaration kind `FunctionDef`.

Inputs: `(cls, card: types.AgentCard)`. Output annotation: `a2a_pb2.AgentCard`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.AgentCard(capabilities=cls.capabilities(card.capabilities), default_input_modes=list(card.default_input_modes), default_output_modes=list(card.default_output_modes), description=card.description, documentation_url=card.documentation_url, name=card.name, provider=cls.provider(card.provider), security=cls.security(card.security), security_schemes=cls.s … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AgentCard`, `cls.capabilities`, `list`, `cls.provider`, `cls.security`, `cls.security_schemes`, `bool`, `cls.skill`, `cls.agent_interface`, `cls.agent_card_signature`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def agent_card(cls, card: types.AgentCard) -> a2a_pb2.AgentCard:
    return a2a_pb2.AgentCard(capabilities=cls.capabilities(card.capabilities), default_input_modes=list(card.default_input_modes), default_output_modes=list(card.default_output_modes), description=card.description, documentation_url=card.documentation_url, name=card.name, provider=cls.provider(card.provider), security=cls.security(card.security), security_schemes=cls.security_schemes(card.security_schemes), skills=[cls.skill(x) for x in card.skills] if card.skills else [], url=card.url, version=card.version, supports_authenticated_extended_card=bool(card.supports_authenticated_extended_card), preferred_transport=card.preferred_transport, protocol_version=card.protocol_version, additional_interfaces=[cls.agent_interface(x) for x in card.additional_interfaces] if card.additional_interfaces else None, signatures=[cls.agent_card_signature(x) for x in card.signatures] if card.signatures else None)
```

</details>

### `ToProto.agent_card_signature`

Source lines 411–420; declaration kind `FunctionDef`.

Inputs: `(cls, signature: types.AgentCardSignature)`. Output annotation: `a2a_pb2.AgentCardSignature`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.AgentCardSignature(protected=signature.protected, signature=signature.signature, header=dict_to_struct(signature.header) if signature.header is not None else None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AgentCardSignature`, `dict_to_struct`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def agent_card_signature(cls, signature: types.AgentCardSignature) -> a2a_pb2.AgentCardSignature:
    return a2a_pb2.AgentCardSignature(protected=signature.protected, signature=signature.signature, header=dict_to_struct(signature.header) if signature.header is not None else None)
```

</details>

### `ToProto.agent_interface`

Source lines 423–430; declaration kind `FunctionDef`.

Inputs: `(cls, interface: types.AgentInterface)`. Output annotation: `a2a_pb2.AgentInterface`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.AgentInterface(transport=interface.transport, url=interface.url)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AgentInterface`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def agent_interface(cls, interface: types.AgentInterface) -> a2a_pb2.AgentInterface:
    return a2a_pb2.AgentInterface(transport=interface.transport, url=interface.url)
```

</details>

### `ToProto.capabilities`

Source lines 433–442; declaration kind `FunctionDef`.

Inputs: `(cls, capabilities: types.AgentCapabilities)`. Output annotation: `a2a_pb2.AgentCapabilities`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.AgentCapabilities(streaming=bool(capabilities.streaming), push_notifications=bool(capabilities.push_notifications), extensions=[cls.extension(x) for x in capabilities.extensions or []])`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AgentCapabilities`, `bool`, `cls.extension`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def capabilities(cls, capabilities: types.AgentCapabilities) -> a2a_pb2.AgentCapabilities:
    return a2a_pb2.AgentCapabilities(streaming=bool(capabilities.streaming), push_notifications=bool(capabilities.push_notifications), extensions=[cls.extension(x) for x in capabilities.extensions or []])
```

</details>

### `ToProto.extension`

Source lines 445–456; declaration kind `FunctionDef`.

Inputs: `(cls, extension: types.AgentExtension)`. Output annotation: `a2a_pb2.AgentExtension`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.AgentExtension(uri=extension.uri, description=extension.description, params=dict_to_struct(extension.params) if extension.params else None, required=extension.required)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AgentExtension`, `dict_to_struct`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def extension(cls, extension: types.AgentExtension) -> a2a_pb2.AgentExtension:
    return a2a_pb2.AgentExtension(uri=extension.uri, description=extension.description, params=dict_to_struct(extension.params) if extension.params else None, required=extension.required)
```

</details>

### `ToProto.provider`

Source lines 459–467; declaration kind `FunctionDef`.

Inputs: `(cls, provider: types.AgentProvider | None)`. Output annotation: `a2a_pb2.AgentProvider | None`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not provider`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `a2a_pb2.AgentProvider(organization=provider.organization, url=provider.url)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AgentProvider`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def provider(cls, provider: types.AgentProvider | None) -> a2a_pb2.AgentProvider | None:
    if not provider:
        return None
    return a2a_pb2.AgentProvider(organization=provider.organization, url=provider.url)
```

</details>

### `ToProto.security`

Source lines 470–481; declaration kind `FunctionDef`.

Inputs: `(cls, security: list[dict[str, list[str]]] | None)`. Output annotation: `list[a2a_pb2.Security] | None`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not security`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `[a2a_pb2.Security(schemes={k: a2a_pb2.StringList(list=v) for k, v in s.items()}) for s in security]`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.Security`, `a2a_pb2.StringList`, `s.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def security(cls, security: list[dict[str, list[str]]] | None) -> list[a2a_pb2.Security] | None:
    if not security:
        return None
    return [a2a_pb2.Security(schemes={k: a2a_pb2.StringList(list=v) for k, v in s.items()}) for s in security]
```

</details>

### `ToProto.security_schemes`

Source lines 484–490; declaration kind `FunctionDef`.

Inputs: `(cls, schemes: dict[str, types.SecurityScheme] | None)`. Output annotation: `dict[str, a2a_pb2.SecurityScheme] | None`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not schemes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `{k: cls.security_scheme(v) for k, v in schemes.items()}`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `cls.security_scheme`, `schemes.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def security_schemes(cls, schemes: dict[str, types.SecurityScheme] | None) -> dict[str, a2a_pb2.SecurityScheme] | None:
    if not schemes:
        return None
    return {k: cls.security_scheme(v) for k, v in schemes.items()}
```

</details>

### `ToProto.security_scheme`

Source lines 493–531; declaration kind `FunctionDef`.

Inputs: `(cls, scheme: types.SecurityScheme)`. Output annotation: `a2a_pb2.SecurityScheme`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(scheme.root, types.APIKeySecurityScheme)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `isinstance(scheme.root, types.HTTPAuthSecurityScheme)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `isinstance(scheme.root, types.OAuth2SecurityScheme)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `isinstance(scheme.root, types.MutualTLSSecurityScheme)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Returns `a2a_pb2.SecurityScheme(open_id_connect_security_scheme=a2a_pb2.OpenIdConnectSecurityScheme(description=scheme.root.description, open_id_connect_url=scheme.root.open_id_connect_url))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `a2a_pb2.SecurityScheme`, `a2a_pb2.OpenIdConnectSecurityScheme`, `a2a_pb2.APIKeySecurityScheme`, `a2a_pb2.HTTPAuthSecurityScheme`, `a2a_pb2.OAuth2SecurityScheme`, `a2a_pb2.MutualTlsSecurityScheme`, `cls.oauth2_flows`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def security_scheme(cls, scheme: types.SecurityScheme) -> a2a_pb2.SecurityScheme:
    if isinstance(scheme.root, types.APIKeySecurityScheme):
        return a2a_pb2.SecurityScheme(api_key_security_scheme=a2a_pb2.APIKeySecurityScheme(description=scheme.root.description, location=scheme.root.in_.value, name=scheme.root.name))
    if isinstance(scheme.root, types.HTTPAuthSecurityScheme):
        return a2a_pb2.SecurityScheme(http_auth_security_scheme=a2a_pb2.HTTPAuthSecurityScheme(description=scheme.root.description, scheme=scheme.root.scheme, bearer_format=scheme.root.bearer_format))
    if isinstance(scheme.root, types.OAuth2SecurityScheme):
        return a2a_pb2.SecurityScheme(oauth2_security_scheme=a2a_pb2.OAuth2SecurityScheme(description=scheme.root.description, flows=cls.oauth2_flows(scheme.root.flows)))
    if isinstance(scheme.root, types.MutualTLSSecurityScheme):
        return a2a_pb2.SecurityScheme(mtls_security_scheme=a2a_pb2.MutualTlsSecurityScheme(description=scheme.root.description))
    return a2a_pb2.SecurityScheme(open_id_connect_security_scheme=a2a_pb2.OpenIdConnectSecurityScheme(description=scheme.root.description, open_id_connect_url=scheme.root.open_id_connect_url))
```

</details>

### `ToProto.oauth2_flows`

Source lines 534–568; declaration kind `FunctionDef`.

Inputs: `(cls, flows: types.OAuthFlows)`. Output annotation: `a2a_pb2.OAuthFlows`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `flows.authorization_code`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `flows.client_credentials`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `flows.implicit`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `flows.password`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Raises `ValueError('Unknown oauth flow definition')`.

Explicit errors: `ValueError('Unknown oauth flow definition')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `ValueError`, `a2a_pb2.OAuthFlows`, `a2a_pb2.AuthorizationCodeOAuthFlow`, `a2a_pb2.ClientCredentialsOAuthFlow`, `a2a_pb2.ImplicitOAuthFlow`, `a2a_pb2.PasswordOAuthFlow`, `dict`, `flows.authorization_code.scopes.items`, `flows.client_credentials.scopes.items`, `flows.implicit.scopes.items`, `flows.password.scopes.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def oauth2_flows(cls, flows: types.OAuthFlows) -> a2a_pb2.OAuthFlows:
    if flows.authorization_code:
        return a2a_pb2.OAuthFlows(authorization_code=a2a_pb2.AuthorizationCodeOAuthFlow(authorization_url=flows.authorization_code.authorization_url, refresh_url=flows.authorization_code.refresh_url, scopes=dict(flows.authorization_code.scopes.items()), token_url=flows.authorization_code.token_url))
    if flows.client_credentials:
        return a2a_pb2.OAuthFlows(client_credentials=a2a_pb2.ClientCredentialsOAuthFlow(refresh_url=flows.client_credentials.refresh_url, scopes=dict(flows.client_credentials.scopes.items()), token_url=flows.client_credentials.token_url))
    if flows.implicit:
        return a2a_pb2.OAuthFlows(implicit=a2a_pb2.ImplicitOAuthFlow(authorization_url=flows.implicit.authorization_url, refresh_url=flows.implicit.refresh_url, scopes=dict(flows.implicit.scopes.items())))
    if flows.password:
        return a2a_pb2.OAuthFlows(password=a2a_pb2.PasswordOAuthFlow(refresh_url=flows.password.refresh_url, scopes=dict(flows.password.scopes.items()), token_url=flows.password.token_url))
    raise ValueError('Unknown oauth flow definition')
```

</details>

### `ToProto.skill`

Source lines 571–580; declaration kind `FunctionDef`.

Inputs: `(cls, skill: types.AgentSkill)`. Output annotation: `a2a_pb2.AgentSkill`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `a2a_pb2.AgentSkill(id=skill.id, name=skill.name, description=skill.description, tags=skill.tags, examples=skill.examples, input_modes=skill.input_modes, output_modes=skill.output_modes)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `a2a_pb2.AgentSkill`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def skill(cls, skill: types.AgentSkill) -> a2a_pb2.AgentSkill:
    return a2a_pb2.AgentSkill(id=skill.id, name=skill.name, description=skill.description, tags=skill.tags, examples=skill.examples, input_modes=skill.input_modes, output_modes=skill.output_modes)
```

</details>

### `ToProto.role`

Source lines 583–590; declaration kind `FunctionDef`.

Inputs: `(cls, role: types.Role)`. Output annotation: `a2a_pb2.Role`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Dispatches on `role` using the exact case map below; default case controls unsupported/unknown input.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def role(cls, role: types.Role) -> a2a_pb2.Role:
    match role:
        case types.Role.user:
            return a2a_pb2.Role.ROLE_USER
        case types.Role.agent:
            return a2a_pb2.Role.ROLE_AGENT
        case _:
            return a2a_pb2.Role.ROLE_UNSPECIFIED
```

</details>

### `FromProto`

Source lines 593–1099; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Converts proto types to Python types.

Declared operations: `message`, `metadata`, `part`, `data`, `file`, `task_or_message`, `task`, `task_status`, `task_state`, `artifact`, `task_artifact_update_event`, `task_status_update_event`, `push_notification_config`, `authentication_info`, `message_send_configuration`, `message_send_params`, `task_id_params`, `task_push_notification_config_request`, `task_push_notification_config`, `agent_card`, `agent_card_signature`, `agent_interface`, `task_query_params`, `capabilities`, `agent_extension`, `security`, `provider`, `security_schemes`, `security_scheme`, `oauth2_flows`, `stream_response`, `list_task_push_notification_config_response`, `skill`, `role`. Each method is traced below; constructor determines retained state.

### `FromProto.message`

Source lines 597–606; declaration kind `FunctionDef`.

Inputs: `(cls, message: a2a_pb2.Message)`. Output annotation: `types.Message`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.Message(message_id=message.message_id, parts=[cls.part(p) for p in message.content], context_id=message.context_id or None, task_id=message.task_id or None, role=cls.role(message.role), metadata=cls.metadata(message.metadata), extensions=list(message.extensions) or None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.Message`, `cls.role`, `cls.metadata`, `cls.part`, `list`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def message(cls, message: a2a_pb2.Message) -> types.Message:
    return types.Message(message_id=message.message_id, parts=[cls.part(p) for p in message.content], context_id=message.context_id or None, task_id=message.task_id or None, role=cls.role(message.role), metadata=cls.metadata(message.metadata), extensions=list(message.extensions) or None)
```

</details>

### `FromProto.metadata`

Source lines 609–612; declaration kind `FunctionDef`.

Inputs: `(cls, metadata: struct_pb2.Struct)`. Output annotation: `dict[str, Any]`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not metadata.fields`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `json_format.MessageToDict(metadata)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `json_format.MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def metadata(cls, metadata: struct_pb2.Struct) -> dict[str, Any]:
    if not metadata.fields:
        return {}
    return json_format.MessageToDict(metadata)
```

</details>

### `FromProto.part`

Source lines 615–643; declaration kind `FunctionDef`.

Inputs: `(cls, part: a2a_pb2.Part)`. Output annotation: `types.Part`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `part.HasField('text')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `part.HasField('file')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `part.HasField('data')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Raises `ValueError(f'Unsupported part type: {part}')`.

Explicit errors: `ValueError(f'Unsupported part type: {part}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `part.HasField`, `ValueError`, `types.Part`, `types.TextPart`, `types.FilePart`, `types.DataPart`, `cls.file`, `cls.data`, `cls.metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def part(cls, part: a2a_pb2.Part) -> types.Part:
    if part.HasField('text'):
        return types.Part(root=types.TextPart(text=part.text, metadata=cls.metadata(part.metadata) if part.metadata else None))
    if part.HasField('file'):
        return types.Part(root=types.FilePart(file=cls.file(part.file), metadata=cls.metadata(part.metadata) if part.metadata else None))
    if part.HasField('data'):
        return types.Part(root=types.DataPart(data=cls.data(part.data), metadata=cls.metadata(part.metadata) if part.metadata else None))
    raise ValueError(f'Unsupported part type: {part}')
```

</details>

### `FromProto.data`

Source lines 646–648; declaration kind `FunctionDef`.

Inputs: `(cls, data: a2a_pb2.DataPart)`. Output annotation: `dict[str, Any]`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `json_data` from `json_format.MessageToJson(data.data)`; output construction/calls here execute immediately when this method runs.
2. Returns `json.loads(json_data)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `json_format.MessageToJson`, `json.loads`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def data(cls, data: a2a_pb2.DataPart) -> dict[str, Any]:
    json_data = json_format.MessageToJson(data.data)
    return json.loads(json_data)
```

</details>

### `FromProto.file`

Source lines 651–666; declaration kind `FunctionDef`.

Inputs: `(cls, file: a2a_pb2.FilePart)`. Output annotation: `types.FileWithUri | types.FileWithBytes`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `common_args` from `{'mime_type': file.mime_type or None, 'name': file.name or None}`; output construction/calls here execute immediately when this method runs.
2. Branches on `file.HasField('file_with_uri')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `types.FileWithBytes(bytes=file.file_with_bytes.decode('utf-8'), **common_args)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `file.HasField`, `types.FileWithBytes`, `types.FileWithUri`, `file.file_with_bytes.decode`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def file(cls, file: a2a_pb2.FilePart) -> types.FileWithUri | types.FileWithBytes:
    common_args = {'mime_type': file.mime_type or None, 'name': file.name or None}
    if file.HasField('file_with_uri'):
        return types.FileWithUri(uri=file.file_with_uri, **common_args)
    return types.FileWithBytes(bytes=file.file_with_bytes.decode('utf-8'), **common_args)
```

</details>

### `FromProto.task_or_message`

Source lines 669–674; declaration kind `FunctionDef`.

Inputs: `(cls, event: a2a_pb2.SendMessageResponse)`. Output annotation: `types.Task | types.Message`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `event.HasField('msg')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `cls.task(event.task)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `event.HasField`, `cls.task`, `cls.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_or_message(cls, event: a2a_pb2.SendMessageResponse) -> types.Task | types.Message:
    if event.HasField('msg'):
        return cls.message(event.msg)
    return cls.task(event.task)
```

</details>

### `FromProto.task`

Source lines 677–685; declaration kind `FunctionDef`.

Inputs: `(cls, task: a2a_pb2.Task)`. Output annotation: `types.Task`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.Task(id=task.id, context_id=task.context_id, status=cls.task_status(task.status), artifacts=[cls.artifact(a) for a in task.artifacts], history=[cls.message(h) for h in task.history], metadata=cls.metadata(task.metadata))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.Task`, `cls.task_status`, `cls.metadata`, `cls.artifact`, `cls.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task(cls, task: a2a_pb2.Task) -> types.Task:
    return types.Task(id=task.id, context_id=task.context_id, status=cls.task_status(task.status), artifacts=[cls.artifact(a) for a in task.artifacts], history=[cls.message(h) for h in task.history], metadata=cls.metadata(task.metadata))
```

</details>

### `FromProto.task_status`

Source lines 688–692; declaration kind `FunctionDef`.

Inputs: `(cls, status: a2a_pb2.TaskStatus)`. Output annotation: `types.TaskStatus`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.TaskStatus(state=cls.task_state(status.state), message=cls.message(status.update))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.TaskStatus`, `cls.task_state`, `cls.message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_status(cls, status: a2a_pb2.TaskStatus) -> types.TaskStatus:
    return types.TaskStatus(state=cls.task_state(status.state), message=cls.message(status.update))
```

</details>

### `FromProto.task_state`

Source lines 695–714; declaration kind `FunctionDef`.

Inputs: `(cls, state: a2a_pb2.TaskState)`. Output annotation: `types.TaskState`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Dispatches on `state` using the exact case map below; default case controls unsupported/unknown input.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_state(cls, state: a2a_pb2.TaskState) -> types.TaskState:
    match state:
        case a2a_pb2.TaskState.TASK_STATE_SUBMITTED:
            return types.TaskState.submitted
        case a2a_pb2.TaskState.TASK_STATE_WORKING:
            return types.TaskState.working
        case a2a_pb2.TaskState.TASK_STATE_COMPLETED:
            return types.TaskState.completed
        case a2a_pb2.TaskState.TASK_STATE_CANCELLED:
            return types.TaskState.canceled
        case a2a_pb2.TaskState.TASK_STATE_FAILED:
            return types.TaskState.failed
        case a2a_pb2.TaskState.TASK_STATE_INPUT_REQUIRED:
            return types.TaskState.input_required
        case a2a_pb2.TaskState.TASK_STATE_AUTH_REQUIRED:
            return types.TaskState.auth_required
        case a2a_pb2.TaskState.TASK_STATE_REJECTED:
            return types.TaskState.rejected
        case _:
            return types.TaskState.unknown
```

</details>

### `FromProto.artifact`

Source lines 717–725; declaration kind `FunctionDef`.

Inputs: `(cls, artifact: a2a_pb2.Artifact)`. Output annotation: `types.Artifact`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.Artifact(artifact_id=artifact.artifact_id, description=artifact.description, metadata=cls.metadata(artifact.metadata), name=artifact.name, parts=[cls.part(p) for p in artifact.parts], extensions=artifact.extensions or None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.Artifact`, `cls.metadata`, `cls.part`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def artifact(cls, artifact: a2a_pb2.Artifact) -> types.Artifact:
    return types.Artifact(artifact_id=artifact.artifact_id, description=artifact.description, metadata=cls.metadata(artifact.metadata), name=artifact.name, parts=[cls.part(p) for p in artifact.parts], extensions=artifact.extensions or None)
```

</details>

### `FromProto.task_artifact_update_event`

Source lines 728–738; declaration kind `FunctionDef`.

Inputs: `(cls, event: a2a_pb2.TaskArtifactUpdateEvent)`. Output annotation: `types.TaskArtifactUpdateEvent`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.TaskArtifactUpdateEvent(task_id=event.task_id, context_id=event.context_id, artifact=cls.artifact(event.artifact), metadata=cls.metadata(event.metadata), append=event.append, last_chunk=event.last_chunk)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.TaskArtifactUpdateEvent`, `cls.artifact`, `cls.metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_artifact_update_event(cls, event: a2a_pb2.TaskArtifactUpdateEvent) -> types.TaskArtifactUpdateEvent:
    return types.TaskArtifactUpdateEvent(task_id=event.task_id, context_id=event.context_id, artifact=cls.artifact(event.artifact), metadata=cls.metadata(event.metadata), append=event.append, last_chunk=event.last_chunk)
```

</details>

### `FromProto.task_status_update_event`

Source lines 741–750; declaration kind `FunctionDef`.

Inputs: `(cls, event: a2a_pb2.TaskStatusUpdateEvent)`. Output annotation: `types.TaskStatusUpdateEvent`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.TaskStatusUpdateEvent(task_id=event.task_id, context_id=event.context_id, status=cls.task_status(event.status), metadata=cls.metadata(event.metadata), final=event.final)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.TaskStatusUpdateEvent`, `cls.task_status`, `cls.metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_status_update_event(cls, event: a2a_pb2.TaskStatusUpdateEvent) -> types.TaskStatusUpdateEvent:
    return types.TaskStatusUpdateEvent(task_id=event.task_id, context_id=event.context_id, status=cls.task_status(event.status), metadata=cls.metadata(event.metadata), final=event.final)
```

</details>

### `FromProto.push_notification_config`

Source lines 753–763; declaration kind `FunctionDef`.

Inputs: `(cls, config: a2a_pb2.PushNotificationConfig)`. Output annotation: `types.PushNotificationConfig`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.PushNotificationConfig(id=config.id, url=config.url, token=config.token, authentication=cls.authentication_info(config.authentication) if config.HasField('authentication') else None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.PushNotificationConfig`, `config.HasField`, `cls.authentication_info`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def push_notification_config(cls, config: a2a_pb2.PushNotificationConfig) -> types.PushNotificationConfig:
    return types.PushNotificationConfig(id=config.id, url=config.url, token=config.token, authentication=cls.authentication_info(config.authentication) if config.HasField('authentication') else None)
```

</details>

### `FromProto.authentication_info`

Source lines 766–772; declaration kind `FunctionDef`.

Inputs: `(cls, info: a2a_pb2.AuthenticationInfo)`. Output annotation: `types.PushNotificationAuthenticationInfo`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.PushNotificationAuthenticationInfo(schemes=list(info.schemes), credentials=info.credentials)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.PushNotificationAuthenticationInfo`, `list`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def authentication_info(cls, info: a2a_pb2.AuthenticationInfo) -> types.PushNotificationAuthenticationInfo:
    return types.PushNotificationAuthenticationInfo(schemes=list(info.schemes), credentials=info.credentials)
```

</details>

### `FromProto.message_send_configuration`

Source lines 775–787; declaration kind `FunctionDef`.

Inputs: `(cls, config: a2a_pb2.SendMessageConfiguration)`. Output annotation: `types.MessageSendConfiguration`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.MessageSendConfiguration(accepted_output_modes=list(config.accepted_output_modes), push_notification_config=cls.push_notification_config(config.push_notification) if config.HasField('push_notification') else None, history_length=config.history_length, blocking=config.blocking)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.MessageSendConfiguration`, `list`, `config.HasField`, `cls.push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def message_send_configuration(cls, config: a2a_pb2.SendMessageConfiguration) -> types.MessageSendConfiguration:
    return types.MessageSendConfiguration(accepted_output_modes=list(config.accepted_output_modes), push_notification_config=cls.push_notification_config(config.push_notification) if config.HasField('push_notification') else None, history_length=config.history_length, blocking=config.blocking)
```

</details>

### `FromProto.message_send_params`

Source lines 790–797; declaration kind `FunctionDef`.

Inputs: `(cls, request: a2a_pb2.SendMessageRequest)`. Output annotation: `types.MessageSendParams`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.MessageSendParams(configuration=cls.message_send_configuration(request.configuration), message=cls.message(request.request), metadata=cls.metadata(request.metadata))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.MessageSendParams`, `cls.message_send_configuration`, `cls.message`, `cls.metadata`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def message_send_params(cls, request: a2a_pb2.SendMessageRequest) -> types.MessageSendParams:
    return types.MessageSendParams(configuration=cls.message_send_configuration(request.configuration), message=cls.message(request.request), metadata=cls.metadata(request.metadata))
```

</details>

### `FromProto.task_id_params`

Source lines 800–816; declaration kind `FunctionDef`.

Inputs: `(cls, request: a2a_pb2.CancelTaskRequest | a2a_pb2.TaskSubscriptionRequest | a2a_pb2.GetTaskPushNotificationConfigRequest)`. Output annotation: `types.TaskIdParams`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(request, a2a_pb2.GetTaskPushNotificationConfigRequest)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Assigns `m` from `TASK_NAME_MATCH.match(request.name)`; output construction/calls here execute immediately when this method runs.
3. Branches on `not m`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `types.TaskIdParams(id=m.group(1))`; this is the output/delegation boundary for this path.

Explicit errors: `InvalidParamsError(message=f'No task for {request.name}')`; `InvalidParamsError(message=f'No task for {request.name}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `TASK_NAME_MATCH.match`, `types.TaskIdParams`, `TASK_PUSH_CONFIG_NAME_MATCH.match`, `InvalidParamsError`, `m.group`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_id_params(cls, request: a2a_pb2.CancelTaskRequest | a2a_pb2.TaskSubscriptionRequest | a2a_pb2.GetTaskPushNotificationConfigRequest) -> types.TaskIdParams:
    if isinstance(request, a2a_pb2.GetTaskPushNotificationConfigRequest):
        m = TASK_PUSH_CONFIG_NAME_MATCH.match(request.name)
        if not m:
            raise InvalidParamsError(message=f'No task for {request.name}')
        return types.TaskIdParams(id=m.group(1))
    m = TASK_NAME_MATCH.match(request.name)
    if not m:
        raise InvalidParamsError(message=f'No task for {request.name}')
    return types.TaskIdParams(id=m.group(1))
```

</details>

### `FromProto.task_push_notification_config_request`

Source lines 819–831; declaration kind `FunctionDef`.

Inputs: `(cls, request: a2a_pb2.CreateTaskPushNotificationConfigRequest)`. Output annotation: `types.TaskPushNotificationConfig`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `m` from `TASK_NAME_MATCH.match(request.parent)`; output construction/calls here execute immediately when this method runs.
2. Branches on `not m`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `types.TaskPushNotificationConfig(push_notification_config=cls.push_notification_config(request.config.push_notification_config), task_id=m.group(1))`; this is the output/delegation boundary for this path.

Explicit errors: `InvalidParamsError(message=f'No task for {request.parent}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `TASK_NAME_MATCH.match`, `types.TaskPushNotificationConfig`, `InvalidParamsError`, `cls.push_notification_config`, `m.group`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_push_notification_config_request(cls, request: a2a_pb2.CreateTaskPushNotificationConfigRequest) -> types.TaskPushNotificationConfig:
    m = TASK_NAME_MATCH.match(request.parent)
    if not m:
        raise InvalidParamsError(message=f'No task for {request.parent}')
    return types.TaskPushNotificationConfig(push_notification_config=cls.push_notification_config(request.config.push_notification_config), task_id=m.group(1))
```

</details>

### `FromProto.task_push_notification_config`

Source lines 834–848; declaration kind `FunctionDef`.

Inputs: `(cls, config: a2a_pb2.TaskPushNotificationConfig)`. Output annotation: `types.TaskPushNotificationConfig`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `m` from `TASK_PUSH_CONFIG_NAME_MATCH.match(config.name)`; output construction/calls here execute immediately when this method runs.
2. Branches on `not m`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `types.TaskPushNotificationConfig(push_notification_config=cls.push_notification_config(config.push_notification_config), task_id=m.group(1))`; this is the output/delegation boundary for this path.

Explicit errors: `InvalidParamsError(message=f'Bad TaskPushNotificationConfig resource name {config.name}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `TASK_PUSH_CONFIG_NAME_MATCH.match`, `types.TaskPushNotificationConfig`, `InvalidParamsError`, `cls.push_notification_config`, `m.group`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_push_notification_config(cls, config: a2a_pb2.TaskPushNotificationConfig) -> types.TaskPushNotificationConfig:
    m = TASK_PUSH_CONFIG_NAME_MATCH.match(config.name)
    if not m:
        raise InvalidParamsError(message=f'Bad TaskPushNotificationConfig resource name {config.name}')
    return types.TaskPushNotificationConfig(push_notification_config=cls.push_notification_config(config.push_notification_config), task_id=m.group(1))
```

</details>

### `FromProto.agent_card`

Source lines 851–879; declaration kind `FunctionDef`.

Inputs: `(cls, card: a2a_pb2.AgentCard)`. Output annotation: `types.AgentCard`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.AgentCard(capabilities=cls.capabilities(card.capabilities), default_input_modes=list(card.default_input_modes), default_output_modes=list(card.default_output_modes), description=card.description, documentation_url=card.documentation_url, name=card.name, provider=cls.provider(card.provider), security=cls.security(list(card.security)), security_schemes=c … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.AgentCard`, `cls.capabilities`, `list`, `cls.provider`, `cls.security`, `cls.security_schemes`, `dict`, `cls.skill`, `cls.agent_interface`, `cls.agent_card_signature`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def agent_card(cls, card: a2a_pb2.AgentCard) -> types.AgentCard:
    return types.AgentCard(capabilities=cls.capabilities(card.capabilities), default_input_modes=list(card.default_input_modes), default_output_modes=list(card.default_output_modes), description=card.description, documentation_url=card.documentation_url, name=card.name, provider=cls.provider(card.provider), security=cls.security(list(card.security)), security_schemes=cls.security_schemes(dict(card.security_schemes)), skills=[cls.skill(x) for x in card.skills] if card.skills else [], url=card.url, version=card.version, supports_authenticated_extended_card=card.supports_authenticated_extended_card, preferred_transport=card.preferred_transport, protocol_version=card.protocol_version, additional_interfaces=[cls.agent_interface(x) for x in card.additional_interfaces] if card.additional_interfaces else None, signatures=[cls.agent_card_signature(x) for x in card.signatures] if card.signatures else None)
```

</details>

### `FromProto.agent_card_signature`

Source lines 882–889; declaration kind `FunctionDef`.

Inputs: `(cls, signature: a2a_pb2.AgentCardSignature)`. Output annotation: `types.AgentCardSignature`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.AgentCardSignature(protected=signature.protected, signature=signature.signature, header=json_format.MessageToDict(signature.header))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.AgentCardSignature`, `json_format.MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def agent_card_signature(cls, signature: a2a_pb2.AgentCardSignature) -> types.AgentCardSignature:
    return types.AgentCardSignature(protected=signature.protected, signature=signature.signature, header=json_format.MessageToDict(signature.header))
```

</details>

### `FromProto.agent_interface`

Source lines 892–899; declaration kind `FunctionDef`.

Inputs: `(cls, interface: a2a_pb2.AgentInterface)`. Output annotation: `types.AgentInterface`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.AgentInterface(transport=interface.transport, url=interface.url)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.AgentInterface`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def agent_interface(cls, interface: a2a_pb2.AgentInterface) -> types.AgentInterface:
    return types.AgentInterface(transport=interface.transport, url=interface.url)
```

</details>

### `FromProto.task_query_params`

Source lines 902–915; declaration kind `FunctionDef`.

Inputs: `(cls, request: a2a_pb2.GetTaskRequest)`. Output annotation: `types.TaskQueryParams`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `m` from `TASK_NAME_MATCH.match(request.name)`; output construction/calls here execute immediately when this method runs.
2. Branches on `not m`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `types.TaskQueryParams(history_length=request.history_length if request.history_length else None, id=m.group(1), metadata=None)`; this is the output/delegation boundary for this path.

Explicit errors: `InvalidParamsError(message=f'No task for {request.name}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `TASK_NAME_MATCH.match`, `types.TaskQueryParams`, `InvalidParamsError`, `m.group`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def task_query_params(cls, request: a2a_pb2.GetTaskRequest) -> types.TaskQueryParams:
    m = TASK_NAME_MATCH.match(request.name)
    if not m:
        raise InvalidParamsError(message=f'No task for {request.name}')
    return types.TaskQueryParams(history_length=request.history_length if request.history_length else None, id=m.group(1), metadata=None)
```

</details>

### `FromProto.capabilities`

Source lines 918–927; declaration kind `FunctionDef`.

Inputs: `(cls, capabilities: a2a_pb2.AgentCapabilities)`. Output annotation: `types.AgentCapabilities`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.AgentCapabilities(streaming=capabilities.streaming, push_notifications=capabilities.push_notifications, extensions=[cls.agent_extension(x) for x in capabilities.extensions])`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.AgentCapabilities`, `cls.agent_extension`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def capabilities(cls, capabilities: a2a_pb2.AgentCapabilities) -> types.AgentCapabilities:
    return types.AgentCapabilities(streaming=capabilities.streaming, push_notifications=capabilities.push_notifications, extensions=[cls.agent_extension(x) for x in capabilities.extensions])
```

</details>

### `FromProto.agent_extension`

Source lines 930–939; declaration kind `FunctionDef`.

Inputs: `(cls, extension: a2a_pb2.AgentExtension)`. Output annotation: `types.AgentExtension`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.AgentExtension(uri=extension.uri, description=extension.description, params=json_format.MessageToDict(extension.params), required=extension.required)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.AgentExtension`, `json_format.MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def agent_extension(cls, extension: a2a_pb2.AgentExtension) -> types.AgentExtension:
    return types.AgentExtension(uri=extension.uri, description=extension.description, params=json_format.MessageToDict(extension.params), required=extension.required)
```

</details>

### `FromProto.security`

Source lines 942–950; declaration kind `FunctionDef`.

Inputs: `(cls, security: list[a2a_pb2.Security] | None)`. Output annotation: `list[dict[str, list[str]]] | None`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not security`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `[{k: list(v.list) for k, v in s.schemes.items()} for s in security]`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `list`, `s.schemes.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def security(cls, security: list[a2a_pb2.Security] | None) -> list[dict[str, list[str]]] | None:
    if not security:
        return None
    return [{k: list(v.list) for k, v in s.schemes.items()} for s in security]
```

</details>

### `FromProto.provider`

Source lines 953–961; declaration kind `FunctionDef`.

Inputs: `(cls, provider: a2a_pb2.AgentProvider | None)`. Output annotation: `types.AgentProvider | None`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `not provider`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `types.AgentProvider(organization=provider.organization, url=provider.url)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.AgentProvider`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def provider(cls, provider: a2a_pb2.AgentProvider | None) -> types.AgentProvider | None:
    if not provider:
        return None
    return types.AgentProvider(organization=provider.organization, url=provider.url)
```

</details>

### `FromProto.security_schemes`

Source lines 964–967; declaration kind `FunctionDef`.

Inputs: `(cls, schemes: dict[str, a2a_pb2.SecurityScheme])`. Output annotation: `dict[str, types.SecurityScheme]`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `{k: cls.security_scheme(v) for k, v in schemes.items()}`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `cls.security_scheme`, `schemes.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def security_schemes(cls, schemes: dict[str, a2a_pb2.SecurityScheme]) -> dict[str, types.SecurityScheme]:
    return {k: cls.security_scheme(v) for k, v in schemes.items()}
```

</details>

### `FromProto.security_scheme`

Source lines 970–1008; declaration kind `FunctionDef`.

Inputs: `(cls, scheme: a2a_pb2.SecurityScheme)`. Output annotation: `types.SecurityScheme`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `scheme.HasField('api_key_security_scheme')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `scheme.HasField('http_auth_security_scheme')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `scheme.HasField('oauth2_security_scheme')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `scheme.HasField('mtls_security_scheme')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Returns `types.SecurityScheme(root=types.OpenIdConnectSecurityScheme(description=scheme.open_id_connect_security_scheme.description, open_id_connect_url=scheme.open_id_connect_security_scheme.open_id_connect_url))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `scheme.HasField`, `types.SecurityScheme`, `types.OpenIdConnectSecurityScheme`, `types.APIKeySecurityScheme`, `types.HTTPAuthSecurityScheme`, `types.OAuth2SecurityScheme`, `types.MutualTLSSecurityScheme`, `types.In`, `cls.oauth2_flows`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def security_scheme(cls, scheme: a2a_pb2.SecurityScheme) -> types.SecurityScheme:
    if scheme.HasField('api_key_security_scheme'):
        return types.SecurityScheme(root=types.APIKeySecurityScheme(description=scheme.api_key_security_scheme.description, name=scheme.api_key_security_scheme.name, in_=types.In(scheme.api_key_security_scheme.location)))
    if scheme.HasField('http_auth_security_scheme'):
        return types.SecurityScheme(root=types.HTTPAuthSecurityScheme(description=scheme.http_auth_security_scheme.description, scheme=scheme.http_auth_security_scheme.scheme, bearer_format=scheme.http_auth_security_scheme.bearer_format))
    if scheme.HasField('oauth2_security_scheme'):
        return types.SecurityScheme(root=types.OAuth2SecurityScheme(description=scheme.oauth2_security_scheme.description, flows=cls.oauth2_flows(scheme.oauth2_security_scheme.flows)))
    if scheme.HasField('mtls_security_scheme'):
        return types.SecurityScheme(root=types.MutualTLSSecurityScheme(description=scheme.mtls_security_scheme.description))
    return types.SecurityScheme(root=types.OpenIdConnectSecurityScheme(description=scheme.open_id_connect_security_scheme.description, open_id_connect_url=scheme.open_id_connect_security_scheme.open_id_connect_url))
```

</details>

### `FromProto.oauth2_flows`

Source lines 1011–1043; declaration kind `FunctionDef`.

Inputs: `(cls, flows: a2a_pb2.OAuthFlows)`. Output annotation: `types.OAuthFlows`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `flows.HasField('authorization_code')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `flows.HasField('client_credentials')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `flows.HasField('implicit')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `types.OAuthFlows(password=types.PasswordOAuthFlow(refresh_url=flows.password.refresh_url, scopes=dict(flows.password.scopes.items()), token_url=flows.password.token_url))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `flows.HasField`, `types.OAuthFlows`, `types.PasswordOAuthFlow`, `types.AuthorizationCodeOAuthFlow`, `types.ClientCredentialsOAuthFlow`, `types.ImplicitOAuthFlow`, `dict`, `flows.password.scopes.items`, `flows.authorization_code.scopes.items`, `flows.client_credentials.scopes.items`, `flows.implicit.scopes.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def oauth2_flows(cls, flows: a2a_pb2.OAuthFlows) -> types.OAuthFlows:
    if flows.HasField('authorization_code'):
        return types.OAuthFlows(authorization_code=types.AuthorizationCodeOAuthFlow(authorization_url=flows.authorization_code.authorization_url, refresh_url=flows.authorization_code.refresh_url, scopes=dict(flows.authorization_code.scopes.items()), token_url=flows.authorization_code.token_url))
    if flows.HasField('client_credentials'):
        return types.OAuthFlows(client_credentials=types.ClientCredentialsOAuthFlow(refresh_url=flows.client_credentials.refresh_url, scopes=dict(flows.client_credentials.scopes.items()), token_url=flows.client_credentials.token_url))
    if flows.HasField('implicit'):
        return types.OAuthFlows(implicit=types.ImplicitOAuthFlow(authorization_url=flows.implicit.authorization_url, refresh_url=flows.implicit.refresh_url, scopes=dict(flows.implicit.scopes.items())))
    return types.OAuthFlows(password=types.PasswordOAuthFlow(refresh_url=flows.password.refresh_url, scopes=dict(flows.password.scopes.items()), token_url=flows.password.token_url))
```

</details>

### `FromProto.stream_response`

Source lines 1046–1063; declaration kind `FunctionDef`.

Inputs: `(cls, response: a2a_pb2.StreamResponse)`. Output annotation: `types.Message | types.Task | types.TaskStatusUpdateEvent | types.TaskArtifactUpdateEvent`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `response.HasField('msg')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Branches on `response.HasField('task')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `response.HasField('status_update')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `response.HasField('artifact_update')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Raises `ValueError('Unsupported StreamResponse type')`.

Explicit errors: `ValueError('Unsupported StreamResponse type')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `response.HasField`, `ValueError`, `cls.message`, `cls.task`, `cls.task_status_update_event`, `cls.task_artifact_update_event`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def stream_response(cls, response: a2a_pb2.StreamResponse) -> types.Message | types.Task | types.TaskStatusUpdateEvent | types.TaskArtifactUpdateEvent:
    if response.HasField('msg'):
        return cls.message(response.msg)
    if response.HasField('task'):
        return cls.task(response.task)
    if response.HasField('status_update'):
        return cls.task_status_update_event(response.status_update)
    if response.HasField('artifact_update'):
        return cls.task_artifact_update_event(response.artifact_update)
    raise ValueError('Unsupported StreamResponse type')
```

</details>

### `FromProto.list_task_push_notification_config_response`

Source lines 1066–1077; declaration kind `FunctionDef`.

Inputs: `(cls, response: a2a_pb2.ListTaskPushNotificationConfigResponse)`. Output annotation: `types.ListTaskPushNotificationConfigResponse`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.ListTaskPushNotificationConfigResponse(root=types.ListTaskPushNotificationConfigSuccessResponse(result=[cls.task_push_notification_config(c) for c in response.configs], id=None))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.ListTaskPushNotificationConfigResponse`, `types.ListTaskPushNotificationConfigSuccessResponse`, `cls.task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def list_task_push_notification_config_response(cls, response: a2a_pb2.ListTaskPushNotificationConfigResponse) -> types.ListTaskPushNotificationConfigResponse:
    return types.ListTaskPushNotificationConfigResponse(root=types.ListTaskPushNotificationConfigSuccessResponse(result=[cls.task_push_notification_config(c) for c in response.configs], id=None))
```

</details>

### `FromProto.skill`

Source lines 1080–1089; declaration kind `FunctionDef`.

Inputs: `(cls, skill: a2a_pb2.AgentSkill)`. Output annotation: `types.AgentSkill`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types.AgentSkill(id=skill.id, name=skill.name, description=skill.description, tags=list(skill.tags), examples=list(skill.examples), input_modes=list(skill.input_modes), output_modes=list(skill.output_modes))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types.AgentSkill`, `list`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def skill(cls, skill: a2a_pb2.AgentSkill) -> types.AgentSkill:
    return types.AgentSkill(id=skill.id, name=skill.name, description=skill.description, tags=list(skill.tags), examples=list(skill.examples), input_modes=list(skill.input_modes), output_modes=list(skill.output_modes))
```

</details>

### `FromProto.role`

Source lines 1092–1099; declaration kind `FunctionDef`.

Inputs: `(cls, role: a2a_pb2.Role)`. Output annotation: `types.Role`. Decorators: `classmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Dispatches on `role` using the exact case map below; default case controls unsupported/unknown input.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@classmethod
def role(cls, role: a2a_pb2.Role) -> types.Role:
    match role:
        case a2a_pb2.Role.ROLE_USER:
            return types.Role.user
        case a2a_pb2.Role.ROLE_AGENT:
            return types.Role.agent
        case _:
            return types.Role.agent
```

</details>
