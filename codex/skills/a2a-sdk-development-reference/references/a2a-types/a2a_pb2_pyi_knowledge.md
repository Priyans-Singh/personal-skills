# `types/a2a_pb2.pyi` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/types/a2a_pb2.pyi`. SHA-256: `9043d39968ee701c636142ad9474e1306f14a2b8f635d45a35565af3ffa1e13c`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import datetime
from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
```

Static type surface, not runtime execution. Every AST class and constructor is enumerated below with fully qualified scope and source line, preserving repeated ScopesEntry/key/value names across enclosing models. __slots__, field-number constants, and annotated container/union types are evidence of fields. Constructor bodies are ellipsis: real validation/storage is generated protobuf runtime. See a2a_pb2 field catalog for exact wire numbers, presence, required options, and oneofs.

## Public/constants/type aliases and module initialization

```python
DESCRIPTOR: _descriptor.FileDescriptor
```

```python
TASK_STATE_UNSPECIFIED: TaskState
```

```python
TASK_STATE_SUBMITTED: TaskState
```

```python
TASK_STATE_WORKING: TaskState
```

```python
TASK_STATE_COMPLETED: TaskState
```

```python
TASK_STATE_FAILED: TaskState
```

```python
TASK_STATE_CANCELED: TaskState
```

```python
TASK_STATE_INPUT_REQUIRED: TaskState
```

```python
TASK_STATE_REJECTED: TaskState
```

```python
TASK_STATE_AUTH_REQUIRED: TaskState
```

```python
ROLE_UNSPECIFIED: Role
```

```python
ROLE_USER: Role
```

```python
ROLE_AGENT: Role
```

## Declarations and execution

### `TaskState` (line 18)

Coverage ID: `a2a_pb2.pyi:18:TaskState`.

Generated enum type or nested map-entry support.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class TaskState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_STATE_UNSPECIFIED: _ClassVar[TaskState]
    TASK_STATE_SUBMITTED: _ClassVar[TaskState]
    TASK_STATE_WORKING: _ClassVar[TaskState]
    TASK_STATE_COMPLETED: _ClassVar[TaskState]
    TASK_STATE_FAILED: _ClassVar[TaskState]
    TASK_STATE_CANCELED: _ClassVar[TaskState]
    TASK_STATE_INPUT_REQUIRED: _ClassVar[TaskState]
    TASK_STATE_REJECTED: _ClassVar[TaskState]
    TASK_STATE_AUTH_REQUIRED: _ClassVar[TaskState]
```

### `Role` (line 30)

Coverage ID: `a2a_pb2.pyi:30:Role`.

Generated enum type or nested map-entry support.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLE_UNSPECIFIED: _ClassVar[Role]
    ROLE_USER: _ClassVar[Role]
    ROLE_AGENT: _ClassVar[Role]
```

### `SendMessageConfiguration` (line 48)

Coverage ID: `a2a_pb2.pyi:48:SendMessageConfiguration`.

Execution hints attached to send requests: output MIME preferences, push configuration, optional history limit, immediate-return flag. No scheduling is performed here.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class SendMessageConfiguration(_message.Message):
    __slots__ = ('accepted_output_modes', 'task_push_notification_config', 'history_length', 'return_immediately')
    ACCEPTED_OUTPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    TASK_PUSH_NOTIFICATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    HISTORY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    RETURN_IMMEDIATELY_FIELD_NUMBER: _ClassVar[int]
    accepted_output_modes: _containers.RepeatedScalarFieldContainer[str]
    task_push_notification_config: TaskPushNotificationConfig
    history_length: int
    return_immediately: bool

    def __init__(self, accepted_output_modes: _Optional[_Iterable[str]]=..., task_push_notification_config: _Optional[_Union[TaskPushNotificationConfig, _Mapping]]=..., history_length: _Optional[int]=..., return_immediately: _Optional[bool]=...) -> None:
        ...
```

### `SendMessageConfiguration.__init__` (line 58)

Coverage ID: `a2a_pb2.pyi:58:SendMessageConfiguration.__init__`.

Execution hints attached to send requests: output MIME preferences, push configuration, optional history limit, immediate-return flag. No scheduling is performed here.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, accepted_output_modes: _Optional[_Iterable[str]]=..., task_push_notification_config: _Optional[_Union[TaskPushNotificationConfig, _Mapping]]=..., history_length: _Optional[int]=..., return_immediately: _Optional[bool]=...) -> None:
    ...
```

### `Task` (line 60)

Coverage ID: `a2a_pb2.pyi:60:Task`.

Task resource snapshot: id identifies task; context_id groups conversation; status is current state; artifacts are outputs and history is messages. Mutating snapshot does not update a task store.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `Task.__init__` (line 74)

Coverage ID: `a2a_pb2.pyi:74:Task.__init__`.

Task resource snapshot: id identifies task; context_id groups conversation; status is current state; artifacts are outputs and history is messages. Mutating snapshot does not update a task store.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, id: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskStatus, _Mapping]]=..., artifacts: _Optional[_Iterable[_Union[Artifact, _Mapping]]]=..., history: _Optional[_Iterable[_Union[Message, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### `TaskStatus` (line 76)

Coverage ID: `a2a_pb2.pyi:76:TaskStatus`.

State plus optional agent/user message and protobuf Timestamp. Enum assignment is not a state-machine transition.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class TaskStatus(_message.Message):
    __slots__ = ('state', 'message', 'timestamp')
    STATE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    state: TaskState
    message: Message
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, state: _Optional[_Union[TaskState, str]]=..., message: _Optional[_Union[Message, _Mapping]]=..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...
```

### `TaskStatus.__init__` (line 84)

Coverage ID: `a2a_pb2.pyi:84:TaskStatus.__init__`.

State plus optional agent/user message and protobuf Timestamp. Enum assignment is not a state-machine transition.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, state: _Optional[_Union[TaskState, str]]=..., message: _Optional[_Union[Message, _Mapping]]=..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
    ...
```

### `Part` (line 86)

Coverage ID: `a2a_pb2.pyi:86:Part`.

One content alternative: text, raw bytes, URL reference, or arbitrary protobuf Value; metadata/filename/media_type annotate it. URL construction does not fetch content.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class Part(_message.Message):
    __slots__ = ('text', 'raw', 'url', 'data', 'metadata', 'filename', 'media_type')
    TEXT_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MEDIA_TYPE_FIELD_NUMBER: _ClassVar[int]
    text: str
    raw: bytes
    url: str
    data: _struct_pb2.Value
    metadata: _struct_pb2.Struct
    filename: str
    media_type: str

    def __init__(self, text: _Optional[str]=..., raw: _Optional[bytes]=..., url: _Optional[str]=..., data: _Optional[_Union[_struct_pb2.Value, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., filename: _Optional[str]=..., media_type: _Optional[str]=...) -> None:
        ...
```

### `Part.__init__` (line 102)

Coverage ID: `a2a_pb2.pyi:102:Part.__init__`.

One content alternative: text, raw bytes, URL reference, or arbitrary protobuf Value; metadata/filename/media_type annotate it. URL construction does not fetch content.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, text: _Optional[str]=..., raw: _Optional[bytes]=..., url: _Optional[str]=..., data: _Optional[_Union[_struct_pb2.Value, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., filename: _Optional[str]=..., media_type: _Optional[str]=...) -> None:
    ...
```

### `Message` (line 104)

Coverage ID: `a2a_pb2.pyi:104:Message`.

Message identity, task/context linkage, role, required repeated Parts; metadata/extensions/reference task IDs carry context. IDs are supplied by caller, never generated here.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class Message(_message.Message):
    __slots__ = ('message_id', 'context_id', 'task_id', 'role', 'parts', 'metadata', 'extensions', 'reference_task_ids')
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_TASK_IDS_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    context_id: str
    task_id: str
    role: Role
    parts: _containers.RepeatedCompositeFieldContainer[Part]
    metadata: _struct_pb2.Struct
    extensions: _containers.RepeatedScalarFieldContainer[str]
    reference_task_ids: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, message_id: _Optional[str]=..., context_id: _Optional[str]=..., task_id: _Optional[str]=..., role: _Optional[_Union[Role, str]]=..., parts: _Optional[_Iterable[_Union[Part, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., extensions: _Optional[_Iterable[str]]=..., reference_task_ids: _Optional[_Iterable[str]]=...) -> None:
        ...
```

### `Message.__init__` (line 122)

Coverage ID: `a2a_pb2.pyi:122:Message.__init__`.

Message identity, task/context linkage, role, required repeated Parts; metadata/extensions/reference task IDs carry context. IDs are supplied by caller, never generated here.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, message_id: _Optional[str]=..., context_id: _Optional[str]=..., task_id: _Optional[str]=..., role: _Optional[_Union[Role, str]]=..., parts: _Optional[_Iterable[_Union[Part, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., extensions: _Optional[_Iterable[str]]=..., reference_task_ids: _Optional[_Iterable[str]]=...) -> None:
    ...
```

### `Artifact` (line 124)

Coverage ID: `a2a_pb2.pyi:124:Artifact`.

Output identified by artifact_id with required Parts and optional descriptive fields; no file write or remote object exists from construction.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `Artifact.__init__` (line 138)

Coverage ID: `a2a_pb2.pyi:138:Artifact.__init__`.

Output identified by artifact_id with required Parts and optional descriptive fields; no file write or remote object exists from construction.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, artifact_id: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., parts: _Optional[_Iterable[_Union[Part, _Mapping]]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=..., extensions: _Optional[_Iterable[str]]=...) -> None:
    ...
```

### `TaskStatusUpdateEvent` (line 140)

Coverage ID: `a2a_pb2.pyi:140:TaskStatusUpdateEvent`.

Task/context identity plus replacement status and metadata; no final flag in this version.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class TaskStatusUpdateEvent(_message.Message):
    __slots__ = ('task_id', 'context_id', 'status', 'metadata')
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    context_id: str
    status: TaskStatus
    metadata: _struct_pb2.Struct

    def __init__(self, task_id: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskStatus, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### `TaskStatusUpdateEvent.__init__` (line 150)

Coverage ID: `a2a_pb2.pyi:150:TaskStatusUpdateEvent.__init__`.

Task/context identity plus replacement status and metadata; no final flag in this version.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, task_id: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskStatus, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### `TaskArtifactUpdateEvent` (line 152)

Coverage ID: `a2a_pb2.pyi:152:TaskArtifactUpdateEvent`.

Task/context identity plus artifact and append/last_chunk flags. Consumer implements merge/assembly; generated class does not append to Task.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `TaskArtifactUpdateEvent.__init__` (line 166)

Coverage ID: `a2a_pb2.pyi:166:TaskArtifactUpdateEvent.__init__`.

Task/context identity plus artifact and append/last_chunk flags. Consumer implements merge/assembly; generated class does not append to Task.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, task_id: _Optional[str]=..., context_id: _Optional[str]=..., artifact: _Optional[_Union[Artifact, _Mapping]]=..., append: _Optional[bool]=..., last_chunk: _Optional[bool]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### `AuthenticationInfo` (line 168)

Coverage ID: `a2a_pb2.pyi:168:AuthenticationInfo`.

Callback authentication declaration with scheme and credentials string. Sensitive data may be serialized; no encryption, expiry, credential refresh, or authorization enforcement.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class AuthenticationInfo(_message.Message):
    __slots__ = ('scheme', 'credentials')
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    scheme: str
    credentials: str

    def __init__(self, scheme: _Optional[str]=..., credentials: _Optional[str]=...) -> None:
        ...
```

### `AuthenticationInfo.__init__` (line 174)

Coverage ID: `a2a_pb2.pyi:174:AuthenticationInfo.__init__`.

Callback authentication declaration with scheme and credentials string. Sensitive data may be serialized; no encryption, expiry, credential refresh, or authorization enforcement.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, scheme: _Optional[str]=..., credentials: _Optional[str]=...) -> None:
    ...
```

### `AgentInterface` (line 176)

Coverage ID: `a2a_pb2.pyi:176:AgentInterface`.

Agent endpoint URL plus binding, optional tenant and required protocol_version; discovery/routing data, not live connection.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class AgentInterface(_message.Message):
    __slots__ = ('url', 'protocol_binding', 'tenant', 'protocol_version')
    URL_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_BINDING_FIELD_NUMBER: _ClassVar[int]
    TENANT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    url: str
    protocol_binding: str
    tenant: str
    protocol_version: str

    def __init__(self, url: _Optional[str]=..., protocol_binding: _Optional[str]=..., tenant: _Optional[str]=..., protocol_version: _Optional[str]=...) -> None:
        ...
```

### `AgentInterface.__init__` (line 186)

Coverage ID: `a2a_pb2.pyi:186:AgentInterface.__init__`.

Agent endpoint URL plus binding, optional tenant and required protocol_version; discovery/routing data, not live connection.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, url: _Optional[str]=..., protocol_binding: _Optional[str]=..., tenant: _Optional[str]=..., protocol_version: _Optional[str]=...) -> None:
    ...
```

### `AgentCard` (line 188)

Coverage ID: `a2a_pb2.pyi:188:AgentCard`.

Discovery document with capabilities/interfaces/provider/skills/security definitions and signatures. version is agent version; interface protocol_version is distinct. No implicit endpoint probe.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class AgentCard(_message.Message):
    __slots__ = ('name', 'description', 'supported_interfaces', 'provider', 'version', 'documentation_url', 'capabilities', 'security_schemes', 'security_requirements', 'default_input_modes', 'default_output_modes', 'skills', 'signatures', 'icon_url')

    class SecuritySchemesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SecurityScheme

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[SecurityScheme, _Mapping]]=...) -> None:
            ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_URL_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_SCHEMES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_OUTPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    SKILLS_FIELD_NUMBER: _ClassVar[int]
    SIGNATURES_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    supported_interfaces: _containers.RepeatedCompositeFieldContainer[AgentInterface]
    provider: AgentProvider
    version: str
    documentation_url: str
    capabilities: AgentCapabilities
    security_schemes: _containers.MessageMap[str, SecurityScheme]
    security_requirements: _containers.RepeatedCompositeFieldContainer[SecurityRequirement]
    default_input_modes: _containers.RepeatedScalarFieldContainer[str]
    default_output_modes: _containers.RepeatedScalarFieldContainer[str]
    skills: _containers.RepeatedCompositeFieldContainer[AgentSkill]
    signatures: _containers.RepeatedCompositeFieldContainer[AgentCardSignature]
    icon_url: str

    def __init__(self, name: _Optional[str]=..., description: _Optional[str]=..., supported_interfaces: _Optional[_Iterable[_Union[AgentInterface, _Mapping]]]=..., provider: _Optional[_Union[AgentProvider, _Mapping]]=..., version: _Optional[str]=..., documentation_url: _Optional[str]=..., capabilities: _Optional[_Union[AgentCapabilities, _Mapping]]=..., security_schemes: _Optional[_Mapping[str, SecurityScheme]]=..., security_requirements: _Optional[_Iterable[_Union[SecurityRequirement, _Mapping]]]=..., default_input_modes: _Optional[_Iterable[str]]=..., default_output_modes: _Optional[_Iterable[str]]=..., skills: _Optional[_Iterable[_Union[AgentSkill, _Mapping]]]=..., signatures: _Optional[_Iterable[_Union[AgentCardSignature, _Mapping]]]=..., icon_url: _Optional[str]=...) -> None:
        ...
```

### `AgentCard.SecuritySchemesEntry` (line 190)

Coverage ID: `a2a_pb2.pyi:190:AgentCard.SecuritySchemesEntry`.

Discovery document with capabilities/interfaces/provider/skills/security definitions and signatures. version is agent version; interface protocol_version is distinct. No implicit endpoint probe.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `AgentCard.SecuritySchemesEntry.__init__` (line 196)

Coverage ID: `a2a_pb2.pyi:196:AgentCard.SecuritySchemesEntry.__init__`.

Discovery document with capabilities/interfaces/provider/skills/security definitions and signatures. version is agent version; interface protocol_version is distinct. No implicit endpoint probe.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[SecurityScheme, _Mapping]]=...) -> None:
    ...
```

### `AgentCard.__init__` (line 225)

Coverage ID: `a2a_pb2.pyi:225:AgentCard.__init__`.

Discovery document with capabilities/interfaces/provider/skills/security definitions and signatures. version is agent version; interface protocol_version is distinct. No implicit endpoint probe.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, name: _Optional[str]=..., description: _Optional[str]=..., supported_interfaces: _Optional[_Iterable[_Union[AgentInterface, _Mapping]]]=..., provider: _Optional[_Union[AgentProvider, _Mapping]]=..., version: _Optional[str]=..., documentation_url: _Optional[str]=..., capabilities: _Optional[_Union[AgentCapabilities, _Mapping]]=..., security_schemes: _Optional[_Mapping[str, SecurityScheme]]=..., security_requirements: _Optional[_Iterable[_Union[SecurityRequirement, _Mapping]]]=..., default_input_modes: _Optional[_Iterable[str]]=..., default_output_modes: _Optional[_Iterable[str]]=..., skills: _Optional[_Iterable[_Union[AgentSkill, _Mapping]]]=..., signatures: _Optional[_Iterable[_Union[AgentCardSignature, _Mapping]]]=..., icon_url: _Optional[str]=...) -> None:
    ...
```

### `AgentProvider` (line 227)

Coverage ID: `a2a_pb2.pyi:227:AgentProvider`.

Organization and URL identity metadata, not authenticated principal.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `AgentProvider.__init__` (line 233)

Coverage ID: `a2a_pb2.pyi:233:AgentProvider.__init__`.

Organization and URL identity metadata, not authenticated principal.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, url: _Optional[str]=..., organization: _Optional[str]=...) -> None:
    ...
```

### `AgentCapabilities` (line 235)

Coverage ID: `a2a_pb2.pyi:235:AgentCapabilities`.

Optional booleans distinguish absent from explicit false, plus extension declarations; no capability implementation is created.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class AgentCapabilities(_message.Message):
    __slots__ = ('streaming', 'push_notifications', 'extensions', 'extended_agent_card')
    STREAMING_FIELD_NUMBER: _ClassVar[int]
    PUSH_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_AGENT_CARD_FIELD_NUMBER: _ClassVar[int]
    streaming: bool
    push_notifications: bool
    extensions: _containers.RepeatedCompositeFieldContainer[AgentExtension]
    extended_agent_card: bool

    def __init__(self, streaming: _Optional[bool]=..., push_notifications: _Optional[bool]=..., extensions: _Optional[_Iterable[_Union[AgentExtension, _Mapping]]]=..., extended_agent_card: _Optional[bool]=...) -> None:
        ...
```

### `AgentCapabilities.__init__` (line 245)

Coverage ID: `a2a_pb2.pyi:245:AgentCapabilities.__init__`.

Optional booleans distinguish absent from explicit false, plus extension declarations; no capability implementation is created.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, streaming: _Optional[bool]=..., push_notifications: _Optional[bool]=..., extensions: _Optional[_Iterable[_Union[AgentExtension, _Mapping]]]=..., extended_agent_card: _Optional[bool]=...) -> None:
    ...
```

### `AgentExtension` (line 247)

Coverage ID: `a2a_pb2.pyi:247:AgentExtension`.

Extension URI/description/required flag plus arbitrary Struct parameters; untrusted params can nest and impact signing depth.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `AgentExtension.__init__` (line 257)

Coverage ID: `a2a_pb2.pyi:257:AgentExtension.__init__`.

Extension URI/description/required flag plus arbitrary Struct parameters; untrusted params can nest and impact signing depth.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, uri: _Optional[str]=..., description: _Optional[str]=..., required: _Optional[bool]=..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### `AgentSkill` (line 259)

Coverage ID: `a2a_pb2.pyi:259:AgentSkill`.

Skill identifier/documentation/tags/examples and optional MIME/security requirements. Generated class does not enforce selection or execute skill.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class AgentSkill(_message.Message):
    __slots__ = ('id', 'name', 'description', 'tags', 'examples', 'input_modes', 'output_modes', 'security_requirements')
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    INPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_MODES_FIELD_NUMBER: _ClassVar[int]
    SECURITY_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    examples: _containers.RepeatedScalarFieldContainer[str]
    input_modes: _containers.RepeatedScalarFieldContainer[str]
    output_modes: _containers.RepeatedScalarFieldContainer[str]
    security_requirements: _containers.RepeatedCompositeFieldContainer[SecurityRequirement]

    def __init__(self, id: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., tags: _Optional[_Iterable[str]]=..., examples: _Optional[_Iterable[str]]=..., input_modes: _Optional[_Iterable[str]]=..., output_modes: _Optional[_Iterable[str]]=..., security_requirements: _Optional[_Iterable[_Union[SecurityRequirement, _Mapping]]]=...) -> None:
        ...
```

### `AgentSkill.__init__` (line 277)

Coverage ID: `a2a_pb2.pyi:277:AgentSkill.__init__`.

Skill identifier/documentation/tags/examples and optional MIME/security requirements. Generated class does not enforce selection or execute skill.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, id: _Optional[str]=..., name: _Optional[str]=..., description: _Optional[str]=..., tags: _Optional[_Iterable[str]]=..., examples: _Optional[_Iterable[str]]=..., input_modes: _Optional[_Iterable[str]]=..., output_modes: _Optional[_Iterable[str]]=..., security_requirements: _Optional[_Iterable[_Union[SecurityRequirement, _Mapping]]]=...) -> None:
    ...
```

### `AgentCardSignature` (line 279)

Coverage ID: `a2a_pb2.pyi:279:AgentCardSignature`.

Detached JWS protected header and signature base64url strings, plus unprotected Struct header. Payload comes from canonicalized AgentCard without signatures.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `AgentCardSignature.__init__` (line 287)

Coverage ID: `a2a_pb2.pyi:287:AgentCardSignature.__init__`.

Detached JWS protected header and signature base64url strings, plus unprotected Struct header. Payload comes from canonicalized AgentCard without signatures.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, protected: _Optional[str]=..., signature: _Optional[str]=..., header: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### `TaskPushNotificationConfig` (line 289)

Coverage ID: `a2a_pb2.pyi:289:TaskPushNotificationConfig`.

Configuration resource keyed by tenant/task_id/id; callback url/token/authentication stored as proto values. Credentials/token destination is callback consumer/sender integration, not agent-card public security scheme. Model imposes no lifetime, revocation, persistence, or outbound HTTP.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class TaskPushNotificationConfig(_message.Message):
    __slots__ = ('tenant', 'id', 'task_id', 'url', 'token', 'authentication')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    id: str
    task_id: str
    url: str
    token: str
    authentication: AuthenticationInfo

    def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=..., task_id: _Optional[str]=..., url: _Optional[str]=..., token: _Optional[str]=..., authentication: _Optional[_Union[AuthenticationInfo, _Mapping]]=...) -> None:
        ...
```

### `TaskPushNotificationConfig.__init__` (line 303)

Coverage ID: `a2a_pb2.pyi:303:TaskPushNotificationConfig.__init__`.

Configuration resource keyed by tenant/task_id/id; callback url/token/authentication stored as proto values. Credentials/token destination is callback consumer/sender integration, not agent-card public security scheme. Model imposes no lifetime, revocation, persistence, or outbound HTTP.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=..., task_id: _Optional[str]=..., url: _Optional[str]=..., token: _Optional[str]=..., authentication: _Optional[_Union[AuthenticationInfo, _Mapping]]=...) -> None:
    ...
```

### `StringList` (line 305)

Coverage ID: `a2a_pb2.pyi:305:StringList`.

Repeated string wrapper enabling protobuf map values of scope lists.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class StringList(_message.Message):
    __slots__ = ('list',)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, list: _Optional[_Iterable[str]]=...) -> None:
        ...
```

### `StringList.__init__` (line 309)

Coverage ID: `a2a_pb2.pyi:309:StringList.__init__`.

Repeated string wrapper enabling protobuf map values of scope lists.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, list: _Optional[_Iterable[str]]=...) -> None:
    ...
```

### `SecurityRequirement` (line 311)

Coverage ID: `a2a_pb2.pyi:311:SecurityRequirement`.

Map security scheme names to StringList scope requirements. Schema data; no matching, AND/OR evaluation, credential acquisition, or enforcement occurs here.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class SecurityRequirement(_message.Message):
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

### `SecurityRequirement.SchemesEntry` (line 313)

Coverage ID: `a2a_pb2.pyi:313:SecurityRequirement.SchemesEntry`.

Map security scheme names to StringList scope requirements. Schema data; no matching, AND/OR evaluation, credential acquisition, or enforcement occurs here.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `SecurityRequirement.SchemesEntry.__init__` (line 319)

Coverage ID: `a2a_pb2.pyi:319:SecurityRequirement.SchemesEntry.__init__`.

Map security scheme names to StringList scope requirements. Schema data; no matching, AND/OR evaluation, credential acquisition, or enforcement occurs here.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[StringList, _Mapping]]=...) -> None:
    ...
```

### `SecurityRequirement.__init__` (line 322)

Coverage ID: `a2a_pb2.pyi:322:SecurityRequirement.__init__`.

Map security scheme names to StringList scope requirements. Schema data; no matching, AND/OR evaluation, credential acquisition, or enforcement occurs here.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, schemes: _Optional[_Mapping[str, StringList]]=...) -> None:
    ...
```

### `SecurityScheme` (line 324)

Coverage ID: `a2a_pb2.pyi:324:SecurityScheme`.

Oneof union of API key, HTTP auth, OAuth2, OIDC, mutual TLS definitions; switching scheme clears previous choice.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `SecurityScheme.__init__` (line 336)

Coverage ID: `a2a_pb2.pyi:336:SecurityScheme.__init__`.

Oneof union of API key, HTTP auth, OAuth2, OIDC, mutual TLS definitions; switching scheme clears previous choice.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, api_key_security_scheme: _Optional[_Union[APIKeySecurityScheme, _Mapping]]=..., http_auth_security_scheme: _Optional[_Union[HTTPAuthSecurityScheme, _Mapping]]=..., oauth2_security_scheme: _Optional[_Union[OAuth2SecurityScheme, _Mapping]]=..., open_id_connect_security_scheme: _Optional[_Union[OpenIdConnectSecurityScheme, _Mapping]]=..., mtls_security_scheme: _Optional[_Union[MutualTlsSecurityScheme, _Mapping]]=...) -> None:
    ...
```

### `APIKeySecurityScheme` (line 338)

Coverage ID: `a2a_pb2.pyi:338:APIKeySecurityScheme`.

API key description/location/name describes credential destination (header/query/cookie convention is consumer responsibility). Stores no actual key.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `APIKeySecurityScheme.__init__` (line 346)

Coverage ID: `a2a_pb2.pyi:346:APIKeySecurityScheme.__init__`.

API key description/location/name describes credential destination (header/query/cookie convention is consumer responsibility). Stores no actual key.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, description: _Optional[str]=..., location: _Optional[str]=..., name: _Optional[str]=...) -> None:
    ...
```

### `HTTPAuthSecurityScheme` (line 348)

Coverage ID: `a2a_pb2.pyi:348:HTTPAuthSecurityScheme`.

HTTP scheme and bearer-format hint; no bearer token acquisition/validation.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `HTTPAuthSecurityScheme.__init__` (line 356)

Coverage ID: `a2a_pb2.pyi:356:HTTPAuthSecurityScheme.__init__`.

HTTP scheme and bearer-format hint; no bearer token acquisition/validation.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, description: _Optional[str]=..., scheme: _Optional[str]=..., bearer_format: _Optional[str]=...) -> None:
    ...
```

### `OAuth2SecurityScheme` (line 358)

Coverage ID: `a2a_pb2.pyi:358:OAuth2SecurityScheme`.

OAuth flows and optional metadata URL; no discovery fetch or token exchange.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `OAuth2SecurityScheme.__init__` (line 366)

Coverage ID: `a2a_pb2.pyi:366:OAuth2SecurityScheme.__init__`.

OAuth flows and optional metadata URL; no discovery fetch or token exchange.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, description: _Optional[str]=..., flows: _Optional[_Union[OAuthFlows, _Mapping]]=..., oauth2_metadata_url: _Optional[str]=...) -> None:
    ...
```

### `OpenIdConnectSecurityScheme` (line 368)

Coverage ID: `a2a_pb2.pyi:368:OpenIdConnectSecurityScheme`.

Discovery URL metadata; no network request or ID-token validation.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `OpenIdConnectSecurityScheme.__init__` (line 374)

Coverage ID: `a2a_pb2.pyi:374:OpenIdConnectSecurityScheme.__init__`.

Discovery URL metadata; no network request or ID-token validation.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, description: _Optional[str]=..., open_id_connect_url: _Optional[str]=...) -> None:
    ...
```

### `MutualTlsSecurityScheme` (line 376)

Coverage ID: `a2a_pb2.pyi:376:MutualTlsSecurityScheme`.

mTLS description; no certificate/key or TLS configuration.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class MutualTlsSecurityScheme(_message.Message):
    __slots__ = ('description',)
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: str

    def __init__(self, description: _Optional[str]=...) -> None:
        ...
```

### `MutualTlsSecurityScheme.__init__` (line 380)

Coverage ID: `a2a_pb2.pyi:380:MutualTlsSecurityScheme.__init__`.

mTLS description; no certificate/key or TLS configuration.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, description: _Optional[str]=...) -> None:
    ...
```

### `OAuthFlows` (line 382)

Coverage ID: `a2a_pb2.pyi:382:OAuthFlows`.

Oneof flow: authorization_code, client_credentials, implicit, password, device_code. Unlike an arbitrary multi-flow mapping, only one can be selected at once. implicit/password descriptor fields are deprecated.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class OAuthFlows(_message.Message):
    __slots__ = ('authorization_code', 'client_credentials', 'implicit', 'password', 'device_code')
    AUTHORIZATION_CODE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    IMPLICIT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CODE_FIELD_NUMBER: _ClassVar[int]
    authorization_code: AuthorizationCodeOAuthFlow
    client_credentials: ClientCredentialsOAuthFlow
    implicit: ImplicitOAuthFlow
    password: PasswordOAuthFlow
    device_code: DeviceCodeOAuthFlow

    def __init__(self, authorization_code: _Optional[_Union[AuthorizationCodeOAuthFlow, _Mapping]]=..., client_credentials: _Optional[_Union[ClientCredentialsOAuthFlow, _Mapping]]=..., implicit: _Optional[_Union[ImplicitOAuthFlow, _Mapping]]=..., password: _Optional[_Union[PasswordOAuthFlow, _Mapping]]=..., device_code: _Optional[_Union[DeviceCodeOAuthFlow, _Mapping]]=...) -> None:
        ...
```

### `OAuthFlows.__init__` (line 394)

Coverage ID: `a2a_pb2.pyi:394:OAuthFlows.__init__`.

Oneof flow: authorization_code, client_credentials, implicit, password, device_code. Unlike an arbitrary multi-flow mapping, only one can be selected at once. implicit/password descriptor fields are deprecated.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, authorization_code: _Optional[_Union[AuthorizationCodeOAuthFlow, _Mapping]]=..., client_credentials: _Optional[_Union[ClientCredentialsOAuthFlow, _Mapping]]=..., implicit: _Optional[_Union[ImplicitOAuthFlow, _Mapping]]=..., password: _Optional[_Union[PasswordOAuthFlow, _Mapping]]=..., device_code: _Optional[_Union[DeviceCodeOAuthFlow, _Mapping]]=...) -> None:
    ...
```

### `AuthorizationCodeOAuthFlow` (line 396)

Coverage ID: `a2a_pb2.pyi:396:AuthorizationCodeOAuthFlow`.

Authorization/token/refresh endpoints, scope descriptions, PKCE-required flag. Describes token destinations, does not generate verifier/challenge or store tokens.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class AuthorizationCodeOAuthFlow(_message.Message):
    __slots__ = ('authorization_url', 'token_url', 'refresh_url', 'scopes', 'pkce_required')

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
    PKCE_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    authorization_url: str
    token_url: str
    refresh_url: str
    scopes: _containers.ScalarMap[str, str]
    pkce_required: bool

    def __init__(self, authorization_url: _Optional[str]=..., token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=..., pkce_required: _Optional[bool]=...) -> None:
        ...
```

### `AuthorizationCodeOAuthFlow.ScopesEntry` (line 398)

Coverage ID: `a2a_pb2.pyi:398:AuthorizationCodeOAuthFlow.ScopesEntry`.

Authorization/token/refresh endpoints, scope descriptions, PKCE-required flag. Describes token destinations, does not generate verifier/challenge or store tokens.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `AuthorizationCodeOAuthFlow.ScopesEntry.__init__` (line 404)

Coverage ID: `a2a_pb2.pyi:404:AuthorizationCodeOAuthFlow.ScopesEntry.__init__`.

Authorization/token/refresh endpoints, scope descriptions, PKCE-required flag. Describes token destinations, does not generate verifier/challenge or store tokens.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### `AuthorizationCodeOAuthFlow.__init__` (line 415)

Coverage ID: `a2a_pb2.pyi:415:AuthorizationCodeOAuthFlow.__init__`.

Authorization/token/refresh endpoints, scope descriptions, PKCE-required flag. Describes token destinations, does not generate verifier/challenge or store tokens.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, authorization_url: _Optional[str]=..., token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=..., pkce_required: _Optional[bool]=...) -> None:
    ...
```

### `ClientCredentialsOAuthFlow` (line 417)

Coverage ID: `a2a_pb2.pyi:417:ClientCredentialsOAuthFlow`.

Token/refresh endpoints and scope descriptions; no client secret storage or issuance.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `ClientCredentialsOAuthFlow.ScopesEntry` (line 419)

Coverage ID: `a2a_pb2.pyi:419:ClientCredentialsOAuthFlow.ScopesEntry`.

Token/refresh endpoints and scope descriptions; no client secret storage or issuance.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `ClientCredentialsOAuthFlow.ScopesEntry.__init__` (line 425)

Coverage ID: `a2a_pb2.pyi:425:ClientCredentialsOAuthFlow.ScopesEntry.__init__`.

Token/refresh endpoints and scope descriptions; no client secret storage or issuance.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### `ClientCredentialsOAuthFlow.__init__` (line 432)

Coverage ID: `a2a_pb2.pyi:432:ClientCredentialsOAuthFlow.__init__`.

Token/refresh endpoints and scope descriptions; no client secret storage or issuance.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### `ImplicitOAuthFlow` (line 434)

Coverage ID: `a2a_pb2.pyi:434:ImplicitOAuthFlow`.

Deprecated flow metadata; authorization/refresh URLs and scopes, no browser redirect.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `ImplicitOAuthFlow.ScopesEntry` (line 436)

Coverage ID: `a2a_pb2.pyi:436:ImplicitOAuthFlow.ScopesEntry`.

Deprecated flow metadata; authorization/refresh URLs and scopes, no browser redirect.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `ImplicitOAuthFlow.ScopesEntry.__init__` (line 442)

Coverage ID: `a2a_pb2.pyi:442:ImplicitOAuthFlow.ScopesEntry.__init__`.

Deprecated flow metadata; authorization/refresh URLs and scopes, no browser redirect.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### `ImplicitOAuthFlow.__init__` (line 449)

Coverage ID: `a2a_pb2.pyi:449:ImplicitOAuthFlow.__init__`.

Deprecated flow metadata; authorization/refresh URLs and scopes, no browser redirect.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, authorization_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### `PasswordOAuthFlow` (line 451)

Coverage ID: `a2a_pb2.pyi:451:PasswordOAuthFlow`.

Deprecated flow metadata; token/refresh URLs and scopes, no password collection.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `PasswordOAuthFlow.ScopesEntry` (line 453)

Coverage ID: `a2a_pb2.pyi:453:PasswordOAuthFlow.ScopesEntry`.

Deprecated flow metadata; token/refresh URLs and scopes, no password collection.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `PasswordOAuthFlow.ScopesEntry.__init__` (line 459)

Coverage ID: `a2a_pb2.pyi:459:PasswordOAuthFlow.ScopesEntry.__init__`.

Deprecated flow metadata; token/refresh URLs and scopes, no password collection.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### `PasswordOAuthFlow.__init__` (line 466)

Coverage ID: `a2a_pb2.pyi:466:PasswordOAuthFlow.__init__`.

Deprecated flow metadata; token/refresh URLs and scopes, no password collection.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### `DeviceCodeOAuthFlow` (line 468)

Coverage ID: `a2a_pb2.pyi:468:DeviceCodeOAuthFlow`.

Device authorization/token/refresh URLs and scopes; no polling loop, expiry/retry intervals, or user-code generation.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class DeviceCodeOAuthFlow(_message.Message):
    __slots__ = ('device_authorization_url', 'token_url', 'refresh_url', 'scopes')

    class ScopesEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    DEVICE_AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URL_FIELD_NUMBER: _ClassVar[int]
    REFRESH_URL_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    device_authorization_url: str
    token_url: str
    refresh_url: str
    scopes: _containers.ScalarMap[str, str]

    def __init__(self, device_authorization_url: _Optional[str]=..., token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
        ...
```

### `DeviceCodeOAuthFlow.ScopesEntry` (line 470)

Coverage ID: `a2a_pb2.pyi:470:DeviceCodeOAuthFlow.ScopesEntry`.

Device authorization/token/refresh URLs and scopes; no polling loop, expiry/retry intervals, or user-code generation.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

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

### `DeviceCodeOAuthFlow.ScopesEntry.__init__` (line 476)

Coverage ID: `a2a_pb2.pyi:476:DeviceCodeOAuthFlow.ScopesEntry.__init__`.

Device authorization/token/refresh URLs and scopes; no polling loop, expiry/retry intervals, or user-code generation.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
    ...
```

### `DeviceCodeOAuthFlow.__init__` (line 485)

Coverage ID: `a2a_pb2.pyi:485:DeviceCodeOAuthFlow.__init__`.

Device authorization/token/refresh URLs and scopes; no polling loop, expiry/retry intervals, or user-code generation.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, device_authorization_url: _Optional[str]=..., token_url: _Optional[str]=..., refresh_url: _Optional[str]=..., scopes: _Optional[_Mapping[str, str]]=...) -> None:
    ...
```

### `SendMessageRequest` (line 487)

Coverage ID: `a2a_pb2.pyi:487:SendMessageRequest`.

Tenant routing scope, required Message, optional configuration/metadata; used by unary and server-streaming send.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class SendMessageRequest(_message.Message):
    __slots__ = ('tenant', 'message', 'configuration', 'metadata')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    message: Message
    configuration: SendMessageConfiguration
    metadata: _struct_pb2.Struct

    def __init__(self, tenant: _Optional[str]=..., message: _Optional[_Union[Message, _Mapping]]=..., configuration: _Optional[_Union[SendMessageConfiguration, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### `SendMessageRequest.__init__` (line 497)

Coverage ID: `a2a_pb2.pyi:497:SendMessageRequest.__init__`.

Tenant routing scope, required Message, optional configuration/metadata; used by unary and server-streaming send.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., message: _Optional[_Union[Message, _Mapping]]=..., configuration: _Optional[_Union[SendMessageConfiguration, _Mapping]]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### `GetTaskRequest` (line 499)

Coverage ID: `a2a_pb2.pyi:499:GetTaskRequest`.

Tenant and required task id, optional history_length with explicit-zero presence semantics.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class GetTaskRequest(_message.Message):
    __slots__ = ('tenant', 'id', 'history_length')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    HISTORY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    id: str
    history_length: int

    def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=..., history_length: _Optional[int]=...) -> None:
        ...
```

### `GetTaskRequest.__init__` (line 507)

Coverage ID: `a2a_pb2.pyi:507:GetTaskRequest.__init__`.

Tenant and required task id, optional history_length with explicit-zero presence semantics.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=..., history_length: _Optional[int]=...) -> None:
    ...
```

### `ListTasksRequest` (line 509)

Coverage ID: `a2a_pb2.pyi:509:ListTasksRequest`.

Tenant/context/status/time filters, optional page size/history/include_artifacts and cursor. No filter application, snapshot consistency, ordering, or page defaulting occurs here.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class ListTasksRequest(_message.Message):
    __slots__ = ('tenant', 'context_id', 'status', 'page_size', 'page_token', 'history_length', 'status_timestamp_after', 'include_artifacts')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    HISTORY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    STATUS_TIMESTAMP_AFTER_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    context_id: str
    status: TaskState
    page_size: int
    page_token: str
    history_length: int
    status_timestamp_after: _timestamp_pb2.Timestamp
    include_artifacts: bool

    def __init__(self, tenant: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskState, str]]=..., page_size: _Optional[int]=..., page_token: _Optional[str]=..., history_length: _Optional[int]=..., status_timestamp_after: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]]=..., include_artifacts: _Optional[bool]=...) -> None:
        ...
```

### `ListTasksRequest.__init__` (line 527)

Coverage ID: `a2a_pb2.pyi:527:ListTasksRequest.__init__`.

Tenant/context/status/time filters, optional page size/history/include_artifacts and cursor. No filter application, snapshot consistency, ordering, or page defaulting occurs here.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., context_id: _Optional[str]=..., status: _Optional[_Union[TaskState, str]]=..., page_size: _Optional[int]=..., page_token: _Optional[str]=..., history_length: _Optional[int]=..., status_timestamp_after: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]]=..., include_artifacts: _Optional[bool]=...) -> None:
    ...
```

### `ListTasksResponse` (line 529)

Coverage ID: `a2a_pb2.pyi:529:ListTasksResponse`.

Tasks page plus next cursor/page size/total size. REQUIRED annotations on empty cursor/numeric zero can conflict with business meaning when generic required validator is applied; generated serializer permits them.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class ListTasksResponse(_message.Message):
    __slots__ = ('tasks', 'next_page_token', 'page_size', 'total_size')
    TASKS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    next_page_token: str
    page_size: int
    total_size: int

    def __init__(self, tasks: _Optional[_Iterable[_Union[Task, _Mapping]]]=..., next_page_token: _Optional[str]=..., page_size: _Optional[int]=..., total_size: _Optional[int]=...) -> None:
        ...
```

### `ListTasksResponse.__init__` (line 539)

Coverage ID: `a2a_pb2.pyi:539:ListTasksResponse.__init__`.

Tasks page plus next cursor/page size/total size. REQUIRED annotations on empty cursor/numeric zero can conflict with business meaning when generic required validator is applied; generated serializer permits them.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tasks: _Optional[_Iterable[_Union[Task, _Mapping]]]=..., next_page_token: _Optional[str]=..., page_size: _Optional[int]=..., total_size: _Optional[int]=...) -> None:
    ...
```

### `CancelTaskRequest` (line 541)

Coverage ID: `a2a_pb2.pyi:541:CancelTaskRequest`.

Tenant/task id plus metadata; serializing this does not cancel work. Remote handler owns cancelability and races.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class CancelTaskRequest(_message.Message):
    __slots__ = ('tenant', 'id', 'metadata')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    id: str
    metadata: _struct_pb2.Struct

    def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
        ...
```

### `CancelTaskRequest.__init__` (line 549)

Coverage ID: `a2a_pb2.pyi:549:CancelTaskRequest.__init__`.

Tenant/task id plus metadata; serializing this does not cancel work. Remote handler owns cancelability and races.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]]=...) -> None:
    ...
```

### `GetTaskPushNotificationConfigRequest` (line 551)

Coverage ID: `a2a_pb2.pyi:551:GetTaskPushNotificationConfigRequest`.

Tenant/task_id/config id lookup; identifiers are separate scalar values, not parsed resource paths.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class GetTaskPushNotificationConfigRequest(_message.Message):
    __slots__ = ('tenant', 'task_id', 'id')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    task_id: str
    id: str

    def __init__(self, tenant: _Optional[str]=..., task_id: _Optional[str]=..., id: _Optional[str]=...) -> None:
        ...
```

### `GetTaskPushNotificationConfigRequest.__init__` (line 559)

Coverage ID: `a2a_pb2.pyi:559:GetTaskPushNotificationConfigRequest.__init__`.

Tenant/task_id/config id lookup; identifiers are separate scalar values, not parsed resource paths.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., task_id: _Optional[str]=..., id: _Optional[str]=...) -> None:
    ...
```

### `DeleteTaskPushNotificationConfigRequest` (line 561)

Coverage ID: `a2a_pb2.pyi:561:DeleteTaskPushNotificationConfigRequest`.

Tenant/task_id/config id deletion request. No local delete side effect; remote call requires caller authorization.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class DeleteTaskPushNotificationConfigRequest(_message.Message):
    __slots__ = ('tenant', 'task_id', 'id')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    task_id: str
    id: str

    def __init__(self, tenant: _Optional[str]=..., task_id: _Optional[str]=..., id: _Optional[str]=...) -> None:
        ...
```

### `DeleteTaskPushNotificationConfigRequest.__init__` (line 569)

Coverage ID: `a2a_pb2.pyi:569:DeleteTaskPushNotificationConfigRequest.__init__`.

Tenant/task_id/config id deletion request. No local delete side effect; remote call requires caller authorization.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., task_id: _Optional[str]=..., id: _Optional[str]=...) -> None:
    ...
```

### `SubscribeToTaskRequest` (line 571)

Coverage ID: `a2a_pb2.pyi:571:SubscribeToTaskRequest`.

Tenant/task id subscription request; no iterator/state replay/cursor exists until transport is invoked.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class SubscribeToTaskRequest(_message.Message):
    __slots__ = ('tenant', 'id')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    id: str

    def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=...) -> None:
        ...
```

### `SubscribeToTaskRequest.__init__` (line 577)

Coverage ID: `a2a_pb2.pyi:577:SubscribeToTaskRequest.__init__`.

Tenant/task id subscription request; no iterator/state replay/cursor exists until transport is invoked.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., id: _Optional[str]=...) -> None:
    ...
```

### `ListTaskPushNotificationConfigsRequest` (line 579)

Coverage ID: `a2a_pb2.pyi:579:ListTaskPushNotificationConfigsRequest`.

Task-scoped listing with page size/cursor; page_size is nonpresence scalar (absent vs zero indistinguishable). Tenant field number is 4.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class ListTaskPushNotificationConfigsRequest(_message.Message):
    __slots__ = ('tenant', 'task_id', 'page_size', 'page_token')
    TENANT_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    tenant: str
    task_id: str
    page_size: int
    page_token: str

    def __init__(self, tenant: _Optional[str]=..., task_id: _Optional[str]=..., page_size: _Optional[int]=..., page_token: _Optional[str]=...) -> None:
        ...
```

### `ListTaskPushNotificationConfigsRequest.__init__` (line 589)

Coverage ID: `a2a_pb2.pyi:589:ListTaskPushNotificationConfigsRequest.__init__`.

Task-scoped listing with page size/cursor; page_size is nonpresence scalar (absent vs zero indistinguishable). Tenant field number is 4.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=..., task_id: _Optional[str]=..., page_size: _Optional[int]=..., page_token: _Optional[str]=...) -> None:
    ...
```

### `GetExtendedAgentCardRequest` (line 591)

Coverage ID: `a2a_pb2.pyi:591:GetExtendedAgentCardRequest`.

Tenant-only request; generated type does not prove authentication or authorization.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class GetExtendedAgentCardRequest(_message.Message):
    __slots__ = ('tenant',)
    TENANT_FIELD_NUMBER: _ClassVar[int]
    tenant: str

    def __init__(self, tenant: _Optional[str]=...) -> None:
        ...
```

### `GetExtendedAgentCardRequest.__init__` (line 595)

Coverage ID: `a2a_pb2.pyi:595:GetExtendedAgentCardRequest.__init__`.

Tenant-only request; generated type does not prove authentication or authorization.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, tenant: _Optional[str]=...) -> None:
    ...
```

### `SendMessageResponse` (line 597)

Coverage ID: `a2a_pb2.pyi:597:SendMessageResponse`.

Oneof payload returns Task snapshot or direct Message; empty response is constructible.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class SendMessageResponse(_message.Message):
    __slots__ = ('task', 'message')
    TASK_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    task: Task
    message: Message

    def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., message: _Optional[_Union[Message, _Mapping]]=...) -> None:
        ...
```

### `SendMessageResponse.__init__` (line 603)

Coverage ID: `a2a_pb2.pyi:603:SendMessageResponse.__init__`.

Oneof payload returns Task snapshot or direct Message; empty response is constructible.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., message: _Optional[_Union[Message, _Mapping]]=...) -> None:
    ...
```

### `StreamResponse` (line 605)

Coverage ID: `a2a_pb2.pyi:605:StreamResponse`.

Oneof payload with Task/Message/status/artifact updates. Not a Python async iterator; each wire stream item is one envelope.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class StreamResponse(_message.Message):
    __slots__ = ('task', 'message', 'status_update', 'artifact_update')
    TASK_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_UPDATE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_UPDATE_FIELD_NUMBER: _ClassVar[int]
    task: Task
    message: Message
    status_update: TaskStatusUpdateEvent
    artifact_update: TaskArtifactUpdateEvent

    def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., message: _Optional[_Union[Message, _Mapping]]=..., status_update: _Optional[_Union[TaskStatusUpdateEvent, _Mapping]]=..., artifact_update: _Optional[_Union[TaskArtifactUpdateEvent, _Mapping]]=...) -> None:
        ...
```

### `StreamResponse.__init__` (line 615)

Coverage ID: `a2a_pb2.pyi:615:StreamResponse.__init__`.

Oneof payload with Task/Message/status/artifact updates. Not a Python async iterator; each wire stream item is one envelope.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, task: _Optional[_Union[Task, _Mapping]]=..., message: _Optional[_Union[Message, _Mapping]]=..., status_update: _Optional[_Union[TaskStatusUpdateEvent, _Mapping]]=..., artifact_update: _Optional[_Union[TaskArtifactUpdateEvent, _Mapping]]=...) -> None:
    ...
```

### `ListTaskPushNotificationConfigsResponse` (line 617)

Coverage ID: `a2a_pb2.pyi:617:ListTaskPushNotificationConfigsResponse`.

Repeated callback configurations plus next page token; sensitive callback configuration fields remain serializable.

Static definition: fields annotate storage; map-entry nested classes have key/value and __init__, and are implementation support for map containers. No independent persistence or external resource lifetime. Enum stubs describe integer-compatible values; runtime enum wrapper is not instantiated like a message.

```python
class ListTaskPushNotificationConfigsResponse(_message.Message):
    __slots__ = ('configs', 'next_page_token')
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[TaskPushNotificationConfig]
    next_page_token: str

    def __init__(self, configs: _Optional[_Iterable[_Union[TaskPushNotificationConfig, _Mapping]]]=..., next_page_token: _Optional[str]=...) -> None:
        ...
```

### `ListTaskPushNotificationConfigsResponse.__init__` (line 623)

Coverage ID: `a2a_pb2.pyi:623:ListTaskPushNotificationConfigsResponse.__init__`.

Repeated callback configurations plus next page token; sensitive callback configuration fields remain serializable.

Constructor accepts optional keyword field values/iterables/mappings exactly as annotated; returns None after populating new message. Type/presence/oneof and protobuf errors follow runtime surface reference; no business validation or network call.

```python
def __init__(self, configs: _Optional[_Iterable[_Union[TaskPushNotificationConfig, _Mapping]]]=..., next_page_token: _Optional[str]=...) -> None:
    ...
```
