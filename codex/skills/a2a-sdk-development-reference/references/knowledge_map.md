# Complete A2A knowledge map

Bundled from the workspace's eleven A2A knowledge folders on 2026-10-07. These are reference sections within **one skill**, not independent module skills.

| Knowledge folder | Entry point | Contents |
|---|---|---|
| a2a-client | [index](a2a-client/index_knowledge.md) | All client root files, auth and transports |
| a2a-server | [overview](a2a-server/overview_knowledge.md) | Execution, queues, handlers, routes, stores, contexts and examples |
| a2a-auth | [navigation](a2a-auth/README.md) | User/anonymous identity and imports |
| a2a-compat | [navigation](a2a-compat/README.md) | Complete v0.3 package and protocol assets |
| a2a-extensions | [navigation](a2a-extensions/README.md) | Extension parsing and lookup |
| a2a-helpers | [navigation](a2a-helpers/README.md) | Value constructors/extractors and card display |
| a2a-migrations | [navigation](a2a-migrations/README.md) | Environment, helpers, revisions and generation template |
| a2a-types | [navigation](a2a-types/README.md) | Descriptors, static/generated/runtime surfaces |
| a2a-utils | [overview](a2a-utils/overview_knowledge.md) | Every utility file and supporting boundaries |
| a2a-root | [navigation](a2a-root/README.md) | Loose root source/configuration files |
| a2a-reference | [overview](a2a-reference/README.md) | Cross-module evidence and scope audit |

Local guide-to-guide links retain the folder layout. Installed-source links point to the original workspace. Examples, manifests, indexes and validators are retained where they support a module guide. Generated caches and reference-generation builders are excluded. Validation reports are evidence from their stated runs, not a claim that optional services were exercised while packaging this skill.

Use the module entry point to find the individual source file guide, then follow direct implementation dependencies as needed. For a cross-module flow, combine only the relevant guides. The client/server coverage counts and the remaining-package audit counts use their own scopes; do not conflate generated runtime callable counts with AST declaration counts.
