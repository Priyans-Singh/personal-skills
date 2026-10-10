# `auth/`: credential lookup and authentication hooks

Source: all three `a2a/client/auth` Python files, a2a-sdk 1.1.4. [Hooks](../hooks_knowledge.md) defines hook arguments; [core](../core_knowledge.md) defines ordering.

## `__init__.py`

Re-exports `AuthInterceptor`, `CredentialService`, `InMemoryContextCredentialStore`. No declared callables.

## `credentials.py`

`CredentialService` is abstract; async `get_credentials(security_scheme_name,context)` returns credential string or `None`. Applications implement acquisition, storage or refresh themselves.

`InMemoryContextCredentialStore.__init__` creates `_store: dict[session_id,dict[scheme_name,credential]]`. `set_credentials(session_id,security_scheme_name,credential)` creates session map if absent and inserts/replaces credential. `get_credentials` returns `None` without context or `context.state['sessionId']`; otherwise looks up exact session then exact scheme. Session-key type is not explicitly validated by the store.

Credentials last until overwritten or store object is discarded. No expiration, encryption, persistence, deletion API, locks, external identity validation or token refresh is implemented. The local session ID is a lookup key, not proof of caller identity, and differs from protocol context/task IDs.

## `interceptor.py`

`AuthInterceptor.__init__(credential_service)` retains the service. `before(args)` returns immediately if the card lacks top-level security requirements or schemes. For each requirement and scheme entry, awaits credential lookup. A nonempty credential with a declared scheme causes context/service-parameter mapping to be created if needed, then:

| Scheme | Destination |
|---|---|
| HTTP scheme equal to bearer, case-insensitive | `Authorization: Bearer <credential>` |
| OAuth2 or OpenID Connect | Same bearer header |
| API key whose location equals header, case-insensitive | Header named by scheme, value is credential |
| Other scheme, query/cookie key, mTLS | Skipped |

Returns immediately after installing **one** supported credential. It can overwrite an existing parameter under that name. It does not fulfill every scheme of a multi-scheme requirement, validate OAuth scopes, consult skill-specific security, acquire a token, check expiry, or refresh on a remote rejection. Missing credentials do not cause local refusal; the transport can send an unauthenticated request.

`after(args)` is a no-op. Credential-service exceptions propagate. Logs scheme names at DEBUG, not token values. Header parameters are later sent to the selected HTTP endpoint or lower-cased into gRPC metadata; they persist in a reused mutable context until callers change them. Use separate contexts/services where session isolation matters.

Initial card resolution bypasses this interceptor. Auth can be applied to extended-card retrieval through the existing client's ordinary hook chain.
