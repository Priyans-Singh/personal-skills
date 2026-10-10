# Agents, middleware, and structured output (LangChain 1.3.18)

`create_agent` is the local high-level entry point. It accepts a model object or model string, tools, middleware, response format, schemas, checkpointer/store, interruption controls, cache/debug/name, then constructs and compiles a LangGraph `StateGraph`.

## Execution shape

`before_agent` runs once, followed by the per-turn `before_model -> model -> after_model` cycle. If the AI response has outstanding client-side tool calls, the graph emits a LangGraph `Send` per call to ToolNode; results usually return to another model turn. It ends on no calls, `return_direct`, completed structured output, or a permitted middleware jump. Before hooks run in registration order; after hooks run reverse. `wrap_model_call` and tool-call wrappers compose with the first registered wrapper outermost.

Regular callable/Core tools and middleware tools become a LangGraph ToolNode. Dict tools are provider-side tool descriptions bound only to the model. Unknown dynamically added client tools fail unless a tool-call wrapper resolves them. Default recursion limit is 9999.

## State and middleware

Middleware state schemas merge before caller schema; caller fields win conflicts. `OmitFromSchema` hides state from generated input/output shapes. `ModelRequest` is the mutable request envelope and `override()` produces adjusted requests. `ModelResponse` holds messages plus optional structured output. Hooks can return state updates; this does not itself persist state—checkpointing is the persistence boundary.

Sync/async execution requires compatible middleware hook implementations. A hook `jump_to` must declare `can_jump_to`; graph/resume/goto commands from a model wrapper are unsupported.

## Structured output

Raw schema input means `AutoStrategy`. The factory picks native `ProviderStrategy` when model profile/heuristic allows it, otherwise `ToolStrategy`. Native mode sends JSON-schema response format, joins text blocks, parses JSON, and validates Pydantic/dataclass/TypedDict with `TypeAdapter`; raw JSON-schema dict output is not locally validated. Tool mode builds synthetic structured tools, parses the selected tool call, and writes `structured_response`. Error policy can return feedback ToolMessages for retry or raise.

## Built-in policy implications

Shell middleware’s host/Codex-sandbox/Docker execution policy is the command boundary. File search resolves paths and constrains them to its configured root. Tool retry can duplicate non-idempotent effects. Fallback may route calls to another provider and strips incompatible Anthropic cache markers. PII middleware can mutate streaming deltas. Context editing/summarization deliberately remove or compress model context. Human-in-the-loop interruption needs a checkpointer for durable pause/resume.

## Subagents

Named nested agent tasks whose `lc_agent_name` differs from the parent are surfaced as typed sync/async subagent run streams. Unnamed nested graphs are excluded; a named ordinary nested graph inheriting agent configuration can be included.
