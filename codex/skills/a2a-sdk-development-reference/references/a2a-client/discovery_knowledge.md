# `card_resolver.py`: Agent Card discovery

Source: a2a-sdk 1.1.4. Resolver uses HTTPX directly; it does not own a transport or call the client interceptors.

## Parse and backward compatibility

`parse_agent_card(agent_card_data)` takes a dictionary, mutates it through three helpers, then calls `ParseDict(..., AgentCard(), ignore_unknown_fields=True)`. Output is a protobuf. Unknown fields are ignored for discovery; this differs from strict parsing in most current transport responses. Malformed known fields can raise protobuf `ParseError`; badly shaped containers can also cause ordinary Python exceptions.

- `_handle_extended_card_compatibility`: pops `supportsAuthenticatedExtendedCard`. If truthy, sets `capabilities.extendedAgentCard=True` only if that modern key is absent. Explicit modern false is preserved.
- `_handle_connection_fields_compatibility`: pops legacy `url`, `preferredTransport` (default JSONRPC), `protocolVersion` (default `0.3.0`), and `additionalInterfaces`. If modern `supportedInterfaces` is absent and main URL is truthy, creates main interface and additional interface entries using the same legacy version. Existing modern interfaces win; legacy keys are still removed.
- `_map_legacy_security`: creates a new list of requirement dictionaries with `schemes -> scheme name -> {'list': scopes}`. It wraps scope lists; it does not validate credentials or security policy.
- `_handle_security_compatibility`: removes root/skill legacy `security` and inserts converted `securityRequirements` only when modern field is absent. For each security scheme it pops legacy `type`, wraps recognized schemes in modern oneof names (`apiKeySecurityScheme`, `httpAuthSecurityScheme`, `oauth2SecurityScheme`, `openIdConnectSecurityScheme`, `mtlsSecurityScheme`), and maps API-key `in` to `location`. Uses copied inner dictionary, clears and updates the original scheme dictionary. Unrecognized types are removed but not wrapped.

Copy source dictionaries if they must be reused in original form. Compatibility parsing is structural adaptation, not trust verification.

## Resolver calls and URL handling

`A2ACardResolver.__init__(httpx_client,base_url,agent_card_path='/.well-known/agent-card.json')` retains client; strips trailing slashes from base and leading slashes from card path. It performs no I/O.

`get_agent_card(relative_card_path=None,http_kwargs=None,signature_verifier=None)` selects configured path for a falsy override. An override `'/'` strips to empty and addresses base URL itself. Builds URL by string concatenation, calls `httpx_client.get(target_url,**http_kwargs)`, checks status, decodes JSON, logs fetched card data at INFO, parses, then optionally synchronously verifies the protobuf. Returns the card after successful verification.

Resolver kwargs can carry HTTPX headers and timeouts for discovery. These are separate from runtime `ClientCallContext`. There is no retry, signature verifier by default, or persistent discovery cache. The resolver never closes the HTTPX resource.

## Error boundary

| Failure | Result |
|---|---|
| HTTP status error | `AgentCardResolutionError` with `status_code` and chained cause |
| HTTPX request/network/timeout error | `AgentCardResolutionError`; discovery timeout is not `A2AClientTimeoutError` |
| JSON decoding | `AgentCardResolutionError` |
| Protobuf `ParseError` | `AgentCardResolutionError` |
| Other structural errors | Propagate unless matching one of the catches |
| Signature verifier | Ordinary exceptions propagate; verifier is inside the same try, so matching HTTPX/JSON/ParseError exceptions would be wrapped |

Logging includes card contents, but the resolver does not itself print credentials or add auth information. A fetched card can influence destination URL and auth header selection; supply a verifier when your application requires signed-card trust. Local source does not establish whether a destination is trustworthy.
