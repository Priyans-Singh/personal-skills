# Bedrock AgentCore Gateway: Internal Working Reference

Last inspected: 2026-09-20  
Source: the installed `bedrock_agentcore.gateway` package in this repository's `.venv`.

This is an implementation-first guide to every installed Gateway file and callable, including the optional Strands semantic-tool-search plugin and its README-described runtime requirements. Gateway is a managed MCP aggregation boundary: it exposes selected connector/server tools behind one MCP endpoint. This SDK manages that control-plane resource; it is not an MCP transport client.

## Mental Model

```text
application / IaC
  -> GatewayClient.create_gateway(...)              control plane: Gateway resource
  -> create_gateway_target(...) / target helper     control plane: target + exposed tools
  -> wait until Gateway and target are READY

MCP client -> Gateway MCP endpoint
  -> tool discovery or x_amz_bedrock_agentcore_search
  -> Gateway resolves target-prefixed tool name
  -> configured connector/server invokes its upstream target
  -> result returns through MCP
```

A **gateway** is the MCP-facing container. A **gateway target** attaches a tool source to that gateway: an AWS connector configuration, Lambda/API Gateway-compatible target, or an MCP server (the exact target schema is enforced by the Bedrock AgentCore control-plane service, not recreated in this wrapper). A target can expose several tools. Gateway gives each discovered tool a target-derived prefix, avoiding collisions: a `WebSearch` tool in target `amazon-web-search` appears to an agent as `amazon-web-search___WebSearch`.

The SDK uses only `bedrock-agentcore-control` here. Creating a target means the control-plane definition has been accepted; its connector becomes callable only after the target reaches `READY`. The `*_and_wait` methods make that asynchronous lifecycle explicit.

## Package Map and Imports

```python
from bedrock_agentcore.gateway import GatewayClient

from bedrock_agentcore.gateway.integrations.strands.plugins import (
    AgentCoreToolSearchPlugin,
)
from bedrock_agentcore.gateway.integrations.strands.plugins.agentcore_tool_search import (
    IntentProvider, StrandsIntentProvider,
)
```

| File | Role |
|---|---|
| `gateway/__init__.py` | Re-exports only `GatewayClient`. |
| `gateway/client.py` | Gateway/target control-plane facade, waiters, lookups, and three connector-specific target builders. |
| `integrations/__init__.py`, `integrations/strands/__init__.py` | Namespace markers; no behavior or exports. |
| `integrations/strands/plugins/__init__.py` | Public short import for `AgentCoreToolSearchPlugin`. |
| `.../agentcore_tool_search/plugin.py` | Strands before-invocation hook: derive intent, semantically search gateway, register just matching MCP tools. |
| `.../intent_providers/intent_provider.py` | Abstract intent-provider contract. |
| `.../intent_providers/strands_intent_provider.py` | Default LLM-based implementation, intentionally limited to user text. |
| plugin `README.md` | Installation, MCP connection, prerequisites, and intended per-invocation flow. |

The image under the plugin's `images/` directory is documentation artwork, not executable SDK behavior.

## `GatewayClient`: Construction and Raw Control-Plane Access

```python
client = GatewayClient(region_name="us-east-1")
```

`GatewayClient.__init__(region_name=None, integration_source=None, boto3_session=None)` chooses the supplied boto3 session or creates `boto3.Session()`. Region precedence is explicit argument, session region, then hard-coded `us-west-2`. `integration_source` is passed to `build_user_agent_suffix` and becomes botocore's `user_agent_extra`, for SDK/integration telemetry; it does not change Gateway semantics. The constructed `cp_client` is `session.client("bedrock-agentcore-control", region_name=..., config=Config(...))`.

`GatewayClient.__getattr__(name)` is a deliberately narrow raw-method proxy. It exposes only these boto3 control-plane operations and wraps each with `accept_snake_case_kwargs`, so Pythonic `gateway_identifier=` becomes the API's `gatewayIdentifier=`:

| Raw forwarded operation | Use |
|---|---|
| `create_gateway`, `get_gateway`, `list_gateways`, `update_gateway`, `delete_gateway` | Direct gateway CRUD. |
| `create_gateway_target`, `get_gateway_target`, `list_gateway_targets`, `update_gateway_target`, `delete_gateway_target` | Direct target CRUD. |

No other boto3 method is implicitly available. An unknown name raises `AttributeError`, even if the underlying client might possess it. Use `client.cp_client` deliberately when bypassing this SDK boundary is actually intended.

Raw direct CRUD returns when the API operation returns; it does not wait for `READY` or deletion. Arguments are service-model-defined, including gateway protocol, IAM role, target configuration, credentials, and pagination tokens.

## Lifecycle: Waiters and State Handling

Gateway creation/update treats `FAILED` and `UPDATE_UNSUCCESSFUL` as terminal failure. Target creation/update additionally treats `SYNCHRONIZE_UNSUCCESSFUL` as terminal failure. In success cases `wait_until` polls `get_gateway` or `get_gateway_target` until `status == "READY"`; it raises `RuntimeError` on those failed states and `TimeoutError` when the supplied/default `WaitConfig` exhausts its time budget. Defaults are documented by the methods as a 300-second maximum and 10-second polling interval.

| Callable | Exact sequence |
|---|---|
| `create_gateway_and_wait(wait_config=None, **kwargs)` | Converts snake-case request keys, calls control-plane `create_gateway`, reads returned `gatewayId`, polls that ID to `READY`. |
| `update_gateway_and_wait(...)` | Calls `update_gateway`, uses its returned `gatewayId`, then polls to `READY`. |
| `create_gateway_target_and_wait(...)` | Calls `create_gateway_target`; obtains `targetId` and derives gateway ID from `gatewayArn.rsplit('/', 1)[-1]`; polls `get_gateway_target(gatewayIdentifier, targetId)` to `READY`. |
| `update_gateway_target_and_wait(...)` | Same derivation/polling after `update_gateway_target`. Caller must pass target identity in update kwargs. |
| `delete_gateway_and_wait(...)` | Calls `delete_gateway`, takes returned `gatewayId`, then `wait_until_deleted(get_gateway(...))`. It returns `None`; successful delete response is not the guarantee—the subsequent absent-resource result is. |
| `delete_gateway_target_and_wait(...)` | Calls deletion, derives gateway ID and target ID from its response, then waits for `get_gateway_target` to become deleted. |

All six waiter methods call `convert_kwargs` themselves before invoking boto3. Do not assume a create/update response contains a full usable resource description: waiters return the later `get_*` result. The target waiters assume service responses include `gatewayArn` in slash-delimited form; malformed mocked responses can fail before polling.

## Connector Builders: What They Construct

These helpers build an MCP connector-shaped `targetConfiguration`, default it to gateway IAM-role credentials, merge caller `**kwargs` last, and call `create_gateway_target_and_wait`. The last merge is important: a caller can intentionally replace *any* built top-level field—including `targetConfiguration` or credentials—so it also can defeat helper assumptions.

### `create_knowledge_base_target`

```python
target = client.create_knowledge_base_target(
    gateway_identifier="gw-id-or-arn",
    knowledge_base_id="KB123",
    description="Retrieve approved product documentation.",
    retrieval_configuration={"vectorSearchConfiguration": {"numberOfResults": 5}},
)
```

`create_knowledge_base_target(gateway_identifier, knowledge_base_id, name=None, description=None, retrieval_configuration=None, parameter_overrides=None, wait_config=None, **kwargs)` exposes connector `bedrock-knowledge-bases`, enables only `Retrieve`, and configures that tool with mandatory `parameterValues.knowledgeBaseId`. It adds `retrievalConfiguration` only when a truthy object is supplied, adds description and per-parameter overrides only when truthy, and defaults target name to `kb-<knowledge_base_id>`. The helper's credential default is `[{'credentialProviderType': 'GATEWAY_IAM_ROLE'}]`.

`parameter_overrides` is passed unchanged; it is the service's mechanism for changing a tool parameter's visibility/description. It is not locally schema-validated. The Gateway role must be authorized for the underlying Knowledge Base work; service/IAM failures surface during target creation/synchronization or later invocation.

### `create_agentic_retrieve_target`

`create_agentic_retrieve_target(gateway_identifier, retrievers, model_arn, name=None, description=None, max_agent_iteration=None, parameter_overrides=None, wait_config=None, **kwargs)` exposes connector `bedrock-agentic-retrieve`, enables only `AgenticRetrieveStream`, and constructs:

```text
parameterValues
├─ retrievers: caller list (for example knowledgeBaseId plus service-supported overrides)
└─ agenticRetrieveConfiguration
   └─ foundationModelConfiguration.bedrock.modelArn: required model_arn
      └─ maxAgentIteration: included only if truthy
```

Default name is `agentic-retrieve-<unix-seconds>`, so repeated calls in a single second can collide. `max_agent_iteration=0` is omitted rather than sent; validation and legal retriever shapes are deferred to the service. It uses the same gateway-IAM-role credential default and wait path as the Knowledge Base helper.

### `create_web_search_target`

```python
target = client.create_web_search_target(
    gateway_identifier="gw-id",
    include_domains=["docs.example.com"],
    exclude_domains=["untrusted.example"],
)
# agent-facing name: amazon-web-search___WebSearch
```

`create_web_search_target(gateway_identifier, name=None, description=None, exclude_domains=None, include_domains=None, connector_version=None, parameter_overrides=None, wait_config=None, **kwargs)` exposes connector ID `web-search`, enables `WebSearch`, defaults name to `DEFAULT_WEB_SEARCH_TARGET_NAME` (`"amazon-web-search"`), and uses gateway-IAM-role credentials.

It **always** sends `configurations: [{'name': 'WebSearch', 'parameterValues': {}}]`, even without filters. This is a service-specific necessity: an absent `parameterValues` makes the service discard the configuration before validation, producing “Connector configurations must not be empty.” An empty object is valid.

Domain behavior is intersection/union-safe rather than merely cosmetic:

| Input | Builder behavior | Invocation consequence |
|---|---|---|
| `exclude_domains` | Writes `parameterValues.domainFilter.exclude`; up to 100. | A result excluded by target or caller list is removed. Callers can narrow results, never relax the target deny list. |
| `include_domains` | Writes `domainFilter.include`; up to 100. | Result must appear in every include list. Caller and target lists intersect; disjoint lists yield no results. Root domains match subdomains. |
| `include_domains` with no version | Pins source version `1.2.0`. | Target-level allow lists require that first supported connector version; the connector's default is older. |
| include list with `connector_version < 1.2.0` | Fails locally before API call. | Prevents an invalid target request. |
| explicit compatible/newer `connector_version` | Preserved as provided. | Service still owns final connector-version validation. |

The gateway service role needs `bedrock-agentcore:InvokeWebSearch` for this connector; an eventual caller needs `bedrock-agentcore:InvokeGateway` on the gateway ARN. There is no API key parameter for Amazon Web Search.

### Private web-search validators

`_checked_domains(argument, domains)` makes a list copy and raises `ValueError` if its length exceeds `_MAX_DOMAIN_FILTER_ENTRIES` (100). It does not validate domain syntax, deduplicate, normalize casing, or reject empty strings; that belongs to the caller/service.

`_connector_version_for_include_domains(connector_version)` returns `1.2.0` when no version was specified. Otherwise it compares parsed tuples and raises `ValueError` only when a recognizably numeric supplied version predates `1.2.0`.

`_version_tuple(version)` parses at most three dot-separated all-digit components, with missing pieces zero-filled—so `"1.2" == "1.2.0"`. Any non-numeric component or a fourth component yields `(inf,)`, deliberately sorting *above* known versions. Thus unrecognized versions are passed to the service instead of rejected locally; this favors forward compatibility but means `"bad-version"` is not validation success.

## Name Lookup and Pagination

`get_gateway_by_name(name, **kwargs)` converts extra snake-case kwargs, discards an incoming `nextToken`, then pages `list_gateways`. It compares exact `item['name']` equality, stops at the first match, and calls `get_gateway(gatewayIdentifier=item['gatewayId'])` to return the full object; it returns `None` if pages end. It intentionally does not return the potentially abbreviated list item.

`get_gateway_target_by_name(gateway_identifier, name, **kwargs)` is the target analogue: it removes caller `nextToken`, force-sets `gatewayIdentifier` (overriding any duplicate in kwargs), pages `list_gateway_targets`, exact-matches name, and returns `get_gateway_target` for the first match or `None`. Both helpers have no duplicate-name resolution beyond first service ordering, so treat names as a convenience lookup, not a unique ID guarantee unless your provisioning policy makes them unique.

## Strands Semantic Tool Search Plugin

The plugin solves a scale problem: loading every gateway tool into an agent's context can be expensive and confusing. It does **not** call MCP `list_tools`. Instead, before every agent invocation it turns recent user intent into a query for the Gateway built-in `x_amz_bedrock_agentcore_search` tool, then dynamically registers only returned tools.

```text
Strands BeforeInvocationEvent
  -> `IntentProvider.derive_intent(event.messages, model=event.agent.model)`
  -> empty? leave no prior dynamic tools and return
  -> MCPClient.call_tool_sync(name="x_amz_bedrock_agentcore_search",
                              tool_use_id="intent-search", arguments={"query": intent})
  -> parse tool definitions from structuredContent or JSON text content
  -> MCPTool -> MCPAgentTool -> agent.tool_registry.register_tool
  -> parent agent invokes model with just those dynamically registered tools
```

The README requires an AgentCore Gateway with semantic search enabled, registered tools with descriptions, AWS credentials permitted to access it, the optional package install `pip install 'bedrock-agentcore[strands-agents]'`, and an MCP client connected to the gateway MCP endpoint. It illustrates `mcp_proxy_for_aws.client.aws_iam_streamablehttp_client` with AWS service `bedrock-agentcore`, followed by `mcp_client.start()` or `with mcp_client:`. Constructing the plugin does not start the MCP client.

### `AgentCoreToolSearchPlugin`

`AgentCoreToolSearchPlugin.__init__(mcp_client, intent_provider=None)` stores the required connected Strands `MCPClient`, uses `StrandsIntentProvider()` when no strategy is supplied, and initializes `_loaded_tool_names` as a set. The class name used by Strands is fixed as `agentcore-tool-search-plugin`.

Its `tools` property returns `[]` deliberately: static plugin tool enumeration is empty because tools appear only through its hook.

`on_before_invocation(event)` is decorated with Strands `@hook` and performs this exact safety/replacement behavior:

1. Reads `event.messages` or `[]`, derives intent using the **parent agent's model** argument (unless provider chooses otherwise).
2. Removes every name previously loaded by this plugin directly from `event.agent.tool_registry.registry`, then clears the set. This prevents stale intent tools persisting into a later turn.
3. If intent is empty, returns now—meaning the invocation proceeds with static tools only.
4. Synchronously calls the Gateway search tool with constant `tool_use_id="intent-search"` and `{"query": intent}`.
5. Converts results via `_build_tools_from_search_result`. A search exception is logged and swallowed; the parent agent still runs, without dynamic tools.
6. For each resulting tool, preserves a static/non-dynamic tool of the same name: if its name is already registered but not in this plugin's tracked set, it skips it. Otherwise it registers and tracks it. Individual registration failures are likewise logged and skipped.

Direct dictionary removal is scoped only to `_loaded_tool_names`; it cannot remove a static name it never registered. But plugin-owned tools with an identical name to a newly registered static tool are a potential registry-ownership edge case. Tool names returned by Gateway should be trusted only within the gateway security boundary.

`_build_tools_from_search_result(result)` returns `list[MCPAgentTool]`, never raises for missing/malformed outer result. It accepts only a dict result. It prefers `result['structuredContent']['tools']`; otherwise scans `result['content']` blocks for a dict block's `text`, JSON-decodes it, and uses its `tools`. Invalid JSON/text is skipped. For every dict tool definition containing `name`, it creates `mcp.types.Tool(name, description=default-empty, inputSchema=default-empty-object-schema)`, then wraps it in Strands `MCPAgentTool` bound to the plugin's same MCP client. It does not validate duplicate names, description quality, JSON Schema correctness, or tool execution permissions.

### Intent-provider contract and default implementation

`IntentProvider` is an abstract base class. Its abstract `derive_intent(messages: list[dict], model=None) -> str` must return a concise plain-text intent, or `""` if it cannot determine one. A custom provider may be deterministic, policy-filtered, or use another model; the plugin uses no other provider method.

`StrandsIntentProvider.__init__(message_window=5, model=None, system_prompt=INTENT_SYSTEM_PROMPT)` stores a recent-message limit, optional explicit classifier model, and classifier prompt. The prompt asks for a one-sentence task type, without specifics, and only the description as output.

`StrandsIntentProvider.derive_intent(messages, model=None)` takes at most the last `message_window` records. Empty input returns `""` without an LLM call. Otherwise it builds a zero-tool `strands.Agent` with the configured system prompt. Model precedence is constructor's explicit model, then the parent model passed by plugin, then Strands' own default when neither exists. It invokes that classifier Agent on formatted text and returns `str(response).strip()`. Any exception—including model credentials, malformed message, or model failure—is logged and converted to `""`; this intentionally degrades to no dynamic tools rather than failing the parent invocation.

`_format_messages_for_prompt(messages)` is a privacy and prompt-scope control: it includes only `role == 'user'`, deliberately excluding assistant replies and tool results (which can contain PII/secrets). For user content represented as a list, it joins `text` from dict blocks only. Non-list content, non-dict blocks, empty text, and non-user roles contribute nothing. Newlines separate retained user messages. This means an all-string Strands message shape produces no intent under this implementation; use a custom provider if your integration uses a different shape.

## Per-File Callable Index

| File | Callables explicitly covered above |
|---|---|
| `client.py` | `GatewayClient.__init__`, `__getattr__`, six `*_and_wait` lifecycle methods, `create_knowledge_base_target`, `create_agentic_retrieve_target`, `create_web_search_target`, `get_gateway_by_name`, `get_gateway_target_by_name`, `_checked_domains`, `_connector_version_for_include_domains`, `_version_tuple`. |
| `plugin.py` | `AgentCoreToolSearchPlugin.__init__`, `tools`, `on_before_invocation`, `_build_tools_from_search_result`. |
| `intent_provider.py` | `IntentProvider.derive_intent`. |
| `strands_intent_provider.py` | `StrandsIntentProvider.__init__`, `derive_intent`, `_format_messages_for_prompt`. |
| every package `__init__.py` | Import/export boundaries documented in Package Map; empty initializers have no callables. |
| plugin `README.md` | Installation, MCP connection, prerequisites, semantic-search flow, model/custom-provider variants captured in the plugin section. |

## Operational Rules and Failure Modes

1. Wait after every gateway or target mutation before treating it as callable. `READY` is the usable-state contract; service accepted is not enough.
2. Preserve the target tool-name prefix in agent prompts and permissions reasoning. It disambiguates same-named tools from different targets.
3. A target helper's `**kwargs` win over generated defaults. That is powerful for role/credential customization but can silently replace the entire connector configuration.
4. Web-search domain allow lists are restrictive intersections. Test them with real intended domains; an allow-list mismatch commonly appears as zero results rather than an error.
5. Gateway semantic search depends heavily on target/tool descriptions. Poor descriptions make the plugin select poorly even when every tool works.
6. The plugin removes prior **dynamic** tools each invocation, catches search/classifier errors, and lets the agent proceed. Monitor logs/metrics if “agent answered without tools” is unacceptable; exceptions are intentionally not propagated.
7. Keep the intent model's cost/latency separate in planning: every nonempty invocation normally makes one classifier LLM call plus Gateway search before the main model call. Reusing `event.agent.model` avoids a second model configuration, not a second inference.
8. `StrandsIntentProvider` exposes only user text to the classifier, reducing leakage but sacrificing assistant/tool context. Replace `IntentProvider` only after consciously evaluating that privacy-relevance tradeoff.

## Safe Baseline

```python
from bedrock_agentcore.gateway import GatewayClient

gateway = GatewayClient(region_name="us-east-1")

# Gateway creation's required fields are service/IAM-specific; wait for readiness.
created = gateway.create_gateway_and_wait(
    name="research-tools",
    role_arn="arn:aws:iam::123456789012:role/AgentCoreGatewayRole",
    protocol_type="MCP",
)

web = gateway.create_web_search_target(
    gateway_identifier=created["gatewayId"],
    include_domains=["docs.example.com"],
    description="Search the approved product documentation.",
)

# `web` is a full target result observed in READY state.
```

Use the Gateway endpoint from the ready resource with an authenticated MCP client. Add the Strands plugin only when semantic search is enabled and an agent has enough potential tools that per-turn narrowing is beneficial.
