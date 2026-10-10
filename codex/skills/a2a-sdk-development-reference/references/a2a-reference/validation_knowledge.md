# Evidence and verification boundaries

Inspected installed a2a-sdk **1.1.4**, Python 3.11, **2026-10-07**. This reference covers seven root folders and loose package-root files, excluding existing client/server references.

## What the inventory proves

The snapshot records all **61 non-cache source/support files** with SHA-256. The exact source path, lexical declaration name, line and AST kind identify **776 declarations**, including private/nested functions, properties, generated servicers and PYI stubs. Every file has a guide and every declaration has an index entry. Template signatures, annotated model fields, anonymous lambdas and generated runtime callables are handled separately from executable AST counts.

Whole-scope validation compares the actual installed folder/file set, hashes and declaration identities against the saved indexes. It also checks guide existence, local Markdown links, final newlines, trailing whitespace and code fences. Per-package validators additionally check narrative/index mappings and behavior fixtures. These checks make coverage auditable; they cannot prove every statement or every possible runtime branch correct. Read the implementation explanations and evidence together.

## Local behavior evidence

Parent checks exercised abstract/anonymous identity, repeated and empty extension headers, exact card lookup, Pydantic alias rules and every current helper family. Helper checks covered content variants, UUID creation versus message-ID backfilling, copied protobuf ownership, task validation, artifact/status updates, all stream-text branches and captured card-display output.

Utils/types verification passed **1,071 checks**, including source/declaration/field inventories, descriptor equality, message presence and oneofs, serialization, query/required-field validation, error shaping, signing, canonicalization, version handling and fake gRPC channel/registration behavior. It inventories **2,506 generated message callable entries**, separate from source declarations. Full assertions and limitations are recorded in [utils results](../a2a-utils/validation_results.json) and [types validation](../a2a-types/validation_knowledge.md).

Compatibility's independent [validation results](../a2a-compat/validation_report.json) passed **17,897 checks**, including **37 behavior fixtures**, using local conversions and HTTP mocks. Its legacy schema inventory includes 292 declared Pydantic fields, 51 protobuf message types, 165 protobuf fields and 10 RPC methods. [Execution boundaries](../a2a-compat/execution_boundaries_knowledge.md) distinguish actual translation behavior from operations delegated to current client/server/runtime dependencies.

Parent reran both delegated validators successfully. The final whole-scope audit passed for every folder and loose root file: **61 files, 776 declarations**. The parent-owned small-package audit also passed. All 84 Markdown documents across the new reference folders had resolving local links at final review. Client/server references are outside these totals.

## Reproduce

Run from the workspace root:

```sh
.venv/bin/python a2a-reference/validate_small_packages.py
.venv/bin/python a2a-reference/validate_scope.py
.venv/bin/python a2a-utils/validate_reference.py
.venv/bin/python -B a2a-compat/validate_reference.py
```

Package behavior validators refresh their output-folder reports. The whole-scope and small-package validators only read files. Expected error logs from exercised negative cases do not indicate a failing run; the exit status and final report establish success.

## Limits

No live HTTP/gRPC peer, DNS resolution, cloud API, callback delivery, database engine, DDL or migration was exercised. gRPC, Alembic and SQLAlchemy are absent locally; their implementations were traced statically, with generated gRPC wiring exercised through local fakes. Compiled protobuf upb interiors are unavailable as Python source: descriptors, installed supporting Python runtime source and explicit local observations ground those sections. Credentials, remote authorization, persistence, task scheduling and deployment guarantees require integration-specific validation.

No SDK source was edited, dependencies installed or existing client/server guides rewritten. The visible delegated Codex sessions owned compatibility and utils/types; parent reviewed their output and documented the other folders and loose files. All runtime checks stayed local.
