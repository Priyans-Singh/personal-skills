# v0_3/__init__.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/__init__.py`. SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Mental model and import surface

The initializer is empty. `from a2a.compat.v0_3 import conversions, types, proto_utils` resolves submodules through Python import machinery; there are no explicit re-exports or `__all__`. Importing the namespace alone does not initialize HTTP or gRPC clients. Import individual adapters only when their optional dependencies exist.

Legacy Pydantic models are the pivot. JSON-RPC speaks these models directly. REST and gRPC use legacy protobuf and go through `proto_utils`; `conversions` bridges pivot models and current core protobuf. SDK distribution version 1.1.4 is separate from wire versions 0.3 and 1.0. Legacy protobuf's package is `a2a.v1`, whereas current protobuf is `lf.a2a.v1`.

## Declaration-by-declaration execution reference

No AST declarations. Empty initializers have no execution; dynamically built protobuf objects are documented in the descriptor catalog below.
