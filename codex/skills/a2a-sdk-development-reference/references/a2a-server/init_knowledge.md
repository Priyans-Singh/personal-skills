# Root initializer and public imports

Source: [`server/__init__.py`](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/__init__.py), a2a-sdk 1.1.4.

The root initializer has only the docstring “Server-side components for implementing an A2A agent.” It defines no callables, imports, application factory, or server startup behavior. Import from subpackages.

| Import location | Exported names |
|---|---|
| `a2a.server.agent_execution` | `AgentExecutor`, `RequestContext`, `RequestContextBuilder`, `SimpleRequestContextBuilder` |
| `a2a.server.events` | `Event`, `EventConsumer` (legacy), `EventQueue`, `EventQueueLegacy`, `InMemoryQueueManager`, `QueueManager`, `NoTaskQueue`, `TaskQueueExists` |
| `a2a.server.request_handlers` | `DefaultRequestHandler` (V2 alias), `DefaultRequestHandlerV2`, `LegacyRequestHandler`, `RequestHandler`, `validate_request_params`, response helpers, and optional gRPC classes |
| `a2a.server.routes` | `create_agent_card_routes`, `create_jsonrpc_routes`, `create_rest_routes`, `add_a2a_routes_to_fastapi`, HTTP context-builder classes |
| `a2a.server.tasks` | Task stores/managers/updater/aggregator, push sender/config stores, `PushNotificationEvent` |

`ActiveTask`, `ActiveTaskRegistry`, `EventQueueSource`, `EventQueueSink`, `CopyingTaskStoreAdapter`, and `validate` require their defining module imports. They are not exported by those subpackage initializers.

Optional package behavior is not uniform. Task and request-handler initializers catch ImportError for database/gRPC implementations and expose placeholder constructors that raise installation guidance. HTTP integration guards often fail at factory/dispatcher construction, but compatibility adapter imports can require Starlette/SSE earlier than expected. Do not assume a minimal installation can import every server subpackage.

In the gRPC ImportError branch only `GrpcHandler` receives a placeholder; context-builder names remain in `__all__` without fallback definitions. Importing those builders without gRPC can fail. In the task initializer both placeholders share `_original_error`; later assignment can change the exception chained by the earlier placeholder. These affect diagnostics, not the normal installed-dependency path.

Installed metadata offers `[http-server]`, `[fastapi]`, `[grpc]`, `[sqlite]`, `[postgresql]`, `[mysql]`, `[sql]`, `[encryption]`, `[telemetry]`, and `[db-cli]` extras. Extras describe installable dependencies, not necessarily dependencies present now. [Usage](usage_knowledge.md) records what is available locally.
