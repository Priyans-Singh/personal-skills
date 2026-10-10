# `graph/`

Primary application authoring API. `state.py` exposes `StateGraph` and `CompiledStateGraph`: define state/reducers, add nodes/edges/conditional edges, then compile with optional checkpoint/store/cache. `message.py` provides `add_messages`, `MessagesState`, and legacy `MessageGraph`; messages append but same IDs replace. `_branch.py` resolves conditional routing and `_node.py` builds runnable node specs. `ui.py` supports UI-message state operations. Prefer this package for custom orchestration.
