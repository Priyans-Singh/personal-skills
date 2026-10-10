# Bedrock AgentCore Identity: Internal Working Reference

Last inspected: 2026-09-19  
Source: installed `bedrock_agentcore.identity`, its backing `bedrock_agentcore.services.identity`, and directly coupled WAT propagation utility.

The `identity/` package is intentionally small: its public surface is decorators. The operational client is in `services/identity.py`. This is not unrelated generated-service material: `identity/auth.py` imports `IdentityClient` from that exact file, so it belongs in the Identity guide. Other `services/` modules, such as `resource_policy.py`, are not covered here and should be documented in a separate Services guide.

## Mental Model: Three Different Credentials

```text
AgentCore Runtime invocation
  -> Runtime mints/provides a Workload Access Token (WAT) in context
  -> agent asks Identity for an external OAuth access token or API key
  -> decorated function receives credential in an explicit keyword argument
  -> agent calls external resource

AgentCore Runtime -> downstream AgentCore Runtime/Gateway
  -> WAT from context
  -> X-Amz-Bedrock-AgentCore-Identity-WAT header
  -> downstream verifies and extends workload identity chain

AWS execution role -> external OIDC-aware service
  -> STS GetWebIdentityToken JWT
  -> function receives AWS-signed JWT
```

| Credential | What it authenticates | How it is obtained |
|---|---|---|
| Workload Access Token (WAT) | The AgentCore workload and downstream AgentCore identity chain | Runtime supplies it in `BedrockAgentCoreContext`; local development can request it through Identity. |
| OAuth2 access token | A resource represented by an Identity OAuth credential provider | `IdentityClient.get_token` requests/caches/authorizes it using WAT. |
| API key | A resource represented by an Identity API-key credential provider | `IdentityClient.get_api_key` requests it using WAT. |
| IAM JWT | An external OIDC-validating service that trusts AWS federation | Direct STS `GetWebIdentityToken`; it does not use `IdentityClient`. |

WAT is not an OAuth access token and should not be sent as an external API bearer credential. OAuth/API-key decorators retrieve separate resource credentials. Identity itself issues/uses WAT and must not receive a propagated WAT header.

## Public Surface and File Boundaries

```python
from bedrock_agentcore.identity import (
    requires_access_token, requires_api_key, requires_wat,
)
# `requires_iam_access_token` exists in auth.py but is not re-exported at package root.
from bedrock_agentcore.identity.auth import requires_iam_access_token
from bedrock_agentcore.services.identity import IdentityClient, TokenPoller
```

| File | Role |
|---|---|
| `identity/__init__.py` | Re-exports the three standard decorators only. |
| `identity/auth.py` | Decorators, runtime/local WAT acquisition, callback URL/region/event-loop helpers. |
| `services/identity.py` | Actual high-level Identity control/data plane client and OAuth polling logic. |
| `_utils/identity_propagation.py` | Registers automatic WAT forwarding on eligible AgentCore boto3 invocations. |

## `requires_access_token`: OAuth2 Decorator Execution

```python
@requires_access_token(
    provider_name="github-provider",
    scopes=["repo:read"],
    auth_flow="USER_FEDERATION",
    into="access_token",
)
def list_repos(*, access_token: str):
    return call_api({"Authorization": f"Bearer {access_token}"})
```

Decoration time and call time differ:

1. Calling `requires_access_token(...)` validates no remote state; it returns `decorator`.
2. Decorating a function creates one `IdentityClient(_get_region())` in the closure.
3. Each function invocation calls closure `_get_token`, which obtains a WAT and awaits `client.get_token(...)`.
4. Returned token overwrites `kwargs[into]`; a caller-supplied value under that key is not preserved.
5. The wrapped target executes after token retrieval.

`auth_flow` is one of `M2M`, `USER_FEDERATION`, or `ON_BEHALF_OF_TOKEN_EXCHANGE`. It forwards scopes, optional resources/audiences, `force_authentication`, custom OAuth state/parameters, optional callback URL, an auth-URL callback, and optional custom poller directly to `IdentityClient.get_token`.

For an async target, `async_wrapper` awaits credential retrieval and target. For a sync target, `sync_wrapper` uses `asyncio.run` locally. If it is called while an event loop already runs (such as an AgentCore async runtime), it copies `contextvars` and performs `asyncio.run(_get_token())` in a short-lived worker thread. This preserves context—critically WAT context—while avoiding Python's “asyncio.run cannot be called from a running event loop” error. It is safe for compatibility, but making the decorated target async avoids the blocking wait.

## `IdentityClient` (`services/identity.py`): Backing Client

This file is part of Identity, not an optional parallel API. `auth.py` uses it for all Identity decorators.

`IdentityClient(region)` builds two boto3 clients, respecting `CP_ENDPOINT_OVERRIDE` and `DP_ENDPOINT_OVERRIDE`:

| Plane | boto3 service | Purpose |
|---|---|---|
| Control | `bedrock-agentcore-control` | Credential provider/workload identity lifecycle. |
| Data | `bedrock-agentcore` | WAT issuance, OAuth/API credential retrieval and consent completion. |

`__getattr__` only forwards an allowlist and accepts snake_case aliases. Forwarded control APIs are OAuth2/API key provider get/list/update/delete; forwarded data APIs are resource OAuth/API-key token calls and JWT/user-ID WAT calls. Unsupported names raise an informative `AttributeError` rather than becoming an accidental raw client proxy.

### Credential provider and workload identity lifecycle

| Method | Behavior |
|---|---|
| `create_oauth2_credential_provider(req)` | Passes supplied provider request to control plane. Provider name/config are later selected by OAuth decorator. |
| `create_api_key_credential_provider(req)` | Creates an external API-key provider. |
| forwarded get/list/update/delete provider APIs | Use `__getattr__`; no separate local validation beyond boto3 service model. |
| `create_workload_identity(name=None, allowed_resource_oauth_2_return_urls=None)` | Creates named workload identity. Omitted name becomes `workload-<8 hex>`. Callback allowlist defaults to empty. |
| `update_workload_identity(name, allowed_resource_oauth_2_return_urls)` | Replaces the allowed OAuth2 return URL list. This is a security boundary: callback URL must be pre-registered. |
| `get_workload_identity(name)` | Reads workload identity configuration. |

The payment credential provider CRUD methods in this file—`create_payment_credential_provider`, `update_payment_credential_provider`, `delete_payment_credential_provider`, `get_payment_credential_provider`, and `list_payment_credential_providers`—are Identity-owned credential storage operations used by the Payments control-plane flow. They are included because they live in the backing Identity client. `list_payment_credential_providers` validates `max_results` is 1–20 and otherwise passes optional pagination token transparently.

### WAT issuance

```python
response = client.get_workload_access_token(
    workload_name="my-agent", user_token="upstream-idp-jwt"
)
wat = response["workloadAccessToken"]
```

`get_workload_access_token(workload_name, user_token=None, user_id=None)` chooses one data-plane request:

| Inputs | Data-plane operation |
|---|---|
| `user_token` (takes priority, warns if user ID also supplied) | `get_workload_access_token_for_jwt(workloadName, userToken)` |
| only `user_id` | `get_workload_access_token_for_user_id(workloadName, userId)` |
| neither | raw `get_workload_access_token(workloadName)` |

`UserTokenIdentifier(user_token)` and `UserIdIdentifier(user_id)` are Pydantic value models for OAuth consent completion. `complete_resource_token_auth(session_uri, user_identifier)` maps exactly one to `{userToken: ...}` or `{userId: ...}` and sends it with the session URI. A different type raises `ValueError` before the service call.

### OAuth token acquisition and user consent

`get_token` is async because a user federation flow can wait minutes:

```text
get_resource_oauth2_token(provider, scopes, flow, WAT, ...)
  -> accessToken? return immediately
  -> authorizationUrl + sessionUri?
       call on_auth_url (await if coroutine)
       clear forceAuthentication after first attempt
       poll same request/session URI until accessToken exists
  -> neither? RuntimeError
```

It builds the wire request with required `resourceCredentialProviderName`, `scopes`, `oauth2Flow`, and `workloadIdentityToken`; includes optional resources, audiences, registered callback, forced login, custom state and custom parameters only when supplied.

`TokenPoller` is an abstract contract with `poll_for_token() -> str`. `_DefaultApiTokenPoller(auth_url, func)` polls every 5 seconds for up to 600 seconds. Its `poll_for_token` logs the authorization URL, invokes `func` for token availability, and raises `asyncio.TimeoutError` if the user never completes consent. Supply a custom `TokenPoller` to change polling/storage/control behavior without changing decorator code.

`get_api_key(provider_name, agent_identity_token)` is the simpler async data-plane path: it sends provider name + WAT to `get_resource_api_key` and returns the `apiKey` field. It does not implement interactive authorization handling itself.

## How Decorators Obtain WAT (`identity/auth.py`)

`_get_workload_access_token(client)` first reads `BedrockAgentCoreContext.get_workload_access_token()`.

```text
Runtime invocation: WAT exists in context -> use it
Local development: WAT absent -> _set_up_local_auth(client)
Docker runtime with WAT absent -> error explaining user-ID header requirement
```

`_set_up_local_auth` is deliberately developer-convenient and has filesystem side effects:

1. Reads project-local `.agentcore.json` if it exists.
2. Reuses `workload_identity_name` and `user_id`; creates missing workload identity and random 8-character user ID.
3. Attempts to write those values back to `.agentcore.json` (warns instead of failing if it cannot).
4. Calls `get_workload_access_token(workload_identity_name, user_id=...)` and returns `workloadAccessToken`.

This means decorator use on a local machine may create a cloud workload identity and write project config. Use an explicit setup process if that side effect is not acceptable.

`_get_oauth2_callback_url` selects the decorator's explicit callback first, otherwise `BedrockAgentCoreContext.get_oauth2_callback_url()`. `_get_region` uses `AWS_REGION`, then boto session region, then `us-west-2`. `_has_running_loop` probes `asyncio.get_running_loop` to choose the sync-wrapper strategy.

## Other Decorators

### `requires_api_key`

This mirrors `requires_access_token`, except closure `_get_api_key` obtains WAT and calls `IdentityClient.get_api_key`. It injects the returned string into `into` (default `api_key`). Its `async_wrapper` awaits the fetch; its `sync_wrapper` uses local `asyncio.run` or a context-propagating thread when an event loop is already live.

### `requires_iam_access_token`

This decorator is not root-exported. It is intentionally separate from AgentCore Identity:

```python
@requires_iam_access_token(
    audience=["https://external.example"],
    signing_algorithm="ES384", duration_seconds=300,
)
def call_external(*, access_token): ...
```

It validates a nonempty audience, algorithm `ES384` or `RS256`, and 60–3600 second lifetime at decoration time. Its nested `_get_iam_jwt_token(region)` creates STS client and calls `get_web_identity_token` with audience, algorithm, duration and optional tags. It returns `WebIdentityToken`; a `FeatureDisabledException` becomes a specific `RuntimeError` explaining that AWS IAM Outbound Web Identity Federation needs enabling. Async and sync wrappers inject the JWT under `into` then call the target. No `IdentityClient`, workload identity, OAuth provider, or client secret is involved.

### `requires_wat`

`requires_wat(into="identity_wat")` does **not mint** a WAT. Nested `_get_wat` reads it from runtime context and raises `ValueError` outside AgentCore runtime. Both wrappers insert it under `into`. Use it when code needs to pass WAT explicitly—especially raw HTTP/Gateway MCP requests—or to make an identity-chain dependency visible in a function signature.

## WAT Propagation (`_utils/identity_propagation.py`)

`register_identity_wat_propagation(client)` registers a `before-sign.bedrock-agentcore.<operation>` hook, with stable `unique_id`, for only:

- `InvokeAgentRuntime`
- `InvokeAgentRuntimeCommand`
- `InvokeHarness`
- `InvokeGateway`

At signing time `_inject_identity_wat_header(request, **kwargs)` reads the current context WAT and, when present, writes `X-Amz-Bedrock-AgentCore-Identity-WAT`. It is a no-op without WAT. Identity calls are deliberately excluded because Identity mints/consumes credential operations rather than extending a downstream workload chain.

This helper only covers boto3 operations. Gateway MCP uses raw HTTP, so application code must manually set the same header from `BedrockAgentCoreContext.get_workload_access_token()`.

## Complete Callable Index

| File | Callable | Use |
|---|---|---|
| `identity/auth.py` | `requires_access_token` | OAuth decorator factory; sees full flow above. |
| | `requires_iam_access_token` | STS JWT decorator factory. |
| | `_get_iam_jwt_token` | Nested STS token fetcher. |
| | `requires_api_key` / `_get_api_key` | API-key decorator and nested fetch. |
| | `requires_wat` / `_get_wat` | Runtime-context WAT decorator/read. |
| | all `decorator`, `async_wrapper`, `sync_wrapper` closures | Select wrapper at decoration time; retrieve/inject credential at call time. There are separate closures for each decorator. |
| | `_get_oauth2_callback_url`, `_get_workload_access_token`, `_set_up_local_auth`, `_get_region`, `_has_running_loop` | Callback selection, runtime/local WAT logic, local persistence/setup, region and event-loop detection. |
| `services/identity.py` | `TokenPoller.poll_for_token` | Abstract custom polling contract. |
| | `_DefaultApiTokenPoller.__init__`, `poll_for_token` | Store URL/poller and execute 5-second, 10-minute default consent polling. |
| | `IdentityClient.__init__`, `__getattr__` | Create two service clients / forward allowlisted raw APIs. |
| | OAuth/API provider create methods and forwarded CRUD | Control-plane credential provider lifecycle. |
| | `get_workload_access_token`, workload identity create/update/get, `complete_resource_token_auth` | Workload credential issuance/identity and consent completion. |
| | `get_token`, `get_api_key` | OAuth authorization/polling and API-key retrieval. |
| | all payment credential provider CRUD/list methods | Identity-side storage lifecycle used by Payments. |
| `_utils/identity_propagation.py` | `_inject_identity_wat_header`, `register_identity_wat_propagation` | Signing-time header injection and per-operation hook registration. |

## Failure Modes and Safe Defaults

| Symptom | Cause / response |
|---|---|
| OAuth decorator waits then times out | User did not complete consent. Expose the authorization URL via `on_auth_url`, use a suitable `TokenPoller`, and retain no token in logs. |
| Callback rejected or missing | Register callback URL on the workload identity; explicit decorator callback must match allowed list. |
| WAT missing in Docker/Runtime | Runtime was not invoked with needed user identity context. Follow error guidance; do not silently generate a substitute. |
| Local execution created identity/config unexpectedly | `_set_up_local_auth` is the fallback. Preconfigure `.agentcore.json` or use an explicit non-decorator setup path. |
| Sync function blocks async server | Sync wrapper waits for worker-thread credential fetch. Prefer decorating async functions in async agent code. |
| Downstream runtime lacks caller identity | Register WAT propagation on its boto3 client or manually attach header for raw Gateway HTTP. |
| Identity call sends WAT forwarding header | It should not. WAT propagation is only for downstream runtime/gateway invocation operations. |

Safe baseline:

1. Treat WAT, OAuth tokens, API keys, and IAM JWTs as separate credentials with separate destinations.
2. Use OAuth decorators for resource access; use `requires_wat` only for AgentCore identity-chain forwarding.
3. Register and validate exact OAuth callback URLs before enabling user federation.
4. Use short IAM JWT durations and exact audiences.
5. Never write tokens, provider secrets, raw authorization URLs with sensitive state, or arbitrary service errors into prompts/logs.
