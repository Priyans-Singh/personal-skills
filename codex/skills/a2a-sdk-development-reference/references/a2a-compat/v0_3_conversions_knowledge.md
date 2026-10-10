# v0_3/conversions.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/conversions.py`. SHA-256: `ba4148b95cf79a3a4476e613f5d40cedc6633405513dfb56e3f67df70b61bfa9`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Mental model: current core ↔ legacy pivot

All functions are synchronous structural conversions. They allocate output messages/models and recurse through local helpers; they perform no I/O, retry, polling, persistence, signing, credential acquisition, URL fetching, or cancellation. Inputs are the annotated model types, not arbitrary dictionaries; Pydantic/protobuf conversion failures propagate. Request envelope IDs belong to JSON-RPC only and are supplied separately for legacy output. `to_core_*` does not transfer those IDs to business task/message IDs.

## Content and identity translation

Part text maps directly. Legacy file base64 strings decode into core `raw` bytes; URI maps to `url`; MIME/name map to `media_type`/`filename`. Core raw bytes encode to base64 text on the reverse path. No URI is opened. Python's default `b64decode` is used without strict validation. Unsupported core content raises `ValueError`; an unrecognized pivot part yields an empty core part. Part metadata becomes protobuf Struct via `ParseDict`.

Core `data` is protobuf Value, while legacy DataPart requires a dictionary. Non-dict Value output is wrapped as `{'value': value}` and tagged with metadata `data_part_compat=True`. Returning to core removes the tag and `ParseDict`s the wrapped value into Value; the untagged path parses into `struct_value`. A peer-controlled tag can change interpretation and a missing `value` produces `KeyError`. Object data whose own key is `value` remains ordinary object data unless tagged. Empty metadata and optional absence do not always survive round trips.

Message IDs, context IDs, task IDs, references, extensions, parts and metadata map explicitly. Missing legacy context/task becomes core empty string; reverse empty values become `None`. User maps to ROLE_USER; any other core role maps to legacy agent, including unspecified. Task history and artifacts recurse; no core status yields a legacy unknown status. State map includes canceled (one l) and all nine legacy states. Unknown enum values fall back to unspecified/unknown. Status timestamp uses `FromJsonString` after replacing `+00:00` with `Z`; malformed timestamps propagate protobuf errors. Reverse uses `ToJsonString` only on presence.

## Configuration, events, and lossy edges

`blocking` is inverted to core `return_immediately` only when non-None; the core default is false (blocking). Reverse always emits `blocking=not return_immediately`. Optional history length uses presence, preserving zero on this direct bridge. Output modes and push settings recurse.

Status-update input `final` is discarded. Reverse recomputes final for completed, canceled, failed, rejected only; input-required/auth-required are false here. Artifact append/last_chunk copy when supplied; reverse emits core bool values even when defaults. These converters do not terminate a stream themselves. `to_core_send_message_response` and `to_core_list_task_push_notification_config_response` return empty core output for legacy error roots, so callers must handle errors before conversion. Unknown core stream oneof raises `ValueError`; unknown legacy runtime event produces empty core StreamResponse.

## Agent cards and security

Legacy primary url/preferredTransport/protocolVersion becomes first supported interface; default binding JSONRPC and default version 0.3. Additional legacy interfaces get version 0.3. Reverse keeps interfaces with empty version or `is_legacy_version`, selects the first, and raises `VersionNotSupportedError` when none qualify. It does not select based on endpoint health or binding availability. Provider, skills, modes, security requirements, extensions and signatures recurse. Authenticated extended-card flag moves into capabilities. State-transition history is dropped. Signatures are copied, never verified or recomputed after structural changes.

Security requirements translate maps of scheme name to lists of scopes into `SecurityRequirement.schemes[StringList]`. API key, HTTP, OAuth2, OIDC and mTLS branches are distinct; mTLS explicitly `SetInParent`s its empty submessage. Reverse unknown scheme raises `ValueError` and invalid API-key location raises enum construction `ValueError`. OAuth legacy models may hold multiple flows, but core has a oneof: assignment order authorization-code, client-credentials, implicit, password makes the **last present** win. Reverse core device-code flow disappears. This differs from legacy proto utility's first-present selection.

Push configuration moves taskId from the legacy wrapper into flattened core TaskPushNotificationConfig. URL/token/credentials remain string values. Legacy authentication schemes list becomes only its first element in core `scheme`; reverse returns zero or one. These are credentials for the configured callback destination, not outgoing A2A peer authorization. Conversion does not expire, rotate, encrypt, or use them.

## Request/response envelopes

Send requests translate message/configuration/metadata. Get task carries ID and optional history; metadata is dropped there. Cancel carries metadata. Subscribe only carries task ID. Get push-config supports TaskIdParams (no config ID) or richer params. Delete carries task/config IDs. Create flattens nested config with task ID. List config request only carries task ID: page-size/page-token are dropped; response similarly drops pagination. Extended card request discards input and returns an empty core request; reverse only restores a JSON-RPC envelope ID. Tenant fields in modern requests have no conversion in this module.

## Pure example

```python
from a2a.compat.v0_3 import conversions, types
legacy = types.Message(message_id='m1', role=types.Role.user,
    parts=[types.Part(root=types.TextPart(text='hello'))])
core = conversions.to_core_message(legacy)
assert core.message_id == 'm1' and core.parts[0].text == 'hello'
assert conversions.to_compat_message(core).message_id == 'm1'
```

Use round-trip fixtures for every representation you depend on, especially bytes, unknown roles, optional zero values, multiple OAuth flows, callback authentication schemes and signatures. Structural conversion does not establish wire equivalence for discarded fields.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import base64
from typing import Any
from google.protobuf.json_format import MessageToDict, ParseDict
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.versions import is_legacy_version
from a2a.types import a2a_pb2 as pb2_v10
from a2a.utils import constants, errors
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
_COMPAT_TO_CORE_TASK_STATE: dict[types_v03.TaskState, Any] = {types_v03.TaskState.unknown: pb2_v10.TaskState.TASK_STATE_UNSPECIFIED, types_v03.TaskState.submitted: pb2_v10.TaskState.TASK_STATE_SUBMITTED, types_v03.TaskState.working: pb2_v10.TaskState.TASK_STATE_WORKING, types_v03.TaskState.completed: pb2_v10.TaskState.TASK_STATE_COMPLETED, types_v03.TaskState.failed: pb2_v10.TaskState.TASK_STATE_FAILED, types_v03.TaskState.canceled: pb2_v10.TaskState.TASK_STATE_CANCELED, types_v03.TaskState.input_required: pb2_v10.TaskState.TASK_STATE_INPUT_REQUIRED, types_v03.TaskState.rejected: pb2_v10.TaskState.TASK_STATE_REJECTED, types_v03.TaskState.auth_required: pb2_v10.TaskState.TASK_STATE_AUTH_REQUIRED}
_CORE_TO_COMPAT_TASK_STATE: dict[Any, types_v03.TaskState] = {v: k for k, v in _COMPAT_TO_CORE_TASK_STATE.items()}
```

## Declaration-by-declaration execution reference

### `to_core_part`

Source lines 30–72; declaration kind `FunctionDef`.

Inputs: `(compat_part: types_v03.Part)`. Output annotation: `pb2_v10.Part`. Decorators: `none`.

Source intent: Converts a v0.3 Part (Pydantic model) to a v1.0 core Part (Protobuf object).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_part` from `pb2_v10.Part()`; output construction/calls here execute immediately when this method runs.
2. Assigns `root` from `compat_part.root`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(root, types_v03.TextPart)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_part`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.Part`, `isinstance`, `ParseDict`, `dict`, `meta.pop`, `base64.b64decode`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_part(compat_part: types_v03.Part) -> pb2_v10.Part:
    core_part = pb2_v10.Part()
    root = compat_part.root
    if isinstance(root, types_v03.TextPart):
        core_part.text = root.text
        if root.metadata is not None:
            ParseDict(root.metadata, core_part.metadata)
    elif isinstance(root, types_v03.DataPart):
        if root.metadata is None:
            data_part_compat = False
        else:
            meta = dict(root.metadata)
            data_part_compat = meta.pop('data_part_compat', False)
            if meta:
                ParseDict(meta, core_part.metadata)
        if data_part_compat:
            val = root.data['value']
            ParseDict(val, core_part.data)
        else:
            ParseDict(root.data, core_part.data.struct_value)
    elif isinstance(root, types_v03.FilePart):
        if isinstance(root.file, types_v03.FileWithBytes):
            core_part.raw = base64.b64decode(root.file.bytes)
            if root.file.mime_type:
                core_part.media_type = root.file.mime_type
            if root.file.name:
                core_part.filename = root.file.name
        elif isinstance(root.file, types_v03.FileWithUri):
            core_part.url = root.file.uri
            if root.file.mime_type:
                core_part.media_type = root.file.mime_type
            if root.file.name:
                core_part.filename = root.file.name
        if root.metadata is not None:
            ParseDict(root.metadata, core_part.metadata)
    return core_part
```

</details>

### `to_compat_part`

Source lines 75–120; declaration kind `FunctionDef`.

Inputs: `(core_part: pb2_v10.Part)`. Output annotation: `types_v03.Part`. Decorators: `none`.

Source intent: Converts a v1.0 core Part (Protobuf object) to a v0.3 Part (Pydantic model).

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `which` from `core_part.WhichOneof('content')`; output construction/calls here execute immediately when this method runs.
2. Assigns `metadata` from `MessageToDict(core_part.metadata) if core_part.HasField('metadata') else None`; output construction/calls here execute immediately when this method runs.
3. Branches on `which == 'text'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `which == 'data'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `which in ('raw', 'url')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Raises `ValueError(f'Unknown part content type: {which}')`.

Explicit errors: `ValueError(f'Unknown part content type: {which}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `core_part.WhichOneof`, `ValueError`, `core_part.HasField`, `MessageToDict`, `types_v03.Part`, `types_v03.FileWithUri`, `isinstance`, `base64.b64encode(core_part.raw).decode`, `types_v03.FileWithBytes`, `types_v03.TextPart`, `types_v03.DataPart`, `types_v03.FilePart`, `base64.b64encode`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_part(core_part: pb2_v10.Part) -> types_v03.Part:
    which = core_part.WhichOneof('content')
    metadata = MessageToDict(core_part.metadata) if core_part.HasField('metadata') else None
    if which == 'text':
        return types_v03.Part(root=types_v03.TextPart(text=core_part.text, metadata=metadata))
    if which == 'data':
        data_dict = MessageToDict(core_part.data)
        if not isinstance(data_dict, dict):
            data_dict = {'value': data_dict}
            metadata = metadata or {}
            metadata['data_part_compat'] = True
        return types_v03.Part(root=types_v03.DataPart(data=data_dict, metadata=metadata))
    if which in ('raw', 'url'):
        media_type = core_part.media_type if core_part.media_type else None
        filename = core_part.filename if core_part.filename else None
        if which == 'raw':
            b64 = base64.b64encode(core_part.raw).decode('utf-8')
            file_obj_bytes = types_v03.FileWithBytes(bytes=b64, mime_type=media_type, name=filename)
            return types_v03.Part(root=types_v03.FilePart(file=file_obj_bytes, metadata=metadata))
        file_obj_uri = types_v03.FileWithUri(uri=core_part.url, mime_type=media_type, name=filename)
        return types_v03.Part(root=types_v03.FilePart(file=file_obj_uri, metadata=metadata))
    raise ValueError(f'Unknown part content type: {which}')
```

</details>

### `to_core_message`

Source lines 123–146; declaration kind `FunctionDef`.

Inputs: `(compat_msg: types_v03.Message)`. Output annotation: `pb2_v10.Message`. Decorators: `none`.

Source intent: Convert message to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_msg` from `pb2_v10.Message(message_id=compat_msg.message_id, context_id=compat_msg.context_id or '', task_id=compat_msg.task_id or '')`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_msg.reference_task_ids`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_msg.role == types_v03.Role.user`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_msg.metadata`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_msg.extensions`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Iterates `compat_msg.parts` into `p`; each iteration performs the shown conversion/delegation, preserving iteration order.
7. Returns `core_msg`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.Message`, `core_msg.reference_task_ids.extend`, `ParseDict`, `core_msg.extensions.extend`, `core_msg.parts.append`, `to_core_part`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_message(compat_msg: types_v03.Message) -> pb2_v10.Message:
    core_msg = pb2_v10.Message(message_id=compat_msg.message_id, context_id=compat_msg.context_id or '', task_id=compat_msg.task_id or '')
    if compat_msg.reference_task_ids:
        core_msg.reference_task_ids.extend(compat_msg.reference_task_ids)
    if compat_msg.role == types_v03.Role.user:
        core_msg.role = pb2_v10.Role.ROLE_USER
    elif compat_msg.role == types_v03.Role.agent:
        core_msg.role = pb2_v10.Role.ROLE_AGENT
    if compat_msg.metadata:
        ParseDict(compat_msg.metadata, core_msg.metadata)
    if compat_msg.extensions:
        core_msg.extensions.extend(compat_msg.extensions)
    for p in compat_msg.parts:
        core_msg.parts.append(to_core_part(p))
    return core_msg
```

</details>

### `to_compat_message`

Source lines 149–169; declaration kind `FunctionDef`.

Inputs: `(core_msg: pb2_v10.Message)`. Output annotation: `types_v03.Message`. Decorators: `none`.

Source intent: Convert message to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `role` from `types_v03.Role.user if core_msg.role == pb2_v10.Role.ROLE_USER else types_v03.Role.agent`; output construction/calls here execute immediately when this method runs.
2. Returns `types_v03.Message(message_id=core_msg.message_id, role=role, context_id=core_msg.context_id or None, task_id=core_msg.task_id or None, reference_task_ids=list(core_msg.reference_task_ids) if core_msg.reference_task_ids else None, metadata=MessageToDict(core_msg.metadata) if core_msg.metadata else None, extensions=list(core_msg.extensions) if core_msg.extensi … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.Message`, `list`, `MessageToDict`, `to_compat_part`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_message(core_msg: pb2_v10.Message) -> types_v03.Message:
    role = types_v03.Role.user if core_msg.role == pb2_v10.Role.ROLE_USER else types_v03.Role.agent
    return types_v03.Message(message_id=core_msg.message_id, role=role, context_id=core_msg.context_id or None, task_id=core_msg.task_id or None, reference_task_ids=list(core_msg.reference_task_ids) if core_msg.reference_task_ids else None, metadata=MessageToDict(core_msg.metadata) if core_msg.metadata else None, extensions=list(core_msg.extensions) if core_msg.extensions else None, parts=[to_compat_part(p) for p in core_msg.parts])
```

</details>

### `to_core_task_status`

Source lines 172–188; declaration kind `FunctionDef`.

Inputs: `(compat_status: types_v03.TaskStatus)`. Output annotation: `pb2_v10.TaskStatus`. Decorators: `none`.

Source intent: Convert task status to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_status` from `pb2_v10.TaskStatus()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_status.state`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_status.message`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_status.timestamp`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Returns `core_status`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.TaskStatus`, `_COMPAT_TO_CORE_TASK_STATE.get`, `core_status.message.CopyFrom`, `core_status.timestamp.FromJsonString`, `to_core_message`, `str(compat_status.timestamp).replace`, `str`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_task_status(compat_status: types_v03.TaskStatus) -> pb2_v10.TaskStatus:
    core_status = pb2_v10.TaskStatus()
    if compat_status.state:
        core_status.state = _COMPAT_TO_CORE_TASK_STATE.get(compat_status.state, pb2_v10.TaskState.TASK_STATE_UNSPECIFIED)
    if compat_status.message:
        core_status.message.CopyFrom(to_core_message(compat_status.message))
    if compat_status.timestamp:
        core_status.timestamp.FromJsonString(str(compat_status.timestamp).replace('+00:00', 'Z'))
    return core_status
```

</details>

### `to_compat_task_status`

Source lines 191–210; declaration kind `FunctionDef`.

Inputs: `(core_status: pb2_v10.TaskStatus)`. Output annotation: `types_v03.TaskStatus`. Decorators: `none`.

Source intent: Convert task status to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `state_enum` from `_CORE_TO_COMPAT_TASK_STATE.get(core_status.state, types_v03.TaskState.unknown)`; output construction/calls here execute immediately when this method runs.
2. Assigns `update` from `to_compat_message(core_status.message) if core_status.HasField('message') else None`; output construction/calls here execute immediately when this method runs.
3. Assigns `ts` from `core_status.timestamp.ToJsonString() if core_status.HasField('timestamp') else None`; output construction/calls here execute immediately when this method runs.
4. Returns `types_v03.TaskStatus(state=state_enum, message=update, timestamp=ts)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `_CORE_TO_COMPAT_TASK_STATE.get`, `types_v03.TaskStatus`, `core_status.HasField`, `to_compat_message`, `core_status.timestamp.ToJsonString`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_task_status(core_status: pb2_v10.TaskStatus) -> types_v03.TaskStatus:
    state_enum = _CORE_TO_COMPAT_TASK_STATE.get(core_status.state, types_v03.TaskState.unknown)
    update = to_compat_message(core_status.message) if core_status.HasField('message') else None
    ts = core_status.timestamp.ToJsonString() if core_status.HasField('timestamp') else None
    return types_v03.TaskStatus(state=state_enum, message=update, timestamp=ts)
```

</details>

### `to_core_task`

Source lines 213–229; declaration kind `FunctionDef`.

Inputs: `(compat_task: types_v03.Task)`. Output annotation: `pb2_v10.Task`. Decorators: `none`.

Source intent: Convert task to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_task` from `pb2_v10.Task(id=compat_task.id, context_id=compat_task.context_id)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_task.status`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_task.history`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_task.artifacts`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_task.metadata`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `core_task`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.Task`, `core_task.status.CopyFrom`, `ParseDict`, `to_core_task_status`, `core_task.history.append`, `core_task.artifacts.append`, `to_core_message`, `to_core_artifact`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_task(compat_task: types_v03.Task) -> pb2_v10.Task:
    core_task = pb2_v10.Task(id=compat_task.id, context_id=compat_task.context_id)
    if compat_task.status:
        core_task.status.CopyFrom(to_core_task_status(compat_task.status))
    if compat_task.history:
        for m in compat_task.history:
            core_task.history.append(to_core_message(m))
    if compat_task.artifacts:
        for a in compat_task.artifacts:
            core_task.artifacts.append(to_core_artifact(a))
    if compat_task.metadata:
        ParseDict(compat_task.metadata, core_task.metadata)
    return core_task
```

</details>

### `to_compat_task`

Source lines 232–249; declaration kind `FunctionDef`.

Inputs: `(core_task: pb2_v10.Task)`. Output annotation: `types_v03.Task`. Decorators: `none`.

Source intent: Convert task to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.Task(id=core_task.id, context_id=core_task.context_id, status=to_compat_task_status(core_task.status) if core_task.HasField('status') else types_v03.TaskStatus(state=types_v03.TaskState.unknown), history=[to_compat_message(m) for m in core_task.history] if core_task.history else None, artifacts=[to_compat_artifact(a) for a in core_task.artifacts] i … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.Task`, `core_task.HasField`, `to_compat_task_status`, `types_v03.TaskStatus`, `MessageToDict`, `to_compat_message`, `to_compat_artifact`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_task(core_task: pb2_v10.Task) -> types_v03.Task:
    return types_v03.Task(id=core_task.id, context_id=core_task.context_id, status=to_compat_task_status(core_task.status) if core_task.HasField('status') else types_v03.TaskStatus(state=types_v03.TaskState.unknown), history=[to_compat_message(m) for m in core_task.history] if core_task.history else None, artifacts=[to_compat_artifact(a) for a in core_task.artifacts] if core_task.artifacts else None, metadata=MessageToDict(core_task.metadata) if core_task.HasField('metadata') else None)
```

</details>

### `to_core_authentication_info`

Source lines 252–261; declaration kind `FunctionDef`.

Inputs: `(compat_auth: types_v03.PushNotificationAuthenticationInfo)`. Output annotation: `pb2_v10.AuthenticationInfo`. Decorators: `none`.

Source intent: Convert authentication info to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_auth` from `pb2_v10.AuthenticationInfo()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_auth.schemes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_auth.credentials`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_auth`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AuthenticationInfo`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_authentication_info(compat_auth: types_v03.PushNotificationAuthenticationInfo) -> pb2_v10.AuthenticationInfo:
    core_auth = pb2_v10.AuthenticationInfo()
    if compat_auth.schemes:
        core_auth.scheme = compat_auth.schemes[0]
    if compat_auth.credentials:
        core_auth.credentials = compat_auth.credentials
    return core_auth
```

</details>

### `to_compat_authentication_info`

Source lines 264–271; declaration kind `FunctionDef`.

Inputs: `(core_auth: pb2_v10.AuthenticationInfo)`. Output annotation: `types_v03.PushNotificationAuthenticationInfo`. Decorators: `none`.

Source intent: Convert authentication info to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.PushNotificationAuthenticationInfo(schemes=[core_auth.scheme] if core_auth.scheme else [], credentials=core_auth.credentials if core_auth.credentials else None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.PushNotificationAuthenticationInfo`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_authentication_info(core_auth: pb2_v10.AuthenticationInfo) -> types_v03.PushNotificationAuthenticationInfo:
    return types_v03.PushNotificationAuthenticationInfo(schemes=[core_auth.scheme] if core_auth.scheme else [], credentials=core_auth.credentials if core_auth.credentials else None)
```

</details>

### `to_core_push_notification_config`

Source lines 274–287; declaration kind `FunctionDef`.

Inputs: `(compat_config: types_v03.PushNotificationConfig)`. Output annotation: `pb2_v10.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Convert push notification config to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_config` from `pb2_v10.TaskPushNotificationConfig(url=compat_config.url)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_config.id`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_config.token`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_config.authentication`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Returns `core_config`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.TaskPushNotificationConfig`, `core_config.authentication.CopyFrom`, `to_core_authentication_info`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_push_notification_config(compat_config: types_v03.PushNotificationConfig) -> pb2_v10.TaskPushNotificationConfig:
    core_config = pb2_v10.TaskPushNotificationConfig(url=compat_config.url)
    if compat_config.id:
        core_config.id = compat_config.id
    if compat_config.token:
        core_config.token = compat_config.token
    if compat_config.authentication:
        core_config.authentication.CopyFrom(to_core_authentication_info(compat_config.authentication))
    return core_config
```

</details>

### `to_compat_push_notification_config`

Source lines 290–301; declaration kind `FunctionDef`.

Inputs: `(core_config: pb2_v10.TaskPushNotificationConfig)`. Output annotation: `types_v03.PushNotificationConfig`. Decorators: `none`.

Source intent: Convert push notification config to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.PushNotificationConfig(url=core_config.url if core_config.url else '', id=core_config.id if core_config.id else None, token=core_config.token if core_config.token else None, authentication=to_compat_authentication_info(core_config.authentication) if core_config.HasField('authentication') else None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.PushNotificationConfig`, `core_config.HasField`, `to_compat_authentication_info`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_push_notification_config(core_config: pb2_v10.TaskPushNotificationConfig) -> types_v03.PushNotificationConfig:
    return types_v03.PushNotificationConfig(url=core_config.url if core_config.url else '', id=core_config.id if core_config.id else None, token=core_config.token if core_config.token else None, authentication=to_compat_authentication_info(core_config.authentication) if core_config.HasField('authentication') else None)
```

</details>

### `to_core_send_message_configuration`

Source lines 304–324; declaration kind `FunctionDef`.

Inputs: `(compat_config: types_v03.MessageSendConfiguration)`. Output annotation: `pb2_v10.SendMessageConfiguration`. Decorators: `none`.

Source intent: Convert send message configuration to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_config` from `pb2_v10.SendMessageConfiguration()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_config.accepted_output_modes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_config.push_notification_config`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_config.history_length is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_config.blocking is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `core_config`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.SendMessageConfiguration`, `core_config.accepted_output_modes.extend`, `core_config.task_push_notification_config.CopyFrom`, `to_core_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_send_message_configuration(compat_config: types_v03.MessageSendConfiguration) -> pb2_v10.SendMessageConfiguration:
    core_config = pb2_v10.SendMessageConfiguration()
    if compat_config.accepted_output_modes:
        core_config.accepted_output_modes.extend(compat_config.accepted_output_modes)
    if compat_config.push_notification_config:
        core_config.task_push_notification_config.CopyFrom(to_core_push_notification_config(compat_config.push_notification_config))
    if compat_config.history_length is not None:
        core_config.history_length = compat_config.history_length
    if compat_config.blocking is not None:
        core_config.return_immediately = not compat_config.blocking
    return core_config
```

</details>

### `to_compat_send_message_configuration`

Source lines 327–344; declaration kind `FunctionDef`.

Inputs: `(core_config: pb2_v10.SendMessageConfiguration)`. Output annotation: `types_v03.MessageSendConfiguration`. Decorators: `none`.

Source intent: Convert send message configuration to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.MessageSendConfiguration(accepted_output_modes=list(core_config.accepted_output_modes) if core_config.accepted_output_modes else None, push_notification_config=to_compat_push_notification_config(core_config.task_push_notification_config) if core_config.HasField('task_push_notification_config') else None, history_length=core_config.history_length if … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.MessageSendConfiguration`, `list`, `core_config.HasField`, `to_compat_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_send_message_configuration(core_config: pb2_v10.SendMessageConfiguration) -> types_v03.MessageSendConfiguration:
    return types_v03.MessageSendConfiguration(accepted_output_modes=list(core_config.accepted_output_modes) if core_config.accepted_output_modes else None, push_notification_config=to_compat_push_notification_config(core_config.task_push_notification_config) if core_config.HasField('task_push_notification_config') else None, history_length=core_config.history_length if core_config.HasField('history_length') else None, blocking=not core_config.return_immediately)
```

</details>

### `to_core_artifact`

Source lines 347–360; declaration kind `FunctionDef`.

Inputs: `(compat_artifact: types_v03.Artifact)`. Output annotation: `pb2_v10.Artifact`. Decorators: `none`.

Source intent: Convert artifact to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_artifact` from `pb2_v10.Artifact(artifact_id=compat_artifact.artifact_id)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_artifact.name`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_artifact.description`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Iterates `compat_artifact.parts` into `p`; each iteration performs the shown conversion/delegation, preserving iteration order.
5. Branches on `compat_artifact.metadata`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Branches on `compat_artifact.extensions`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
7. Returns `core_artifact`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.Artifact`, `core_artifact.parts.append`, `ParseDict`, `core_artifact.extensions.extend`, `to_core_part`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_artifact(compat_artifact: types_v03.Artifact) -> pb2_v10.Artifact:
    core_artifact = pb2_v10.Artifact(artifact_id=compat_artifact.artifact_id)
    if compat_artifact.name:
        core_artifact.name = compat_artifact.name
    if compat_artifact.description:
        core_artifact.description = compat_artifact.description
    for p in compat_artifact.parts:
        core_artifact.parts.append(to_core_part(p))
    if compat_artifact.metadata:
        ParseDict(compat_artifact.metadata, core_artifact.metadata)
    if compat_artifact.extensions:
        core_artifact.extensions.extend(compat_artifact.extensions)
    return core_artifact
```

</details>

### `to_compat_artifact`

Source lines 363–378; declaration kind `FunctionDef`.

Inputs: `(core_artifact: pb2_v10.Artifact)`. Output annotation: `types_v03.Artifact`. Decorators: `none`.

Source intent: Convert artifact to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.Artifact(artifact_id=core_artifact.artifact_id, name=core_artifact.name if core_artifact.name else None, description=core_artifact.description if core_artifact.description else None, parts=[to_compat_part(p) for p in core_artifact.parts], metadata=MessageToDict(core_artifact.metadata) if core_artifact.HasField('metadata') else None, extensions=list … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.Artifact`, `to_compat_part`, `core_artifact.HasField`, `MessageToDict`, `list`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_artifact(core_artifact: pb2_v10.Artifact) -> types_v03.Artifact:
    return types_v03.Artifact(artifact_id=core_artifact.artifact_id, name=core_artifact.name if core_artifact.name else None, description=core_artifact.description if core_artifact.description else None, parts=[to_compat_part(p) for p in core_artifact.parts], metadata=MessageToDict(core_artifact.metadata) if core_artifact.HasField('metadata') else None, extensions=list(core_artifact.extensions) if core_artifact.extensions else None)
```

</details>

### `to_core_task_status_update_event`

Source lines 381–392; declaration kind `FunctionDef`.

Inputs: `(compat_event: types_v03.TaskStatusUpdateEvent)`. Output annotation: `pb2_v10.TaskStatusUpdateEvent`. Decorators: `none`.

Source intent: Convert task status update event to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_event` from `pb2_v10.TaskStatusUpdateEvent(task_id=compat_event.task_id, context_id=compat_event.context_id)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_event.status`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_event.metadata`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_event`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.TaskStatusUpdateEvent`, `core_event.status.CopyFrom`, `ParseDict`, `to_core_task_status`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_task_status_update_event(compat_event: types_v03.TaskStatusUpdateEvent) -> pb2_v10.TaskStatusUpdateEvent:
    core_event = pb2_v10.TaskStatusUpdateEvent(task_id=compat_event.task_id, context_id=compat_event.context_id)
    if compat_event.status:
        core_event.status.CopyFrom(to_core_task_status(compat_event.status))
    if compat_event.metadata:
        ParseDict(compat_event.metadata, core_event.metadata)
    return core_event
```

</details>

### `to_compat_task_status_update_event`

Source lines 395–418; declaration kind `FunctionDef`.

Inputs: `(core_event: pb2_v10.TaskStatusUpdateEvent)`. Output annotation: `types_v03.TaskStatusUpdateEvent`. Decorators: `none`.

Source intent: Convert task status update event to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `status` from `to_compat_task_status(core_event.status) if core_event.HasField('status') else types_v03.TaskStatus(state=types_v03.TaskState.unknown)`; output construction/calls here execute immediately when this method runs.
2. Assigns `final` from `status.state in (types_v03.TaskState.completed, types_v03.TaskState.canceled, types_v03.TaskState.failed, types_v03.TaskState.rejected)`; output construction/calls here execute immediately when this method runs.
3. Returns `types_v03.TaskStatusUpdateEvent(task_id=core_event.task_id, context_id=core_event.context_id, status=status, metadata=MessageToDict(core_event.metadata) if core_event.HasField('metadata') else None, final=final)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.TaskStatusUpdateEvent`, `core_event.HasField`, `to_compat_task_status`, `types_v03.TaskStatus`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_task_status_update_event(core_event: pb2_v10.TaskStatusUpdateEvent) -> types_v03.TaskStatusUpdateEvent:
    status = to_compat_task_status(core_event.status) if core_event.HasField('status') else types_v03.TaskStatus(state=types_v03.TaskState.unknown)
    final = status.state in (types_v03.TaskState.completed, types_v03.TaskState.canceled, types_v03.TaskState.failed, types_v03.TaskState.rejected)
    return types_v03.TaskStatusUpdateEvent(task_id=core_event.task_id, context_id=core_event.context_id, status=status, metadata=MessageToDict(core_event.metadata) if core_event.HasField('metadata') else None, final=final)
```

</details>

### `to_core_task_artifact_update_event`

Source lines 421–436; declaration kind `FunctionDef`.

Inputs: `(compat_event: types_v03.TaskArtifactUpdateEvent)`. Output annotation: `pb2_v10.TaskArtifactUpdateEvent`. Decorators: `none`.

Source intent: Convert task artifact update event to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_event` from `pb2_v10.TaskArtifactUpdateEvent(task_id=compat_event.task_id, context_id=compat_event.context_id)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_event.artifact`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_event.append is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_event.last_chunk is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_event.metadata`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `core_event`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.TaskArtifactUpdateEvent`, `core_event.artifact.CopyFrom`, `ParseDict`, `to_core_artifact`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_task_artifact_update_event(compat_event: types_v03.TaskArtifactUpdateEvent) -> pb2_v10.TaskArtifactUpdateEvent:
    core_event = pb2_v10.TaskArtifactUpdateEvent(task_id=compat_event.task_id, context_id=compat_event.context_id)
    if compat_event.artifact:
        core_event.artifact.CopyFrom(to_core_artifact(compat_event.artifact))
    if compat_event.append is not None:
        core_event.append = compat_event.append
    if compat_event.last_chunk is not None:
        core_event.last_chunk = compat_event.last_chunk
    if compat_event.metadata:
        ParseDict(compat_event.metadata, core_event.metadata)
    return core_event
```

</details>

### `to_core_security_requirement`

Source lines 439–448; declaration kind `FunctionDef`.

Inputs: `(compat_req: dict[str, list[str]])`. Output annotation: `pb2_v10.SecurityRequirement`. Decorators: `none`.

Source intent: Convert security requirement to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_req` from `pb2_v10.SecurityRequirement()`; output construction/calls here execute immediately when this method runs.
2. Iterates `compat_req.items()` into `(scheme_name, scopes)`; each iteration performs the shown conversion/delegation, preserving iteration order.
3. Returns `core_req`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.SecurityRequirement`, `compat_req.items`, `pb2_v10.StringList`, `sl.list.extend`, `core_req.schemes[scheme_name].CopyFrom`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_security_requirement(compat_req: dict[str, list[str]]) -> pb2_v10.SecurityRequirement:
    core_req = pb2_v10.SecurityRequirement()
    for scheme_name, scopes in compat_req.items():
        sl = pb2_v10.StringList()
        sl.list.extend(scopes)
        core_req.schemes[scheme_name].CopyFrom(sl)
    return core_req
```

</details>

### `to_compat_security_requirement`

Source lines 451–458; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.SecurityRequirement)`. Output annotation: `dict[str, list[str]]`. Decorators: `none`.

Source intent: Convert security requirement to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `{scheme_name: list(string_list.list) for scheme_name, string_list in core_req.schemes.items()}`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `list`, `core_req.schemes.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_security_requirement(core_req: pb2_v10.SecurityRequirement) -> dict[str, list[str]]:
    return {scheme_name: list(string_list.list) for scheme_name, string_list in core_req.schemes.items()}
```

</details>

### `to_core_oauth_flows`

Source lines 461–503; declaration kind `FunctionDef`.

Inputs: `(compat_flows: types_v03.OAuthFlows)`. Output annotation: `pb2_v10.OAuthFlows`. Decorators: `none`.

Source intent: Convert oauth flows to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_flows` from `pb2_v10.OAuthFlows()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_flows.authorization_code`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_flows.client_credentials`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_flows.implicit`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_flows.password`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `core_flows`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.OAuthFlows`, `pb2_v10.AuthorizationCodeOAuthFlow`, `core_flows.authorization_code.CopyFrom`, `pb2_v10.ClientCredentialsOAuthFlow`, `core_flows.client_credentials.CopyFrom`, `pb2_v10.ImplicitOAuthFlow`, `core_flows.implicit.CopyFrom`, `pb2_v10.PasswordOAuthFlow`, `core_flows.password.CopyFrom`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_oauth_flows(compat_flows: types_v03.OAuthFlows) -> pb2_v10.OAuthFlows:
    core_flows = pb2_v10.OAuthFlows()
    if compat_flows.authorization_code:
        f = pb2_v10.AuthorizationCodeOAuthFlow(authorization_url=compat_flows.authorization_code.authorization_url, token_url=compat_flows.authorization_code.token_url, scopes=compat_flows.authorization_code.scopes)
        if compat_flows.authorization_code.refresh_url:
            f.refresh_url = compat_flows.authorization_code.refresh_url
        core_flows.authorization_code.CopyFrom(f)
    if compat_flows.client_credentials:
        f_client = pb2_v10.ClientCredentialsOAuthFlow(token_url=compat_flows.client_credentials.token_url, scopes=compat_flows.client_credentials.scopes)
        if compat_flows.client_credentials.refresh_url:
            f_client.refresh_url = compat_flows.client_credentials.refresh_url
        core_flows.client_credentials.CopyFrom(f_client)
    if compat_flows.implicit:
        f_impl = pb2_v10.ImplicitOAuthFlow(authorization_url=compat_flows.implicit.authorization_url, scopes=compat_flows.implicit.scopes)
        if compat_flows.implicit.refresh_url:
            f_impl.refresh_url = compat_flows.implicit.refresh_url
        core_flows.implicit.CopyFrom(f_impl)
    if compat_flows.password:
        f_pass = pb2_v10.PasswordOAuthFlow(token_url=compat_flows.password.token_url, scopes=compat_flows.password.scopes)
        if compat_flows.password.refresh_url:
            f_pass.refresh_url = compat_flows.password.refresh_url
        core_flows.password.CopyFrom(f_pass)
    return core_flows
```

</details>

### `to_compat_oauth_flows`

Source lines 506–553; declaration kind `FunctionDef`.

Inputs: `(core_flows: pb2_v10.OAuthFlows)`. Output annotation: `types_v03.OAuthFlows`. Decorators: `none`.

Source intent: Convert oauth flows to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `which` from `core_flows.WhichOneof('flow')`; output construction/calls here execute immediately when this method runs.
2. Assigns `(auth_code, client_cred, implicit, password)` from `(None, None, None, None)`; output construction/calls here execute immediately when this method runs.
3. Branches on `which == 'authorization_code'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `types_v03.OAuthFlows(authorization_code=auth_code, client_credentials=client_cred, implicit=implicit, password=password)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `core_flows.WhichOneof`, `types_v03.OAuthFlows`, `types_v03.AuthorizationCodeOAuthFlow`, `types_v03.ClientCredentialsOAuthFlow`, `dict`, `types_v03.ImplicitOAuthFlow`, `types_v03.PasswordOAuthFlow`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_oauth_flows(core_flows: pb2_v10.OAuthFlows) -> types_v03.OAuthFlows:
    which = core_flows.WhichOneof('flow')
    auth_code, client_cred, implicit, password = (None, None, None, None)
    if which == 'authorization_code':
        auth_code = types_v03.AuthorizationCodeOAuthFlow(authorization_url=core_flows.authorization_code.authorization_url, token_url=core_flows.authorization_code.token_url, scopes=dict(core_flows.authorization_code.scopes), refresh_url=core_flows.authorization_code.refresh_url if core_flows.authorization_code.refresh_url else None)
    elif which == 'client_credentials':
        client_cred = types_v03.ClientCredentialsOAuthFlow(token_url=core_flows.client_credentials.token_url, scopes=dict(core_flows.client_credentials.scopes), refresh_url=core_flows.client_credentials.refresh_url if core_flows.client_credentials.refresh_url else None)
    elif which == 'implicit':
        implicit = types_v03.ImplicitOAuthFlow(authorization_url=core_flows.implicit.authorization_url, scopes=dict(core_flows.implicit.scopes), refresh_url=core_flows.implicit.refresh_url if core_flows.implicit.refresh_url else None)
    elif which == 'password':
        password = types_v03.PasswordOAuthFlow(token_url=core_flows.password.token_url, scopes=dict(core_flows.password.scopes), refresh_url=core_flows.password.refresh_url if core_flows.password.refresh_url else None)
    return types_v03.OAuthFlows(authorization_code=auth_code, client_credentials=client_cred, implicit=implicit, password=password)
```

</details>

### `to_core_security_scheme`

Source lines 556–604; declaration kind `FunctionDef`.

Inputs: `(compat_scheme: types_v03.SecurityScheme)`. Output annotation: `pb2_v10.SecurityScheme`. Decorators: `none`.

Source intent: Convert security scheme to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_scheme` from `pb2_v10.SecurityScheme()`; output construction/calls here execute immediately when this method runs.
2. Assigns `root` from `compat_scheme.root`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(root, types_v03.APIKeySecurityScheme)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_scheme`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.SecurityScheme`, `isinstance`, `core_scheme.oauth2_security_scheme.flows.CopyFrom`, `to_core_oauth_flows`, `core_scheme.mtls_security_scheme.SetInParent`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_security_scheme(compat_scheme: types_v03.SecurityScheme) -> pb2_v10.SecurityScheme:
    core_scheme = pb2_v10.SecurityScheme()
    root = compat_scheme.root
    if isinstance(root, types_v03.APIKeySecurityScheme):
        core_scheme.api_key_security_scheme.location = root.in_.value
        core_scheme.api_key_security_scheme.name = root.name
        if root.description:
            core_scheme.api_key_security_scheme.description = root.description
    elif isinstance(root, types_v03.HTTPAuthSecurityScheme):
        core_scheme.http_auth_security_scheme.scheme = root.scheme
        if root.bearer_format:
            core_scheme.http_auth_security_scheme.bearer_format = root.bearer_format
        if root.description:
            core_scheme.http_auth_security_scheme.description = root.description
    elif isinstance(root, types_v03.OAuth2SecurityScheme):
        core_scheme.oauth2_security_scheme.flows.CopyFrom(to_core_oauth_flows(root.flows))
        if root.oauth2_metadata_url:
            core_scheme.oauth2_security_scheme.oauth2_metadata_url = root.oauth2_metadata_url
        if root.description:
            core_scheme.oauth2_security_scheme.description = root.description
    elif isinstance(root, types_v03.OpenIdConnectSecurityScheme):
        core_scheme.open_id_connect_security_scheme.open_id_connect_url = root.open_id_connect_url
        if root.description:
            core_scheme.open_id_connect_security_scheme.description = root.description
    elif isinstance(root, types_v03.MutualTLSSecurityScheme):
        core_scheme.mtls_security_scheme.SetInParent()
        if root.description:
            core_scheme.mtls_security_scheme.description = root.description
    return core_scheme
```

</details>

### `to_compat_security_scheme`

Source lines 607–666; declaration kind `FunctionDef`.

Inputs: `(core_scheme: pb2_v10.SecurityScheme)`. Output annotation: `types_v03.SecurityScheme`. Decorators: `none`.

Source intent: Convert security scheme to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `which` from `core_scheme.WhichOneof('scheme')`; output construction/calls here execute immediately when this method runs.
2. Branches on `which == 'api_key_security_scheme'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `which == 'http_auth_security_scheme'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `which == 'oauth2_security_scheme'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `which == 'open_id_connect_security_scheme'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Branches on `which == 'mtls_security_scheme'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
7. Raises `ValueError(f'Unknown security scheme type: {which}')`.

Explicit errors: `ValueError(f'Unknown security scheme type: {which}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `core_scheme.WhichOneof`, `ValueError`, `types_v03.SecurityScheme`, `types_v03.APIKeySecurityScheme`, `types_v03.HTTPAuthSecurityScheme`, `types_v03.OAuth2SecurityScheme`, `types_v03.OpenIdConnectSecurityScheme`, `types_v03.MutualTLSSecurityScheme`, `types_v03.In`, `to_compat_oauth_flows`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_security_scheme(core_scheme: pb2_v10.SecurityScheme) -> types_v03.SecurityScheme:
    which = core_scheme.WhichOneof('scheme')
    if which == 'api_key_security_scheme':
        s_api = core_scheme.api_key_security_scheme
        return types_v03.SecurityScheme(root=types_v03.APIKeySecurityScheme(in_=types_v03.In(s_api.location), name=s_api.name, description=s_api.description if s_api.description else None))
    if which == 'http_auth_security_scheme':
        s_http = core_scheme.http_auth_security_scheme
        return types_v03.SecurityScheme(root=types_v03.HTTPAuthSecurityScheme(scheme=s_http.scheme, bearer_format=s_http.bearer_format if s_http.bearer_format else None, description=s_http.description if s_http.description else None))
    if which == 'oauth2_security_scheme':
        s_oauth = core_scheme.oauth2_security_scheme
        return types_v03.SecurityScheme(root=types_v03.OAuth2SecurityScheme(flows=to_compat_oauth_flows(s_oauth.flows), oauth2_metadata_url=s_oauth.oauth2_metadata_url if s_oauth.oauth2_metadata_url else None, description=s_oauth.description if s_oauth.description else None))
    if which == 'open_id_connect_security_scheme':
        s_oidc = core_scheme.open_id_connect_security_scheme
        return types_v03.SecurityScheme(root=types_v03.OpenIdConnectSecurityScheme(open_id_connect_url=s_oidc.open_id_connect_url, description=s_oidc.description if s_oidc.description else None))
    if which == 'mtls_security_scheme':
        s_mtls = core_scheme.mtls_security_scheme
        return types_v03.SecurityScheme(root=types_v03.MutualTLSSecurityScheme(description=s_mtls.description if s_mtls.description else None))
    raise ValueError(f'Unknown security scheme type: {which}')
```

</details>

### `to_core_agent_interface`

Source lines 669–677; declaration kind `FunctionDef`.

Inputs: `(compat_interface: types_v03.AgentInterface)`. Output annotation: `pb2_v10.AgentInterface`. Decorators: `none`.

Source intent: Convert agent interface to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `pb2_v10.AgentInterface(url=compat_interface.url, protocol_binding=compat_interface.transport, protocol_version=constants.PROTOCOL_VERSION_0_3)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AgentInterface`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_agent_interface(compat_interface: types_v03.AgentInterface) -> pb2_v10.AgentInterface:
    return pb2_v10.AgentInterface(url=compat_interface.url, protocol_binding=compat_interface.transport, protocol_version=constants.PROTOCOL_VERSION_0_3)
```

</details>

### `to_compat_agent_interface`

Source lines 680–686; declaration kind `FunctionDef`.

Inputs: `(core_interface: pb2_v10.AgentInterface)`. Output annotation: `types_v03.AgentInterface`. Decorators: `none`.

Source intent: Convert agent interface to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.AgentInterface(url=core_interface.url, transport=core_interface.protocol_binding)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.AgentInterface`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_agent_interface(core_interface: pb2_v10.AgentInterface) -> types_v03.AgentInterface:
    return types_v03.AgentInterface(url=core_interface.url, transport=core_interface.protocol_binding)
```

</details>

### `to_core_agent_provider`

Source lines 689–695; declaration kind `FunctionDef`.

Inputs: `(compat_provider: types_v03.AgentProvider)`. Output annotation: `pb2_v10.AgentProvider`. Decorators: `none`.

Source intent: Convert agent provider to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `pb2_v10.AgentProvider(url=compat_provider.url, organization=compat_provider.organization)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AgentProvider`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_agent_provider(compat_provider: types_v03.AgentProvider) -> pb2_v10.AgentProvider:
    return pb2_v10.AgentProvider(url=compat_provider.url, organization=compat_provider.organization)
```

</details>

### `to_compat_agent_provider`

Source lines 698–704; declaration kind `FunctionDef`.

Inputs: `(core_provider: pb2_v10.AgentProvider)`. Output annotation: `types_v03.AgentProvider`. Decorators: `none`.

Source intent: Convert agent provider to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.AgentProvider(url=core_provider.url, organization=core_provider.organization)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.AgentProvider`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_agent_provider(core_provider: pb2_v10.AgentProvider) -> types_v03.AgentProvider:
    return types_v03.AgentProvider(url=core_provider.url, organization=core_provider.organization)
```

</details>

### `to_core_agent_extension`

Source lines 707–720; declaration kind `FunctionDef`.

Inputs: `(compat_ext: types_v03.AgentExtension)`. Output annotation: `pb2_v10.AgentExtension`. Decorators: `none`.

Source intent: Convert agent extension to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_ext` from `pb2_v10.AgentExtension()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_ext.uri`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_ext.description`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_ext.required is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_ext.params`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Returns `core_ext`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AgentExtension`, `ParseDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_agent_extension(compat_ext: types_v03.AgentExtension) -> pb2_v10.AgentExtension:
    core_ext = pb2_v10.AgentExtension()
    if compat_ext.uri:
        core_ext.uri = compat_ext.uri
    if compat_ext.description:
        core_ext.description = compat_ext.description
    if compat_ext.required is not None:
        core_ext.required = compat_ext.required
    if compat_ext.params:
        ParseDict(compat_ext.params, core_ext.params)
    return core_ext
```

</details>

### `to_compat_agent_extension`

Source lines 723–734; declaration kind `FunctionDef`.

Inputs: `(core_ext: pb2_v10.AgentExtension)`. Output annotation: `types_v03.AgentExtension`. Decorators: `none`.

Source intent: Convert agent extension to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.AgentExtension(uri=core_ext.uri, description=core_ext.description if core_ext.description else None, required=core_ext.required, params=MessageToDict(core_ext.params) if core_ext.HasField('params') else None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.AgentExtension`, `core_ext.HasField`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_agent_extension(core_ext: pb2_v10.AgentExtension) -> types_v03.AgentExtension:
    return types_v03.AgentExtension(uri=core_ext.uri, description=core_ext.description if core_ext.description else None, required=core_ext.required, params=MessageToDict(core_ext.params) if core_ext.HasField('params') else None)
```

</details>

### `to_core_agent_capabilities`

Source lines 737–750; declaration kind `FunctionDef`.

Inputs: `(compat_cap: types_v03.AgentCapabilities)`. Output annotation: `pb2_v10.AgentCapabilities`. Decorators: `none`.

Source intent: Convert agent capabilities to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_cap` from `pb2_v10.AgentCapabilities()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_cap.streaming is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_cap.push_notifications is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_cap.extensions`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Returns `core_cap`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AgentCapabilities`, `core_cap.extensions.extend`, `to_core_agent_extension`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_agent_capabilities(compat_cap: types_v03.AgentCapabilities) -> pb2_v10.AgentCapabilities:
    core_cap = pb2_v10.AgentCapabilities()
    if compat_cap.streaming is not None:
        core_cap.streaming = compat_cap.streaming
    if compat_cap.push_notifications is not None:
        core_cap.push_notifications = compat_cap.push_notifications
    if compat_cap.extensions:
        core_cap.extensions.extend([to_core_agent_extension(e) for e in compat_cap.extensions])
    return core_cap
```

</details>

### `to_compat_agent_capabilities`

Source lines 753–768; declaration kind `FunctionDef`.

Inputs: `(core_cap: pb2_v10.AgentCapabilities)`. Output annotation: `types_v03.AgentCapabilities`. Decorators: `none`.

Source intent: Convert agent capabilities to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.AgentCapabilities(streaming=core_cap.streaming if core_cap.HasField('streaming') else None, push_notifications=core_cap.push_notifications if core_cap.HasField('push_notifications') else None, extensions=[to_compat_agent_extension(e) for e in core_cap.extensions] if core_cap.extensions else None, state_transition_history=None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.AgentCapabilities`, `core_cap.HasField`, `to_compat_agent_extension`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_agent_capabilities(core_cap: pb2_v10.AgentCapabilities) -> types_v03.AgentCapabilities:
    return types_v03.AgentCapabilities(streaming=core_cap.streaming if core_cap.HasField('streaming') else None, push_notifications=core_cap.push_notifications if core_cap.HasField('push_notifications') else None, extensions=[to_compat_agent_extension(e) for e in core_cap.extensions] if core_cap.extensions else None, state_transition_history=None)
```

</details>

### `to_core_agent_skill`

Source lines 771–792; declaration kind `FunctionDef`.

Inputs: `(compat_skill: types_v03.AgentSkill)`. Output annotation: `pb2_v10.AgentSkill`. Decorators: `none`.

Source intent: Convert agent skill to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_skill` from `pb2_v10.AgentSkill(id=compat_skill.id, name=compat_skill.name, description=compat_skill.description)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_skill.tags`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_skill.examples`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_skill.input_modes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_skill.output_modes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Branches on `compat_skill.security`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
7. Returns `core_skill`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AgentSkill`, `core_skill.tags.extend`, `core_skill.examples.extend`, `core_skill.input_modes.extend`, `core_skill.output_modes.extend`, `core_skill.security_requirements.extend`, `to_core_security_requirement`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_agent_skill(compat_skill: types_v03.AgentSkill) -> pb2_v10.AgentSkill:
    core_skill = pb2_v10.AgentSkill(id=compat_skill.id, name=compat_skill.name, description=compat_skill.description)
    if compat_skill.tags:
        core_skill.tags.extend(compat_skill.tags)
    if compat_skill.examples:
        core_skill.examples.extend(compat_skill.examples)
    if compat_skill.input_modes:
        core_skill.input_modes.extend(compat_skill.input_modes)
    if compat_skill.output_modes:
        core_skill.output_modes.extend(compat_skill.output_modes)
    if compat_skill.security:
        core_skill.security_requirements.extend([to_core_security_requirement(r) for r in compat_skill.security])
    return core_skill
```

</details>

### `to_compat_agent_skill`

Source lines 795–817; declaration kind `FunctionDef`.

Inputs: `(core_skill: pb2_v10.AgentSkill)`. Output annotation: `types_v03.AgentSkill`. Decorators: `none`.

Source intent: Convert agent skill to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.AgentSkill(id=core_skill.id, name=core_skill.name, description=core_skill.description, tags=list(core_skill.tags) if core_skill.tags else [], examples=list(core_skill.examples) if core_skill.examples else None, input_modes=list(core_skill.input_modes) if core_skill.input_modes else None, output_modes=list(core_skill.output_modes) if core_skill.outp … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.AgentSkill`, `list`, `to_compat_security_requirement`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_agent_skill(core_skill: pb2_v10.AgentSkill) -> types_v03.AgentSkill:
    return types_v03.AgentSkill(id=core_skill.id, name=core_skill.name, description=core_skill.description, tags=list(core_skill.tags) if core_skill.tags else [], examples=list(core_skill.examples) if core_skill.examples else None, input_modes=list(core_skill.input_modes) if core_skill.input_modes else None, output_modes=list(core_skill.output_modes) if core_skill.output_modes else None, security=[to_compat_security_requirement(r) for r in core_skill.security_requirements] if core_skill.security_requirements else None)
```

</details>

### `to_core_agent_card_signature`

Source lines 820–829; declaration kind `FunctionDef`.

Inputs: `(compat_sig: types_v03.AgentCardSignature)`. Output annotation: `pb2_v10.AgentCardSignature`. Decorators: `none`.

Source intent: Convert agent card signature to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_sig` from `pb2_v10.AgentCardSignature(protected=compat_sig.protected, signature=compat_sig.signature)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_sig.header`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `core_sig`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AgentCardSignature`, `ParseDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_agent_card_signature(compat_sig: types_v03.AgentCardSignature) -> pb2_v10.AgentCardSignature:
    core_sig = pb2_v10.AgentCardSignature(protected=compat_sig.protected, signature=compat_sig.signature)
    if compat_sig.header:
        ParseDict(compat_sig.header, core_sig.header)
    return core_sig
```

</details>

### `to_compat_agent_card_signature`

Source lines 832–842; declaration kind `FunctionDef`.

Inputs: `(core_sig: pb2_v10.AgentCardSignature)`. Output annotation: `types_v03.AgentCardSignature`. Decorators: `none`.

Source intent: Convert agent card signature to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.AgentCardSignature(protected=core_sig.protected, signature=core_sig.signature, header=MessageToDict(core_sig.header) if core_sig.HasField('header') else None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.AgentCardSignature`, `core_sig.HasField`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_agent_card_signature(core_sig: pb2_v10.AgentCardSignature) -> types_v03.AgentCardSignature:
    return types_v03.AgentCardSignature(protected=core_sig.protected, signature=core_sig.signature, header=MessageToDict(core_sig.header) if core_sig.HasField('header') else None)
```

</details>

### `to_core_agent_card`

Source lines 845–913; declaration kind `FunctionDef`.

Inputs: `(compat_card: types_v03.AgentCard)`. Output annotation: `pb2_v10.AgentCard`. Decorators: `none`.

Source intent: Convert agent card to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_card` from `pb2_v10.AgentCard(name=compat_card.name, description=compat_card.description, version=compat_card.version)`; output construction/calls here execute immediately when this method runs.
2. Assigns `primary_interface` from `pb2_v10.AgentInterface(url=compat_card.url, protocol_binding=compat_card.preferred_transport or 'JSONRPC', protocol_version=compat_card.protocol_version or constants.PROTOCOL_VERSION_0_3)`; output construction/calls here execute immediately when this method runs.
3. Executes `core_card.supported_interfaces.append(primary_interface)`.
4. Branches on `compat_card.additional_interfaces`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `compat_card.provider`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Branches on `compat_card.documentation_url`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
7. Branches on `compat_card.icon_url`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
8. Assigns `core_cap` from `to_core_agent_capabilities(compat_card.capabilities)`; output construction/calls here execute immediately when this method runs.
9. Branches on `compat_card.supports_authenticated_extended_card is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
10. Executes `core_card.capabilities.CopyFrom(core_cap)`.
11. Branches on `compat_card.security_schemes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
12. Branches on `compat_card.security`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
13. Branches on `compat_card.default_input_modes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
14. Branches on `compat_card.default_output_modes`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
15. Branches on `compat_card.skills`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
16. Branches on `compat_card.signatures`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
17. Returns `core_card`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.AgentCard`, `pb2_v10.AgentInterface`, `core_card.supported_interfaces.append`, `to_core_agent_capabilities`, `core_card.capabilities.CopyFrom`, `core_card.supported_interfaces.extend`, `core_card.provider.CopyFrom`, `compat_card.security_schemes.items`, `core_card.security_requirements.extend`, `core_card.default_input_modes.extend`, `core_card.default_output_modes.extend`, `core_card.skills.extend`, `core_card.signatures.extend`, `to_core_agent_provider`, `core_card.security_schemes[k].CopyFrom`, `to_core_agent_interface`, `to_core_security_scheme`, `to_core_security_requirement`, `to_core_agent_skill`, `to_core_agent_card_signature`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_agent_card(compat_card: types_v03.AgentCard) -> pb2_v10.AgentCard:
    core_card = pb2_v10.AgentCard(name=compat_card.name, description=compat_card.description, version=compat_card.version)
    primary_interface = pb2_v10.AgentInterface(url=compat_card.url, protocol_binding=compat_card.preferred_transport or 'JSONRPC', protocol_version=compat_card.protocol_version or constants.PROTOCOL_VERSION_0_3)
    core_card.supported_interfaces.append(primary_interface)
    if compat_card.additional_interfaces:
        core_card.supported_interfaces.extend([to_core_agent_interface(i) for i in compat_card.additional_interfaces])
    if compat_card.provider:
        core_card.provider.CopyFrom(to_core_agent_provider(compat_card.provider))
    if compat_card.documentation_url:
        core_card.documentation_url = compat_card.documentation_url
    if compat_card.icon_url:
        core_card.icon_url = compat_card.icon_url
    core_cap = to_core_agent_capabilities(compat_card.capabilities)
    if compat_card.supports_authenticated_extended_card is not None:
        core_cap.extended_agent_card = compat_card.supports_authenticated_extended_card
    core_card.capabilities.CopyFrom(core_cap)
    if compat_card.security_schemes:
        for k, v in compat_card.security_schemes.items():
            core_card.security_schemes[k].CopyFrom(to_core_security_scheme(v))
    if compat_card.security:
        core_card.security_requirements.extend([to_core_security_requirement(r) for r in compat_card.security])
    if compat_card.default_input_modes:
        core_card.default_input_modes.extend(compat_card.default_input_modes)
    if compat_card.default_output_modes:
        core_card.default_output_modes.extend(compat_card.default_output_modes)
    if compat_card.skills:
        core_card.skills.extend([to_core_agent_skill(s) for s in compat_card.skills])
    if compat_card.signatures:
        core_card.signatures.extend([to_core_agent_card_signature(s) for s in compat_card.signatures])
    return core_card
```

</details>

### `to_compat_agent_card`

Source lines 916–988; declaration kind `FunctionDef`.

Inputs: `(core_card: pb2_v10.AgentCard)`. Output annotation: `types_v03.AgentCard`. Decorators: `none`.

Source intent: Convert agent card to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `compat_interfaces` from `[interface for interface in core_card.supported_interfaces if not interface.protocol_version or is_legacy_version(interface.protocol_version)]`; output construction/calls here execute immediately when this method runs.
2. Branches on `not compat_interfaces`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Assigns `primary_interface` from `compat_interfaces[0]`; output construction/calls here execute immediately when this method runs.
4. Assigns `additional_interfaces` from `[to_compat_agent_interface(i) for i in compat_interfaces[1:]]`; output construction/calls here execute immediately when this method runs.
5. Assigns `compat_cap` from `to_compat_agent_capabilities(core_card.capabilities)`; output construction/calls here execute immediately when this method runs.
6. Assigns `supports_authenticated_extended_card` from `core_card.capabilities.extended_agent_card if core_card.capabilities.HasField('extended_agent_card') else None`; output construction/calls here execute immediately when this method runs.
7. Returns `types_v03.AgentCard(name=core_card.name, description=core_card.description, version=core_card.version, url=primary_interface.url, preferred_transport=primary_interface.protocol_binding, protocol_version=primary_interface.protocol_version or constants.PROTOCOL_VERSION_0_3, additional_interfaces=additional_interfaces or None, provider=to_compat_agent_provider( … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: `errors.VersionNotSupportedError('AgentCard must have at least one interface with compatible protocol version.')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `to_compat_agent_capabilities`, `types_v03.AgentCard`, `errors.VersionNotSupportedError`, `to_compat_agent_interface`, `core_card.capabilities.HasField`, `is_legacy_version`, `core_card.HasField`, `to_compat_agent_provider`, `list`, `to_compat_security_scheme`, `to_compat_security_requirement`, `to_compat_agent_skill`, `to_compat_agent_card_signature`, `core_card.security_schemes.items`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_agent_card(core_card: pb2_v10.AgentCard) -> types_v03.AgentCard:
    compat_interfaces = [interface for interface in core_card.supported_interfaces if not interface.protocol_version or is_legacy_version(interface.protocol_version)]
    if not compat_interfaces:
        raise errors.VersionNotSupportedError('AgentCard must have at least one interface with compatible protocol version.')
    primary_interface = compat_interfaces[0]
    additional_interfaces = [to_compat_agent_interface(i) for i in compat_interfaces[1:]]
    compat_cap = to_compat_agent_capabilities(core_card.capabilities)
    supports_authenticated_extended_card = core_card.capabilities.extended_agent_card if core_card.capabilities.HasField('extended_agent_card') else None
    return types_v03.AgentCard(name=core_card.name, description=core_card.description, version=core_card.version, url=primary_interface.url, preferred_transport=primary_interface.protocol_binding, protocol_version=primary_interface.protocol_version or constants.PROTOCOL_VERSION_0_3, additional_interfaces=additional_interfaces or None, provider=to_compat_agent_provider(core_card.provider) if core_card.HasField('provider') else None, documentation_url=core_card.documentation_url if core_card.HasField('documentation_url') else None, icon_url=core_card.icon_url if core_card.HasField('icon_url') else None, capabilities=compat_cap, supports_authenticated_extended_card=supports_authenticated_extended_card, security_schemes={k: to_compat_security_scheme(v) for k, v in core_card.security_schemes.items()} if core_card.security_schemes else None, security=[to_compat_security_requirement(r) for r in core_card.security_requirements] if core_card.security_requirements else None, default_input_modes=list(core_card.default_input_modes) if core_card.default_input_modes else [], default_output_modes=list(core_card.default_output_modes) if core_card.default_output_modes else [], skills=[to_compat_agent_skill(s) for s in core_card.skills] if core_card.skills else [], signatures=[to_compat_agent_card_signature(s) for s in core_card.signatures] if core_card.signatures else None)
```

</details>

### `to_compat_task_artifact_update_event`

Source lines 991–1004; declaration kind `FunctionDef`.

Inputs: `(core_event: pb2_v10.TaskArtifactUpdateEvent)`. Output annotation: `types_v03.TaskArtifactUpdateEvent`. Decorators: `none`.

Source intent: Convert task artifact update event to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.TaskArtifactUpdateEvent(task_id=core_event.task_id, context_id=core_event.context_id, artifact=to_compat_artifact(core_event.artifact), append=core_event.append, last_chunk=core_event.last_chunk, metadata=MessageToDict(core_event.metadata) if core_event.HasField('metadata') else None)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.TaskArtifactUpdateEvent`, `to_compat_artifact`, `core_event.HasField`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_task_artifact_update_event(core_event: pb2_v10.TaskArtifactUpdateEvent) -> types_v03.TaskArtifactUpdateEvent:
    return types_v03.TaskArtifactUpdateEvent(task_id=core_event.task_id, context_id=core_event.context_id, artifact=to_compat_artifact(core_event.artifact), append=core_event.append, last_chunk=core_event.last_chunk, metadata=MessageToDict(core_event.metadata) if core_event.HasField('metadata') else None)
```

</details>

### `to_core_task_push_notification_config`

Source lines 1007–1020; declaration kind `FunctionDef`.

Inputs: `(compat_config: types_v03.TaskPushNotificationConfig)`. Output annotation: `pb2_v10.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Convert task push notification config to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_config` from `pb2_v10.TaskPushNotificationConfig(task_id=compat_config.task_id)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_config.push_notification_config`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `core_config`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.TaskPushNotificationConfig`, `core_config.MergeFrom`, `to_core_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_task_push_notification_config(compat_config: types_v03.TaskPushNotificationConfig) -> pb2_v10.TaskPushNotificationConfig:
    core_config = pb2_v10.TaskPushNotificationConfig(task_id=compat_config.task_id)
    if compat_config.push_notification_config:
        core_config.MergeFrom(to_core_push_notification_config(compat_config.push_notification_config))
    return core_config
```

</details>

### `to_compat_task_push_notification_config`

Source lines 1023–1032; declaration kind `FunctionDef`.

Inputs: `(core_config: pb2_v10.TaskPushNotificationConfig)`. Output annotation: `types_v03.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Convert task push notification config to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.TaskPushNotificationConfig(task_id=core_config.task_id, push_notification_config=to_compat_push_notification_config(core_config))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.TaskPushNotificationConfig`, `to_compat_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_task_push_notification_config(core_config: pb2_v10.TaskPushNotificationConfig) -> types_v03.TaskPushNotificationConfig:
    return types_v03.TaskPushNotificationConfig(task_id=core_config.task_id, push_notification_config=to_compat_push_notification_config(core_config))
```

</details>

### `to_core_send_message_request`

Source lines 1035–1048; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.SendMessageRequest)`. Output annotation: `pb2_v10.SendMessageRequest`. Decorators: `none`.

Source intent: Convert send message request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_req` from `pb2_v10.SendMessageRequest()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_req.params.message`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `compat_req.params.configuration`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `compat_req.params.metadata`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Returns `core_req`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.SendMessageRequest`, `core_req.message.CopyFrom`, `core_req.configuration.CopyFrom`, `ParseDict`, `to_core_message`, `to_core_send_message_configuration`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_send_message_request(compat_req: types_v03.SendMessageRequest) -> pb2_v10.SendMessageRequest:
    core_req = pb2_v10.SendMessageRequest()
    if compat_req.params.message:
        core_req.message.CopyFrom(to_core_message(compat_req.params.message))
    if compat_req.params.configuration:
        core_req.configuration.CopyFrom(to_core_send_message_configuration(compat_req.params.configuration))
    if compat_req.params.metadata:
        ParseDict(compat_req.params.metadata, core_req.metadata)
    return core_req
```

</details>

### `to_compat_send_message_request`

Source lines 1051–1068; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.SendMessageRequest, request_id: str | int)`. Output annotation: `types_v03.SendMessageRequest`. Decorators: `none`.

Source intent: Convert send message request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.SendMessageRequest(id=request_id, params=types_v03.MessageSendParams(message=to_compat_message(core_req.message), configuration=to_compat_send_message_configuration(core_req.configuration) if core_req.HasField('configuration') else None, metadata=MessageToDict(core_req.metadata) if core_req.HasField('metadata') else None))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.SendMessageRequest`, `types_v03.MessageSendParams`, `to_compat_message`, `core_req.HasField`, `to_compat_send_message_configuration`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_send_message_request(core_req: pb2_v10.SendMessageRequest, request_id: str | int) -> types_v03.SendMessageRequest:
    return types_v03.SendMessageRequest(id=request_id, params=types_v03.MessageSendParams(message=to_compat_message(core_req.message), configuration=to_compat_send_message_configuration(core_req.configuration) if core_req.HasField('configuration') else None, metadata=MessageToDict(core_req.metadata) if core_req.HasField('metadata') else None))
```

</details>

### `to_core_get_task_request`

Source lines 1071–1079; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.GetTaskRequest)`. Output annotation: `pb2_v10.GetTaskRequest`. Decorators: `none`.

Source intent: Convert get task request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_req` from `pb2_v10.GetTaskRequest()`; output construction/calls here execute immediately when this method runs.
2. Assigns `core_req.id` from `compat_req.params.id`; output construction/calls here execute immediately when this method runs.
3. Branches on `compat_req.params.history_length is not None`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_req`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.GetTaskRequest`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_get_task_request(compat_req: types_v03.GetTaskRequest) -> pb2_v10.GetTaskRequest:
    core_req = pb2_v10.GetTaskRequest()
    core_req.id = compat_req.params.id
    if compat_req.params.history_length is not None:
        core_req.history_length = compat_req.params.history_length
    return core_req
```

</details>

### `to_compat_get_task_request`

Source lines 1082–1094; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.GetTaskRequest, request_id: str | int)`. Output annotation: `types_v03.GetTaskRequest`. Decorators: `none`.

Source intent: Convert get task request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.GetTaskRequest(id=request_id, params=types_v03.TaskQueryParams(id=core_req.id, history_length=core_req.history_length if core_req.HasField('history_length') else None))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.GetTaskRequest`, `types_v03.TaskQueryParams`, `core_req.HasField`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_get_task_request(core_req: pb2_v10.GetTaskRequest, request_id: str | int) -> types_v03.GetTaskRequest:
    return types_v03.GetTaskRequest(id=request_id, params=types_v03.TaskQueryParams(id=core_req.id, history_length=core_req.history_length if core_req.HasField('history_length') else None))
```

</details>

### `to_core_cancel_task_request`

Source lines 1097–1104; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.CancelTaskRequest)`. Output annotation: `pb2_v10.CancelTaskRequest`. Decorators: `none`.

Source intent: Convert cancel task request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_req` from `pb2_v10.CancelTaskRequest(id=compat_req.params.id)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_req.params.metadata`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `core_req`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.CancelTaskRequest`, `ParseDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_cancel_task_request(compat_req: types_v03.CancelTaskRequest) -> pb2_v10.CancelTaskRequest:
    core_req = pb2_v10.CancelTaskRequest(id=compat_req.params.id)
    if compat_req.params.metadata:
        ParseDict(compat_req.params.metadata, core_req.metadata)
    return core_req
```

</details>

### `to_compat_cancel_task_request`

Source lines 1107–1119; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.CancelTaskRequest, request_id: str | int)`. Output annotation: `types_v03.CancelTaskRequest`. Decorators: `none`.

Source intent: Convert cancel task request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.CancelTaskRequest(id=request_id, params=types_v03.TaskIdParams(id=core_req.id, metadata=MessageToDict(core_req.metadata) if core_req.HasField('metadata') else None))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.CancelTaskRequest`, `types_v03.TaskIdParams`, `core_req.HasField`, `MessageToDict`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_cancel_task_request(core_req: pb2_v10.CancelTaskRequest, request_id: str | int) -> types_v03.CancelTaskRequest:
    return types_v03.CancelTaskRequest(id=request_id, params=types_v03.TaskIdParams(id=core_req.id, metadata=MessageToDict(core_req.metadata) if core_req.HasField('metadata') else None))
```

</details>

### `to_core_get_task_push_notification_config_request`

Source lines 1122–1135; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.GetTaskPushNotificationConfigRequest)`. Output annotation: `pb2_v10.GetTaskPushNotificationConfigRequest`. Decorators: `none`.

Source intent: Convert get task push notification config request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `isinstance(compat_req.params, types_v03.GetTaskPushNotificationConfigParams)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Returns `pb2_v10.GetTaskPushNotificationConfigRequest(task_id=compat_req.params.id)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `isinstance`, `pb2_v10.GetTaskPushNotificationConfigRequest`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_get_task_push_notification_config_request(compat_req: types_v03.GetTaskPushNotificationConfigRequest) -> pb2_v10.GetTaskPushNotificationConfigRequest:
    if isinstance(compat_req.params, types_v03.GetTaskPushNotificationConfigParams):
        return pb2_v10.GetTaskPushNotificationConfigRequest(task_id=compat_req.params.id, id=compat_req.params.push_notification_config_id)
    return pb2_v10.GetTaskPushNotificationConfigRequest(task_id=compat_req.params.id)
```

</details>

### `to_compat_get_task_push_notification_config_request`

Source lines 1138–1154; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.GetTaskPushNotificationConfigRequest, request_id: str | int)`. Output annotation: `types_v03.GetTaskPushNotificationConfigRequest`. Decorators: `none`.

Source intent: Convert get task push notification config request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Declares `params: types_v03.GetTaskPushNotificationConfigParams | types_v03.TaskIdParams`.
2. Branches on `core_req.id`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `types_v03.GetTaskPushNotificationConfigRequest(id=request_id, params=params)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.GetTaskPushNotificationConfigRequest`, `types_v03.GetTaskPushNotificationConfigParams`, `types_v03.TaskIdParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_get_task_push_notification_config_request(core_req: pb2_v10.GetTaskPushNotificationConfigRequest, request_id: str | int) -> types_v03.GetTaskPushNotificationConfigRequest:
    params: types_v03.GetTaskPushNotificationConfigParams | types_v03.TaskIdParams
    if core_req.id:
        params = types_v03.GetTaskPushNotificationConfigParams(id=core_req.task_id, push_notification_config_id=core_req.id)
    else:
        params = types_v03.TaskIdParams(id=core_req.task_id)
    return types_v03.GetTaskPushNotificationConfigRequest(id=request_id, params=params)
```

</details>

### `to_core_delete_task_push_notification_config_request`

Source lines 1157–1164; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.DeleteTaskPushNotificationConfigRequest)`. Output annotation: `pb2_v10.DeleteTaskPushNotificationConfigRequest`. Decorators: `none`.

Source intent: Convert delete task push notification config request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `pb2_v10.DeleteTaskPushNotificationConfigRequest(task_id=compat_req.params.id, id=compat_req.params.push_notification_config_id)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.DeleteTaskPushNotificationConfigRequest`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_delete_task_push_notification_config_request(compat_req: types_v03.DeleteTaskPushNotificationConfigRequest) -> pb2_v10.DeleteTaskPushNotificationConfigRequest:
    return pb2_v10.DeleteTaskPushNotificationConfigRequest(task_id=compat_req.params.id, id=compat_req.params.push_notification_config_id)
```

</details>

### `to_compat_delete_task_push_notification_config_request`

Source lines 1167–1177; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.DeleteTaskPushNotificationConfigRequest, request_id: str | int)`. Output annotation: `types_v03.DeleteTaskPushNotificationConfigRequest`. Decorators: `none`.

Source intent: Convert delete task push notification config request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.DeleteTaskPushNotificationConfigRequest(id=request_id, params=types_v03.DeleteTaskPushNotificationConfigParams(id=core_req.task_id, push_notification_config_id=core_req.id))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.DeleteTaskPushNotificationConfigRequest`, `types_v03.DeleteTaskPushNotificationConfigParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_delete_task_push_notification_config_request(core_req: pb2_v10.DeleteTaskPushNotificationConfigRequest, request_id: str | int) -> types_v03.DeleteTaskPushNotificationConfigRequest:
    return types_v03.DeleteTaskPushNotificationConfigRequest(id=request_id, params=types_v03.DeleteTaskPushNotificationConfigParams(id=core_req.task_id, push_notification_config_id=core_req.id))
```

</details>

### `to_core_create_task_push_notification_config_request`

Source lines 1180–1193; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.SetTaskPushNotificationConfigRequest)`. Output annotation: `pb2_v10.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Convert create task push notification config request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_req` from `pb2_v10.TaskPushNotificationConfig(task_id=compat_req.params.task_id)`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_req.params.push_notification_config`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `core_req`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.TaskPushNotificationConfig`, `core_req.MergeFrom`, `to_core_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_create_task_push_notification_config_request(compat_req: types_v03.SetTaskPushNotificationConfigRequest) -> pb2_v10.TaskPushNotificationConfig:
    core_req = pb2_v10.TaskPushNotificationConfig(task_id=compat_req.params.task_id)
    if compat_req.params.push_notification_config:
        core_req.MergeFrom(to_core_push_notification_config(compat_req.params.push_notification_config))
    return core_req
```

</details>

### `to_compat_create_task_push_notification_config_request`

Source lines 1196–1209; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.TaskPushNotificationConfig, request_id: str | int)`. Output annotation: `types_v03.SetTaskPushNotificationConfigRequest`. Decorators: `none`.

Source intent: Convert create task push notification config request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.SetTaskPushNotificationConfigRequest(id=request_id, params=types_v03.TaskPushNotificationConfig(task_id=core_req.task_id, push_notification_config=to_compat_push_notification_config(core_req)))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.SetTaskPushNotificationConfigRequest`, `types_v03.TaskPushNotificationConfig`, `to_compat_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_create_task_push_notification_config_request(core_req: pb2_v10.TaskPushNotificationConfig, request_id: str | int) -> types_v03.SetTaskPushNotificationConfigRequest:
    return types_v03.SetTaskPushNotificationConfigRequest(id=request_id, params=types_v03.TaskPushNotificationConfig(task_id=core_req.task_id, push_notification_config=to_compat_push_notification_config(core_req)))
```

</details>

### `to_core_subscribe_to_task_request`

Source lines 1212–1216; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.TaskResubscriptionRequest)`. Output annotation: `pb2_v10.SubscribeToTaskRequest`. Decorators: `none`.

Source intent: Convert subscribe to task request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `pb2_v10.SubscribeToTaskRequest(id=compat_req.params.id)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.SubscribeToTaskRequest`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_subscribe_to_task_request(compat_req: types_v03.TaskResubscriptionRequest) -> pb2_v10.SubscribeToTaskRequest:
    return pb2_v10.SubscribeToTaskRequest(id=compat_req.params.id)
```

</details>

### `to_compat_subscribe_to_task_request`

Source lines 1219–1225; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.SubscribeToTaskRequest, request_id: str | int)`. Output annotation: `types_v03.TaskResubscriptionRequest`. Decorators: `none`.

Source intent: Convert subscribe to task request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.TaskResubscriptionRequest(id=request_id, params=types_v03.TaskIdParams(id=core_req.id))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.TaskResubscriptionRequest`, `types_v03.TaskIdParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_subscribe_to_task_request(core_req: pb2_v10.SubscribeToTaskRequest, request_id: str | int) -> types_v03.TaskResubscriptionRequest:
    return types_v03.TaskResubscriptionRequest(id=request_id, params=types_v03.TaskIdParams(id=core_req.id))
```

</details>

### `to_core_list_task_push_notification_config_request`

Source lines 1228–1235; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.ListTaskPushNotificationConfigRequest)`. Output annotation: `pb2_v10.ListTaskPushNotificationConfigsRequest`. Decorators: `none`.

Source intent: Convert list task push notification config request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_req` from `pb2_v10.ListTaskPushNotificationConfigsRequest()`; output construction/calls here execute immediately when this method runs.
2. Branches on `compat_req.params.id`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Returns `core_req`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.ListTaskPushNotificationConfigsRequest`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_list_task_push_notification_config_request(compat_req: types_v03.ListTaskPushNotificationConfigRequest) -> pb2_v10.ListTaskPushNotificationConfigsRequest:
    core_req = pb2_v10.ListTaskPushNotificationConfigsRequest()
    if compat_req.params.id:
        core_req.task_id = compat_req.params.id
    return core_req
```

</details>

### `to_compat_list_task_push_notification_config_request`

Source lines 1238–1248; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.ListTaskPushNotificationConfigsRequest, request_id: str | int)`. Output annotation: `types_v03.ListTaskPushNotificationConfigRequest`. Decorators: `none`.

Source intent: Convert list task push notification config request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.ListTaskPushNotificationConfigRequest(id=request_id, params=types_v03.ListTaskPushNotificationConfigParams(id=core_req.task_id))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.ListTaskPushNotificationConfigRequest`, `types_v03.ListTaskPushNotificationConfigParams`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_list_task_push_notification_config_request(core_req: pb2_v10.ListTaskPushNotificationConfigsRequest, request_id: str | int) -> types_v03.ListTaskPushNotificationConfigRequest:
    return types_v03.ListTaskPushNotificationConfigRequest(id=request_id, params=types_v03.ListTaskPushNotificationConfigParams(id=core_req.task_id))
```

</details>

### `to_core_list_task_push_notification_config_response`

Source lines 1251–1262; declaration kind `FunctionDef`.

Inputs: `(compat_res: types_v03.ListTaskPushNotificationConfigResponse)`. Output annotation: `pb2_v10.ListTaskPushNotificationConfigsResponse`. Decorators: `none`.

Source intent: Convert list task push notification config response to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_res` from `pb2_v10.ListTaskPushNotificationConfigsResponse()`; output construction/calls here execute immediately when this method runs.
2. Assigns `root` from `compat_res.root`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(root, types_v03.ListTaskPushNotificationConfigSuccessResponse)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_res`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.ListTaskPushNotificationConfigsResponse`, `isinstance`, `core_res.configs.append`, `to_core_task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_list_task_push_notification_config_response(compat_res: types_v03.ListTaskPushNotificationConfigResponse) -> pb2_v10.ListTaskPushNotificationConfigsResponse:
    core_res = pb2_v10.ListTaskPushNotificationConfigsResponse()
    root = compat_res.root
    if isinstance(root, types_v03.ListTaskPushNotificationConfigSuccessResponse):
        for c in root.result:
            core_res.configs.append(to_core_task_push_notification_config(c))
    return core_res
```

</details>

### `to_compat_list_task_push_notification_config_response`

Source lines 1265–1278; declaration kind `FunctionDef`.

Inputs: `(core_res: pb2_v10.ListTaskPushNotificationConfigsResponse, request_id: str | int | None=None)`. Output annotation: `types_v03.ListTaskPushNotificationConfigResponse`. Decorators: `none`.

Source intent: Convert list task push notification config response to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.ListTaskPushNotificationConfigResponse(root=types_v03.ListTaskPushNotificationConfigSuccessResponse(id=request_id, result=[to_compat_task_push_notification_config(c) for c in core_res.configs]))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.ListTaskPushNotificationConfigResponse`, `types_v03.ListTaskPushNotificationConfigSuccessResponse`, `to_compat_task_push_notification_config`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_list_task_push_notification_config_response(core_res: pb2_v10.ListTaskPushNotificationConfigsResponse, request_id: str | int | None=None) -> types_v03.ListTaskPushNotificationConfigResponse:
    return types_v03.ListTaskPushNotificationConfigResponse(root=types_v03.ListTaskPushNotificationConfigSuccessResponse(id=request_id, result=[to_compat_task_push_notification_config(c) for c in core_res.configs]))
```

</details>

### `to_core_send_message_response`

Source lines 1281–1292; declaration kind `FunctionDef`.

Inputs: `(compat_res: types_v03.SendMessageResponse)`. Output annotation: `pb2_v10.SendMessageResponse`. Decorators: `none`.

Source intent: Convert send message response to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_res` from `pb2_v10.SendMessageResponse()`; output construction/calls here execute immediately when this method runs.
2. Assigns `root` from `compat_res.root`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(root, types_v03.SendMessageSuccessResponse)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_res`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.SendMessageResponse`, `isinstance`, `core_res.task.CopyFrom`, `core_res.message.CopyFrom`, `to_core_task`, `to_core_message`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_send_message_response(compat_res: types_v03.SendMessageResponse) -> pb2_v10.SendMessageResponse:
    core_res = pb2_v10.SendMessageResponse()
    root = compat_res.root
    if isinstance(root, types_v03.SendMessageSuccessResponse):
        if isinstance(root.result, types_v03.Task):
            core_res.task.CopyFrom(to_core_task(root.result))
        else:
            core_res.message.CopyFrom(to_core_message(root.result))
    return core_res
```

</details>

### `to_compat_send_message_response`

Source lines 1295–1311; declaration kind `FunctionDef`.

Inputs: `(core_res: pb2_v10.SendMessageResponse, request_id: str | int | None=None)`. Output annotation: `types_v03.SendMessageResponse`. Decorators: `none`.

Source intent: Convert send message response to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Branches on `core_res.HasField('task')`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
2. Assigns `result_msg` from `to_compat_message(core_res.message)`; output construction/calls here execute immediately when this method runs.
3. Returns `types_v03.SendMessageResponse(root=types_v03.SendMessageSuccessResponse(id=request_id, result=result_msg))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `core_res.HasField`, `to_compat_message`, `types_v03.SendMessageResponse`, `to_compat_task`, `types_v03.SendMessageSuccessResponse`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_send_message_response(core_res: pb2_v10.SendMessageResponse, request_id: str | int | None=None) -> types_v03.SendMessageResponse:
    if core_res.HasField('task'):
        result_task = to_compat_task(core_res.task)
        return types_v03.SendMessageResponse(root=types_v03.SendMessageSuccessResponse(id=request_id, result=result_task))
    result_msg = to_compat_message(core_res.message)
    return types_v03.SendMessageResponse(root=types_v03.SendMessageSuccessResponse(id=request_id, result=result_msg))
```

</details>

### `to_core_stream_response`

Source lines 1314–1332; declaration kind `FunctionDef`.

Inputs: `(compat_res: types_v03.SendStreamingMessageSuccessResponse)`. Output annotation: `pb2_v10.StreamResponse`. Decorators: `none`.

Source intent: Convert stream response to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `core_res` from `pb2_v10.StreamResponse()`; output construction/calls here execute immediately when this method runs.
2. Assigns `root` from `compat_res.result`; output construction/calls here execute immediately when this method runs.
3. Branches on `isinstance(root, types_v03.Message)`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Returns `core_res`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.StreamResponse`, `isinstance`, `core_res.message.CopyFrom`, `to_core_message`, `core_res.task.CopyFrom`, `to_core_task`, `core_res.status_update.CopyFrom`, `to_core_task_status_update_event`, `core_res.artifact_update.CopyFrom`, `to_core_task_artifact_update_event`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_stream_response(compat_res: types_v03.SendStreamingMessageSuccessResponse) -> pb2_v10.StreamResponse:
    core_res = pb2_v10.StreamResponse()
    root = compat_res.result
    if isinstance(root, types_v03.Message):
        core_res.message.CopyFrom(to_core_message(root))
    elif isinstance(root, types_v03.Task):
        core_res.task.CopyFrom(to_core_task(root))
    elif isinstance(root, types_v03.TaskStatusUpdateEvent):
        core_res.status_update.CopyFrom(to_core_task_status_update_event(root))
    elif isinstance(root, types_v03.TaskArtifactUpdateEvent):
        core_res.artifact_update.CopyFrom(to_core_task_artifact_update_event(root))
    return core_res
```

</details>

### `to_compat_stream_response`

Source lines 1335–1361; declaration kind `FunctionDef`.

Inputs: `(core_res: pb2_v10.StreamResponse, request_id: str | int | None=None)`. Output annotation: `types_v03.SendStreamingMessageSuccessResponse`. Decorators: `none`.

Source intent: Convert stream response to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `which` from `core_res.WhichOneof('payload')`; output construction/calls here execute immediately when this method runs.
2. Branches on `which == 'message'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
3. Branches on `which == 'task'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
4. Branches on `which == 'status_update'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
5. Branches on `which == 'artifact_update'`; selected body controls conversion/default/error behavior. Both branches are shown in the implementation below.
6. Raises `ValueError(f'Unknown stream response event type: {which}')`.

Explicit errors: `ValueError(f'Unknown stream response event type: {which}')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `core_res.WhichOneof`, `ValueError`, `types_v03.SendStreamingMessageSuccessResponse`, `to_compat_message`, `to_compat_task`, `to_compat_task_status_update_event`, `to_compat_task_artifact_update_event`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_stream_response(core_res: pb2_v10.StreamResponse, request_id: str | int | None=None) -> types_v03.SendStreamingMessageSuccessResponse:
    which = core_res.WhichOneof('payload')
    if which == 'message':
        return types_v03.SendStreamingMessageSuccessResponse(id=request_id, result=to_compat_message(core_res.message))
    if which == 'task':
        return types_v03.SendStreamingMessageSuccessResponse(id=request_id, result=to_compat_task(core_res.task))
    if which == 'status_update':
        return types_v03.SendStreamingMessageSuccessResponse(id=request_id, result=to_compat_task_status_update_event(core_res.status_update))
    if which == 'artifact_update':
        return types_v03.SendStreamingMessageSuccessResponse(id=request_id, result=to_compat_task_artifact_update_event(core_res.artifact_update))
    raise ValueError(f'Unknown stream response event type: {which}')
```

</details>

### `to_core_get_extended_agent_card_request`

Source lines 1364–1368; declaration kind `FunctionDef`.

Inputs: `(compat_req: types_v03.GetAuthenticatedExtendedCardRequest)`. Output annotation: `pb2_v10.GetExtendedAgentCardRequest`. Decorators: `none`.

Source intent: Convert get extended agent card request to v1.0 core type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `pb2_v10.GetExtendedAgentCardRequest()`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `pb2_v10.GetExtendedAgentCardRequest`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_core_get_extended_agent_card_request(compat_req: types_v03.GetAuthenticatedExtendedCardRequest) -> pb2_v10.GetExtendedAgentCardRequest:
    return pb2_v10.GetExtendedAgentCardRequest()
```

</details>

### `to_compat_get_extended_agent_card_request`

Source lines 1371–1375; declaration kind `FunctionDef`.

Inputs: `(core_req: pb2_v10.GetExtendedAgentCardRequest, request_id: str | int)`. Output annotation: `types_v03.GetAuthenticatedExtendedCardRequest`. Decorators: `none`.

Source intent: Convert get extended agent card request to v0.3 compat type.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `types_v03.GetAuthenticatedExtendedCardRequest(id=request_id)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.GetAuthenticatedExtendedCardRequest`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def to_compat_get_extended_agent_card_request(core_req: pb2_v10.GetExtendedAgentCardRequest, request_id: str | int) -> types_v03.GetAuthenticatedExtendedCardRequest:
    return types_v03.GetAuthenticatedExtendedCardRequest(id=request_id)
```

</details>
