# Validation and limitations

Run `.venv/bin/python a2a-utils/validate_reference.py` from workspace. Rebuild per-file/descriptor docs with `.venv/bin/python a2a-utils/build_reference.py`; authored overview/runtime guides remain separate.

```json
{
  "version": "1.1.4",
  "date": "2026-10-07",
  "counts": {
    "utils": {
      "non_cache_files": 14,
      "ast_declarations": 91,
      "classes": 26,
      "functions_and_async_functions": 65,
      "pyi_declarations": 0,
      "annotated_entries": 26,
      "anonymous_callables": 2
    },
    "types": {
      "non_cache_files": 4,
      "ast_declarations": 131,
      "classes": 56,
      "functions_and_async_functions": 75,
      "pyi_declarations": 104,
      "annotated_entries": 405,
      "anonymous_callables": 0
    }
  },
  "descriptor_counts": {
    "top_level_messages": 44,
    "all_messages_including_nested": 51,
    "fields_including_map_entries": 190,
    "oneofs_including_synthetic_optional": 15,
    "top_level_enums": 2,
    "enum_values": 12,
    "services": 1,
    "rpc_methods": 11
  },
  "checks_passed": 1071,
  "optional_grpc_available": false,
  "generated_message_callable_entries": 2506,
  "generated_channel_callable_assignments": 11,
  "limitations": [
    "No real grpc import or RPC: grpc absent; AST/fake-channel bindings verified.",
    "Compiled upb internals not available as Python source; descriptor/common runtime source and pure examples inspected.",
    "No DNS resolver/network push URL test, no cloud APIs, no external persistence/authorization guarantee.",
    "Coverage checks establish inventory and behavior evidence, not complete branch correctness of installed SDK."
  ]
}
```

Evidence beyond name matching: exact `(file,line,qualified-name,kind)` declaration multiset comparison; authored utility execution sections; raw decoded descriptor equality; source SHA-256 equality; concrete local presence/oneof/ownership/validation/serialization/signing/version/error assertions; all 11 fake-channel generated bindings/static forwarders/unimplemented skeletons and full registration dictionary. Every PYI repeated class/constructor/annotation is separately scoped. Markdown links, balanced code fences and whitespace checked. Full passed-check list is in validation_results.json. Anonymous lambdas and annotations are separately inventoried; compiled runtime callable inventory is separate from AST count.
