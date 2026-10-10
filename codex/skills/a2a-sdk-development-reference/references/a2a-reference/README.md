# A2A library references beyond server/client

Source-grounded inspection of installed **a2a-sdk 1.1.4**, Python 3.11, **2026-10-07**, at `.venv/lib/python3.11/site-packages/a2a/`. The source package has seven remaining root folders; each gets its own reference. Loose root files are also covered. `server` and `client` are excluded from new primary analysis; their existing guides remain untouched.

| Reference | What to learn |
|---|---|
| [auth](../a2a-auth/README.md) | Identity properties, anonymous scope, authentication versus authorization |
| [compat](../a2a-compat/README.md) | Full v0.3 compatibility package, transports/adapters, model/wire conversions, generated schema |
| [extensions](../a2a-extensions/README.md) | Header parsing, card lookup, requested versus implemented extensions |
| [helpers](../a2a-helpers/README.md) | Every protobuf value factory/extractor and card display |
| [migrations](../a2a-migrations/README.md) | Every schema helper/revision, engine lifecycle, template/README, online/offline behavior |
| [types](../a2a-types/README.md) | Generated wire values, fields/oneofs/presence, stubs, gRPC bindings |
| [utils](../a2a-utils/README.md) | Validation, errors, signing/canonicalization, queues, tasks, telemetry, URL policy |
| [package-root files](../a2a-root/README.md) | Pydantic base, migration CLI, Alembic logging, typing marker |

Read each README for file-by-file navigation. Behavioral guides explain implementation and practical usage; manifests/indexes verify source and declaration coverage. Generated classes/stubs/protobuf descriptors are documented as such, rather than mistaken for handwritten agent execution.

## Coverage

| Area | Non-cache source/support files | AST declarations, including stubs |
|---|---:|---:|
| auth | 2 | 6 |
| compat | 24 | 496 |
| extensions | 2 | 2 |
| helpers | 3 | 29 |
| migrations | 8 | 16 |
| types | 4 | 131 |
| utils | 14 | 91 |
| Loose root files | 4 | 5 |
| **Total** | **61** | **776** |

Declarations include classes, functions, methods, properties and nested closures. Utils' two lambdas and the generated protobuf runtime surface are inventoried separately. Current protobuf descriptors cover 51 message types including nested map entries, 190 fields, 15 oneofs, two enums and 11 RPC methods. These counts describe coverage, not branch correctness.

## Package boundaries

**types** defines current protobuf values; **compat** translates old Pydantic/protobuf wire representations to/from them. **helpers** constructs/extracts values; it does not send or persist them. **auth** supplies an identity contract, not credential validation. **extensions** collects requested extension identifiers, not implementation activation. **utils** implements common policies and transformations. **migrations/root CLI** form a schema administration control plane, separate from runtime server TaskStore I/O.

SDK release version 1.1.4 differs from current protocol version 1.0 and legacy version 0.3. Choose the interface/version advertised by AgentCard; do not copy a legacy example into current APIs without conversion.

## Verification

[Evidence and verification boundaries](validation_knowledge.md) explains coverage, behavior fixtures and integration limits.

[Whole-scope source inventory](source_inventory.json) includes every non-cache file under remaining root folders and every loose root file with SHA-256. Each package has its own evidence/checks, with runtime limitations reported. Parent-owned packages can be checked together:

```sh
.venv/bin/python a2a-reference/validate_small_packages.py
.venv/bin/python a2a-reference/validate_scope.py
.venv/bin/python a2a-utils/validate_reference.py
.venv/bin/python -B a2a-compat/validate_reference.py
```

No library source was changed, external API invoked, credentials reproduced, database migration run, or dependencies installed. Pure/local checks exercise helper and model semantics. Optional integrations need their own dependencies/environment before runtime validation.

## Delegated analysis

Two visible Codex helper sessions used the explicitly requested library-deep-dive skill: compatibility, and utils/types. Parent performed the other folders/root files and final evidence review. Helpers had disjoint output ownership and no further delegation. Their Herdr panes remain available for inspection after completion.
