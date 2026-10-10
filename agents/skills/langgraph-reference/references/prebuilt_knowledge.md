# `prebuilt/`

Ready-made agent/tool components. `create_react_agent` builds a model-to-tools loop, but is deprecated in this installed version for new work in favor of `langchain.agents.create_agent`. `ToolNode` executes tool calls, supports parallel calls, validation, error policy, injected graph dependencies, and `Command` results; `tools_condition` routes model output to tools or `END`. `ValidationNode` validates arguments. Streaming tool-call transformers and human-interrupt payload contracts live in the remaining files.
