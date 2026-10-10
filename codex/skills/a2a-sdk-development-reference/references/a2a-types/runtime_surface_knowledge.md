# Protobuf runtime surface and ownership

Inspected a2a-sdk 1.1.4 on 2026-10-07, `.venv/lib/python3.11/site-packages/a2a/types/`. Supporting source inspected: `google/protobuf/internal/builder.py`, `enum_type_wrapper.py`, `message.py`, `python_message.py`, `json_format.py`. These implement the runtime surface invoked by generated modules; they are not another A2A package to duplicate. Installed runtime uses compiled upb: compiled method interiors cannot be traced as Python source. The descriptor and pure local checks establish the behavior below.

## Object creation and mutations

Builder creates 51 message classes recursively (44 top-level plus 7 map entries), supplies DESCRIPTOR/module/qualname, registers each in symbol database. The generated module passes `a2a_pb2` as module name even though imported under `a2a.types.a2a_pb2`; avoid assuming `__module__` always equals import path. Two enum wrapper objects and 12 integer constants are built; `_NAME` globals are descriptors. `_A2ASERVICE` is a service descriptor, not a servicer. Generated classes inherit protobuf Message.

`Model(**fields)` allocates local mutable state. Scalar kwargs assign values; repeated scalars accept iterables, repeated messages copy elements, message kwargs accept messages/mappings. Unknown keyword fields, incompatible types, and integer range errors surface from runtime. Do not treat constructor success as required-field/business validation. New mutable snapshots are not synchronized or persisted. No auth checks or IDs are generated.

A singular message attribute exposes a child object even while absent. Reading it does not set presence; mutating a descendant or `SetInParent()` does. Assign scalars directly; populate singular messages via constructor, `CopyFrom`, or child mutation rather than direct message assignment. Repeated scalar containers support append/extend/insert/slice assignment/deletion; repeated message containers provide `add(**kwargs)`, append/extend copying, indexing and deletion; whole repeated field assignment is forbidden. Map-of-message values need `map[key].CopyFrom(value)`, and reading a missing key can insert a default entry. Plain scalar-map assignment is allowed. Avoid unexpected insertion during lookup: use membership checks.

Oneofs allow zero or one selected member. Assigning a default scalar inside a oneof still selects it. Assigning a different member clears old member. Empty nested message construction/copy selects its member; `WhichOneof(group)` reveals selected field. Synthetic `_field` oneofs implement optional scalar presence, not application alternatives. REQUIRED annotations do not require selection of Part.content, SecurityScheme.scheme or response.payload unless separately validated by business logic. OAuthFlows.flow permits one selected flow, not all five simultaneously.

## Common generated methods, including private/inherited methods

These families are identical across each generated message, so their behavior is specified once rather than repeated 51 times. Generated callable inventory lists actual accessible callable names for every message, separately from AST/PYI declarations.

| Callable | Input → output; effects/errors |
|---|---|
| `__init__` | Keyword fields → None; creates/populates local message; rejects unsupported fields/types/ranges. |
| `CopyFrom` | Same message type → None; replaces contents with copy (self-copy no-op). Other message type rejected. |
| `MergeFrom` | Same type → None; set singular scalars replace, nested messages recursively merge, repeated append, maps merge; self-merge can duplicate repeated content. |
| `Clear` | No args → None; clears known and unknown fields, resets presence/defaults. |
| `ClearField` | Python field or oneof name → None; clears field/selected member; invalid name ValueError. |
| `HasField` | Presence field or oneof name → bool; nonpresence scalar/repeated/map or unknown name raises ValueError. |
| `WhichOneof` | Oneof name → selected field name/None; unknown group ValueError. |
| `SetInParent` | No args → None; marks empty child present in parent. |
| `ListFields` | No args → ordered list `(FieldDescriptor,value)` for present/nondefault/nonempty fields. Child/container values remain mutable references. |
| `SerializeToString` | Optional deterministic=True → binary bytes; no Google REQUIRED validation. Protobuf EncodeError possible for actual proto2 required constraints/type errors. |
| `SerializePartialToString` | Same serialization without initialization check; bytes. Neither serialization signs, encrypts, or sends anything. |
| `ParseFromString` | Buffer/bytes → bytes-read integer; clears first then binary merges. DecodeError may leave changed state; parse into fresh message when atomicity matters. |
| `MergeFromString` | Buffer/bytes → bytes-read integer; appends/merges rather than replaces; malformed data DecodeError. |
| `FromString` | Class callable(bytes) → fresh parsed instance; DecodeError propagated. |
| `ByteSize` | No args → binary serialized size integer, includes nested contents; not JSON size. |
| `IsInitialized` | No args → bool for protobuf required rules, not google.api REQUIRED or domain validity. |
| `FindInitializationErrors` | No args → list of missing proto2 required paths; empty for these proto3 models despite omitted annotated fields. |
| `DiscardUnknownFields` | No args → None; recursively drops unknown wire fields, sacrificing forward round-trip preservation. |
| `UnknownFields` | No args → unknown-field access according to backend; upb can raise NotImplementedError. Use supported `google.protobuf.unknown_fields.UnknownFieldSet` if needed. |
| `HasExtension`, `ClearExtension` | Extension descriptor → presence or clear; repeated extension presence invalid. A2A messages declare no own extensions; these inherited methods do not make arbitrary fields extendable. |
| `_SetListener` | Internal parent listener bookkeeping interface; inherited abstraction in upb can raise NotImplementedError. Not application notification callback. |
| `__deepcopy__` | memo → independent clone via MergeFrom. |
| `__eq__`, `__ne__` | Other message → recursive value/structure comparison; presence contributes. |
| `__hash__` | Raises TypeError; mutable messages unhashable. |
| `__str__`, `__repr__`, `__unicode__` | Human-readable text representation; no promise of canonical signing/JSON wire bytes. |
| `__dir__` | Returns accessible names including descriptor fields, removes unusable Extensions. |
| `__contains__` | Presence check for named field on normal messages; no-presence/unknown raises ValueError; WKT Struct/ListValue have different key/item behavior. |
| `__getstate__` | Serialized partial bytes in dict for pickle. |
| `__setstate__` | state serialized bytes (legacy text encoded latin1) → None; reinitializes and parses. |
| `__reduce__` | Pickle reconstruction tuple; nested types use symbol_database lookup by full name. Never unpickle untrusted input. |
| `__sizeof__`, `__getattribute__`, `__setattr__`, `__delattr__`, `__new__`, `__format__`, `__reduce_ex__`, `__init_subclass__`, `__subclasshook__`, `__getstate__` | Python/backend object protocol. Field access/mutation delegates generated runtime; these are not extra protocol operations. Inventory distinguishes inherited interpreter methods from generated API. |

Enum wrapper `Name(number)` returns symbolic name; unknown int ValueError, non-int lookup TypeError. `Value(name)` returns integer or ValueError. `keys`, `values`, `items` return fresh lists in declaration order. `__getattr__` exposes enum constants or raises AttributeError. `__or__` on Python ≥3.10 makes a type union with wrapper type; it is not bitwise enum combination. Constructor accepts enum descriptor. TaskState does not validate transitions; unknown proto3 numeric enum values can be carried on wire.

## JSON and binary boundaries

`MessageToDict` maps proto field names to JSON aliases (default lower camelcase), emits enum symbolic names, bytes base64, Timestamp RFC3339 string, Struct/Value as natural JSON, and omits nonpresence defaults. Set optional false/zero remains representable. Binary uses field numbers and oneof/presence; unknown binary fields are retained until discarded. JSON unknown fields are rejected by default by ParseDict/Parse, or ignored with explicit ignore_unknown_fields=True; unknown-field JSON round-trip is not binary unknown retention.

`ParseDict(obj,message)` mutates provided message; `Parse(json_text,message)` parses text then delegates. Scalars/enums/timestamps/base64/oneof conflicts can raise ParseError. Do not use direct `json.dumps(proto)`: choose MessageToDict/MessageToJson first. Struct numbers use doubles; large integers can lose precision; utils normalize/restore helpers are opt-in heuristics, not automatic model behavior. Deterministic protobuf serialization is not RFC8785 canonical JSON. Signing utility uses cleaned protobuf JSON and local JCS, excluding signatures, not binary serialization.

## Local example

```python
from google.protobuf.json_format import MessageToDict
from a2a.types import GetTaskRequest, Message, Part, Task
from a2a.types import a2a_pb2 as pb
from a2a.utils.proto_utils import validate_proto_required_fields, to_stream_response

request = GetTaskRequest(id='t1')
assert request.history_length == 0 and not request.HasField('history_length')
request.history_length = 0
assert request.HasField('history_length')
part = Part(text='hello')
part.raw = b'x'
assert part.WhichOneof('content') == 'raw' and part.text == ''
message = Message(message_id='m1', role=pb.ROLE_USER, parts=[Part(text='hello')])
validate_proto_required_fields(message)
task = Task(id='t1', context_id='c1', history=[message])
task.status.state = pb.TASK_STATE_WORKING
validate_proto_required_fields(task)
envelope = to_stream_response(task)
task.id = 'changed'
assert envelope.task.id == 't1'
wire = envelope.SerializeToString()
assert pb.StreamResponse.FromString(wire) == envelope
assert MessageToDict(envelope)['task']['id'] == 't1'
```

No network, task execution, cancellation, push callback, or persistence occurs in this example.

## Compiled private helpers and interpreter callables

`_ListFieldsItemKey(entry)` is a compiled static helper returning entry[0].number for `(FieldDescriptor,value)` tuples; local checks produced wire numbers 1 and 3. Missing argument raises TypeError. `_CheckCalledFromGeneratedFile()` is a compiled descriptor-construction guard used by descriptor.py constructors; direct application invocation raises TypeError (Descriptors cannot be created directly). They are implementation support, not A2A methods. Their interiors are unavailable as installed Python source; observations are marked as local runtime checks rather than inferred control flow.

Nested `SecuritySchemesEntry`, `SchemesEntry`, `ScopesEntry` class attributes are callable map-entry constructors already covered by descriptor catalog and scoped PYI constructors. `__class__` exposes metaclass identity, not a wire field. `__lt__`, `__le__`, `__gt__`, `__ge__` are inherited ordering slots rather than task ordering; messages do not define domain ordering, and unsupported comparisons can raise TypeError. Every runtime inventory callable has an explanation in this guide or the nested model/constructor catalog.
