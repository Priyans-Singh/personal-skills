# ServerCallContext

Source: [`server/context.py`](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/context.py).

`State` aliases `MutableMapping[str, Any]`. `ServerCallContext` is a Pydantic BaseModel with arbitrary types enabled, allowing framework-specific objects such as a gRPC servicer context.

| Field | Default | Meaning / use |
|---|---|---|
| `state` | Fresh dictionary | App/framework data; HTTP builder includes headers and available auth; JSON-RPC adds method/request ID; gRPC stores its context |
| `user` | Fresh `UnauthenticatedUser` | Identity used by default owner resolution |
| `tenant` | Empty string | Routing/protocol tenant identifier, not automatically an ownership component |
| `requested_extensions` | Fresh set | Extension URIs parsed from request headers/metadata |

There are no declared methods here. Pydantic handles construction/validation; the object itself does no authentication, persistence, version checking, or authorization. Callers/builders can mutate its fields and mapping. Do not store reusable secrets or unfiltered full request bodies in state just because it accepts arbitrary values.

Default HTTP construction copies incoming headers into state and adapts Starlette's authenticated user if middleware supplied one. Default gRPC construction always uses unauthenticated identity; override its builder to authenticate. REST tenant comes from a path parameter, JSON-RPC/gRPC from request model fields where available. Extension collection records requests; it does not enforce required extensions or activate application behavior automatically.

A background ActiveTask can retain call context beyond transport response completion. Use stable, validated identity values and avoid request-local objects that become unusable after disconnect. See [owner resolver](owner_resolver_knowledge.md) and [routes](routes_knowledge.md).
