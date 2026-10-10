---
name: langchain-library-skill
description: Work accurately with the installed LangChain 1.3.18 package—agents, middleware, chat-model and embedding factories—by tracing its local source and LangGraph/Core boundaries. Use for LangChain implementation, debugging, or architecture questions; not generic LLM guidance.
metadata:
  short-description: Trace LangChain package execution
---

# LangChain Library Skill

Use this skill when work depends on how the locally installed `langchain` package actually behaves. It is source-grounded for LangChain 1.3.18 at `.venv/lib/python3.11/site-packages/langchain`; do not assume details apply to other versions.

## Reference routing

Read only the reference matching the package area in scope:

- [package root](references/root.md)
- [agents](references/agents.md)
- [chat models](references/chat-models.md)
- [embeddings](references/embeddings.md)
- [messages](references/messages.md)
- [rate limiters](references/rate-limiters.md)
- [tools](references/tools.md)
- [typing marker](references/py-typed.md)

## Working rules

Treat `langchain` as a composition facade. Confirm behavior in the installed source before making version-specific claims. Most model/message/tool semantics belong to `langchain_core`; graph execution, ToolNode behavior, and persistence belong to `langgraph`. Trace into those packages only to the needed boundary rather than duplicating them.

Distinguish construction from execution: `init_chat_model` and `init_embeddings` lazily import and instantiate integrations; provider I/O occurs later through the returned object. `create_agent` compiles a LangGraph and can execute tools only when the compiled graph is run.

When changing or diagnosing agents, identify state-schema ownership, middleware ordering, model/tool wrappers, the graph edge taken, structured-output strategy, and whether errors are propagated, retried, converted into ToolMessages, or handled by a fallback.

Treat shell execution, filesystem search roots, tool retries, model fallback, runtime-configurable credentials, PII redaction, and context summarization as explicit safety/data-retention choices. Do not imply sandboxing, idempotency, persistence, or provider compatibility that the selected middleware/integration does not establish.

For a deep source audit, inventory Python files and declared classes/functions first, then mechanically compare that inventory with the resulting explanation. Keep raw credentials out of output and do not invoke providers merely to inspect local implementation.
