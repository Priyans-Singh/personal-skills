# How to use the server and choose safe defaults

This guide targets the installed 1.1.4 API. Start with [the runnable Starlette example](examples/starlette_server.py), then adapt executor, identity, persistence and lifecycle to your application. It requires packages already present here: Starlette, sse-starlette and httpx. It creates no cloud resources and has no LLM/network dependency.

## Minimal composition

1. Implement AgentExecutor.execute and cancel. Read RequestContext, publish a first Message or Task, then coherent status/artifact updates. TaskUpdater is publishing convenience, not a persistence API.
2. Define accurate AgentCard interfaces/capabilities/skills. Current protobuf values live in a2a.types; legacy Pydantic examples often do not match installed API.
3. Construct DefaultRequestHandler(executor, task_store, card). This is V2. Use create_agent_card_routes and REST/JSON-RPC factories to mount bindings. For gRPC register GrpcHandler through generated service registration.
4. Attach handler.aclose to application shutdown and separately close executor resources, HTTP client and database engine. Bound shutdown time if application jobs can stall.

The example's create_app returns a Starlette ASGI app; `app` is also provided for import-based runners. Advertised URLs assume localhost:8000; update when changing actual host/prefix. Execution emits initial Task with user history, WORKING, an echo artifact, then COMPLETED. cancel publishes CANCELED promptly. It demonstrates a task workflow, not cancellation of external jobs.

## Current HTTP payloads

For `/message:send`, POST application/json with `A2A-Version: 1.0`:

```json
{
  "message": {
    "messageId": "user-message-1",
    "role": "ROLE_USER",
    "parts": [{"text": "Hello"}]
  },
  "configuration": {"acceptedOutputModes": ["text/plain"]}
}
```

Response contains `task` with generated id/contextId, final status, history and echo artifact. Get `/tasks/{id}` with the same version header/caller; `historyLength=0` omits history from the response without deleting it. List `/tasks?includeArtifacts=true&pageSize=10`; retain nextPageToken as opaque cursor. Use returned **both task ID and context ID** for continuation, and a new messageId. Terminal tasks cannot be continued; start another task in the same conversation if appropriate.

For `/rpc`, envelope uses PascalCase method:

```json
{
  "jsonrpc": "2.0",
  "id": "request-1",
  "method": "SendMessage",
  "params": {
    "message": {
      "messageId": "user-message-2",
      "role": "ROLE_USER",
      "parts": [{"text": "Hello via JSON-RPC"}]
    }
  }
}
```

Legacy `message/send` requires enable_v0_3_compat and legacy version/interface. JSON-RPC errors can be HTTP200. Streams are SSE from `/message:stream` or SendStreamingMessage; read both ordinary data and event:error payloads. `returnImmediately=true` still waits for first emitted Task; it does not create execution before output automatically.

## Deployment choices

| Need | Choice / consequence |
|---|---|
| Local demo | InMemoryTaskStore; anonymous users share owner; data disappears on restart |
| Persist task snapshots | DatabaseTaskStore(application-owned AsyncEngine); explicitly initialize/migrate; globally unique IDs |
| Multiple replicas | V2 requires routing live send/subscription to correct execution owner; SQL alone does not distribute event queues |
| Custom distributed queue | LegacyRequestHandler consumes QueueManager; application must implement coordination/authorization/reliability beyond this abstraction |
| FastAPI | add_a2a_routes_to_fastapi before OpenAPI generation; verify schema/wire naming; Starlette dispatch bypasses ordinary endpoint DI |
| Private tasks/cards | Authenticate HTTP middleware/custom gRPC builder, stable subject+validated tenant ownership, explicit extended-card access policy |
| Webhooks | Matching config store/sender, validate URL at registration and delivery, dedicated HTTP client with timeout/no caller auth, optional encryption |
| Reliable webhooks | Custom sender/outbox/retry system; base sender logs failed HTTP delivery without retry |

Locally installed: Starlette/SSE/httpx/protobuf; cryptography available. FastAPI, grpcio and SQLAlchemy are absent. Their implementations are documented from source, but runtime integration checks need the relevant extras and driver. No dependency installation was performed.

## Best practices and troubleshooting

- Keep task IDs globally unique, owner resolution stable, task/config ownership aligned. Default Starlette display_name can be unsuitable as account key; default gRPC user is anonymous.
- Keep executor per-task state isolated; different tasks run concurrently. Do not access context/queue after execute returns. Implement application job timeout and cancellation of external work.
- Always emit first Task or one Message. “Send hangs” can mean no first output, no terminal/interrupted event, blocking webhook, or stalled graceful queue drain.
- Treat protobuf events as immutable; leave memory copying enabled. Never append artifact chunks before creating that artifact ID.
- Do not mix Message and Task workflow; put final agent text into TaskStatus.message or an artifact. TaskUpdater.new_agent_message only constructs a Message.
- Send original context ID on continuation; default V2 builder doesn't derive it from persisted Task during setup. Message IDs help deduplicate history in one consumer path but are not request idempotency keys.
- Authenticate independently of card advertisements. An extended-card capability gate alone does not require authenticated identity.
- Missing streams after restart are expected: stored Task is a snapshot, not a resumable coroutine/event log. Reconstruct application jobs explicitly; subscription alone starts no executor work.
- “Push missing” can be absent sender/config, custom store missing get_info_for_dispatch override, invalid URL, skipped corrupt encrypted row, or swallowed HTTP error. Inspect metadata/logs without logging tokens or headers.
- Close handler before store/client disposal; handler shutdown does not mark all tasks canceled or invoke executor cancel hooks.
- For task deletion, separately define config deletion/retention. Built-in schema has no cascading foreign key, and there is no default public task-delete route.

Validation of the local example and structural documentation is recorded in [coverage](coverage_knowledge.md). These practices derive from inspected implementation; they do not establish external provider guarantees.
