# Bedrock AgentCore Policy Engine Knowledge

This covers every installed file and callable in `bedrock_agentcore.policy`:

```text
policy/
├── __init__.py       public export: PolicyEngineClient
└── client.py         control-plane wrapper and orchestration helpers
```

The package manages AgentCore Policy Engine resources and Cedar policy definitions. It is not an in-process Cedar evaluator: API calls create, retrieve, generate, or delete remotely managed policies. Enforcement/evaluation is a separate service integration concern.

## Mental model

```text
Policy engine (a container / lifecycle boundary)
  ├── policy (a Cedar definition or generated-asset reference)
  └── policy generation
        natural-language content + resource → generation job → generated assets
                                                    └── selected asset → policy
```

All calls go to one boto3 client: `bedrock-agentcore-control`. There is no runtime/data-plane client in this package.

## `__init__.py`: public API

`from bedrock_agentcore.policy import PolicyEngineClient` imports and exports the one public class. It performs no client creation or network work.

## `client.py`: `PolicyEngineClient`

### Construction: `PolicyEngineClient.__init__(region_name=None, integration_source=None, boto3_session=None)`

Uses the supplied boto3 session or creates a default `boto3.Session()`. Region selection is `region_name`, then `session.region_name`, then `us-west-2`. It makes a `bedrock-agentcore-control` client with a `Config(user_agent_extra=...)` identifying the AgentCore SDK and optional sanitized integration source. It saves `region_name` and `integration_source`; the log message reports `cp_client.meta.region_name`.

No resource is created and no credentials are verified at construction. Pass a prepared session for a chosen profile, assumed role, or custom botocore behavior.

Top-level keyword handling matches the Knowledge Base client: pass either AWS camelCase or valid snake_case (`policy_engine_id` → `policyEngineId`), never both. Conversion is shallow; fields inside `definition`, `content`, or `resource` dictionaries must already have the AWS service spelling/shape.

### Dynamic pass-through: `PolicyEngineClient.__getattr__(name)`

When an otherwise missing attribute is in the allowlist and exists on boto3's control-plane client, it returns that boto3 method wrapped so it accepts snake_case keyword arguments. Unknown names raise `AttributeError`, so the wrapper does not expose arbitrary `bedrock-agentcore-control` operations.

| Group | Dynamic callable | What it does |
|---|---|---|
| Engine lifecycle | `create_policy_engine`, `get_policy_engine`, `list_policy_engines`, `update_policy_engine`, `delete_policy_engine` | Create, inspect/list, change, and remove an engine. Raw creates/updates are asynchronous acceptance calls. |
| Policy lifecycle | `create_policy`, `get_policy`, `list_policies`, `update_policy`, `delete_policy` | Manage policies scoped to an engine. `definition` may be direct Cedar content or a generation asset reference depending on the API request. |
| Generation | `start_policy_generation`, `get_policy_generation`, `list_policy_generations`, `list_policy_generation_assets` | Create and observe a natural-language-to-policy generation job and enumerate its output assets. |

These remain boto3 APIs: callers handle pagination (`nextToken`), request validation, retry policy, and AWS exceptions. The dynamic wrapper changes key spelling only.

## Shared wait semantics

The concrete lifecycle helpers use shared `WaitConfig`, `wait_until`, and `wait_until_deleted`.

`WaitConfig()` defaults to 300 seconds maximum with a 10-second interval; both values must be at least one. `wait_until` polls immediately, returns the exact successful get response, raises `RuntimeError` when the resource reports a listed failed status, and raises `TimeoutError` otherwise at deadline. `wait_until_deleted` considers a `ClientError` with `ResourceNotFoundException` successful deletion.

For engine and policy lifecycle helpers, the failed set is `{CREATE_FAILED, UPDATE_FAILED, DELETE_FAILED}`. This is deliberately broad: a create wait can surface any of those terminal statuses, not just `CREATE_FAILED`.

### `create_policy_engine_and_wait(wait_config=None, **kwargs)`

Converts its top-level keywords, calls `create_policy_engine`, reads top-level `policyEngineId`, then polls `get_policy_engine(policyEngineId=...)` until its `status` is `ACTIVE`. It returns the full get response. Failed status produces `RuntimeError`; missing response keys/AWS errors propagate.

### `update_policy_engine_and_wait(wait_config=None, **kwargs)`

Calls `update_policy_engine`, gets the top-level returned engine ID, and uses the same `ACTIVE` polling and failed set. It confirms lifecycle readiness, not semantic equivalence of the new configuration.

### `create_policy_and_wait(wait_config=None, **kwargs)`

Calls `create_policy`, extracts top-level `policyEngineId` and `policyId`, and polls `get_policy(policyEngineId=..., policyId=...)`. It returns the full policy get response once `ACTIVE`. The policy's parent ID is taken from the create response, not inferred from caller input.

### `delete_policy_engine_and_wait(wait_config=None, **kwargs)`

Calls `delete_policy_engine`, extracts its top-level ID, and repeatedly gets that engine until the service says `ResourceNotFoundException`. It returns `None`. An observed failed status uses the shared default reason field, `statusReasons`; this differs from the Knowledge Base deletion helper's explicit `failureReasons` choice.

### `delete_policy_and_wait(wait_config=None, **kwargs)`

Same deletion pattern for one policy, using both top-level IDs returned by `delete_policy`. It returns only when subsequent `get_policy` says the resource is absent. Delete acceptance is not deletion completion.

## Generation orchestration

### `generate_policy_asset_and_wait(policy_engine_id, name, resource, content, client_token=None, wait_config=None, fetch_assets=False)`

This is the safest direct route from text to inspectable policy-generation assets:

1. Builds `start_policy_generation` request with AWS camelCase keys `policyEngineId`, `name`, `resource`, and `content`; it adds `clientToken` only when non-`None`.
2. Starts the generation and reads `policyGenerationId` from the result.
3. Polls `get_policy_generation(policyEngineId=..., policyGenerationId=...)` for `status == "GENERATED"`.
4. Treats `GENERATE_FAILED` and `DELETE_FAILED` as `RuntimeError` terminal failures; other nonterminal/unrecognized statuses can time out.
5. Returns the full get response. When `fetch_assets=True`, it calls `list_policy_generation_assets` once and mutates that returned result by adding `generatedPolicies`, containing `policyGenerationAssets` or `[]`.

`fetch_assets` is not pagination: if the service returns a `nextToken`, this helper does not fetch later pages. Use `list_policy_generation_assets` yourself for complete enumeration. Preserve generated assets for review; successful generation does not automatically create or activate a policy.

### `create_policy_from_generation_asset(policy_engine_id, name, policy_generation_id, policy_generation_asset_id, description=None, validation_mode=None, client_token=None)`

Builds this exact definition:

```python
{
    "policyGeneration": {
        "policyGenerationId": policy_generation_id,
        "policyGenerationAssetId": policy_generation_asset_id,
    }
}
```

It then calls raw `create_policy` with the engine ID, name, and definition. `description`, `validationMode`, and `clientToken` are omitted—not sent as null—unless supplied. `validation_mode` is passed through unchanged (the service values documented in its docstring are `FAIL_ON_ANY_FINDINGS` and `IGNORE_ALL_FINDINGS`). It returns the create response immediately; use `create_policy_and_wait` only if you are constructing a direct definition, or explicitly poll `get_policy` after this helper.

### `generate_and_create_policy(policy_engine_id, generation_name, policy_name, resource, content, description=None, validation_mode=None, wait_config=None)`

An opinionated end-to-end shortcut:

```text
generate_policy_asset_and_wait(fetch_assets=True)
  → take generatedPolicies[0]
  → create_policy_from_generation_asset(...)
  → return immediate create-policy response
```

It does **not** wait for the new policy to become `ACTIVE`, does not expose a generation `client_token`, does not validate/score assets, and does not try another asset. If generation produces no first-page asset it raises `RuntimeError` with the generation ID (or `unknown`). Use the two lower-level methods when humans or tests must choose among generated assets.

## Idempotent create-or-get operations

### `create_or_get_policy_engine(name, description=None, encryption_key_arn=None, tags=None, client_token=None, wait_config=None)`

Builds an engine create request with only non-`None` optional values and calls raw `create_policy_engine`. If successful, it waits for that ID to be `ACTIVE`. If boto3 raises `ClientError` whose exact error code is `ConflictException`, it assumes an existing same-name engine, calls `_find_policy_engine_by_name(name)`, and waits for the found ID to become `ACTIVE`.

Any non-conflict `ClientError` is re-raised. A conflict followed by no matching list result becomes `RuntimeError` chained from the original conflict. This is conflict recovery, not atomic name-based idempotency: concurrent creators and eventual consistency can still make lookup fail or choose an unexpected pre-existing same-name resource. A stable `client_token` should still be used when the AWS API supports the intended idempotency guarantee.

### `create_or_get_policy(policy_engine_id, name, definition, description=None, validation_mode=None, client_token=None, wait_config=None)`

The scoped equivalent for policies. It builds `create_policy` with required engine/name/definition and non-`None` options. On a successful create it waits for `ACTIVE`; on exactly `ConflictException` it calls `_find_policy_by_name(policy_engine_id, name)` and waits for the found policy. All other failures propagate; conflict + failed lookup raises `RuntimeError`.

It does not compare an existing policy's definition, description, or validation mode with requested values. “Get” means same name within the engine, not “ensure the desired definition is installed.” Decide separately whether a mismatch should be updated, rejected, or accepted.

### `_find_policy_engine_by_name(name)`

Private lookup used by conflict recovery. It invokes `list_policy_engines(maxResults=100)`, scans `policyEngines` for the first exact `name`, then follows `nextToken` until found or exhausted. It returns `policyEngineId` or `None`. It does not deduplicate, sort, filter server-side, or protect against same-name ambiguity.

### `_find_policy_by_name(policy_engine_id, name)`

Private policy counterpart. It invokes `list_policies(policyEngineId=..., maxResults=100)`, scans `policies`, follows `nextToken`, and returns the first exact-name `policyId` or `None`. Its scope is the supplied engine.

## Recommended operational sequence

```python
from bedrock_agentcore.policy import PolicyEngineClient
from bedrock_agentcore._utils.config import WaitConfig

policy = PolicyEngineClient(region_name="us-west-2")
engine = policy.create_or_get_policy_engine(
    name="payments-guardrails",
    client_token="<stable-create-token>",
    wait_config=WaitConfig(max_wait=600, poll_interval=5),
)

generation = policy.generate_policy_asset_and_wait(
    policy_engine_id=engine["policyEngineId"],
    name="refund-rules-v1",
    resource={"arn": "<protected-resource-arn>"},
    content={"rawText": "Allow refunds under the approved conditions."},
    fetch_assets=True,
)
# Review/select an asset deliberately; do not assume index zero is correct.
created = policy.create_policy_from_generation_asset(
    policy_engine_id=engine["policyEngineId"],
    name="refund-rules-v1",
    policy_generation_id=generation["policyGenerationId"],
    policy_generation_asset_id=generation["generatedPolicies"][0]["policyGenerationAssetId"],
    validation_mode="FAIL_ON_ANY_FINDINGS",
)
active = policy.get_policy(policy_engine_id=created["policyEngineId"], policy_id=created["policyId"])
```

In production, poll the final policy to `ACTIVE` before binding it to an enforcement path. This package has no combined “generate, create, and wait for policy active” method.

## Failure and safety rules

- `ClientError` is caught only by the two `create_or_get_*` helpers and only for exact `ConflictException`; every other AWS error remains intact.
- Wait helpers are blocking synchronous calls. Put them outside latency-sensitive request handlers or run them in an appropriate worker/thread model.
- Generated Cedar assets are proposals. Review resource scope, principal/action modeling, and validation findings before creating/enforcing them.
- Listing APIs are paginated. The private conflict lookups paginate; dynamic public `list_*` calls do not.
- Do not infer authorization from a successful generation/create response. IAM access to this control plane and authorization/enforcement at runtime are separate layers.

## Callable coverage checklist

Class and concrete methods: `PolicyEngineClient`, `__init__`, `__getattr__`, `create_policy_engine_and_wait`, `update_policy_engine_and_wait`, `create_policy_and_wait`, `delete_policy_engine_and_wait`, `delete_policy_and_wait`, `generate_policy_asset_and_wait`, `create_policy_from_generation_asset`, `generate_and_create_policy`, `create_or_get_policy_engine`, `create_or_get_policy`, `_find_policy_engine_by_name`, `_find_policy_by_name`.

Dynamic allowlisted callables: `create_policy_engine`, `get_policy_engine`, `list_policy_engines`, `update_policy_engine`, `delete_policy_engine`, `create_policy`, `get_policy`, `list_policies`, `update_policy`, `delete_policy`, `start_policy_generation`, `get_policy_generation`, `list_policy_generations`, `list_policy_generation_assets`.

`__init__.py` adds no callable beyond exporting `PolicyEngineClient`.
