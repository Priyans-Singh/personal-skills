---
name: langgraph-reference
description: Use the checked-in source guide to explain or implement LangGraph 1.2.2 workflows, state graphs, agents, persistence, streaming, and runtime behavior. Use for LangGraph questions; not for generic LangChain-only work.
---

# LangGraph Local Reference

Use this skill when working with the LangGraph package inspected from this project's local virtual environment. The guide is source-grounded for `langgraph 1.2.2`; behavior in a different installed version may differ.

Start with [architecture.md](references/architecture.md) for execution flow and package boundaries. Use [module-map.md](references/module-map.md) to choose the right module. Consult [callable-index.md](references/callable-index.md) when tracing a public API or private helper; it inventories every Python file in the package.

For the separate AWS persistence-adapter package, read [langgraph_checkpoint_aws_knowledge.md](references/langgraph_checkpoint_aws_knowledge.md) and its [callable index](references/langgraph_checkpoint_aws_callable_index.md).

Prefer public imports such as `langgraph.graph`, `langgraph.prebuilt`, `langgraph.checkpoint`, and `langgraph.store`. Do not recommend `langgraph._internal` unless the request explicitly concerns implementation details. Checkpoint, cache, and store implementations bundled here are local-memory options unless explicitly identified otherwise; select an external backend package when durable or shared persistence is required.
