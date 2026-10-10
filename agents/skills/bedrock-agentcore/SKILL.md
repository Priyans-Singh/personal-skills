---
name: bedrock-agentcore
description: "Use Bedrock AgentCore SDK knowledge to implement, explain, troubleshoot, or review AgentCore Runtime, Memory, Payments, Identity, Gateway, Evaluation, Knowledge Base, Policy, or related SDK work. Load only the reference for the requested service."
---

# Bedrock AgentCore

Use the bundled source-grounded SDK references to make AgentCore work accurate and implementation-aware. This skill is automatically applicable to Bedrock AgentCore SDK/service requests, including deployment/runtime behavior, integrations, memory, payment authorization, identity, gateway, evaluation, knowledge base, policy, configuration, tools, utilities, and service clients.

## Reference routing

Read exactly the service reference needed by the request; read a second only when the requested execution path crosses services.

| Request area | Read |
|---|---|
| Runtime HTTP/ASGI, invocation context, headers, OpenTelemetry | [runtime.md](references/runtime.md) |
| Evaluation, datasets, spans, custom evaluators, CLI | [evaluation_knowledge.md](references/evaluation_knowledge.md) |
| Memory resources, events, strategies, namespaces, Strands memory | [memory_knowledge.md](references/memory_knowledge.md) |
| Payments, x402/MPP, payment sessions, Strands/LangGraph payment handling | [payments_knowledge.md](references/payments_knowledge.md) |
| OAuth, API keys, WAT, JWT and workload identity | [identity_knowledge.md](references/identity_knowledge.md) |
| Gateway resources, targets, MCP and integrations | [gateway_knowledge.md](references/gateway_knowledge.md) |
| Knowledge Base | [knowledge_base_knowledge.md](references/knowledge_base_knowledge.md) |
| Policy | [policy_knowledge.md](references/policy_knowledge.md) |
| Config bundle | [config_bundle_knowledge.md](references/config_bundle_knowledge.md) |
| AgentCore tool helpers | [tools_knowledge.md](references/tools_knowledge.md) |
| SDK utilities | [utility_knowledge.md](references/utility_knowledge.md) |
| Service clients and resource policy | [services_knowledge.md](references/services_knowledge.md) |

## Working rules

- Treat references as an inspected SDK snapshot, not an immutable cloud-service contract. For exact current behavior, repository-specific code, installed SDK version, CLI flags, AWS availability, or current pricing/limits, inspect the local environment or authoritative AWS documentation before asserting it.
- Lead with the service boundary and execution flow: control plane vs data plane, credentials/identity, request fields, lifecycle state, async/eventual-consistency behavior, and error handling.
- Preserve the distinctions documented in the references—for example event persistence versus memory extraction, WAT versus OAuth token, payment 402 detection versus actual payment settlement, and configuration versus runtime execution.
- Do not make cloud calls, provision resources, delete data, spend funds, or expose credentials merely to answer an explanation. Perform those actions only when the user explicitly requests an in-scope change.
- When implementing, use the reference to choose the intended SDK layer (`PaymentClient` vs `PaymentManager`, `MemorySessionManager` vs compatibility client, control vs data plane) and validate in proportion to risk.
- When a task spans components, state the handoff explicitly. Example: Runtime context supplies WAT → Identity retrieves resource credential → Gateway/HTTP call uses it.

## Reference maintenance

If a user asks to refresh this knowledge, regenerate the relevant guide from the installed source using `$library-deep-dive`; then replace the matching file in `references/` and retain its inspected-version note.
