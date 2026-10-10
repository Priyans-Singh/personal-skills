# `_base.py`: shared Pydantic base

Source: [_base.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/_base.py), a2a-sdk 1.1.4, inspected 2026-10-07.

`to_camel_custom(snake: str) -> str`: if string ends '_', rstrip('_') removes **all** trailing underscores, then Pydantic to_camel converts to camelCase. Used for keyword-conflicting fields such as in_ → in. Non-string inputs can fail normal attribute/conversion operations. No I/O or mutation of input.

`A2ABaseModel` subclasses Pydantic BaseModel with ConfigDict(validate_by_name=True, validate_by_alias=True, serialize_by_alias=True, alias_generator=to_camel_custom). Derived Pydantic classes accept Python field name or generated wire alias and serialize aliases by default. Explicit Pydantic dump options can override behavior. Normal validators/type errors come from Pydantic. It defines no methods, lazy cache, lock or deprecated attribute interception.

**Source-docstring discrepancy:** class docstring claims lazy alias-map loading and deprecated camelCase attribute access/set warnings. Actual file contains only model_config and alias helper; no __getattr__/__setattr__ or warning/cache implementation. Do not infer camelCase Python attribute access from support for input/serialization aliases.

This base is used by legacy compatibility values; current a2a.types values are generated protobuf objects with different constructors, presence, serialization and mutability. Do not apply model_dump to protobuf or use this config as a wire conversion for current messages. No credentials, owner authorization, resource lifetime, async task or persistence is implemented here.

```python
from a2a._base import A2ABaseModel
class Example(A2ABaseModel):
    sample_name: str
    in_: str
value = Example(sampleName="example", **{"in": "header"})
assert value.sample_name == "example"
assert value.model_dump() == {"sampleName": "example", "in": "header"}
```

Pure construction example, not protocol model declaration. Prefer SDK-defined models over adding unspec'd wire fields. Preserve distinction between data aliases and Python attribute names.
