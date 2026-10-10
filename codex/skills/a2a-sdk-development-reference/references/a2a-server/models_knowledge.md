# Database schema models

Source: [`server/models.py`](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py). Import requires SQLAlchemy; absence raises an ImportError listing install extras. These ORM declarations are not wire protocol models.

## Classes and schema

`Base` subclasses SQLAlchemy DeclarativeBase and owns table metadata. `TaskMixin` declares:

| Column | Behavior |
|---|---|
| `id` | String(36), globally unique primary key, indexed |
| `context_id` | String(36), required |
| `kind` | String(16), default `task` |
| `owner` | Nullable String(255) |
| `last_updated` | Nullable DateTime, populated from status timestamp by default converter |
| `status` | Required JSON; protobuf status serialized to a dictionary |
| `artifacts`, `history` | Nullable JSON lists |
| `protocol_version` | Nullable String(16); default store converter writes `1.0` |
| `task_metadata` | Declared-attribute JSON column physically named `metadata` to avoid ORM metadata-name conflict |

`TaskMixin.__table_args__` adds a table-specific index on `(owner, last_updated)`. `TaskMixin.__repr__` shows ID, context, and status. `TaskModel` combines mixin/Base with table `tasks`.

`PushNotificationConfigMixin` uses composite primary key `(task_id, config_id)` with String(36)/String(255), binary `config_data`, nullable indexed owner, and protocol_version. It has no Task foreign key. Its repr shows task/config IDs. `PushNotificationConfigModel` binds table `push_notification_configs`.

## Factories and helpers

`create_task_model(table_name='tasks', base=Base)` dynamically declares a nested TaskModel class, changes its class/qualified name to include table name, and returns the class. The nested repr includes table name. `create_push_notification_config_model(...)` does the same for configuration tables. Declaring duplicate names/tables repeatedly against shared metadata may trigger SQLAlchemy errors; create/reuse models deliberately. Factory base is replaceable, but default stores invoke factories with Base.

The runtime `override(func)` helper is identity-only; TYPE_CHECKING uses typing_extensions.override instead. It does not change execution. The callable index includes it and the nested classes/methods.

## Implications

Owner predicates on reads/deletes do not alter primary-key identity. A store `merge` can update a row with a colliding ID belonging to another owner. Globally unique IDs are required by the default design. Config ownership has the same limitation when task/config keys collide.

No cascade deletes, execution lease, optimistic version, outbox, retry counters, or transaction linking Tasks/configs is declared. Snapshot persistence is not an execution-resumption system. `last_updated` follows task status timestamp, so artifact changes need not change list ordering. SQL type/index definitions alone cannot establish a particular database's isolation/durability guarantees.

Use migrations in deployments that need controlled schema changes; `create_all` performed by stores creates tables but does not migrate existing columns. External `a2a/migrations` and `a2a_db_cli.py` are optional administration, not automatically invoked by server handling.
