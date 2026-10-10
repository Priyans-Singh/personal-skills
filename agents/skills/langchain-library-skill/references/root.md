# `langchain` package root

Source baseline: LangChain 1.3.18. `langchain/__init__.py` only defines `__version__`; importing it does not initialize models, agents, or clients. The root is a facade over eight top-level entries: `agents`, `chat_models`, `embeddings`, `messages`, `rate_limiters`, `tools`, `__init__.py`, and `py.typed`.

The package owns composition. `langchain_core` owns base model, message, tool, runnable, embedding, and rate-limiter semantics. `langgraph` owns compiled state graphs, ToolNode, Send dispatch, runtime, store, and persistence. `langsmith.traceable` is used by agent creation. Provider integrations own credentials and remote requests.

Construction is not execution: factories construct provider objects locally; `create_agent` compiles a graph; provider I/O and tool execution occur only when those objects run.
