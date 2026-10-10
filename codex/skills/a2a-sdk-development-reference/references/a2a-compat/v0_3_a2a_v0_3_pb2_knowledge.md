# v0_3/a2a_v0_3_pb2.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/a2a_v0_3_pb2.py`. SHA-256: `130db434cbc63aacd10cfccefac0f64a150b106e4d0a6fed09d65a8bc5383d33`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Generated runtime and stub family

This guide covers both generated Python and `.pyi`. Runtime module validates public protobuf runtime compatibility with generated version **5.29.3**, imports google.api annotations/client/field_behavior plus protobuf empty/Struct/Timestamp, registers serialized descriptor in default pool, and calls internal builder to materialize messages/enums into module globals. It has **no Python AST class/function declarations**; these objects are dynamically generated. With Python descriptors disabled for C implementation, it additionally installs serialized options and source offsets. The complete decoded descriptor catalog below accounts for generated classes, nested map-entry messages, oneofs, field numbers/types/json names/options, enum values and service RPCs.

Python module name is a2a.compat.v0_3.a2a_v0_3_pb2 while protobuf type namespace is a2a.v1. Importing current a2a.types.a2a_pb2 registers lf.a2a.v1, preventing name collision. Duplicate incompatible registration or runtime mismatch can fail import; no compat retry handles this. Actual compiled descriptor differs in language options from included proto text (for example generated Java package com.a2a.v1 vs source com.google.a2a.v1); treat descriptor as runtime truth and source as shipped schema evidence, not reproducibility proof.

`.pyi` declares constructors, typed fields, field-number constants, nested map entries and Enum wrappers; ellipsis methods are typing declarations, not runtime implementations. Every declaration is indexed below. Constructor keyword values accept messages/mappings; repeated containers use iterable inputs and map inputs use mappings as annotated. Proto3 scalar fields read defaults and lack HasField unless oneof; submessages have presence. `WhichOneof`, `CopyFrom`, `MergeFrom`, `SerializeToString`, `FromString`, ParseFromString, ClearField and HasField come from protobuf runtime. Invalid field/types, unrecognized field names/presence checks, malformed serialized bytes and incompatible CopyFrom types raise runtime exceptions. These inherited APIs are not locally declared callables.

Struct uses double numbers; Timestamp owns RFC3339 parse/format; bytes become base64 in protobuf JSON; enum JSON uses names. JSON names override request→message, msg→message and status.update→message. Those differences explain why direct Pydantic dictionary parsing is not interchangeable with protobuf JSON. API REQUIRED annotations do not add a hand-written Python validation layer here. Oneof assignment replaces prior selected variant. Message fields and nested map types below prove absence/presence independently of converter behavior.

```python
from a2a.compat.v0_3 import a2a_v0_3_pb2 as legacy_pb
wire = legacy_pb.SendMessageResponse(msg=legacy_pb.Message(message_id='m'))
copy = legacy_pb.SendMessageResponse.FromString(wire.SerializeToString())
assert copy.WhichOneof('payload') == 'msg'
assert copy.DESCRIPTOR.full_name == 'a2a.v1.SendMessageResponse'
```

No HTTP/gRPC call is made by serialization alone. Avoid editing generated bindings and do not infer lost-field behavior from descriptors alone: converters intentionally omit some fields they contain.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
```

## Module state and maps

These assignments execute once at import; maps/defaults below are exact source values, not remote state.

```python
_sym_db = _symbol_database.Default()
_globals = globals()
```

## Declaration-by-declaration execution reference

No AST declarations. Empty initializers have no execution; dynamically built protobuf objects are documented in the descriptor catalog below.

## Complete PYI declaration surface

These signatures have ellipsis bodies and perform no runtime action; each class corresponds to a descriptor below. Map-entry constructors are included, not skipped as private/generated helpers.

### PYI `TaskState`

Source lines 18–28.

```python
class TaskState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_STATE_UNSPECIFIED: _ClassVar[TaskState]
    TASK_STATE_SUBMITTED: _ClassVar[TaskState]
    TASK_STATE_WORKING: _ClassVar[TaskState]
    TASK_STATE_COMPLETED: _ClassVar[TaskState]
    TASK_STATE_FAILED: _ClassVar[TaskState]
    TASK_STATE_CANCELLED: _ClassVar[TaskState]
    TASK_STATE_INPUT_REQUIRED: _ClassVar[TaskState]
    TASK_STATE_REJECTED: _ClassVar[TaskState]
    TASK_STATE_AUTH_REQUIRED: _ClassVar[TaskState]
```

### PYI `Role`

Source lines 30–34.

```python
class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLE_UNSPECIFIED: _ClassVar[Role]
    ROLE_USER: _ClassVar[Role]
    ROLE_AGENT: _ClassVar[Role]
```

### PYI `SendMessageConfiguration`

Source lines 48–58.

```python
class SendMessageConfiguration(_message.Message):
    __slots__ = ('accepted_output_modes', 'push_notification', 'history_length', 'blocking')
    ACCEPTED_OUTPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    PUSH_NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    HISTORY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    BLOCKING_FIELD_NUMBER: _ClassVar[int]
    accepted_output_modes: _containers.RepeatedScalarFieldContainer[str]
    push_notification: PushNotificationConfig
    history_length: int
    blocking: bool

    def __init__(self, accepted_output_modes: _Optional[_Iterable[str]]=..., push_notification: _Optional[_Union[PushNotificationConfig, _Mapping]]=..., history_length: _Optional[int]=..., blocking: _Optional[bool]=...) -> None:
        ...
```

### PYI `SendMessageConfiguration.__init__`

Source lines 58–58.

```python
def __init__(self, accepted_output_modes: _Optional[_Iterable[str]]=..., push_notification: _Optional[_Union[PushNotificationConfig, _Mapping]]=..., history_length: _Optional[int]=..., blocking: _Optional[bool]=...) -> None:
    ...
```

### PYI `Task`

Source lines 60–74.

```python
class Task(_message.Message):
    __slots__ = ('id', 'context_id', 'status', 'artifacts', 'history', 'metadata')
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    context_id: str
    status: TaskStatus
    artifacts: _containers.RepeatedCompositeFieldContainer[Artifact]
    history: _containers.RepeatedCompositeFieldContainer[Message]
    metadata: _struct_pb2.Struct

    def __init__(self, id: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskStatus, _Mapping]]=..., artifacts: _Optional[_Iterable[_Union[Artifact, _Mapping]]]=..., history: _Optional[_Iterable[_Union[Message, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `Task.__init__`

Source lines 74–74.

```python
def __init__(self, id: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskStatus, _Mapping]]=..., artifacts: _Optional[_Iterable[_Union[Artifact, _Mapping]]]=..., history: _Optional[_Iterable[_Union[Message, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `TaskStatus`

Source lines 76–84.

```python
class TaskStatus(_message.Message):
    __slots__ = ('state', 'update', 'timestamp')
    STATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    state: TaskState
    update: Message
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, state: _Optional[_Union[TaskState, str]]=..., update: _Optional[_Union[Message, _Mapping]]=..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...
```

### PYI `TaskStatus.__init__`

Source lines 84–84.

```python
def __init__(self, state: _Optional[_Union[TaskState, str]]=..., update: _Optional[_Union[Message, _Mapping]]=..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
    ...
```

### PYI `Part`

Source lines 86–96.

```python
class Part(_message.Message):
    __slots__ = ('text', 'file', 'data', 'metadata')
    TEXT_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    text: str
    file: FilePart
    data: DataPart
    metadata: _struct_pb2.Struct

    def __init__(self, text: _Optional[str]=..., file: _Optional[_Union[FilePart, _Mapping]]=..., data: _Optional[_Union[DataPart, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `Part.__init__`

Source lines 96–96.

```python
def __init__(self, text: _Optional[str]=..., file: _Optional[_Union[FilePart, _Mapping]]=..., data: _Optional[_Union[DataPart, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `FilePart`

Source lines 98–108.

```python
class FilePart(_message.Message):
    __slots__ = ('file_with_uri', 'file_with_bytes', 'mime_type', 'name')
    FILE_WITH_URI_FIELD_NUMBER: _ClassVar[int]
    FILE_WITH_BYTES_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    file_with_uri: str
    file_with_bytes: bytes
    mime_type: str
    name: str

    def __init__(self, file_with_uri: _Optional[str]=..., file_with_bytes: _Optional[bytes]=..., mime_type: _Optional[str]=..., name: _Optional[str]=...) -> None:
        ...
```

### PYI `FilePart.__init__`

Source lines 108–108.

```python
def __init__(self, file_with_uri: _Optional[str]=..., file_with_bytes: _Optional[bytes]=..., mime_type: _Optional[str]=..., name: _Optional[str]=...) -> None:
    ...
```

### PYI `DataPart`

Source lines 110–114.

```python
class DataPart(_message.Message):
    __slots__ = ('data',)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _struct_pb2.Struct

    def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `DataPart.__init__`

Source lines 114–114.

```python
def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `Message`

Source lines 116–132.

```python
class Message(_message.Message):
    __slots__ = ('message_id', 'context_id', 'task_id', 'role', 'content', 'metadata', 'extensions')
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    context_id: str
    task_id: str
    role: Role
    content: _containers.RepeatedCompositeFieldContainer[Part]
    metadata: _struct_pb2.Struct
    extensions: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, message_id: _Optional[str]=..., context_id: _Optional[str]=..., task_id: _Optional[str]=..., role: _Optional[_Union[Role, str]]=..., content: _Optional[_Iterable[_Union[Part, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., extensions: _Optional[_Iterable[str]]=...) -> None:
        ...
```

### PYI `Message.__init__`

Source lines 132–132.

```python
def __init__(self, message_id: _Optional[str]=..., context_id: _Optional[str]=..., task_id: _Optional[str]=..., role: _Optional[_Union[Role, str]]=..., content: _Optional[_Iterable[_Union[Part, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., extensions: _Optional[_Iterable[str]]=...) -> None:
    ...
```

### PYI `Artifact`

Source lines 134–148.

```python
class Artifact(_message.Message):
    __slots__ = ('artifact_id', 'name', 'description', 'parts', 'metadata', 'extensions')
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    artifact_id: str
    name: str
    description: str
    parts: _containers.RepeatedCompositeFieldContainer[Part]
    metadata: _struct_pb2.Struct
    extensions: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, artifact_id: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., parts: _Optional[_Iterable[_Union[Part, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., extensions: _Optional[_Iterable[str]]=...) -> None:
        ...
```

### PYI `Artifact.__init__`

Source lines 148–148.

```python
def __init__(self, artifact_id: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., parts: _Optional[_Iterable[_Union[Part, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., extensions: _Optional[_Iterable[str]]=...) -> None:
    ...
```

### PYI `TaskStatusUpdateEvent`

Source lines 150–162.

```python
class TaskStatusUpdateEvent(_message.Message):
    __slots__ = ('task_id', 'context_id', 'status', 'final', 'metadata')
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINAL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    context_id: str
    status: TaskStatus
    final: bool
    metadata: _struct_pb2.Struct

    def __init__(self, task_id: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskStatus, _Mapping]]=..., final: _Optional[bool]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `TaskStatusUpdateEvent.__init__`

Source lines 162–162.

```python
def __init__(self, task_id: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskStatus, _Mapping]]=..., final: _Optional[bool]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `TaskArtifactUpdateEvent`

Source lines 164–178.

```python
class TaskArtifactUpdateEvent(_message.Message):
    __slots__ = ('task_id', 'context_id', 'artifact', 'append', 'last_chunk', 'metadata')
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_FIELD_NUMBER: _ClassVar[int]
    APPEND_FIELD_NUMBER: _ClassVar[int]
    LAST_CHUNK_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    context_id: str
    artifact: Artifact
    append: bool
    last_chunk: bool
    metadata: _struct_pb2.Struct

    def __init__(self, task_id: _Optional[str]=..., context_id: _Optional[str]=..., artifact: _Optional[_Union[Artifact, _Mapping]]=..., append: _Optional[bool]=..., last_chunk: _Optional[bool]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `TaskArtifactUpdateEvent.__init__`

Source lines 178–178.

```python
def __init__(self, task_id: _Optional[str]=..., context_id: _Optional[str]=..., artifact: _Optional[_Union[Artifact, _Mapping]]=..., append: _Optional[bool]=..., last_chunk: _Optional[bool]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `PushNotificationConfig`

Source lines 180–190.

```python
class PushNotificationConfig(_message.Message):
    __slots__ = ('id', 'url', 'token', 'authentication')
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    token: str
    authentication: AuthenticationInfo

    def __init__(self, id: _Optional[str]=..., url: _Optional[str]=..., token: _Optional[str]=..., authentication: _Optional[_Union[AuthenticationInfo, _Mapping]]=...) -> None:
        ...
```

### PYI `PushNotificationConfig.__init__`

Source lines 190–190.

```python
def __init__(self, id: _Optional[str]=..., url: _Optional[str]=..., token: _Optional[str]=..., authentication: _Optional[_Union[AuthenticationInfo, _Mapping]]=...) -> None:
    ...
```

### PYI `AuthenticationInfo`

Source lines 192–198.

```python
class AuthenticationInfo(_message.Message):
    __slots__ = ('schemes', 'credentials')
    SCHEMES_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    schemes: _containers.RepeatedScalarFieldContainer[str]
    credentials: str

    def __init__(self, schemes: _Optional[_Iterable[str]]=..., credentials: _Optional[str]=...) -> None:
        ...
```

### PYI `AuthenticationInfo.__init__`

Source lines 198–198.

```python
def __init__(self, schemes: _Optional[_Iterable[str]]=..., credentials: _Optional[str]=...) -> None:
    ...
```

### PYI `AgentInterface`

Source lines 200–206.

```python
class AgentInterface(_message.Message):
    __slots__ = ('url', 'transport')
    URL_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    url: str
    transport: str

    def __init__(self, url: _Optional[str]=..., transport: _Optional[str]=...) -> None:
        ...
```

### PYI `AgentInterface.__init__`

Source lines 206–206.

```python
def __init__(self, url: _Optional[str]=..., transport: _Optional[str]=...) -> None:
    ...
```

### PYI `AgentCard`

Source lines 208–253.

```python
class AgentCard(_message.Message):
    __slots__ = ('protocol_version', 'name', 'description', 'url', 'preferred_transport', 'additional_interfaces', 'provider', 'version', 'documentation_url', 'capabilities', 'security_schemes', 'security', 'default_input_modes', 'default_output_modes', 'skills', 'supports_authenticated_extended_card', 'signatures', 'icon_url')

    class SecuritySchemesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SecurityScheme

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[SecurityScheme, _Mapping]]=...) -> None:
            ...
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_URL_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_SCHEMES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_OUTPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    SKILLS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_AUTHENTICATED_EXTENDED_CARD_FIELD_NUMBER: _ClassVar[int]
    SIGNATURES_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    protocol_version: str
    name: str
    description: str
    url: str
    preferred_transport: str
    additional_interfaces: _containers.RepeatedCompositeFieldContainer[AgentInterface]
    provider: AgentProvider
    version: str
    documentation_url: str
    capabilities: AgentCapabilities
    security_schemes: _containers.MessageMap[str, SecurityScheme]
    security: _containers.RepeatedCompositeFieldContainer[Security]
    default_input_modes: _containers.RepeatedScalarFieldContainer[str]
    default_output_modes: _containers.RepeatedScalarFieldContainer[str]
    skills: _containers.RepeatedCompositeFieldContainer[AgentSkill]
    supports_authenticated_extended_card: bool
    signatures: _containers.RepeatedCompositeFieldContainer[AgentCardSignature]
    icon_url: str

    def __init__(self, protocol_version: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., url: _Optional[str]=..., preferred_transport: _Optional[str]=..., additional_interfaces: _Optional[_Iterable[_Union[AgentInterface, _Mapping]]]=..., provider: _Optional[_Union[AgentProvider, _Mapping]]=..., version: _Optional[str]=..., documentation_url: _Optional[str]=..., capabilities: _Optional[_Union[AgentCapabilities, _Mapping]]=..., security_schemes: _Optional[_Mapping[str, SecurityScheme]]=..., security: _Optional[_Iterable[_Union[Security, _Mapping]]]=..., default_input_modes: _Optional[_Iterable[str]]=..., default_output_modes: _Optional[_Iterable[str]]=..., skills: _Optional[_Iterable[_Union[AgentSkill, _Mapping]]]=..., supports_authenticated_extended_card: _Optional[bool]=..., signatures: _Optional[_Iterable[_Union[AgentCardSignature, _Mapping]]]=..., icon_url: _Optional[str]=...) -> None:
        ...
```

### PYI `AgentCard.SecuritySchemesEntry`

Source lines 210–216.

```python
class SecuritySchemesEntry(_message.Message):
    __slots__ = ('key', 'value')
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: SecurityScheme

    def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[SecurityScheme, _Mapping]]=...) -> None:
        ...
```

### PYI `AgentCard.SecuritySchemesEntry.__init__`

Source lines 216–216.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[SecurityScheme, _Mapping]]=...) -> None:
    ...
```

### PYI `AgentCard.__init__`

Source lines 253–253.

```python
def __init__(self, protocol_version: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., url: _Optional[str]=..., preferred_transport: _Optional[str]=..., additional_interfaces: _Optional[_Iterable[_Union[AgentInterface, _Mapping]]]=..., provider: _Optional[_Union[AgentProvider, _Mapping]]=..., version: _Optional[str]=..., documentation_url: _Optional[str]=..., capabilities: _Optional[_Union[AgentCapabilities, _Mapping]]=..., security_schemes: _Optional[_Mapping[str, SecurityScheme]]=..., security: _Optional[_Iterable[_Union[Security, _Mapping]]]=..., default_input_modes: _Optional[_Iterable[str]]=..., default_output_modes: _Optional[_Iterable[str]]=..., skills: _Optional[_Iterable[_Union[AgentSkill, _Mapping]]]=..., supports_authenticated_extended_card: _Optional[bool]=..., signatures: _Optional[_Iterable[_Union[AgentCardSignature, _Mapping]]]=..., icon_url: _Optional[str]=...) -> None:
    ...
```

### PYI `AgentProvider`

Source lines 255–261.

```python
class AgentProvider(_message.Message):
    __slots__ = ('url', 'organization')
    URL_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    url: str
    organization: str

    def __init__(self, url: _Optional[str]=..., organization: _Optional[str]=...) -> None:
        ...
```

### PYI `AgentProvider.__init__`

Source lines 261–261.

```python
def __init__(self, url: _Optional[str]=..., organization: _Optional[str]=...) -> None:
    ...
```

### PYI `AgentCapabilities`

Source lines 263–271.

```python
class AgentCapabilities(_message.Message):
    __slots__ = ('streaming', 'push_notifications', 'extensions')
    STREAMING_FIELD_NUMBER: _ClassVar[int]
    PUSH_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    streaming: bool
    push_notifications: bool
    extensions: _containers.RepeatedCompositeFieldContainer[AgentExtension]

    def __init__(self, streaming: _Optional[bool]=..., push_notifications: _Optional[bool]=..., extensions: _Optional[_Iterable[_Union[AgentExtension, _Mapping]]]=...) -> None:
        ...
```

### PYI `AgentCapabilities.__init__`

Source lines 271–271.

```python
def __init__(self, streaming: _Optional[bool]=..., push_notifications: _Optional[bool]=..., extensions: _Optional[_Iterable[_Union[AgentExtension, _Mapping]]]=...) -> None:
    ...
```

### PYI `AgentExtension`

Source lines 273–283.

```python
class AgentExtension(_message.Message):
    __slots__ = ('uri', 'description', 'required', 'params')
    URI_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    description: str
    required: bool
    params: _struct_pb2.Struct

    def __init__(self, uri: _Optional[str]=..., description: _Optional[str]=..., required: _Optional[bool]=..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `AgentExtension.__init__`

Source lines 283–283.

```python
def __init__(self, uri: _Optional[str]=..., description: _Optional[str]=..., required: _Optional[bool]=..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `AgentSkill`

Source lines 285–303.

```python
class AgentSkill(_message.Message):
    __slots__ = ('id', 'name', 'description', 'tags', 'examples', 'input_modes', 'output_modes', 'security')
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    INPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    examples: _containers.RepeatedScalarFieldContainer[str]
    input_modes: _containers.RepeatedScalarFieldContainer[str]
    output_modes: _containers.RepeatedScalarFieldContainer[str]
    security: _containers.RepeatedCompositeFieldContainer[Security]

    def __init__(self, id: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., tags: _Optional[_Iterable[str]]=..., examples: _Optional[_Iterable[str]]=..., input_modes: _Optional[_Iterable[str]]=..., output_modes: _Optional[_Iterable[str]]=..., security: _Optional[_Iterable[_Union[Security, _Mapping]]]=...) -> None:
        ...
```

### PYI `AgentSkill.__init__`

Source lines 303–303.

```python
def __init__(self, id: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., tags: _Optional[_Iterable[str]]=..., examples: _Optional[_Iterable[str]]=..., input_modes: _Optional[_Iterable[str]]=..., output_modes: _Optional[_Iterable[str]]=..., security: _Optional[_Iterable[_Union[Security, _Mapping]]]=...) -> None:
    ...
```

### PYI `AgentCardSignature`

Source lines 305–313.

```python
class AgentCardSignature(_message.Message):
    __slots__ = ('protected', 'signature', 'header')
    PROTECTED_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    protected: str
    signature: str
    header: _struct_pb2.Struct

    def __init__(self, protected: _Optional[str]=..., signature: _Optional[str]=..., header: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `AgentCardSignature.__init__`

Source lines 313–313.

```python
def __init__(self, protected: _Optional[str]=..., signature: _Optional[str]=..., header: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `TaskPushNotificationConfig`

Source lines 315–321.

```python
class TaskPushNotificationConfig(_message.Message):
    __slots__ = ('name', 'push_notification_config')
    NAME_FIELD_NUMBER: _ClassVar[int]
    PUSH_NOTIFICATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    push_notification_config: PushNotificationConfig

    def __init__(self, name: _Optional[str]=..., push_notification_config: _Optional[_Union[PushNotificationConfig, _Mapping]]=...) -> None:
        ...
```

### PYI `TaskPushNotificationConfig.__init__`

Source lines 321–321.

```python
def __init__(self, name: _Optional[str]=..., push_notification_config: _Optional[_Union[PushNotificationConfig, _Mapping]]=...) -> None:
    ...
```

### PYI `StringList`

Source lines 323–327.

```python
class StringList(_message.Message):
    __slots__ = ('list',)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, list: _Optional[_Iterable[str]]=...) -> None:
        ...
```

### PYI `StringList.__init__`

Source lines 327–327.

```python
def __init__(self, list: _Optional[_Iterable[str]]=...) -> None:
    ...
```

### PYI `Security`

Source lines 329–340.

```python
class Security(_message.Message):
    __slots__ = ('schemes',)

    class SchemesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StringList

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[StringList, _Mapping]]=...) -> None:
            ...
    SCHEMES_FIELD_NUMBER: _ClassVar[int]
    schemes: _containers.MessageMap[str, StringList]

    def __init__(self, schemes: _Optional[_Mapping[str, StringList]]=...) -> None:
        ...
```

### PYI `Security.SchemesEntry`

Source lines 331–337.

```python
class SchemesEntry(_message.Message):
    __slots__ = ('key', 'value')
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: StringList

    def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[StringList, _Mapping]]=...) -> None:
        ...
```

### PYI `Security.SchemesEntry.__init__`

Source lines 337–337.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[StringList, _Mapping]]=...) -> None:
    ...
```

### PYI `Security.__init__`

Source lines 340–340.

```python
def __init__(self, schemes: _Optional[_Mapping[str, StringList]]=...) -> None:
    ...
```

### PYI `SecurityScheme`

Source lines 342–354.

```python
class SecurityScheme(_message.Message):
    __slots__ = ('api_key_security_scheme', 'http_auth_security_scheme', 'oauth2_security_scheme', 'open_id_connect_security_scheme', 'mtls_security_scheme')
    API_KEY_SECURITY_SCHEME_FIELD_NUMBER: _ClassVar[int]
    HTTP_AUTH_SECURITY_SCHEME_FIELD_NUMBER: _ClassVar[int]
    OAUTH2_SECURITY_SCHEME_FIELD_NUMBER: _ClassVar[int]
    OPEN_ID_CONNECT_SECURITY_SCHEME_FIELD_NUMBER: _ClassVar[int]
    MTLS_SECURITY_SCHEME_FIELD_NUMBER: _ClassVar[int]
    api_key_security_scheme: APIKeySecurityScheme
    http_auth_security_scheme: HTTPAuthSecurityScheme
    oauth2_security_scheme: OAuth2SecurityScheme
    open_id_connect_security_scheme: OpenIdConnectSecurityScheme
    mtls_security_scheme: MutualTlsSecurityScheme

    def __init__(self, api_key_security_scheme: _Optional[_Union[APIKeySecurityScheme, _Mapping]]=..., http_auth_security_scheme: _Optional[_Union[HTTPAuthSecurityScheme, _Mapping]]=..., oauth2_security_scheme: _Optional[_Union[OAuth2SecurityScheme, _Mapping]]=..., open_id_connect_security_scheme: _Optional[_Union[OpenIdConnectSecurityScheme, _Mapping]]=..., mtls_security_scheme: _Optional[_Union[MutualTlsSecurityScheme, _Mapping]]=...) -> None:
        ...
```

### PYI `SecurityScheme.__init__`

Source lines 354–354.

```python
def __init__(self, api_key_security_scheme: _Optional[_Union[APIKeySecurityScheme, _Mapping]]=..., http_auth_security_scheme: _Optional[_Union[HTTPAuthSecurityScheme, _Mapping]]=..., oauth2_security_scheme: _Optional[_Union[OAuth2SecurityScheme, _Mapping]]=..., open_id_connect_security_scheme: _Optional[_Union[OpenIdConnectSecurityScheme, _Mapping]]=..., mtls_security_scheme: _Optional[_Union[MutualTlsSecurityScheme, _Mapping]]=...) -> None:
    ...
```

### PYI `APIKeySecurityScheme`

Source lines 356–364.

```python
class APIKeySecurityScheme(_message.Message):
    __slots__ = ('description', 'location', 'name')
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    description: str
    location: str
    name: str

    def __init__(self, description: _Optional[str]=..., location: _Optional[str]=..., name: _Optional[str]=...) -> None:
        ...
```

### PYI `APIKeySecurityScheme.__init__`

Source lines 364–364.

```python
def __init__(self, description: _Optional[str]=..., location: _Optional[str]=..., name: _Optional[str]=...) -> None:
    ...
```

### PYI `HTTPAuthSecurityScheme`

Source lines 366–374.

```python
class HTTPAuthSecurityScheme(_message.Message):
    __slots__ = ('description', 'scheme', 'bearer_format')
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    BEARER_FORMAT_FIELD_NUMBER: _ClassVar[int]
    description: str
    scheme: str
    bearer_format: str

    def __init__(self, description: _Optional[str]=..., scheme: _Optional[str]=..., bearer_format: _Optional[str]=...) -> None:
        ...
```

### PYI `HTTPAuthSecurityScheme.__init__`

Source lines 374–374.

```python
def __init__(self, description: _Optional[str]=..., scheme: _Optional[str]=..., bearer_format: _Optional[str]=...) -> None:
    ...
```

### PYI `OAuth2SecurityScheme`

Source lines 376–384.

```python
class OAuth2SecurityScheme(_message.Message):
    __slots__ = ('description', 'flows', 'oauth2_metadata_url')
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLOWS_FIELD_NUMBER: _ClassVar[int]
    OAUTH2_METADATA_URL_FIELD_NUMBER: _ClassVar[int]
    description: str
    flows: OAuthFlows
    oauth2_metadata_url: str

    def __init__(self, description: _Optional[str]=..., flows: _Optional[_Union[OAuthFlows, _Mapping]]=..., oauth2_metadata_url: _Optional[str]=...) -> None:
        ...
```

### PYI `OAuth2SecurityScheme.__init__`

Source lines 384–384.

```python
def __init__(self, description: _Optional[str]=..., flows: _Optional[_Union[OAuthFlows, _Mapping]]=..., oauth2_metadata_url: _Optional[str]=...) -> None:
    ...
```

### PYI `OpenIdConnectSecurityScheme`

Source lines 386–392.

```python
class OpenIdConnectSecurityScheme(_message.Message):
    __slots__ = ('description', 'open_id_connect_url')
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OPEN_ID_CONNECT_URL_FIELD_NUMBER: _ClassVar[int]
    description: str
    open_id_connect_url: str

    def __init__(self, description: _Optional[str]=..., open_id_connect_url: _Optional[str]=...) -> None:
        ...
```

### PYI `OpenIdConnectSecurityScheme.__init__`

Source lines 392–392.

```python
def __init__(self, description: _Optional[str]=..., open_id_connect_url: _Optional[str]=...) -> None:
    ...
```

### PYI `MutualTlsSecurityScheme`

Source lines 394–398.

```python
class MutualTlsSecurityScheme(_message.Message):
    __slots__ = ('description',)
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: str

    def __init__(self, description: _Optional[str]=...) -> None:
        ...
```

### PYI `MutualTlsSecurityScheme.__init__`

Source lines 398–398.

```python
def __init__(self, description: _Optional[str]=...) -> None:
    ...
```

### PYI `OAuthFlows`

Source lines 400–410.

```python
class OAuthFlows(_message.Message):
    __slots__ = ('authorization_code', 'client_credentials', 'implicit', 'password')
    AUTHORIZATION_CODE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    IMPLICIT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    authorization_code: AuthorizationCodeOAuthFlow
    client_credentials: ClientCredentialsOAuthFlow
    implicit: ImplicitOAuthFlow
    password: PasswordOAuthFlow

    def __init__(self, authorization_code: _Optional[_Union[AuthorizationCodeOAuthFlow, _Mapping]]=..., client_credentials: _Optional[_Union[ClientCredentialsOAuthFlow, _Mapping]]=..., implicit: _Optional[_Union[ImplicitOAuthFlow, _Mapping]]=..., password: _Optional[_Union[PasswordOAuthFlow, _Mapping]]=...) -> None:
        ...
```

### PYI `OAuthFlows.__init__`

Source lines 410–410.

```python
def __init__(self, authorization_code: _Optional[_Union[AuthorizationCodeOAuthFlow, _Mapping]]=..., client_credentials: _Optional[_Union[ClientCredentialsOAuthFlow, _Mapping]]=..., implicit: _Optional[_Union[ImplicitOAuthFlow, _Mapping]]=..., password: _Optional[_Union[PasswordOAuthFlow, _Mapping]]=...) -> None:
    ...
```

### PYI `AuthorizationCodeOAuthFlow`

Source lines 412–429.

```python
class AuthorizationCodeOAuthFlow(_message.Message):
    __slots__ = ('authorization_url', 'token_url', 'refresh_url', 'scopes')

    class ScopesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URL_FIELD_NUMBER: _ClassVar[int]
    REFRESH_URL_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    authorization_url: str
    token_url: str
    refresh_url: str
    scopes: _containers.ScalarMap[str, str]

    def __init__(self, authorization_url: _Optional[str]=..., token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
        ...
```

### PYI `AuthorizationCodeOAuthFlow.ScopesEntry`

Source lines 414–420.

```python
class ScopesEntry(_message.Message):
    __slots__ = ('key', 'value')
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str

    def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
        ...
```

### PYI `AuthorizationCodeOAuthFlow.ScopesEntry.__init__`

Source lines 420–420.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### PYI `AuthorizationCodeOAuthFlow.__init__`

Source lines 429–429.

```python
def __init__(self, authorization_url: _Optional[str]=..., token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### PYI `ClientCredentialsOAuthFlow`

Source lines 431–446.

```python
class ClientCredentialsOAuthFlow(_message.Message):
    __slots__ = ('token_url', 'refresh_url', 'scopes')

    class ScopesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    TOKEN_URL_FIELD_NUMBER: _ClassVar[int]
    REFRESH_URL_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    token_url: str
    refresh_url: str
    scopes: _containers.ScalarMap[str, str]

    def __init__(self, token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
        ...
```

### PYI `ClientCredentialsOAuthFlow.ScopesEntry`

Source lines 433–439.

```python
class ScopesEntry(_message.Message):
    __slots__ = ('key', 'value')
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str

    def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
        ...
```

### PYI `ClientCredentialsOAuthFlow.ScopesEntry.__init__`

Source lines 439–439.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### PYI `ClientCredentialsOAuthFlow.__init__`

Source lines 446–446.

```python
def __init__(self, token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### PYI `ImplicitOAuthFlow`

Source lines 448–463.

```python
class ImplicitOAuthFlow(_message.Message):
    __slots__ = ('authorization_url', 'refresh_url', 'scopes')

    class ScopesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    REFRESH_URL_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    authorization_url: str
    refresh_url: str
    scopes: _containers.ScalarMap[str, str]

    def __init__(self, authorization_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
        ...
```

### PYI `ImplicitOAuthFlow.ScopesEntry`

Source lines 450–456.

```python
class ScopesEntry(_message.Message):
    __slots__ = ('key', 'value')
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str

    def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
        ...
```

### PYI `ImplicitOAuthFlow.ScopesEntry.__init__`

Source lines 456–456.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### PYI `ImplicitOAuthFlow.__init__`

Source lines 463–463.

```python
def __init__(self, authorization_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### PYI `PasswordOAuthFlow`

Source lines 465–480.

```python
class PasswordOAuthFlow(_message.Message):
    __slots__ = ('token_url', 'refresh_url', 'scopes')

    class ScopesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    TOKEN_URL_FIELD_NUMBER: _ClassVar[int]
    REFRESH_URL_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    token_url: str
    refresh_url: str
    scopes: _containers.ScalarMap[str, str]

    def __init__(self, token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
        ...
```

### PYI `PasswordOAuthFlow.ScopesEntry`

Source lines 467–473.

```python
class ScopesEntry(_message.Message):
    __slots__ = ('key', 'value')
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str

    def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
        ...
```

### PYI `PasswordOAuthFlow.ScopesEntry.__init__`

Source lines 473–473.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### PYI `PasswordOAuthFlow.__init__`

Source lines 480–480.

```python
def __init__(self, token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### PYI `SendMessageRequest`

Source lines 482–490.

```python
class SendMessageRequest(_message.Message):
    __slots__ = ('request', 'configuration', 'metadata')
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    request: Message
    configuration: SendMessageConfiguration
    metadata: _struct_pb2.Struct

    def __init__(self, request: _Optional[_Union[Message, _Mapping]]=..., configuration: _Optional[_Union[SendMessageConfiguration, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### PYI `SendMessageRequest.__init__`

Source lines 490–490.

```python
def __init__(self, request: _Optional[_Union[Message, _Mapping]]=..., configuration: _Optional[_Union[SendMessageConfiguration, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### PYI `GetTaskRequest`

Source lines 492–498.

```python
class GetTaskRequest(_message.Message):
    __slots__ = ('name', 'history_length')
    NAME_FIELD_NUMBER: _ClassVar[int]
    HISTORY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    name: str
    history_length: int

    def __init__(self, name: _Optional[str]=..., history_length: _Optional[int]=...) -> None:
        ...
```

### PYI `GetTaskRequest.__init__`

Source lines 498–498.

```python
def __init__(self, name: _Optional[str]=..., history_length: _Optional[int]=...) -> None:
    ...
```

### PYI `CancelTaskRequest`

Source lines 500–504.

```python
class CancelTaskRequest(_message.Message):
    __slots__ = ('name',)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str

    def __init__(self, name: _Optional[str]=...) -> None:
        ...
```

### PYI `CancelTaskRequest.__init__`

Source lines 504–504.

```python
def __init__(self, name: _Optional[str]=...) -> None:
    ...
```

### PYI `GetTaskPushNotificationConfigRequest`

Source lines 506–510.

```python
class GetTaskPushNotificationConfigRequest(_message.Message):
    __slots__ = ('name',)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str

    def __init__(self, name: _Optional[str]=...) -> None:
        ...
```

### PYI `GetTaskPushNotificationConfigRequest.__init__`

Source lines 510–510.

```python
def __init__(self, name: _Optional[str]=...) -> None:
    ...
```

### PYI `DeleteTaskPushNotificationConfigRequest`

Source lines 512–516.

```python
class DeleteTaskPushNotificationConfigRequest(_message.Message):
    __slots__ = ('name',)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str

    def __init__(self, name: _Optional[str]=...) -> None:
        ...
```

### PYI `DeleteTaskPushNotificationConfigRequest.__init__`

Source lines 516–516.

```python
def __init__(self, name: _Optional[str]=...) -> None:
    ...
```

### PYI `CreateTaskPushNotificationConfigRequest`

Source lines 518–526.

```python
class CreateTaskPushNotificationConfigRequest(_message.Message):
    __slots__ = ('parent', 'config_id', 'config')
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    parent: str
    config_id: str
    config: TaskPushNotificationConfig

    def __init__(self, parent: _Optional[str]=..., config_id: _Optional[str]=..., config: _Optional[_Union[TaskPushNotificationConfig, _Mapping]]=...) -> None:
        ...
```

### PYI `CreateTaskPushNotificationConfigRequest.__init__`

Source lines 526–526.

```python
def __init__(self, parent: _Optional[str]=..., config_id: _Optional[str]=..., config: _Optional[_Union[TaskPushNotificationConfig, _Mapping]]=...) -> None:
    ...
```

### PYI `TaskSubscriptionRequest`

Source lines 528–532.

```python
class TaskSubscriptionRequest(_message.Message):
    __slots__ = ('name',)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str

    def __init__(self, name: _Optional[str]=...) -> None:
        ...
```

### PYI `TaskSubscriptionRequest.__init__`

Source lines 532–532.

```python
def __init__(self, name: _Optional[str]=...) -> None:
    ...
```

### PYI `ListTaskPushNotificationConfigRequest`

Source lines 534–542.

```python
class ListTaskPushNotificationConfigRequest(_message.Message):
    __slots__ = ('parent', 'page_size', 'page_token')
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str

    def __init__(self, parent: _Optional[str]=..., page_size: _Optional[int]=..., page_token: _Optional[str]=...) -> None:
        ...
```

### PYI `ListTaskPushNotificationConfigRequest.__init__`

Source lines 542–542.

```python
def __init__(self, parent: _Optional[str]=..., page_size: _Optional[int]=..., page_token: _Optional[str]=...) -> None:
    ...
```

### PYI `GetAgentCardRequest`

Source lines 544–546.

```python
class GetAgentCardRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...
```

### PYI `GetAgentCardRequest.__init__`

Source lines 546–546.

```python
def __init__(self) -> None:
    ...
```

### PYI `SendMessageResponse`

Source lines 548–554.

```python
class SendMessageResponse(_message.Message):
    __slots__ = ('task', 'msg')
    TASK_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    task: Task
    msg: Message

    def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., msg: _Optional[_Union[Message, _Mapping]]=...) -> None:
        ...
```

### PYI `SendMessageResponse.__init__`

Source lines 554–554.

```python
def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., msg: _Optional[_Union[Message, _Mapping]]=...) -> None:
    ...
```

### PYI `StreamResponse`

Source lines 556–566.

```python
class StreamResponse(_message.Message):
    __slots__ = ('task', 'msg', 'status_update', 'artifact_update')
    TASK_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    STATUS_UPDATE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_UPDATE_FIELD_NUMBER: _ClassVar[int]
    task: Task
    msg: Message
    status_update: TaskStatusUpdateEvent
    artifact_update: TaskArtifactUpdateEvent

    def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., msg: _Optional[_Union[Message, _Mapping]]=..., status_update: _Optional[_Union[TaskStatusUpdateEvent, _Mapping]]=..., artifact_update: _Optional[_Union[TaskArtifactUpdateEvent, _Mapping]]=...) -> None:
        ...
```

### PYI `StreamResponse.__init__`

Source lines 566–566.

```python
def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., msg: _Optional[_Union[Message, _Mapping]]=..., status_update: _Optional[_Union[TaskStatusUpdateEvent, _Mapping]]=..., artifact_update: _Optional[_Union[TaskArtifactUpdateEvent, _Mapping]]=...) -> None:
    ...
```

### PYI `ListTaskPushNotificationConfigResponse`

Source lines 568–574.

```python
class ListTaskPushNotificationConfigResponse(_message.Message):
    __slots__ = ('configs', 'next_page_token')
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[TaskPushNotificationConfig]
    next_page_token: str

    def __init__(self, configs: _Optional[_Iterable[_Union[TaskPushNotificationConfig, _Mapping]]]=..., next_page_token: _Optional[str]=...) -> None:
        ...
```

### PYI `ListTaskPushNotificationConfigResponse.__init__`

Source lines 574–574.

```python
def __init__(self, configs: _Optional[_Iterable[_Union[TaskPushNotificationConfig, _Mapping]]]=..., next_page_token: _Optional[str]=...) -> None:
    ...
```

## Runtime protobuf descriptor catalog

File `a2a_v0_3.proto`, package `a2a.v1`. Dependencies: `google/api/annotations.proto`, `google/api/client.proto`, `google/api/field_behavior.proto`, `google/protobuf/empty.proto`, `google/protobuf/struct.proto`, `google/protobuf/timestamp.proto`.

### Descriptor `a2a.v1.SendMessageConfiguration`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| accepted_output_modes | 1 | string | True | acceptedOutputModes | — | False | — |
| push_notification | 2 | a2a.v1.PushNotificationConfig | False | pushNotification | — | True | — |
| history_length | 3 | int32 | False | historyLength | — | False | — |
| blocking | 4 | bool | False | blocking | — | False | — |

### Descriptor `a2a.v1.Task`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| id | 1 | string | False | id | — | False | — |
| context_id | 2 | string | False | contextId | — | False | — |
| status | 3 | a2a.v1.TaskStatus | False | status | — | True | — |
| artifacts | 4 | a2a.v1.Artifact | True | artifacts | — | False | — |
| history | 5 | a2a.v1.Message | True | history | — | False | — |
| metadata | 6 | google.protobuf.Struct | False | metadata | — | True | — |

### Descriptor `a2a.v1.TaskStatus`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| state | 1 | a2a.v1.TaskState | False | state | — | False | — |
| update | 2 | a2a.v1.Message | False | message | — | True | — |
| timestamp | 3 | google.protobuf.Timestamp | False | timestamp | — | True | — |

### Descriptor `a2a.v1.Part`

Map-entry: `False`. Oneofs: `part`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| text | 1 | string | False | text | part | True | — |
| file | 2 | a2a.v1.FilePart | False | file | part | True | — |
| data | 3 | a2a.v1.DataPart | False | data | part | True | — |
| metadata | 4 | google.protobuf.Struct | False | metadata | — | True | — |

### Descriptor `a2a.v1.FilePart`

Map-entry: `False`. Oneofs: `file`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| file_with_uri | 1 | string | False | fileWithUri | file | True | — |
| file_with_bytes | 2 | bytes | False | fileWithBytes | file | True | — |
| mime_type | 3 | string | False | mimeType | — | False | — |
| name | 4 | string | False | name | — | False | — |

### Descriptor `a2a.v1.DataPart`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| data | 1 | google.protobuf.Struct | False | data | — | True | — |

### Descriptor `a2a.v1.Message`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| message_id | 1 | string | False | messageId | — | False | — |
| context_id | 2 | string | False | contextId | — | False | — |
| task_id | 3 | string | False | taskId | — | False | — |
| role | 4 | a2a.v1.Role | False | role | — | False | — |
| content | 5 | a2a.v1.Part | True | content | — | False | — |
| metadata | 6 | google.protobuf.Struct | False | metadata | — | True | — |
| extensions | 7 | string | True | extensions | — | False | — |

### Descriptor `a2a.v1.Artifact`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| artifact_id | 1 | string | False | artifactId | — | False | — |
| name | 3 | string | False | name | — | False | — |
| description | 4 | string | False | description | — | False | — |
| parts | 5 | a2a.v1.Part | True | parts | — | False | — |
| metadata | 6 | google.protobuf.Struct | False | metadata | — | True | — |
| extensions | 7 | string | True | extensions | — | False | — |

### Descriptor `a2a.v1.TaskStatusUpdateEvent`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| task_id | 1 | string | False | taskId | — | False | — |
| context_id | 2 | string | False | contextId | — | False | — |
| status | 3 | a2a.v1.TaskStatus | False | status | — | True | — |
| final | 4 | bool | False | final | — | False | — |
| metadata | 5 | google.protobuf.Struct | False | metadata | — | True | — |

### Descriptor `a2a.v1.TaskArtifactUpdateEvent`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| task_id | 1 | string | False | taskId | — | False | — |
| context_id | 2 | string | False | contextId | — | False | — |
| artifact | 3 | a2a.v1.Artifact | False | artifact | — | True | — |
| append | 4 | bool | False | append | — | False | — |
| last_chunk | 5 | bool | False | lastChunk | — | False | — |
| metadata | 6 | google.protobuf.Struct | False | metadata | — | True | — |

### Descriptor `a2a.v1.PushNotificationConfig`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| id | 1 | string | False | id | — | False | — |
| url | 2 | string | False | url | — | False | — |
| token | 3 | string | False | token | — | False | — |
| authentication | 4 | a2a.v1.AuthenticationInfo | False | authentication | — | True | — |

### Descriptor `a2a.v1.AuthenticationInfo`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| schemes | 1 | string | True | schemes | — | False | — |
| credentials | 2 | string | False | credentials | — | False | — |

### Descriptor `a2a.v1.AgentInterface`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| url | 1 | string | False | url | — | False | — |
| transport | 2 | string | False | transport | — | False | — |

### Descriptor `a2a.v1.AgentCard`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| protocol_version | 16 | string | False | protocolVersion | — | False | — |
| name | 1 | string | False | name | — | False | — |
| description | 2 | string | False | description | — | False | — |
| url | 3 | string | False | url | — | False | — |
| preferred_transport | 14 | string | False | preferredTransport | — | False | — |
| additional_interfaces | 15 | a2a.v1.AgentInterface | True | additionalInterfaces | — | False | — |
| provider | 4 | a2a.v1.AgentProvider | False | provider | — | True | — |
| version | 5 | string | False | version | — | False | — |
| documentation_url | 6 | string | False | documentationUrl | — | False | — |
| capabilities | 7 | a2a.v1.AgentCapabilities | False | capabilities | — | True | — |
| security_schemes | 8 | a2a.v1.AgentCard.SecuritySchemesEntry | True | securitySchemes | — | False | — |
| security | 9 | a2a.v1.Security | True | security | — | False | — |
| default_input_modes | 10 | string | True | defaultInputModes | — | False | — |
| default_output_modes | 11 | string | True | defaultOutputModes | — | False | — |
| skills | 12 | a2a.v1.AgentSkill | True | skills | — | False | — |
| supports_authenticated_extended_card | 13 | bool | False | supportsAuthenticatedExtendedCard | — | False | — |
| signatures | 17 | a2a.v1.AgentCardSignature | True | signatures | — | False | — |
| icon_url | 18 | string | False | iconUrl | — | False | — |

### Descriptor `a2a.v1.AgentCard.SecuritySchemesEntry`

Map-entry: `True`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| key | 1 | string | False | key | — | False | — |
| value | 2 | a2a.v1.SecurityScheme | False | value | — | True | — |

### Descriptor `a2a.v1.AgentProvider`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| url | 1 | string | False | url | — | False | — |
| organization | 2 | string | False | organization | — | False | — |

### Descriptor `a2a.v1.AgentCapabilities`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| streaming | 1 | bool | False | streaming | — | False | — |
| push_notifications | 2 | bool | False | pushNotifications | — | False | — |
| extensions | 3 | a2a.v1.AgentExtension | True | extensions | — | False | — |

### Descriptor `a2a.v1.AgentExtension`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| uri | 1 | string | False | uri | — | False | — |
| description | 2 | string | False | description | — | False | — |
| required | 3 | bool | False | required | — | False | — |
| params | 4 | google.protobuf.Struct | False | params | — | True | — |

### Descriptor `a2a.v1.AgentSkill`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| id | 1 | string | False | id | — | False | — |
| name | 2 | string | False | name | — | False | — |
| description | 3 | string | False | description | — | False | — |
| tags | 4 | string | True | tags | — | False | — |
| examples | 5 | string | True | examples | — | False | — |
| input_modes | 6 | string | True | inputModes | — | False | — |
| output_modes | 7 | string | True | outputModes | — | False | — |
| security | 8 | a2a.v1.Security | True | security | — | False | — |

### Descriptor `a2a.v1.AgentCardSignature`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| protected | 1 | string | False | protected | — | False | [google.api.field_behavior]: REQUIRED |
| signature | 2 | string | False | signature | — | False | [google.api.field_behavior]: REQUIRED |
| header | 3 | google.protobuf.Struct | False | header | — | True | — |

### Descriptor `a2a.v1.TaskPushNotificationConfig`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| name | 1 | string | False | name | — | False | — |
| push_notification_config | 2 | a2a.v1.PushNotificationConfig | False | pushNotificationConfig | — | True | — |

### Descriptor `a2a.v1.StringList`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| list | 1 | string | True | list | — | False | — |

### Descriptor `a2a.v1.Security`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| schemes | 1 | a2a.v1.Security.SchemesEntry | True | schemes | — | False | — |

### Descriptor `a2a.v1.Security.SchemesEntry`

Map-entry: `True`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| key | 1 | string | False | key | — | False | — |
| value | 2 | a2a.v1.StringList | False | value | — | True | — |

### Descriptor `a2a.v1.SecurityScheme`

Map-entry: `False`. Oneofs: `scheme`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| api_key_security_scheme | 1 | a2a.v1.APIKeySecurityScheme | False | apiKeySecurityScheme | scheme | True | — |
| http_auth_security_scheme | 2 | a2a.v1.HTTPAuthSecurityScheme | False | httpAuthSecurityScheme | scheme | True | — |
| oauth2_security_scheme | 3 | a2a.v1.OAuth2SecurityScheme | False | oauth2SecurityScheme | scheme | True | — |
| open_id_connect_security_scheme | 4 | a2a.v1.OpenIdConnectSecurityScheme | False | openIdConnectSecurityScheme | scheme | True | — |
| mtls_security_scheme | 5 | a2a.v1.MutualTlsSecurityScheme | False | mtlsSecurityScheme | scheme | True | — |

### Descriptor `a2a.v1.APIKeySecurityScheme`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| description | 1 | string | False | description | — | False | — |
| location | 2 | string | False | location | — | False | — |
| name | 3 | string | False | name | — | False | — |

### Descriptor `a2a.v1.HTTPAuthSecurityScheme`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| description | 1 | string | False | description | — | False | — |
| scheme | 2 | string | False | scheme | — | False | — |
| bearer_format | 3 | string | False | bearerFormat | — | False | — |

### Descriptor `a2a.v1.OAuth2SecurityScheme`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| description | 1 | string | False | description | — | False | — |
| flows | 2 | a2a.v1.OAuthFlows | False | flows | — | True | — |
| oauth2_metadata_url | 3 | string | False | oauth2MetadataUrl | — | False | — |

### Descriptor `a2a.v1.OpenIdConnectSecurityScheme`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| description | 1 | string | False | description | — | False | — |
| open_id_connect_url | 2 | string | False | openIdConnectUrl | — | False | — |

### Descriptor `a2a.v1.MutualTlsSecurityScheme`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| description | 1 | string | False | description | — | False | — |

### Descriptor `a2a.v1.OAuthFlows`

Map-entry: `False`. Oneofs: `flow`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| authorization_code | 1 | a2a.v1.AuthorizationCodeOAuthFlow | False | authorizationCode | flow | True | — |
| client_credentials | 2 | a2a.v1.ClientCredentialsOAuthFlow | False | clientCredentials | flow | True | — |
| implicit | 3 | a2a.v1.ImplicitOAuthFlow | False | implicit | flow | True | — |
| password | 4 | a2a.v1.PasswordOAuthFlow | False | password | flow | True | — |

### Descriptor `a2a.v1.AuthorizationCodeOAuthFlow`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| authorization_url | 1 | string | False | authorizationUrl | — | False | — |
| token_url | 2 | string | False | tokenUrl | — | False | — |
| refresh_url | 3 | string | False | refreshUrl | — | False | — |
| scopes | 4 | a2a.v1.AuthorizationCodeOAuthFlow.ScopesEntry | True | scopes | — | False | — |

### Descriptor `a2a.v1.AuthorizationCodeOAuthFlow.ScopesEntry`

Map-entry: `True`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| key | 1 | string | False | key | — | False | — |
| value | 2 | string | False | value | — | False | — |

### Descriptor `a2a.v1.ClientCredentialsOAuthFlow`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| token_url | 1 | string | False | tokenUrl | — | False | — |
| refresh_url | 2 | string | False | refreshUrl | — | False | — |
| scopes | 3 | a2a.v1.ClientCredentialsOAuthFlow.ScopesEntry | True | scopes | — | False | — |

### Descriptor `a2a.v1.ClientCredentialsOAuthFlow.ScopesEntry`

Map-entry: `True`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| key | 1 | string | False | key | — | False | — |
| value | 2 | string | False | value | — | False | — |

### Descriptor `a2a.v1.ImplicitOAuthFlow`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| authorization_url | 1 | string | False | authorizationUrl | — | False | — |
| refresh_url | 2 | string | False | refreshUrl | — | False | — |
| scopes | 3 | a2a.v1.ImplicitOAuthFlow.ScopesEntry | True | scopes | — | False | — |

### Descriptor `a2a.v1.ImplicitOAuthFlow.ScopesEntry`

Map-entry: `True`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| key | 1 | string | False | key | — | False | — |
| value | 2 | string | False | value | — | False | — |

### Descriptor `a2a.v1.PasswordOAuthFlow`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| token_url | 1 | string | False | tokenUrl | — | False | — |
| refresh_url | 2 | string | False | refreshUrl | — | False | — |
| scopes | 3 | a2a.v1.PasswordOAuthFlow.ScopesEntry | True | scopes | — | False | — |

### Descriptor `a2a.v1.PasswordOAuthFlow.ScopesEntry`

Map-entry: `True`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| key | 1 | string | False | key | — | False | — |
| value | 2 | string | False | value | — | False | — |

### Descriptor `a2a.v1.SendMessageRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| request | 1 | a2a.v1.Message | False | message | — | True | [google.api.field_behavior]: REQUIRED |
| configuration | 2 | a2a.v1.SendMessageConfiguration | False | configuration | — | True | — |
| metadata | 3 | google.protobuf.Struct | False | metadata | — | True | — |

### Descriptor `a2a.v1.GetTaskRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| name | 1 | string | False | name | — | False | [google.api.field_behavior]: REQUIRED |
| history_length | 2 | int32 | False | historyLength | — | False | — |

### Descriptor `a2a.v1.CancelTaskRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| name | 1 | string | False | name | — | False | — |

### Descriptor `a2a.v1.GetTaskPushNotificationConfigRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| name | 1 | string | False | name | — | False | — |

### Descriptor `a2a.v1.DeleteTaskPushNotificationConfigRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| name | 1 | string | False | name | — | False | — |

### Descriptor `a2a.v1.CreateTaskPushNotificationConfigRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| parent | 1 | string | False | parent | — | False | [google.api.field_behavior]: REQUIRED |
| config_id | 2 | string | False | configId | — | False | [google.api.field_behavior]: REQUIRED |
| config | 3 | a2a.v1.TaskPushNotificationConfig | False | config | — | True | [google.api.field_behavior]: REQUIRED |

### Descriptor `a2a.v1.TaskSubscriptionRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| name | 1 | string | False | name | — | False | — |

### Descriptor `a2a.v1.ListTaskPushNotificationConfigRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| parent | 1 | string | False | parent | — | False | — |
| page_size | 2 | int32 | False | pageSize | — | False | — |
| page_token | 3 | string | False | pageToken | — | False | — |

### Descriptor `a2a.v1.GetAgentCardRequest`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|

### Descriptor `a2a.v1.SendMessageResponse`

Map-entry: `False`. Oneofs: `payload`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| task | 1 | a2a.v1.Task | False | task | payload | True | — |
| msg | 2 | a2a.v1.Message | False | message | payload | True | — |

### Descriptor `a2a.v1.StreamResponse`

Map-entry: `False`. Oneofs: `payload`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| task | 1 | a2a.v1.Task | False | task | payload | True | — |
| msg | 2 | a2a.v1.Message | False | message | payload | True | — |
| status_update | 3 | a2a.v1.TaskStatusUpdateEvent | False | statusUpdate | payload | True | — |
| artifact_update | 4 | a2a.v1.TaskArtifactUpdateEvent | False | artifactUpdate | payload | True | — |

### Descriptor `a2a.v1.ListTaskPushNotificationConfigResponse`

Map-entry: `False`. Oneofs: `none`. Constructor and field access use protobuf runtime; no network/persistence.

| Field | # | Wire type | Repeated | JSON name | Oneof | Presence | Options |
|---|---|---|---|---|---|---|---|
| configs | 1 | a2a.v1.TaskPushNotificationConfig | True | configs | — | False | — |
| next_page_token | 2 | string | False | nextPageToken | — | False | — |

### Enum `a2a.v1.TaskState`

`TASK_STATE_UNSPECIFIED=0`, `TASK_STATE_SUBMITTED=1`, `TASK_STATE_WORKING=2`, `TASK_STATE_COMPLETED=3`, `TASK_STATE_FAILED=4`, `TASK_STATE_CANCELLED=5`, `TASK_STATE_INPUT_REQUIRED=6`, `TASK_STATE_REJECTED=7`, `TASK_STATE_AUTH_REQUIRED=8`.

### Enum `a2a.v1.Role`

`ROLE_UNSPECIFIED=0`, `ROLE_USER=1`, `ROLE_AGENT=2`.

### Runtime service methods and generated bound stub attributes

| RPC / stub attribute | Input | Output | Server-streaming | HTTP annotation |
|---|---|---|---|---|
| SendMessage | a2a.v1.SendMessageRequest | a2a.v1.SendMessageResponse | False | post: "/v1/message:send" body: "*" |
| SendStreamingMessage | a2a.v1.SendMessageRequest | a2a.v1.StreamResponse | True | post: "/v1/message:stream" body: "*" |
| GetTask | a2a.v1.GetTaskRequest | a2a.v1.Task | False | get: "/v1/{name=tasks/*}" |
| CancelTask | a2a.v1.CancelTaskRequest | a2a.v1.Task | False | post: "/v1/{name=tasks/*}:cancel" body: "*" |
| TaskSubscription | a2a.v1.TaskSubscriptionRequest | a2a.v1.StreamResponse | True | get: "/v1/{name=tasks/*}:subscribe" |
| CreateTaskPushNotificationConfig | a2a.v1.CreateTaskPushNotificationConfigRequest | a2a.v1.TaskPushNotificationConfig | False | post: "/v1/{parent=tasks/*/pushNotificationConfigs}" body: "config" |
| GetTaskPushNotificationConfig | a2a.v1.GetTaskPushNotificationConfigRequest | a2a.v1.TaskPushNotificationConfig | False | get: "/v1/{name=tasks/*/pushNotificationConfigs/*}" |
| ListTaskPushNotificationConfig | a2a.v1.ListTaskPushNotificationConfigRequest | a2a.v1.ListTaskPushNotificationConfigResponse | False | get: "/v1/{parent=tasks/*}/pushNotificationConfigs" |
| GetAgentCard | a2a.v1.GetAgentCardRequest | a2a.v1.AgentCard | False | get: "/v1/card" |
| DeleteTaskPushNotificationConfig | a2a.v1.DeleteTaskPushNotificationConfigRequest | google.protobuf.Empty | False | delete: "/v1/{name=tasks/*/pushNotificationConfigs/*}" |

## Module-level generated execution evidence

Serialized blob is decoded into the catalog above; remaining import/build/options operations are retained here.

```python
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: a2a_v0_3.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'a2a_v0_3.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2



_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'a2a_v0_3_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\ncom.a2a.v1B\013A2aV03ProtoP\001Z\030google.golang.org/a2a/v1\242\002\003AXX\252\002\006A2a.V1\312\002\006A2a\\V1\342\002\022A2a\\V1\\GPBMetadata\352\002\007A2a::V1'
  _globals['_AGENTCARD_SECURITYSCHEMESENTRY']._loaded_options = None
  _globals['_AGENTCARD_SECURITYSCHEMESENTRY']._serialized_options = b'8\001'
  _globals['_AGENTCARDSIGNATURE'].fields_by_name['protected']._loaded_options = None
  _globals['_AGENTCARDSIGNATURE'].fields_by_name['protected']._serialized_options = b'\340A\002'
  _globals['_AGENTCARDSIGNATURE'].fields_by_name['signature']._loaded_options = None
  _globals['_AGENTCARDSIGNATURE'].fields_by_name['signature']._serialized_options = b'\340A\002'
  _globals['_SECURITY_SCHEMESENTRY']._loaded_options = None
  _globals['_SECURITY_SCHEMESENTRY']._serialized_options = b'8\001'
  _globals['_AUTHORIZATIONCODEOAUTHFLOW_SCOPESENTRY']._loaded_options = None
  _globals['_AUTHORIZATIONCODEOAUTHFLOW_SCOPESENTRY']._serialized_options = b'8\001'
  _globals['_CLIENTCREDENTIALSOAUTHFLOW_SCOPESENTRY']._loaded_options = None
  _globals['_CLIENTCREDENTIALSOAUTHFLOW_SCOPESENTRY']._serialized_options = b'8\001'
  _globals['_IMPLICITOAUTHFLOW_SCOPESENTRY']._loaded_options = None
  _globals['_IMPLICITOAUTHFLOW_SCOPESENTRY']._serialized_options = b'8\001'
  _globals['_PASSWORDOAUTHFLOW_SCOPESENTRY']._loaded_options = None
  _globals['_PASSWORDOAUTHFLOW_SCOPESENTRY']._serialized_options = b'8\001'
  _globals['_SENDMESSAGEREQUEST'].fields_by_name['request']._loaded_options = None
  _globals['_SENDMESSAGEREQUEST'].fields_by_name['request']._serialized_options = b'\340A\002'
  _globals['_GETTASKREQUEST'].fields_by_name['name']._loaded_options = None
  _globals['_GETTASKREQUEST'].fields_by_name['name']._serialized_options = b'\340A\002'
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST'].fields_by_name['parent']._loaded_options = None
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST'].fields_by_name['parent']._serialized_options = b'\340A\002'
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST'].fields_by_name['config_id']._loaded_options = None
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST'].fields_by_name['config_id']._serialized_options = b'\340A\002'
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST'].fields_by_name['config']._loaded_options = None
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST'].fields_by_name['config']._serialized_options = b'\340A\002'
  _globals['_A2ASERVICE'].methods_by_name['SendMessage']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['SendMessage']._serialized_options = b'\202\323\344\223\002\025\"\020/v1/message:send:\001*'
  _globals['_A2ASERVICE'].methods_by_name['SendStreamingMessage']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['SendStreamingMessage']._serialized_options = b'\202\323\344\223\002\027\"\022/v1/message:stream:\001*'
  _globals['_A2ASERVICE'].methods_by_name['GetTask']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['GetTask']._serialized_options = b'\332A\004name\202\323\344\223\002\024\022\022/v1/{name=tasks/*}'
  _globals['_A2ASERVICE'].methods_by_name['CancelTask']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['CancelTask']._serialized_options = b'\202\323\344\223\002\036\"\031/v1/{name=tasks/*}:cancel:\001*'
  _globals['_A2ASERVICE'].methods_by_name['TaskSubscription']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['TaskSubscription']._serialized_options = b'\202\323\344\223\002\036\022\034/v1/{name=tasks/*}:subscribe'
  _globals['_A2ASERVICE'].methods_by_name['CreateTaskPushNotificationConfig']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['CreateTaskPushNotificationConfig']._serialized_options = b'\332A\rparent,config\202\323\344\223\0026\",/v1/{parent=tasks/*/pushNotificationConfigs}:\006config'
  _globals['_A2ASERVICE'].methods_by_name['GetTaskPushNotificationConfig']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['GetTaskPushNotificationConfig']._serialized_options = b'\332A\004name\202\323\344\223\002.\022,/v1/{name=tasks/*/pushNotificationConfigs/*}'
  _globals['_A2ASERVICE'].methods_by_name['ListTaskPushNotificationConfig']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['ListTaskPushNotificationConfig']._serialized_options = b'\332A\006parent\202\323\344\223\002.\022,/v1/{parent=tasks/*}/pushNotificationConfigs'
  _globals['_A2ASERVICE'].methods_by_name['GetAgentCard']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['GetAgentCard']._serialized_options = b'\202\323\344\223\002\n\022\010/v1/card'
  _globals['_A2ASERVICE'].methods_by_name['DeleteTaskPushNotificationConfig']._loaded_options = None
  _globals['_A2ASERVICE'].methods_by_name['DeleteTaskPushNotificationConfig']._serialized_options = b'\332A\004name\202\323\344\223\002.*,/v1/{name=tasks/*/pushNotificationConfigs/*}'
  _globals['_TASKSTATE']._serialized_start=8071
  _globals['_TASKSTATE']._serialized_end=8321
  _globals['_ROLE']._serialized_start=8323
  _globals['_ROLE']._serialized_end=8382
  _globals['_SENDMESSAGECONFIGURATION']._serialized_start=207
  _globals['_SENDMESSAGECONFIGURATION']._serialized_end=429
  _globals['_TASK']._serialized_start=432
  _globals['_TASK']._serialized_end=673
  _globals['_TASKSTATUS']._serialized_start=676
  _globals['_TASKSTATUS']._serialized_end=829
  _globals['_PART']._serialized_start=832
  _globals['_PART']._serialized_end=1001
  _globals['_FILEPART']._serialized_start=1004
  _globals['_FILEPART']._serialized_end=1151
  _globals['_DATAPART']._serialized_start=1153
  _globals['_DATAPART']._serialized_end=1208
  _globals['_MESSAGE']._serialized_start=1211
  _globals['_MESSAGE']._serialized_end=1466
  _globals['_ARTIFACT']._serialized_start=1469
  _globals['_ARTIFACT']._serialized_end=1687
  _globals['_TASKSTATUSUPDATEEVENT']._serialized_start=1690
  _globals['_TASKSTATUSUPDATEEVENT']._serialized_end=1888
  _globals['_TASKARTIFACTUPDATEEVENT']._serialized_start=1891
  _globals['_TASKARTIFACTUPDATEEVENT']._serialized_end=2126
  _globals['_PUSHNOTIFICATIONCONFIG']._serialized_start=2129
  _globals['_PUSHNOTIFICATIONCONFIG']._serialized_end=2277
  _globals['_AUTHENTICATIONINFO']._serialized_start=2279
  _globals['_AUTHENTICATIONINFO']._serialized_end=2359
  _globals['_AGENTINTERFACE']._serialized_start=2361
  _globals['_AGENTINTERFACE']._serialized_end=2425
  _globals['_AGENTCARD']._serialized_start=2428
  _globals['_AGENTCARD']._serialized_end=3396
  _globals['_AGENTCARD_SECURITYSCHEMESENTRY']._serialized_start=3306
  _globals['_AGENTCARD_SECURITYSCHEMESENTRY']._serialized_end=3396
  _globals['_AGENTPROVIDER']._serialized_start=3398
  _globals['_AGENTPROVIDER']._serialized_end=3467
  _globals['_AGENTCAPABILITIES']._serialized_start=3470
  _globals['_AGENTCAPABILITIES']._serialized_end=3622
  _globals['_AGENTEXTENSION']._serialized_start=3625
  _globals['_AGENTEXTENSION']._serialized_end=3770
  _globals['_AGENTSKILL']._serialized_start=3773
  _globals['_AGENTSKILL']._serialized_end=4017
  _globals['_AGENTCARDSIGNATURE']._serialized_start=4020
  _globals['_AGENTCARDSIGNATURE']._serialized_end=4159
  _globals['_TASKPUSHNOTIFICATIONCONFIG']._serialized_start=4162
  _globals['_TASKPUSHNOTIFICATIONCONFIG']._serialized_end=4300
  _globals['_STRINGLIST']._serialized_start=4302
  _globals['_STRINGLIST']._serialized_end=4334
  _globals['_SECURITY']._serialized_start=4337
  _globals['_SECURITY']._serialized_end=4484
  _globals['_SECURITY_SCHEMESENTRY']._serialized_start=4406
  _globals['_SECURITY_SCHEMESENTRY']._serialized_end=4484
  _globals['_SECURITYSCHEME']._serialized_start=4487
  _globals['_SECURITYSCHEME']._serialized_end=4973
  _globals['_APIKEYSECURITYSCHEME']._serialized_start=4975
  _globals['_APIKEYSECURITYSCHEME']._serialized_end=5079
  _globals['_HTTPAUTHSECURITYSCHEME']._serialized_start=5081
  _globals['_HTTPAUTHSECURITYSCHEME']._serialized_end=5200
  _globals['_OAUTH2SECURITYSCHEME']._serialized_start=5203
  _globals['_OAUTH2SECURITYSCHEME']._serialized_end=5349
  _globals['_OPENIDCONNECTSECURITYSCHEME']._serialized_start=5351
  _globals['_OPENIDCONNECTSECURITYSCHEME']._serialized_end=5461
  _globals['_MUTUALTLSSECURITYSCHEME']._serialized_start=5463
  _globals['_MUTUALTLSSECURITYSCHEME']._serialized_end=5522
  _globals['_OAUTHFLOWS']._serialized_start=5525
  _globals['_OAUTHFLOWS']._serialized_end=5829
  _globals['_AUTHORIZATIONCODEOAUTHFLOW']._serialized_start=5832
  _globals['_AUTHORIZATIONCODEOAUTHFLOW']._serialized_end=6098
  _globals['_AUTHORIZATIONCODEOAUTHFLOW_SCOPESENTRY']._serialized_start=6041
  _globals['_AUTHORIZATIONCODEOAUTHFLOW_SCOPESENTRY']._serialized_end=6098
  _globals['_CLIENTCREDENTIALSOAUTHFLOW']._serialized_start=6101
  _globals['_CLIENTCREDENTIALSOAUTHFLOW']._serialized_end=6322
  _globals['_CLIENTCREDENTIALSOAUTHFLOW_SCOPESENTRY']._serialized_start=6041
  _globals['_CLIENTCREDENTIALSOAUTHFLOW_SCOPESENTRY']._serialized_end=6098
  _globals['_IMPLICITOAUTHFLOW']._serialized_start=6325
  _globals['_IMPLICITOAUTHFLOW']._serialized_end=6544
  _globals['_IMPLICITOAUTHFLOW_SCOPESENTRY']._serialized_start=6041
  _globals['_IMPLICITOAUTHFLOW_SCOPESENTRY']._serialized_end=6098
  _globals['_PASSWORDOAUTHFLOW']._serialized_start=6547
  _globals['_PASSWORDOAUTHFLOW']._serialized_end=6750
  _globals['_PASSWORDOAUTHFLOW_SCOPESENTRY']._serialized_start=6041
  _globals['_PASSWORDOAUTHFLOW_SCOPESENTRY']._serialized_end=6098
  _globals['_SENDMESSAGEREQUEST']._serialized_start=6753
  _globals['_SENDMESSAGEREQUEST']._serialized_end=6946
  _globals['_GETTASKREQUEST']._serialized_start=6948
  _globals['_GETTASKREQUEST']._serialized_end=7028
  _globals['_CANCELTASKREQUEST']._serialized_start=7030
  _globals['_CANCELTASKREQUEST']._serialized_end=7069
  _globals['_GETTASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_start=7071
  _globals['_GETTASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_end=7129
  _globals['_DELETETASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_start=7131
  _globals['_DELETETASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_end=7192
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_start=7195
  _globals['_CREATETASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_end=7364
  _globals['_TASKSUBSCRIPTIONREQUEST']._serialized_start=7366
  _globals['_TASKSUBSCRIPTIONREQUEST']._serialized_end=7411
  _globals['_LISTTASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_start=7413
  _globals['_LISTTASKPUSHNOTIFICATIONCONFIGREQUEST']._serialized_end=7536
  _globals['_GETAGENTCARDREQUEST']._serialized_start=7538
  _globals['_GETAGENTCARDREQUEST']._serialized_end=7559
  _globals['_SENDMESSAGERESPONSE']._serialized_start=7561
  _globals['_SENDMESSAGERESPONSE']._serialized_end=7670
  _globals['_STREAMRESPONSE']._serialized_start=7673
  _globals['_STREAMRESPONSE']._serialized_end=7923
  _globals['_LISTTASKPUSHNOTIFICATIONCONFIGRESPONSE']._serialized_start=7926
  _globals['_LISTTASKPUSHNOTIFICATIONCONFIGRESPONSE']._serialized_end=8068
  _globals['_A2ASERVICE']._serialized_start=8385
  _globals['_A2ASERVICE']._serialized_end=9724
# @@protoc_insertion_point(module_scope)
```
