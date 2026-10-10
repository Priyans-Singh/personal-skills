# `client_factory.py`: construction and negotiation

Source: a2a-sdk 1.1.4. [Core](core_knowledge.md) defines returned client behavior.

`TransportProducer` is a callable `(AgentCard, selected_url: str, ClientConfig) -> ClientTransport`. Producers are synchronous; connections/calls can later be asynchronous. Custom producers control their own initialization side effects.

## Factory state and default registration

`ClientFactory.__init__(config=None)` creates defaults if needed, uses injected HTTPX client or creates one, and calls `headers.setdefault('A2A-Version','1.0')`. An existing header is preserved. The factory retains the config and HTTP client, initializes `_registry`, and calls `_register_defaults`.

`_register_defaults(supported)` registers JSONRPC for empty lists or explicit JSONRPC; REST only for `HTTP+JSON`; gRPC only for `GRPC`. Requesting gRPC while its import failed raises `ImportError` with extras installation advice. Missing gRPC channel factory is diagnosed later at transport construction.

Nested `jsonrpc_transport_producer`, `rest_transport_producer`, and `grpc_transport_producer` each re-find an interface filtered by binding and selected URL to determine version. Missing interface falls back to current version. Versions >=0.3 and <1.0 select compatibility JSON-RPC/REST transports; gRPC selects compatibility only if that optional transport imported. Otherwise current transports are used. HTTP producers share the factory HTTPX client. gRPC producers call transport `create(card,url,config)`.

`register(label,generator)` inserts/replaces a producer. Registering alone does not add the label to `supported_protocol_bindings`; include it in configuration and the card so negotiation can choose it.

## `_find_best_interface`: exact priority

Filters interfaces by optional allowed bindings and exact optional URL. Returns `None` if no candidates. Selection preserves first occurrence within these priorities:

1. First version string exactly equal to `1.0`.
2. First parseable version greater than 1.0.
3. First parseable version >=0.3.
4. First interface with empty version.

Invalid version strings are silently ignored. This is not a highest-version sort. String `1.0.0` is numerically >=0.3 but does not satisfy the first exact-string branch; a later version above 1.0 can outrank it. Unversioned interfaces use the current transport because `is_legacy_version` returns false.

## `create(card,interceptors=None)`

Uses configured bindings or `[JSONRPC]`. With `use_client_preference=True`, iterates configured binding order until `_find_best_interface` returns a candidate. Default behavior iterates card interface order, picks the first supported **binding**, then finds the best version across that binding. In the default branch it breaks after that binding even if its candidates have unusable version strings; it does not necessarily try a later binding.

No selected binding/interface raises `ValueError('no compatible transports found.')`. Selected binding without producer raises `ValueError('no client available for ...')`. Producer exceptions propagate. Calls producer with card, interface URL, config. Nonempty interface tenant wraps the result in `TenantTransportDecorator`. Returns `BaseClient(card, config, transport, interceptors or [])`. Direct construction from a card performs no signature verification.

Interface selection is construction-time configuration, not per-request failover. A transport does not automatically switch bindings on error. Selecting a numerically newer interface does not add new protocol implementation behavior: current transports still use their installed methods/current version headers.

## Discovery and convenience functions

`create_from_url(url,interceptors,relative_card_path,resolver_http_kwargs,signature_verifier)` constructs resolver with the factory HTTPX client, awaits card retrieval, then calls `create`. Initial GET uses resolver kwargs and does not run request interceptors. Errors are described in [discovery](discovery_knowledge.md). A construction failure after creating HTTP resources has no explicit factory cleanup path; callers should manage resource lifetime.

Async `create_client(agent, client_config, ...)` creates a new factory. String input uses `create_from_url`; `AgentCard` input goes directly to `create`, ignoring discovery-only arguments, including the verifier. Use a retained factory for transport registration or shared HTTP resources.

`minimal_agent_card(url,transports=None)` returns a skeletal protobuf with one unversioned interface per supplied binding, extended-card capability true, and empty identity/skill/input/output fields. Default `None` becomes `[]`, so the default card has **no interfaces** and cannot negotiate a transport by itself. Supply bindings explicitly. It is a bootstrap for fetching the real extended card, particularly over gRPC; it does not discover capabilities, assert streaming, or validate the endpoint.
