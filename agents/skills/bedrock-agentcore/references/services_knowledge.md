# AgentCore service façades — Identity backing client and Resource Policies

`bedrock_agentcore.services` holds thin service-specific clients. The Identity-facing public decorators are documented in [identity_knowledge.md](identity_knowledge.md); this guide covers the actual backing client too, so no installed `services` callable is hidden.

## `services/identity.py`: imperative Identity client

`IdentityClient(region)` creates control-plane and data-plane boto3 clients, honoring the SDK endpoint overrides. It is the implementation layer used by higher-level Identity flows. `__getattr__` only forwards its narrow allowlists and wraps forwarded calls with `accept_snake_case_kwargs`: control-plane `get/list/update/delete_oauth2_credential_provider`, `get/list/delete_api_key_credential_provider`; data-plane `get_resource_oauth2_token`, `get_resource_api_key`, `get_workload_access_token_for_jwt`, `get_workload_access_token_for_user_id`. Unknown names are `AttributeError`, not unrestricted boto3 access.

`create_oauth2_credential_provider(req)` and `create_api_key_credential_provider(req)` forward full wire-shaped creation requests. `create_workload_identity(name=None, allowed_resource_oauth_2_return_urls=None)` creates an identity, generating `workload-<random>` if name is absent; `update_workload_identity(name, allowed_resource_oauth_2_return_urls)` replaces allowed callbacks; `get_workload_identity(name)` reads it.

`get_workload_access_token(workload_name, user_token=None, user_id=None)` selects JWT exchange when `user_token` exists (and warns if user ID also supplied), otherwise user-ID exchange, otherwise workload-only token minting. `complete_resource_token_auth(session_uri, user_identifier)` completes user authorization using exactly `UserTokenIdentifier(user_token)` or `UserIdIdentifier(user_id)` Pydantic model; any other type is rejected before API call.

`get_token(...)` is async OAuth access-token orchestration. It sends provider name, scopes, flow (`M2M`, `USER_FEDERATION`, or `ON_BEHALF_OF_TOKEN_EXCHANGE`), and workload identity token, plus optional resources/audiences/callback/state/custom parameters. A direct `accessToken` returns immediately. An `authorizationUrl` invokes optional sync or async `on_auth_url`, clears `forceAuthentication` for subsequent polls, retains returned `sessionUri`, then uses supplied `TokenPoller` or `_DefaultApiTokenPoller`. The default polls every 5 seconds for at most 600 seconds and raises `asyncio.TimeoutError`; a response with neither token nor auth URL is `RuntimeError`. `TokenPoller.poll_for_token()` is the abstract async extension point, while `_DefaultApiTokenPoller` supplies that implementation.

`get_api_key(provider_name, agent_identity_token)` retrieves and returns only the API-key string. Payment credential-provider CRUD is also here: `create_payment_credential_provider(name, credential_provider_vendor, provider_configuration_input)`, `update_payment_credential_provider(...)`, `delete_payment_credential_provider(name)`, `get_payment_credential_provider(name)`, `list_payment_credential_providers(next_token=None, max_results=None)`. List validates 1–20 before forwarding pagination. These store vendor credentials/configuration; see [payments_knowledge.md](payments_knowledge.md) for using them in payment flows.

## `services/resource_policy.py`: resource-based IAM policy CRUD

`ResourcePolicyClient(region)` creates the AgentCore control-plane boto3 client, respecting control-plane endpoint override. It manages resource policies that govern principals' access to Agent Runtime, Endpoint, and Gateway resources; it does not evaluate policies locally.

`put_resource_policy(resource_arn, policy)` accepts either a Python dictionary (JSON-serializes it) or already serialized JSON string, calls `put_resource_policy`, then parses and returns the service's stored `policy` as a dictionary. SDK-side serialization is syntactic only: malformed strings or invalid IAM semantics fail at the service.

`get_resource_policy(resource_arn)` calls get and returns parsed policy dict when the response contains `policy`; it returns `None` when that field is absent. Do not infer `None` means permission to proceed—the underlying service may instead raise authorization/not-found errors. `delete_resource_policy(resource_arn)` forwards deletion and returns raw boto3 response; a missing policy can raise `ResourceNotFoundException`.

## Coverage ledger

All `services` files: `__init__.py`, `identity.py`, `resource_policy.py`. Covered identity symbols include `TokenPoller`, `_DefaultApiTokenPoller`, `UserTokenIdentifier`, `UserIdIdentifier`, `IdentityClient`, all allowlisted forwarded operations, and every explicit method; all `ResourcePolicyClient` methods are covered.
