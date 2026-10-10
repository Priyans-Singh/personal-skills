# Bedrock AgentCore Payments: Internal Working Reference

Last inspected: 2026-09-19  
Source: installed `bedrock_agentcore.payments` package in this repository's `.venv`.

This reference explains the SDK as a payment protocol pipeline: provision payment infrastructure once, create a user instrument and bounded session, detect a HTTP 402 challenge, ask AgentCore to sign/pay exactly one supported challenge, attach the returned header, and retry the original request. It covers every installed module and callable.

## Mental Model

```text
control plane (usually provisioning time)
PaymentManager resource
  └─ PaymentConnector (vendor binding)
      └─ CredentialProvider (vendor secrets held by AgentCore)

data plane (agent runtime)
User -> PaymentInstrument (wallet / payment method)
     -> PaymentSession (expiry + spending limits)
     -> HTTP/MCP tool request
     -> 402 Payment Required (x402 or MPP challenge)
     -> PaymentManager.generate_payment_header(...)
     -> ProcessPayment service call: validates instrument, session and budget; signs/pays
     -> retry request with payment header
```

The five resources must not be confused:

| Resource | Ownership / purpose |
|---|---|
| Credential provider | A vendor credential container, such as Coinbase CDP or Stripe Privy. Its secrets are supplied during provisioning and should never be logged. |
| Payment manager | The top-level AgentCore control-plane resource; its ARN is fixed into a runtime `PaymentManager`. |
| Connector | Connects that manager to one provider/vendor. |
| Payment instrument | A user-specific usable wallet/method, made through a connector. |
| Payment session | A temporary authorization context: limits are enforced across payments and it expires. |

`PaymentClient` owns control-plane resource setup. `PaymentManager` owns data-plane user/session/payment actions. The similarly named classes do not interchange.

## Package Map and Public Imports

```python
from bedrock_agentcore.payments import (
    PaymentClient, PaymentManager, PaymentType,
    PaymentManagerStatus, PaymentConnectorStatus,
    parse_www_authenticate, extract_challenges, select_challenge,
)
```

The root exports the two clients, status/type enums, payment exceptions, and MPP parser/selector. Integration config, handlers, plugins and framework helpers require submodule imports.

| File / directory | Role |
|---|---|
| `client.py` | Control-plane resource lifecycle, vendor credential request construction, rollback orchestration. |
| `manager.py` | Data-plane instruments, sessions, payment execution, and x402/MPP header generation. |
| `mpp.py` | Safe, lenient parser and deterministic selector for MPP `WWW-Authenticate` challenges. |
| `_validation.py` | Permit2 allowance constraint guard. |
| `constants.py` | Service statuses, vendors, protocols, defaults, and MPP/X402 network preferences. |
| `integrations/handlers.py` | Tool-result adapters for generic/MCP/HTTP shapes. |
| `integrations/strands/` | Strands plugin and its tool responses. |
| `integrations/langgraph/` | LangGraph middleware, tools, typed error context. |

## Authentication and Request Setup

Both classes resolve region in the same sequence: explicit `region_name`, supplied boto session region, `AWS_REGION`, default boto session/config region, then `us-west-2`. Passing a conflicting explicit region and boto session region raises `ValueError`.

By default botocore signs requests with AWS SigV4. `PaymentManager` can instead use a static `bearer_token` or dynamic `token_provider`; supplying both is rejected. `_is_bearer_auth` identifies that mode. `_inject_bearer_token` is registered on the request path, removes/replaces auth with `Authorization: Bearer <token>`, and calls the provider per request to allow refresh. A blank, non-string, newline-containing token is rejected. With bearer authentication the service derives `userId` from the JWT `sub`, so `user_id` is optional on data-plane methods.

`agent_name` causes `_add_agent_name_header` to add `X-Amzn-Bedrock-AgentCore-Payments-Agent-Name` to every data-plane call. `_validate_and_resolve_region` implements the stated priority/consistency rule, and `_build_client_config` appends the SDK/integration user-agent suffix without discarding caller config. `PaymentManager` is explicitly not thread-safe: make separate instances for concurrent work.

## Provisioning: `PaymentClient` (`client.py`)

`PaymentClient(region_name=None, integration_source=None, boto3_session=None)` creates a `bedrock-agentcore-control` client using the SDK control-plane endpoint. `__getattr__` forwards only the allowlisted raw manager/connector methods, with snake_case keyword acceptance.

### Vendor input shape

The TypedDicts (`CoinbaseCdpConfigurationInput`, `CoinbaseCdpCredentials`, `StripePrivyConfigurationInput`, `StripePrivyCredentials`, `ConnectorCredentialProviderConfig`, `PaymentConnectorConfig`) document Python-side configuration only; they make no calls.

`_is_not_blank` identifies non-`None`, non-empty strings. `_safe_error_message` returns safe `ClientError` code/message and `ValueError` text, but redacts arbitrary exception details to avoid leaking credentials. `_build_provider_config_input` requires complete vendor credentials and converts snake-case application inputs to the service's camel-case union:

```python
{"coinbaseCdpConfiguration": {
  "apiKeyId": "...", "apiKeySecret": "...", "walletSecret": "..."
}}
# or
{"stripePrivyConfiguration": {
  "appId": "...", "appSecret": "...",
  "authorizationPrivateKey": "...", "authorizationId": "..."
}}
```

Never put vendor secrets in application logs or an agent prompt. Missing vendor fields fail locally before the service call.

### Lifecycle methods

| Method | Actual behavior |
|---|---|
| `create_payment_manager` | Creates top-level manager with name, description, authorizer type and optional role. Generates a client token. |
| `get_payment_manager`, `list_payment_managers` | Read manager / paginate manager summaries. |
| `update_payment_manager` | Changes supported mutable manager properties. |
| `delete_payment_manager` | Starts deletion of a manager resource. |
| `create_payment_connector` | Creates a connector under a manager with vendor type, credential provider config/ARN, and provisioning mode. Quick Create uses service/OAuth provisioning. |
| `get_payment_connector`, `list_payment_connectors` | Inspect one / paginate a manager's connectors. `get` exposes authorization URL only while consent is pending. The nested `get_connector_status` closures bind a manager ID so the generic waiter can poll that connector. |
| `update_payment_connector`, `delete_payment_connector` | Modify/delete connector lifecycle. |
| `_wait_for_status` | General poller for expected resource state; surfaces failed state or timeout. |
| `create_payment_manager_with_connector` | Convenience transaction-like workflow: manager → credential provider config → connector → optional readiness wait. If a step fails it rolls back resources already created; rollback failure is logged but the original failure remains primary. |

`PaymentConnectorProvisionMode.QUICK_CREATE` is special: the new connector enters `PENDING_AUTHENTICATION`, returns an authorization URL, and needs human OAuth consent. Do not use `wait_for_ready=True` before that consent; poll `get_payment_connector` for `READY` afterward.

## Runtime: `PaymentManager` (`manager.py`)

```python
manager = PaymentManager(
    payment_manager_arn="arn:aws:bedrock-agentcore:...:payment-manager/...",
    region_name="us-east-1",
)
```

Constructor validation requires nonempty ARN, validates credential-auth configuration, constructs `bedrock-agentcore` data-plane client, and fixes the ARN for all subsequent calls. Its `__getattr__` forwards the raw allowlisted data-plane APIs for advanced usage.

### Instruments and sessions

| Method | What it injects / returns |
|---|---|
| `create_payment_instrument` | Injects manager ARN and creates a user payment method through a connector. Type/details describe embedded wallet configuration. |
| `get_payment_instrument` | Retrieves an instrument and maps missing/inactive service errors to payment exceptions where applicable. |
| `list_payment_instruments` | Paginates instruments for one user/manager. |
| `get_payment_instrument_balance` | Requests balance for selected chain/token. It is a read, not a spend authorization. |
| `delete_payment_instrument` | Removes the user payment instrument. Treat as destructive. |
| `create_payment_session` | Creates temporary spending context from expiry minutes and limits such as `maxSpendAmount`; manager ARN is injected. |
| `get_payment_session`, `list_payment_sessions` | Inspect/paginate sessions for user/manager. |
| `delete_payment_session` | Ends/revokes session. Treat as destructive. |
| `process_payment` | Submits exactly one payment type/input plus manager/session/instrument/user. The service enforces validity, expiry and remaining budget. |

The exception taxonomy makes integration decisions readable: `PaymentInstrumentNotFound`, `PaymentSessionNotFound`, `InvalidPaymentInstrument`, `InsufficientBudget`, and `PaymentSessionExpired` all derive from `PaymentError`. `PaymentInstrumentConfigurationRequired` and `PaymentSessionConfigurationRequired` specifically signal missing plugin config, before any payment request.

### `generate_payment_header`: protocol decision flow

```text
payment-required request (HTTP 402 representation)
  -> validate required manager/session/instrument parameters
  -> MPP Payment WWW-Authenticate present?
       yes -> select MPP challenge -> ProcessPayment -> Authorization: Payment <credential>
       no  -> x402 payment payload -> choose accept for instrument's network
              -> ProcessPayment -> X-Payment / protocol header
```

The one public method accepts a normalized `payment_required_request` containing status, headers and body, plus payment session/instrument/user context. It detects protocol from the 402 rather than making callers select protocol.

| Helper | Why it exists |
|---|---|
| `_validate_input_parameters` | Rejects invalid/missing manager, request, session/instrument identifiers and related input before payment. |
| `_has_x402_payment_required` | Ensures an MPP-absent 402 really exposes a usable x402 offer. |
| `_get_instrument_network` | Reads instrument details to derive the actual wallet network; avoids paying a compatible-looking offer on the wrong chain. |
| `_generate_mpp_payment_header` | Extracts MPP challenges, selects one compatible nonexpired offer, calls `process_payment` once, and formats `Authorization: Payment <token>`. |
| `_extract_x402_payload` | Extracts x402 data from body and identifies its version. |
| `_determine_blockchain_type` | Maps the network identifier into the service's blockchain family. |
| `_select_accept_for_instrument_network` | Picks one advertised x402 `accept` offer based on wallet network and `NETWORK_PREFERENCES`; prevents arbitrary first-offer choice. |
| `_build_payment_header` | Encodes the returned crypto-x402 proof into the exact retry header. |

`validate_permit2_allowance_limit` is called for Permit2 inputs: omitted is allowed; supplied value must be a positive ASCII base-10 integer string of 1–78 digits, denominated in the asset's smallest unit. It blocks floats, signs, whitespace and zero rather than trusting service validation.

## 402 Is Not a Payment Yet

The SDK is designed to respond to a 402 from a **specific already-attempted request**. Do not infer a price from natural-language tool output, invent a payment requirement, or retry a different target with a generated credential. Reuse the originating method/URL/body and only add the header created for its challenge. A retry that returns 402 again means payment was rejected or cannot satisfy the offer; integrations stop bounded retries rather than spending indefinitely.

## MPP (`mpp.py`): Parse, Validate, Choose One Challenge

MPP uses `WWW-Authenticate: Payment ...` on HTTP 402 and a `Authorization: Payment <token>` retry. AgentCore `ProcessPayment` accepts exactly one raw challenge header, so selection is mandatory.

| Function | Deep behavior |
|---|---|
| `_split_outside_quotes` | Comma splitter aware of quotes and escapes; prevents comma-containing auth-param corruption. |
| `_unquote` | Removes surrounding quotes and unescapes `\"` / `\\`. |
| `_parse_auth_param` | Turns `key=value` into lowercased key and unquoted value; malformed fragments return `None`. |
| `_starts_new_auth_scheme` | Detects a non-Payment auth scheme in a combined header, so Bearer parameters are not accidentally appended to the MPP raw bytes. |
| `parse_www_authenticate` | Splits one header field into Payment challenges, preserves each exact raw header, accepts unknown parameters, and drops malformed required-field sets. Its nested `_flush` finalizes/validates one accumulated challenge at each scheme boundary. |
| `extract_challenges` | Case-insensitively scans 402 headers; handles repeated header values represented as strings or lists; retains server order. |
| `is_mpp_payment_required` | True only for a 402 with at least one valid MPP challenge. |
| `decode_challenge_request` | Base64url-decodes a challenge's `request` JSON; rejects illegal alphabet/encoding/JSON. |
| `_is_valid_challenge` | Requires `id`, `realm`, `method`, `intent`, `request`; permits only charge intent and supported EVM/Tempo/Solana methods. |
| `challenge_network` | Derives a concrete network for preference comparison, including aliases/default Solana behavior. |
| `_parse_expires`, `is_expired` | Parse RFC3339 and reject expired offers. An absent/unparseable expiry is handled according to selector validation. |
| `select_challenge` | Rejects no compatible offer with `MppChallengeSelectionError`; otherwise filters supported, nonexpired candidates and deterministically prioritizes configured network preferences then advertisement order. Nested `sort_key` implements that stable preference/index ordering. |

The parser purposefully preserves raw header bytes: an MPP challenge HMAC can bind to the opaque/request encoding, so reconstructing a semantically equivalent header could invalidate it.

## Constants (`constants.py`)

| Enum / constant group | Use |
|---|---|
| `PaymentManagerStatus` | Manager lifecycle status, including readiness/failure transitions. |
| `PaymentConnectorStatus` | Connector lifecycle; notably `PENDING_AUTHENTICATION` and `READY`. |
| `PaymentConnectorType` | Supported vendor connector types. |
| `PaymentConnectorProvisionMode` | Manual versus Quick Create provisioning. |
| `PaymentType` | Data-plane payment type such as `CRYPTO_X402` and MPP counterpart. |
| `PaymentsAuthorizerType` | Manager authorizer options, including AWS IAM and custom JWT/OAuth forms. |
| `DEFAULT_MAX_RESULTS` | Default pagination cap used by convenience methods. |
| MPP constants | Auth scheme, current/default version, supported intent/methods, network aliases/defaults and preference ordering used by parser/selector. |

## Framework-Independent Tool Response Handlers

`integrations/handlers.py` separates payment policy from each tool's result/input shape. `has_mpp_challenge` recognizes usable MPP headers.

`PaymentResponseHandler` is the common contract: `extract_status_code`, `extract_headers`, `extract_body`, `validate_tool_input`, and `apply_payment_header`. A handler must turn a tool result into the normalized 402 request and safely insert the retry header into that same tool's args.

| Handler | Data shape and behavior |
|---|---|
| `GenericPaymentHandler` | Handles generic tool content in dict/list/text/JSON forms. `_extract_content_array`, `_extract_text_from_block`, `_parse_json_or_dict`, and `_extract_payment_required_structure` normalize nested values; public extractors derive status/headers/body; apply method writes retry header. |
| `MCPRequestPaymentHandler` | Strictly validates MCP Gateway request shape. `_is_x402_payment_data`, `_response_headers`, `_is_payment_required` identify gateway 402/x402 data; extractors normalize result; apply method alters the upstream request header location. |
| `HttpRequestPaymentHandler` | Handles an `http_request` tool. `_parse_headers_string` accepts JSON or Python-dict-repr headers; extractors parse response; inherited/implemented apply puts retry header in request headers. |
| `get_payment_handler` | Chooses the specialized handler for known tool names, otherwise generic. |

Tool input validation is a safety boundary: a header must be applied only to an input with enough stable request identity to make a safe retry.

## Strands Integration

`AgentCorePaymentsPluginConfig` is a dataclass-like configuration boundary. `__post_init__` validates required identifiers and options; `update_payment_session_id`, `update_payment_instrument_id`, `add_to_allowlist`, and `remove_from_allowlist` mutate only the relevant runtime configuration. The allowlist constrains which tool names can automatically trigger payment handling.

`strands/tools.py` supplies tool protocol helpers: `validate_required_params` rejects absent/empty or unexpected arguments; `format_error_response` creates a Strands error ToolResult; `format_success_response` makes JSON success ToolResult.

### `AgentCorePaymentsPlugin` (`strands/plugin.py`)

The plugin installs lifecycle behavior around tool calls. `init_agent` connects it to the agent. `before_tool_call` applies pre-flight validation; `after_tool_call` inspects a result for 402. If a 402 is found, `_process_payment_required_request` uses the manager to make a header and signals a controlled retry with changed tool input.

| Method group | Precise role |
|---|---|
| `_check_payment_retry_limit`, `_increment_payment_retry_count` | Bound automatic 402 retries per tool use; prevents a rejected payment loop. |
| `_has_successful_signing`, `_mark_successful_signing` | Invocation-state guard against duplicating a successful signing attempt. |
| `_store_payment_failure_state` | Stores a structured failure for agent-level handling rather than silently swallowing it. |
| `_check_interrupt_retry_limit`, `_increment_interrupt_retry_count`, `_reset_interrupt_retry_count` | Bound/recover control-flow interrupt retries. |
| `_process_payment_required_request` | Validates configured session/instrument, generates header, applies it via handler, and decides retry/failure state. |
| `get_payment_instrument`, `list_payment_instruments`, `get_payment_instrument_balance`, `get_payment_session` | Agent-exposed read tools; no autonomous spend. |
| `http_request` | Agent-exposed request tool whose 402s are settled through plugin policy. |

## LangGraph Integration

`langgraph/tools.py` factory functions make tools that close over middleware: `make_http_request_tool`, `make_get_payment_instrument_tool`, `make_list_payment_instruments_tool`, `make_get_payment_instrument_balance_tool`, and `make_get_payment_session_tool`. They expose controlled request/read capabilities to the graph.

`langgraph/errors.py` provides `ErrorResolution` (the callback's explicit resolution outcome) and `PaymentErrorContext` (error, tool/payment context passed to caller policy).

### `AgentCorePaymentsMiddleware`

It wraps LangGraph tool execution rather than the LLM itself. Construction validates config and creates `PaymentManager`; `_build_tools` registers the helper tools.

```text
wrap_tool_call / awrap_tool_call
  -> normalize ToolMessage content
  -> guard checks: allowlist, retry budget, required config
  -> handler-specific 402 detection (fallback raw JSON detection when needed)
  -> possibly lazy-create auto session
  -> generate header, mutate the original tool args, invoke retry
  -> if retry is still 402: deterministic error/callback resolution
```

| Middleware helper | Role |
|---|---|
| `_prepare_for_handler`, `_get_handler`, `_fallback_detect_402`, `_detect_402` | Normalize result and robustly locate an eligible 402. Fallback is deliberately lenient but only used after canonical detection fails. |
| `_check_guards` | Early exits for tool not allowed, disabled payment, missing config, or retry safety state. |
| `_extract_payment_request` | Creates normalized request passed to `generate_payment_header`. |
| `_inject_payment_header`, `_inject_for_error_retry` | Safely mutate retry args; convert injection errors into ToolMessages. |
| `_check_retry_rejection` | Detects a second 402 after paid retry as rejection, not a new unlimited payment opportunity. |
| `_generate_payment_header`, `_create_auto_session` | Service call and lazy bounded session creation when `auto_session=True`. |
| `_is_async_callback` | Determines whether error policy needs await. |
| `_error_tool_message`, `_build_error_context` | Build deterministic agent-visible error and structured callback input. |
| `_handle_callback_resolution` | Interprets callback result: string becomes ToolMessage; `PROPAGATE` returns through; retry resolution raises to re-enter policy. |
| `wrap_tool_call`, `awrap_tool_call` | Sync/async main wrappers. |
| `_invoke_error_handler`, `_ainvoke_error_handler` | Sync/async user error callback and permitted retry handling. |

`get_payment_error_message` in `integrations/error_messages.py` maps known payment exceptions to deterministic messages. This prevents framework code from exposing arbitrary raw exception text to an LLM.

## Complete Callable Index

All source callable names are represented below; grouped entries share exactly the behavior described in their preceding sections.

| File | Callables |
|---|---|
| `_validation.py` | `validate_permit2_allowance_limit` — positive 1–78 digit allowance guard. |
| `client.py` | `_is_not_blank`, `_safe_error_message`, `_build_provider_config_input`, `__init__`, `__getattr__`, `_wait_for_status`, all manager/connector lifecycle methods, `create_payment_manager_with_connector`. |
| `manager.py` | constructor/auth/header/region helpers; all instrument/session CRUD; `process_payment`; `generate_payment_header`; x402/MPP selection/header helpers; raw forwarding. |
| `mpp.py` | all parsing, validity, expiry, network and selection helpers listed in the MPP table. |
| `integrations/config.py` | `__post_init__`, both ID updaters, `add_to_allowlist`, `remove_from_allowlist`. |
| `integrations/error_messages.py` | `get_payment_error_message`. |
| `integrations/handlers.py` | `has_mpp_challenge`; all base/generic/MCP/HTTP extract, validate and apply handlers; `get_payment_handler`. |
| `integrations/strands/tools.py` | `validate_required_params`, `format_error_response`, `format_success_response`. |
| `integrations/strands/plugin.py` | constructor, init/before/after hooks, all bounded retry/state helpers, payment processor, five agent tools. |
| `integrations/langgraph/tools.py` | all five `make_*_tool` factories. |
| `integrations/langgraph/middleware.py` | constructor; registration, normalization, detection, guards, request extraction, header injection, retry/callback, auto-session and sync/async wrapper helpers. `_FallbackHandler` supplies generic extractors when no specialized handler applies. |

## Operational Rules and Failure Modes

| Symptom | Meaning / response |
|---|---|
| Connector remains `PENDING_AUTHENTICATION` | Quick Create OAuth consent has not completed. Open its current authorization URL and poll again. |
| Header generation refuses to continue | Confirm status is 402, exact request fields are present, one configured session/instrument exists, and the challenge is supported/nonexpired. |
| MPP challenge parse/select failure | The offer may be malformed, expired, unsupported method/intent, or incompatible with wallet network. Do not choose a different arbitrary challenge. |
| Payment fails with insufficient budget | Session limits are the guardrail. Create/obtain a properly authorized session; do not auto-expand limits. |
| Paid retry is another 402 | Treat as payment rejection/offer mismatch. Integration retry limits intentionally stop repeated spending attempts. |
| Header added to wrong request field | Use `get_payment_handler` / framework integration; MCP and generic HTTP tools require different input placement. |
| Raw error appears in agent text | Use deterministic `get_payment_error_message` / tool error formatting, and keep credential-bearing exceptions out of prompts/logs. |

## Safe Baseline

1. Provision managers/connectors in a dedicated setup flow, not during agent execution.
2. Keep vendor credentials in a secret manager/environment used only by provisioning.
3. Create payment instruments per user and payment sessions with finite expiry and explicit spend limits.
4. Allow automatic payment only for a narrow tool allowlist and an originating 402 response.
5. Store the session/instrument IDs in authenticated user-scoped state, never model-generated text.
6. Preserve protocol challenge bytes and retry only the original request with the service-generated header.
7. Make rejected retry, expired session, invalid instrument, and budget exhaustion normal agent-visible outcomes—not silent retries.
