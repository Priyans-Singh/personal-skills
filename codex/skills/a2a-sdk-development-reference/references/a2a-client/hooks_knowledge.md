# Root hooks, parameters, errors and optional types

Source: `a2a/client/{interceptors,service_parameters,errors,optionals}.py`, a2a-sdk 1.1.4.

## `interceptors.py`

`BeforeArgs` dataclass: `input`, `method`, `agent_card`, optional `context`, optional arbitrary `early_return`. Hooks can modify the object or replace fields. `AfterArgs`: `result`, `method`, `agent_card`, optional `context`, boolean `early_return=False`. Context carries local state between hooks. Method strings identify the actual operation (`send_message` versus `send_message_streaming`, for example).

`ClientCallInterceptor` abstract async `before(args)` and `after(args)` methods return no result; mutate their argument instead. BaseClient executes before hooks forward, after hooks backward; stream after hooks run per event. Early-return handling and truthiness are detailed in [core](core_knowledge.md). Exceptions are not swallowed. After hooks do not receive transport failures and are not guaranteed cleanup handlers.

## `service_parameters.py`

`ServiceParameters = dict[str,str]`; `ServiceParametersUpdate = Callable[[ServiceParameters],None]`.

`ServiceParametersFactory.create(updates)` delegates to `create_from(None,updates)`. `create_from(service_parameters,updates)` shallow-copies a nonempty source mapping or starts `{}`, runs each updater in order, returns new mapping. Exceptions propagate and later updates do not run; the original mapping remains separate. Updaters may overwrite preceding values.

`with_a2a_extensions(extensions)` returns nested `update(parameters)` closure. Empty extensions make it a no-op. Otherwise it reads existing exact-key `A2A-Extensions`, splits comma-separated values through `get_requested_extensions`, trims blanks, unions new values, deduplicates, sorts, and writes comma-joined URIs. Repeated use accumulates extensions. This declares requested support; it does not implement an extension or check the card.

HTTP helpers copy service parameters to headers; gRPC lower-cases names into metadata. General parameter keys are not normalized by this factory. Existing headers on the shared HTTPX client also apply. The client does not automatically serialize `context.state` into the request body.

## `errors.py`

`A2AClientError` subclasses supporting `a2a.utils.errors.A2AError`, which carries `message` and optional `data`. `A2AClientTimeoutError` marks runtime transport timeouts. `AgentCardResolutionError.__init__(message,status_code=None)` delegates message initialization and retains optional status. No retry or recovery is attached to these exception classes.

Mapped protocol failures such as `TaskNotFoundError` derive separately from `A2AError`; catching only `A2AClientError` does not catch every domain failure. Protobuf parsing, malformed result shapes, hook errors and verifier errors can also escape as other exception types.

## `optionals.py`

Attempts to import `grpc.aio.Channel`. If import fails, defines type-checking-only `Channel` stub with async `close(grace=None)`; at runtime assigns `Channel=None`. Stub `close` has no operational behavior. It exists for annotations, not as a usable fallback connection. Actual gRPC construction/import has its own explicit failure path.
