# `langchain/tools`

`__init__.py` re-exports Core `BaseTool`, `tool`, `InjectedToolArg`, `InjectedToolCallId`, and `ToolException`, plus LangGraph `InjectedState`, `InjectedStore`, and `ToolRuntime`. `tool_node.py` supplies backward-compatible LangGraph wrapper contracts: `ToolCallRequest`, `ToolCallWithContext`, and `ToolCallWrapper`; it imports ToolNode privately for legacy compatibility.

No tool executes merely through these modules. Tool schema/execution belongs to Core; state/store injection, tool dispatch, parallelism, and ToolNode runtime behavior belong to LangGraph. LangChain’s agent factory composes that node with routing and middleware.
