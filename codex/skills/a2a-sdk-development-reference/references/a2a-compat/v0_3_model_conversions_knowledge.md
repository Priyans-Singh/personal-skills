# v0_3/model_conversions.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/model_conversions.py`. SHA-256: `d5c9699999f8f7cd345b75cd179d16b438c92d5620a726716116dfe690120780`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Persistence format boundary

These functions construct SQLAlchemy model instances or decode already-loaded data; they do not open sessions, issue SQL, commit, delete rows, decrypt, or enforce owner identity. Import requires external `a2a.server.models`, which unconditionally needs SQLAlchemy; SQLAlchemy is absent in inspected environment. Static body review covers all four helpers; no import or DB test occurred.

`core_to_compat_task_model(task,owner)` converts task to pivot, model_dump(mode='json'), creates TaskModel with task.id/context_id and caller owner; extracts status/history/artifacts/metadata into columns and labels protocol_version='0.3'. Task kind/last_updated are left to model defaults/caller. It serializes legacy shape, not protobuf binary. `compat_task_model_to_core` validates stored status and each truthy artifacts/history list into pivot models, uses [] for empty/null lists, preserves task metadata, converts to core. It does not check protocol_version, owner or context permissions.

`core_to_compat_push_notification_config_model(task_id,config,owner,fernet=None)` serializes **inner** PushNotificationConfig JSON as UTF-8 bytes. If caller supplied Fernet, encrypts full payload, including URL/token/auth credentials, otherwise stores plaintext bytes. Row key task_id comes from explicit argument and config_id from core config.id; it does not check explicit task_id agrees with config.task_id. Owner/protocol version are labeled, not validated. Fernet object/key is used transiently and not stored by helper.

`compat_push_notification_config_model_to_core(model_instance:str,task_id)` misleadingly accepts a serialized JSON value rather than ORM model; model_validate_json then adds supplied task_id wrapper and translates. It has no Fernet parameter or decryption: caller must decrypt stored bytes first. Pydantic may accept bytes despite str annotation. Wrong JSON/model fields, decryption exceptions in write helper and conversion failures propagate. Encryption lifetime/key rotation and storage transaction consistency belong to caller/store.

Best practice: route decode by stored protocol_version before invoking; retain owner enforcement in store; decrypt outside this helper; ensure task/config IDs agree; do not log raw config_data. These statements follow actual boundaries, not promises of encryption-by-default.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
from typing import TYPE_CHECKING
from a2a.compat.v0_3 import types as types_v03
from a2a.compat.v0_3.conversions import to_compat_push_notification_config, to_compat_task, to_core_task, to_core_task_push_notification_config
from a2a.server.models import PushNotificationConfigModel, TaskModel
from a2a.types import a2a_pb2 as pb2_v10
from cryptography.fernet import Fernet
```

## Declaration-by-declaration execution reference

### `core_to_compat_task_model`

Source lines 21–35; declaration kind `FunctionDef`.

Inputs: `(task: pb2_v10.Task, owner: str)`. Output annotation: `TaskModel`. Decorators: `none`.

Source intent: Converts a 1.0 core Task to a TaskModel using v0.3 JSON structure.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `compat_task` from `to_compat_task(task)`; output construction/calls here execute immediately when this method runs.
2. Assigns `data` from `compat_task.model_dump(mode='json')`; output construction/calls here execute immediately when this method runs.
3. Returns `TaskModel(id=task.id, context_id=task.context_id, owner=owner, status=data.get('status'), history=data.get('history'), artifacts=data.get('artifacts'), task_metadata=data.get('metadata'), protocol_version='0.3')`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `to_compat_task`, `compat_task.model_dump`, `TaskModel`, `data.get`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def core_to_compat_task_model(task: pb2_v10.Task, owner: str) -> TaskModel:
    compat_task = to_compat_task(task)
    data = compat_task.model_dump(mode='json')
    return TaskModel(id=task.id, context_id=task.context_id, owner=owner, status=data.get('status'), history=data.get('history'), artifacts=data.get('artifacts'), task_metadata=data.get('metadata'), protocol_version='0.3')
```

</details>

### `compat_task_model_to_core`

Source lines 38–56; declaration kind `FunctionDef`.

Inputs: `(task_model: TaskModel)`. Output annotation: `pb2_v10.Task`. Decorators: `none`.

Source intent: Converts a TaskModel with v0.3 structure to a 1.0 core Task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `compat_task` from `types_v03.Task(id=task_model.id, context_id=task_model.context_id, status=types_v03.TaskStatus.model_validate(task_model.status), artifacts=[types_v03.Artifact.model_validate(a) for a in task_model.artifacts] if task_model.artifacts else [], history=[types_v03.Message.model_validate(h) for h in task_model.history] if task_model.history else [], metadata=task … (full expression in body below)`; output construction/calls here execute immediately when this method runs.
2. Returns `to_core_task(compat_task)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.Task`, `to_core_task`, `types_v03.TaskStatus.model_validate`, `types_v03.Artifact.model_validate`, `types_v03.Message.model_validate`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def compat_task_model_to_core(task_model: TaskModel) -> pb2_v10.Task:
    compat_task = types_v03.Task(id=task_model.id, context_id=task_model.context_id, status=types_v03.TaskStatus.model_validate(task_model.status), artifacts=[types_v03.Artifact.model_validate(a) for a in task_model.artifacts] if task_model.artifacts else [], history=[types_v03.Message.model_validate(h) for h in task_model.history] if task_model.history else [], metadata=task_model.task_metadata)
    return to_core_task(compat_task)
```

</details>

### `core_to_compat_push_notification_config_model`

Source lines 59–77; declaration kind `FunctionDef`.

Inputs: `(task_id: str, config: pb2_v10.TaskPushNotificationConfig, owner: str, fernet: 'Fernet | None'=None)`. Output annotation: `PushNotificationConfigModel`. Decorators: `none`.

Source intent: Converts a 1.0 core TaskPushNotificationConfig to a PushNotificationConfigModel using v0.3 JSON structure.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `compat_config` from `to_compat_push_notification_config(config)`; output construction/calls here execute immediately when this method runs.
2. Assigns `json_payload` from `compat_config.model_dump_json().encode('utf-8')`; output construction/calls here execute immediately when this method runs.
3. Assigns `data_to_store` from `fernet.encrypt(json_payload) if fernet else json_payload`; output construction/calls here execute immediately when this method runs.
4. Returns `PushNotificationConfigModel(task_id=task_id, config_id=config.id, owner=owner, config_data=data_to_store, protocol_version='0.3')`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `to_compat_push_notification_config`, `compat_config.model_dump_json().encode`, `PushNotificationConfigModel`, `fernet.encrypt`, `compat_config.model_dump_json`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def core_to_compat_push_notification_config_model(task_id: str, config: pb2_v10.TaskPushNotificationConfig, owner: str, fernet: 'Fernet | None'=None) -> PushNotificationConfigModel:
    compat_config = to_compat_push_notification_config(config)
    json_payload = compat_config.model_dump_json().encode('utf-8')
    data_to_store = fernet.encrypt(json_payload) if fernet else json_payload
    return PushNotificationConfigModel(task_id=task_id, config_id=config.id, owner=owner, config_data=data_to_store, protocol_version='0.3')
```

</details>

### `compat_push_notification_config_model_to_core`

Source lines 80–92; declaration kind `FunctionDef`.

Inputs: `(model_instance: str, task_id: str)`. Output annotation: `pb2_v10.TaskPushNotificationConfig`. Decorators: `none`.

Source intent: Converts a PushNotificationConfigModel with v0.3 structure back to a 1.0 core TaskPushNotificationConfig.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `inner_config` from `types_v03.PushNotificationConfig.model_validate_json(model_instance)`; output construction/calls here execute immediately when this method runs.
2. Returns `to_core_task_push_notification_config(types_v03.TaskPushNotificationConfig(task_id=task_id, push_notification_config=inner_config))`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `types_v03.PushNotificationConfig.model_validate_json`, `to_core_task_push_notification_config`, `types_v03.TaskPushNotificationConfig`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def compat_push_notification_config_model_to_core(model_instance: str, task_id: str) -> pb2_v10.TaskPushNotificationConfig:
    inner_config = types_v03.PushNotificationConfig.model_validate_json(model_instance)
    return to_core_task_push_notification_config(types_v03.TaskPushNotificationConfig(task_id=task_id, push_notification_config=inner_config))
```

</details>
