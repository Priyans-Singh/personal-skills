# OAuth/authentication and experimental tasks

This guide covers all `auth/**` and `experimental/**` source files in MCP 1.30.0. OAuth provider storage, human login, token issuance and revocation persistence are intentionally application responsibilities—not implemented by this SDK.

## Auth model and routing flow

```text
OAuth discovery/authorize/token/register/revoke routes → provider protocol
Bearer MCP request → TokenVerifier → AuthenticatedUser → ContextVar + principal
→ RequireAuth scope/resource check → session is bound to creating principal
```

Namespace-only files are `auth/__init__.py`, `auth/handlers/__init__.py`, `auth/middleware/__init__.py`, and `experimental/__init__.py`.

## Provider, settings and routes

`provider.py` contains Pydantic records `AuthorizationParams`, `AuthorizationCode`, `RefreshToken`, and `AccessToken`; each includes client/scopes/lifetime and optional RFC8707 resource/subject data. `RegistrationError`, `AuthorizeError`, and `TokenError` are frozen error-code/description exceptions. `TokenVerifier.verify_token` returns token or `None`; audience/resource verification is only as strong as the implementation. `OAuthAuthorizationServerProvider` requires application implementations for client lookup/registration, authorization, code/refresh/access storage and exchanges, plus revocation. `construct_redirect_uri` preserves old query pairs and appends non-null values. `ProviderTokenVerifier` is a compatibility adapter to `load_access_token`.

`settings.py`: `ClientRegistrationOptions` controls dynamic registration, secret expiry and scopes; `RevocationOptions` enables revocation. `AuthSettings` holds issuer/docs/options/scopes/resource URL/token resource validation. Validation without a resource URL is invalid. A resource URL with unset validation warns: it is currently not enforced but planned to default on in v3.

`routes.py`: issuer must be HTTPS except localhost/127.0.0.1 and may not have query/fragment. `create_auth_routes` builds metadata, authorize, token, optionally register/revoke; 4MiB limits apply. CORS is permissive for metadata/token/register/revoke (and outermost so 413 has CORS), deliberately absent from redirect-based authorize. `build_metadata` advertises code+refresh, PKCE S256 and basic/post secret methods. `build_resource_metadata_url` / `create_protected_resource_routes` implement RFC9728 well-known protected-resource discovery.

## Endpoint handlers

- `handlers/metadata.py`: `MetadataHandler` and `ProtectedResourceMetadataHandler` return Pydantic JSON with one-hour public cache.
- `handlers/authorize.py`: request model supports authorization code plus PKCE S256. `AuthorizationHandler.handle` reads GET query/POST form; unknown client/invalid redirect returns direct 400, but valid redirect context receives a redirect carrying OAuth error/state. It validates registered redirect/scopes, makes `AuthorizationParams`, delegates human/third-party flow to provider and redirects to provider-returned URL. Provider errors follow OAuth errors; unexpected errors become `server_error`. Helper `best_effort_extract_string` does no coercion; `AnyUrlModel` validates fallback URLs.
- `handlers/token.py`: discriminated code/refresh request models. `TokenHandler` authenticates client first, parses form, checks allowed grant, verifies code ownership/expiry/redirect binding/PKCE SHA-256 URL-safe base64, or refresh ownership/expiry/requested-scope subset, then delegates exchange. It emits Pydantic JSON success/error with `Cache-Control: no-store` and `Pragma: no-cache`. Resource-indicator matching is left to the provider.
- `handlers/register.py`: only routed when enabled. It validates OAuth client metadata, creates UUID ID plus random secret unless auth is `none`, constrains scopes, requires code+refresh grants and code response type, persists through provider and returns 201; registration errors return 400.
- `handlers/revoke.py`: authenticates client, finds access/refresh (hint changes preference), revokes only client-owned token yet returns success for missing/foreign tokens per RFC7009. No-store headers apply.
- `errors.py — stringify_pydantic_error` combines locations/messages. `json_response.py — PydanticJSONResponse.render` serializes Pydantic/URL objects safely.

## Middleware

`bearer_auth.py`: `AuthenticatedUser` makes client ID the Starlette username. `authorization_context` creates `{client_id, issuer, subject}` identity used by HTTP/SSE to bind a session. `BearerAuthBackend` only handles a Bearer header, verifies it and can normalized-compare token resource URL. `RequireAuthMiddleware` demands authenticated user and all required scopes; it writes 401 invalid-token or 403 insufficient-scope with Bearer `WWW-Authenticate`, optionally resource metadata. `auth_context.py` sets/resets a request-local access-token ContextVar; `get_access_token` returns it or `None`. `client_auth.py — ClientAuthenticator` reads form client auth, supports Basic/post/none, uses constant-time secret comparison and expiry checks, and raises `AuthenticationError`.

## Experimental tasks (deprecated)

All task APIs are experimental and deprecated: tasks were removed from the current spec and may return as a separate extension. Do not build a stable product dependency on them.

`task_scope.py` creates `<32hex scope>:<uuid>` IDs. Scoped operations require same scope; unscoped IDs are bearer-accessible but never listed. `task_support.py — TaskSupport` owns a store/queue/task result handler and AnyIO task group; `in_memory` is process-local and `configure_session` adds routing/scope except stateless.

`request_context.py — Experimental` checks task mode/capability, filters task-only tools, and `run_task` creates a task (scope-bound when possible), starts background work, completes returned result or records failure, and returns `CreateTaskResult`. Caller-supplied task IDs are deprecated.

`task_context.py — ServerTaskContext` exposes task state/cancel/status/complete/fail; sends status notifications. Its elicitation/sampling methods check client ability, set `input_required`, queue related-task requests, await `TaskResultHandler` routing, and restore `working` even on cancellation. `elicit_as_task` / `create_message_as_task` additionally poll client-created tasks.

`task_result_handler.py` receives `tasks/result` polls, drains queued messages, associates resolvers with original IDs, returns terminal result with related-task metadata, otherwise races store updates against new queue items. `route_response` / `route_error` wake the worker’s resolver. `session_features.py — ExperimentalServerSessionFeatures` wraps client get/result/poll task operations and task-wrapped elicitation/sampling. `lowlevel/experimental.py — ExperimentalHandlers` registers default handlers, enforces scope for get/result/cancel and manually filters lists without forwarding store cursor, avoiding cross-session ID disclosure.

## Security / consistency conclusions

The SDK does not store tokens or guarantee token rotation, code entropy, audience binding, or provider atomicity. Implement durable storage, expiration, revocation linkage, issuer/audience validation and secure callback routes yourself. Principal binding protects a stateful session from another credential, but endpoint protection does not cover FastMCP custom routes. Task in-memory state is non-durable and cancellation relies on cooperative task code.

