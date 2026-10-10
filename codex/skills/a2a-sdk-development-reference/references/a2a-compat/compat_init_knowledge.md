# __init__.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/__init__.py`. SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Mental model and import surface

`a2a.compat` is an empty namespace package initializer, not a dispatcher, client factory, or version negotiator. Import the specific `a2a.compat.v0_3` module you need. It declares no classes, functions, constants, imports, or side effects. The nested package is the only compatibility generation present in this installed folder. It does not patch current SDK types automatically.

## Declaration-by-declaration execution reference

No AST declarations. Empty initializers have no execution; dynamically built protobuf objects are documented in the descriptor catalog below.
