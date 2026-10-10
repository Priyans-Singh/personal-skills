# A2A helpers reference

Inspected a2a-sdk **1.1.4**, `.venv/lib/python3.11/site-packages/a2a/helpers`, 2026-10-07.

This package constructs/extracts protobuf values and prints AgentCard summaries. It never sends messages, runs an agent, persists a Task, or fetches a URL/file merely because you constructed one.

- [Imports](init_knowledge.md).
- [All value factories, extraction functions and usage](proto_helpers_knowledge.md).
- [Card display](agent_card_knowledge.md).
- [Callable index](callable_index_knowledge.md), [coverage](coverage_knowledge.md).

Related: [types](../a2a-types/README.md) for protobuf fields/presence; [server TaskUpdater](../a2a-server/tasks_knowledge.md) for actually publishing events. Model construction and event publication are distinct steps.
