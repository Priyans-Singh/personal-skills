# A2A client: reading guide

Inspected: **a2a-sdk 1.1.4**, 2026-10-07. Source: `../.venv/lib/python3.11/site-packages/a2a/client/` relative to this folder. Protocol version advertised by current transports is **1.0**, which differs from the SDK distribution version. This reference describes the installed implementation, not a universal promise about other releases or remote servers.

The client discovers an agent, selects one advertised interface, and sends typed requests through that interface. It implements communication and request policy; the remote agent implements task execution.

| Guide | Source scope |
|---|---|
| [Core](core_knowledge.md) | Root `__init__.py`, `client.py`, `base_client.py`; resources, lifecycle, operation contracts and execution flows |
| [Factory](factory_knowledge.md) | Root `client_factory.py`; transport/version negotiation, registration, bootstrap |
| [Discovery](discovery_knowledge.md) | Root `card_resolver.py`; discovery, compatibility transformations and verification |
| [Hooks and parameters](hooks_knowledge.md) | Root `interceptors.py`, `service_parameters.py`, `errors.py`, `optionals.py` |
| [Authentication](auth/auth_knowledge.md) | Every file in root folder `auth/` |
| [Transport contracts and tenancy](transports/transport_knowledge.md) | `transports/__init__.py`, `base.py`, `tenant_decorator.py`; wire-operation comparison |
| [HTTP and SSE](transports/http_helpers_knowledge.md) | `transports/http_helpers.py` |
| [JSON-RPC](transports/jsonrpc_knowledge.md) | `transports/jsonrpc.py` |
| [REST](transports/rest_knowledge.md) | `transports/rest.py` |
| [gRPC](transports/grpc_knowledge.md) | `transports/grpc.py` |
| [Supporting dependencies](dependencies_knowledge.md) | Direct implementation boundaries outside `client/`, including v0.3 transports, protobufs, errors and tracing |
| [Coverage](coverage_knowledge.md) | Complete AST declaration index, source fingerprints and documentation routing |

## Mental model

```text
create_client(URL)
  -> ClientFactory (owns/reuses HTTPX client and transport registry)
  -> A2ACardResolver.get_agent_card() (HTTP GET)
  -> AgentCard (interfaces, capabilities, security, skills)
  -> factory.create(card) (select binding, version, URL, tenant)
  -> BaseClient (settings + interceptors + retained card)
  -> optional TenantTransportDecorator
  -> JSON-RPC / REST / gRPC / custom / legacy transport
  -> remote agent
```

Supplying an `AgentCard` skips discovery. `send_message` always exposes an async iterator: an ordinary response becomes one `StreamResponse`; a streamed call yields individual events. Task reads and mutations are ordinary async calls. The client does not persist tasks or assemble a durable task database.

## Operational semantics

- Streaming defaults on; it is used only if both configuration and card advertise it. Default binding selection is JSON-RPC only.
- `polling=True` sets `return_immediately`; no background polling loop is created. No general request retry, backoff, reconnect or pagination loop is implemented. Legacy REST has one specific POST-to-GET subscription fallback.
- Requests and call contexts are mutable. Configuration, interceptors and the tenant wrapper can change caller-owned objects. Avoid sharing them across concurrent calls without copying or coordination.
- Closing an HTTP-backed client closes the factory's HTTPX client, including an injected client. Multiple clients from one factory can share that resource. gRPC closes its channel.
- Authentication adds headers/metadata from caller-provided credentials. No token acquisition, refresh, expiration handling or authorization decision is implemented locally.
- Cancel and push-configuration create/delete are remote mutations. A timeout does not prove they failed remotely. There is no rollback or automatic reconciliation.
- Card verification is opt-in. Initial discovery bypasses BaseClient interceptors; use resolver HTTP arguments for discovery credentials. Extended-card verification occurs after transport/interceptor processing.
- Stream termination and closing a connection are distinct from cancelling a remote task. The client provides `cancel_task` for the remote request.

## Scope and evidence

All 19 Python files under `client/` are covered, including private and nested callables, the type-checking-only stub, and re-export modules. There are no README or other source-support files in this package inventory. Bytecode caches are excluded.

Supporting dependencies are covered at the execution boundary relevant to this client; unrelated server, database, migration and sibling utility APIs are outside scope. No external agent was contacted. Local source establishes request encoding and exception transformation, not remote authorization, durability, cancellation success or delivery guarantees.

Run `python3 a2a-client/validate_coverage.py` from the workspace to verify declarations, source fingerprints, documentation references, links and whitespace against this snapshot.
