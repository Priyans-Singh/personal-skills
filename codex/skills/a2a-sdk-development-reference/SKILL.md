---
name: a2a-sdk-development-reference
description: Explain, implement, debug, or review Python Agent2Agent integrations using the full locally inspected a2a-sdk knowledge reference. Covers client, server, compatibility, auth, extensions, helpers, models, utilities, and schema tooling; excludes the unrelated legacy PyPI a2a scraper.
---

# A2A SDK Development Reference

One skill for the complete A2A knowledge collection. Read the relevant module guides on demand; do not load every guide or create a separate skill per module.

## Identity and source

The reference describes **a2a-sdk 1.1.4**, inspected **2026-10-07**. SDK release version, current wire version **1.0**, legacy wire version **0.3**, and AgentCard.version have different meanings. Confirm the target environment provides the official `a2a-sdk` distribution; the unrelated `a2a` package can collide with its namespace.

Original workspace: `/Users/priyanssingh/Desktop/Wedn-Demo`. Installed source: `.venv/lib/python3.11/site-packages/a2a/` beneath that workspace. When working elsewhere, locate the target installation and inspect affected implementation when versions/hashes differ. Never use the reference/source path as an application import path or automatically downgrade a target library to match this snapshot.

Read [knowledge map](references/knowledge_map.md), then only the relevant entry points below. Detailed source/callable indexes and validation evidence remain within each module folder.

## Route by execution boundary

| Work | Starting reference |
|---|---|
| Discovery, client construction, hooks, credentials, JSON-RPC/REST/gRPC requests | [client](references/a2a-client/index_knowledge.md) |
| Executors, contexts, queues, handlers, routes, stores, push delivery | [server](references/a2a-server/overview_knowledge.md) |
| v0.3 translations, client transports, server adapters, legacy schemas | [compat](references/a2a-compat/README.md) |
| User identity contract and anonymous identity | [auth](references/a2a-auth/README.md) |
| Extension headers, requested URI sets, card lookup | [extensions](references/a2a-extensions/README.md) |
| Value factories/extractors and Agent Card display | [helpers](references/a2a-helpers/README.md) |
| Current protobuf fields, presence, oneofs, stubs and generated runtime | [types](references/a2a-types/README.md) |
| Validation, error shaping, signing, task helpers, queues, telemetry and URL screening | [utils](references/a2a-utils/overview_knowledge.md) |
| Schema environment, revisions, DDL helpers and migration template | [migrations](references/a2a-migrations/README.md) |
| Pydantic base, database CLI, Alembic config and typing marker | [root files](references/a2a-root/README.md) |
| Cross-module inventory and validation limits | [reference overview](references/a2a-reference/README.md), [evidence](references/a2a-reference/validation_knowledge.md) |

## Execution distinctions to preserve

- Trace the selected interface/version from Agent Card through factory, transport, adapter, handler, executor, queues and storage as relevant. Compatibility adapters translate values; they do not supply missing current-protocol operations or replace core authorization/storage policies.
- Client message sends expose an async iterator even for ordinary responses. Polling configuration does not implement a polling loop; there is no general client retry/reconnect layer. Account for request/context mutation and shared HTTP connection ownership.
- Client request credentials use `ClientCallContext.service_parameters`; discovery uses separate resolver kwargs. Server identity, tenant and storage owner are distinct. Advertised security, identity objects and routing defaults do not themselves authenticate or authorize requests.
- Helpers construct/extract values; queues publish events; TaskManager aggregates snapshots; TaskStore persists them. Process-local ActiveTask/subscriber state is separate from durable storage. Check the specific queue/store/handler implementation before asserting cancellation, replay, isolation or consistency guarantees.
- Requested extensions are declarations, not automatic feature activation. Protobuf presence/oneofs and generated stubs differ from legacy Pydantic schemas; use each model's actual import surface.
- Card verification is opt-in. Key-provider trust/rotation, callback connection safety and credential refresh are integration responsibilities. Read signing/push validation implementations before asserting protection they do not provide.
- Migrations and root CLI are the schema control plane, separate from runtime CRUD. Documentation work does not authorize DDL, downgrades, external requests or resource changes.

## Evidence and verification

Bundled module references are a snapshot of the workspace knowledge folders. Their commands were authored for the original workspace and may refresh reports; use the original paths/environment when rerunning them. Read the relevant validation guide before invoking a validator, and inspect a validator's side effects when needed. Source inspection and local link/coverage checks are sufficient for a reference-only answer; optional dependencies or live infrastructure are not prerequisites unless the user's task needs them.

Source/callable inventories prove scope, not prose correctness or external-service guarantees. Use implementation links and qualified callable names for precise claims; distinguish local observations, static tracing and inference. No live peers or database migrations were used to create this skill.
