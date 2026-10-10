# AgentCore SDK utility modules — working knowledge

`bedrock_agentcore._utils` is intentionally small, but it defines SDK-wide correctness and security rules. Do not copy its behavior casually: endpoint construction, parameter casing, namespace selection, waiting, and identity propagation are shared contracts.

## Endpoint selection: `_utils/endpoints.py`

`DEFAULT_REGION` resolves `AWS_REGION`, then `AWS_DEFAULT_REGION`, then `us-west-2`. `BEDROCK_AGENTCORE_DP_ENDPOINT` and `BEDROCK_AGENTCORE_CP_ENDPOINT` override the normal data/control-plane endpoints. Overrides are useful for supported AWS partitions or local test endpoints, but are still checked to ensure the hostname ends in `.amazonaws.com`, `.amazonaws.com.cn`, or `.api.aws`.

`validate_region(region)` accepts only AWS-style region strings and returns the unchanged value. `InvalidRegionError` is a deliberate SSRF boundary: interpolating a crafted region into a URL must never redirect signed calls. `_validate_endpoint_url(url)` is the second boundary; it validates the resulting host. `get_data_plane_endpoint(region)` produces `https://bedrock-agentcore.<region>.amazonaws.com`; `get_control_plane_endpoint(region)` produces the equivalent `bedrock-agentcore-control` host. Both honor their respective override. `get_gateway_mcp_endpoint(gateway_id, region)` additionally validates the gateway ID as a 1–63-character DNS label, then returns its `/mcp` endpoint. Bad IDs raise `InvalidGatewayIdentifierError`, not a network call.

## Polling: `_utils/config.py`, `_utils/polling.py`

`WaitConfig(max_wait=300, poll_interval=10)` configures synchronous wait helpers; both values must be at least one second. `wait_until(poll_fn, target, failed, wait_config, error_field='statusReasons')` repeatedly calls a zero-argument getter, returns its full response when `status == target`, raises `RuntimeError` on one of the terminal `failed` statuses (including `error_field`), and `TimeoutError` at the deadline. A missing `status` only logs a warning and keeps polling—avoid this helper for APIs that do not return status.

`wait_until_deleted(poll_fn, not_found_code='ResourceNotFoundException', failed=None, ...)` inverts the rule: it succeeds only when the getter raises botocore `ClientError` with the configured not-found code. Other client errors propagate; supplied failure statuses become `RuntimeError`; a resource that simply remains visible times out. Neither helper catches application errors from `poll_fn`.

## Namespace compatibility: `_utils/namespace.py`

`build_namespace_params(namespace, namespace_path)` encodes exactly one selection into service casing: exact `namespace` becomes `{'namespace': ...}`; hierarchical prefix becomes `{'namespacePath': ...}`. Supplying both, neither, or `*` raises `ValueError`. This distinction matters for Memory retrieval: a path is not a wildcard expression.

`resolve_namespace_templates(namespaces, namespace_templates, param_name='namespaces', new_param_name=None)` centralizes migration of control-plane strategy parameters. It returns the new value, or the deprecated old list with `DeprecationWarning`; both together are invalid. `resolve_namespace_prefix_deprecation(namespace_prefix, namespace)` does the comparable session-manager migration: old prefix emits a warning and is temporarily returned as `namespace`; both are invalid. See [memory_knowledge.md](memory_knowledge.md) for callers and service semantics.

## API-shape and observability helpers

`snake_to_camel(name)` converts valid snake_case to boto3 camelCase; names without `_` pass through. Invalid underscore/case shapes raise `ValueError`. `convert_kwargs(kwargs)` applies it to a mapping. `accept_snake_case_kwargs(method)` wraps a boto3 method: mixed spellings of the same parameter, such as `memory_id` plus `memoryId`, raise `TypeError` rather than silently choosing one.

`build_user_agent_suffix(integration_source=None)` returns `bedrock-agentcore/<installed-version>` and, when supplied, a sanitized lower-case integration annotation. It strips every character except alphanumeric, `-`, `_`, preventing header injection. Clients pass it as botocore `user_agent_extra`; it is telemetry, not authorization.

## Workload Access Token propagation: `_utils/identity_propagation.py`

`register_identity_wat_propagation(client)` subscribes `_inject_identity_wat_header` to botocore `before-sign` events for only `InvokeAgentRuntime`, `InvokeAgentRuntimeCommand`, `InvokeHarness`, and `InvokeGateway`. The handler reads `BedrockAgentCoreContext.get_workload_access_token()` and, if present, writes `X-Amz-Bedrock-AgentCore-Identity-WAT`; absent token is a no-op. Identity calls are intentionally excluded because Identity mints WATs rather than consuming them. Raw Gateway MCP HTTP calls bypass boto3 events, so callers must attach the header themselves. Identity lifecycle and context production are covered in [identity_knowledge.md](identity_knowledge.md).

## Coverage ledger

Files covered: `__init__.py`, `config.py`, `endpoints.py`, `identity_propagation.py`, `namespace.py`, `polling.py`, `snake_case.py`, `user_agent.py`. Private helpers are documented where they alter observable behavior.
