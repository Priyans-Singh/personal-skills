# `types/a2a_pb2.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/types/a2a_pb2.py`. SHA-256: `d0aac0be3a3b639b17be3f3c42ac2aab185a10e3d085f38c05410472769483ba`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
```

Generated import-time machinery validates protobuf runtime compatibility against generator 5.29.3, registers a2a.proto bytes into the default descriptor pool, builds message/enum descriptors, then builds top-level Python classes. The pure-Python descriptor branch sets loaded/serialized options and offsets. C-backed runtimes consume descriptor options directly. No handwritten AST classes/functions: runtime builders create them. Read the descriptor catalog below and the separate runtime surface reference.

The descriptor is proto3, package lf.a2a.v1, source name a2a.proto. External google.api annotations/client/field_behavior register extension types before descriptor load; Empty, Struct/Value, Timestamp implement direct model dependencies. Generator comments/offsets are metadata, not an extra service implementation.

## Public/constants/type aliases and module initialization

```python
_sym_db = _symbol_database.Default()
```

`DESCRIPTOR` is the complete serialized schema decoded below, not omitted from coverage.

```python
_globals = globals()
```

## Declarations and execution

## Descriptor model/field/service catalog

See [complete descriptor catalog](descriptor_knowledge.md), [raw decoded metadata](descriptor_inventory.json), and [generated runtime API](runtime_surface_knowledge.md). These cover builder-created declarations absent from AST.
