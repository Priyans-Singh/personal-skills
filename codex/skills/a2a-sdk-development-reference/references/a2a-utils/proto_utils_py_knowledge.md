# `utils/proto_utils.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/proto_utils.py`. SHA-256: `ed01dfae0729f03de1e50b8da9d860ca2351060e12d0fad12044be4dcb829b84`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
from typing import TYPE_CHECKING, Any, TypedDict
from google.api.field_behavior_pb2 import FieldBehavior, field_behavior
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.json_format import ParseDict
from google.protobuf.message import Message as ProtobufMessage
from google.rpc import error_details_pb2
from a2a.utils.errors import InvalidParamsError
from a2a.types.a2a_pb2 import Message, StreamResponse, Task, TaskArtifactUpdateEvent, TaskStatusUpdateEvent
from starlette.datastructures import QueryParams
from starlette.datastructures import QueryParams
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
Event = Message | Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
```

## Declarations and execution

### `to_stream_response` (line 52)

Coverage ID: `proto_utils.py:52:to_stream_response`.

Allocates StreamResponse and CopyFrom into exact variant chosen by isinstance Task/Message/status/artifact. Unsupported input silently returns empty envelope; copies isolate later mutations. No state transition, terminal-event filtering, retry, or streaming I/O.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def to_stream_response(event: Event) -> StreamResponse:
    response = StreamResponse()
    if isinstance(event, Task):
        response.task.CopyFrom(event)
    elif isinstance(event, Message):
        response.message.CopyFrom(event)
    elif isinstance(event, TaskStatusUpdateEvent):
        response.status_update.CopyFrom(event)
    elif isinstance(event, TaskArtifactUpdateEvent):
        response.artifact_update.CopyFrom(event)
    return response
```

### `make_dict_serializable` (line 73)

Coverage ID: `proto_utils.py:73:make_dict_serializable`.

Recursively keeps primitive/None values, dict keys unchanged, tuples/lists become lists, other values str(). No cycle/depth guard; no protobuf conversion or JSON encoding. Non-string keys/nonfinite floats can remain.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def make_dict_serializable(value: Any) -> Any:
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    if isinstance(value, dict):
        return {k: make_dict_serializable(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [make_dict_serializable(item) for item in value]
    return str(value)
```

### `normalize_large_integers_to_strings` (line 93)

Coverage ID: `proto_utils.py:93:normalize_large_integers_to_strings`.

Computes threshold 10**max_safe_digits-1 (default 15 digits, not exact JS 2**53-1). Closure _normalize maps nested dict/list/tuple and turns larger-absolute int into str; leaves other values intact. No mutation or cycle guard.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def normalize_large_integers_to_strings(value: Any, max_safe_digits: int=15) -> Any:
    max_safe_int = 10 ** max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item
    return _normalize(value)
```

### `normalize_large_integers_to_strings._normalize` (line 110)

Coverage ID: `proto_utils.py:110:normalize_large_integers_to_strings._normalize`.

Applies captured integer threshold recursively, listifies tuples, preserves dict keys. Bool remains bool under ordinary positive threshold; invalid threshold choices are not validated.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _normalize(item: Any) -> Any:
    if isinstance(item, int) and abs(item) > max_safe_int:
        return str(item)
    if isinstance(item, dict):
        return {k: _normalize(v) for k, v in item.items()}
    if isinstance(item, list | tuple):
        return [_normalize(i) for i in item]
    return item
```

### `parse_string_integers_in_dict` (line 122)

Coverage ID: `proto_utils.py:122:parse_string_integers_in_dict`.

Recurses dict/list/tuple; string after lstrip(-) all digits and length>max_safe_digits → int(original), else unchanged. Leading zeros count; multiple minus signs can pass digit test then raise ValueError. Can convert user text accidentally; no provenance marker.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def parse_string_integers_in_dict(value: Any, max_safe_digits: int=15) -> Any:
    if isinstance(value, dict):
        return {k: parse_string_integers_in_dict(v, max_safe_digits) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [parse_string_integers_in_dict(item, max_safe_digits) for item in value]
    if isinstance(value, str):
        stripped_value = value.lstrip('-')
        if stripped_value.isdigit() and len(stripped_value) > max_safe_digits:
            return int(value)
    return value
```

### `parse_params` (line 153)

Coverage ID: `proto_utils.py:153:parse_params`.

Camelcase descriptor field lookup; ignores unknown keys. Repeated fields combine repeated keys and comma-split strings, skipping empties. Singular last value wins; bool strings use lower()==true (every other spelling False). ParseDict mutates supplied proto and handles enum/timestamp/number coercion; ParseError and malformed QueryParams errors propagate. Does not invoke REQUIRED validation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def parse_params(params: QueryParams, message: ProtobufMessage) -> None:
    descriptor = message.DESCRIPTOR
    fields = {f.camelcase_name: f for f in descriptor.fields}
    processed: dict[str, Any] = {}
    keys = params.keys()
    for k in keys:
        if k not in fields:
            continue
        field = fields[k]
        v_list = params.getlist(k)
        if field.label == FieldDescriptor.LABEL_REPEATED:
            accumulated: list[Any] = []
            for v in v_list:
                if not v:
                    continue
                if isinstance(v, str):
                    accumulated.extend([x for x in v.split(',') if x])
                else:
                    accumulated.append(v)
            processed[k] = accumulated
        else:
            raw_val = v_list[-1]
            if raw_val is not None:
                parsed_val: Any = raw_val
                if field.type == field.TYPE_BOOL and isinstance(raw_val, str):
                    parsed_val = raw_val.lower() == 'true'
                processed[k] = parsed_val
    ParseDict(processed, message, ignore_unknown_fields=True)
```

### `ValidationDetail` (line 202)

Coverage ID: `proto_utils.py:202:ValidationDetail`.

TypedDict field/message string pair; construction yields ordinary dict. No automatic validation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class ValidationDetail(TypedDict):
    field: str
    message: str
```

### `_check_required_field_violation` (line 209)

Coverage ID: `proto_utils.py:209:_check_required_field_violation`.

Repeated empty → at least one element violation. Presence-bearing absent → required violation. Nonpresence default scalar → required violation. Returns dict or None, not exception. Explicit default in optional/oneof passes presence check.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _check_required_field_violation(msg: ProtobufMessage, field: FieldDescriptor) -> ValidationDetail | None:
    val = getattr(msg, field.name)
    if field.label == FieldDescriptor.LABEL_REPEATED:
        if not val:
            return ValidationDetail(field=field.name, message='Field must contain at least one element.')
    elif field.has_presence:
        if not msg.HasField(field.name):
            return ValidationDetail(field=field.name, message='Field is required.')
    elif val == field.default_value:
        return ValidationDetail(field=field.name, message='Field is required.')
    return None
```

### `_append_nested_errors` (line 233)

Coverage ID: `proto_utils.py:233:_append_nested_errors`.

Appends new field/message dicts to destination, prefix.field or prefix if child field empty. Side effect only destination list; no exception transformation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _append_nested_errors(errors: list[ValidationDetail], prefix: str, sub_errs: list[ValidationDetail]) -> None:
    for sub in sub_errs:
        sub_field = sub['field']
        errors.append(ValidationDetail(field=f'{prefix}.{sub_field}' if sub_field else prefix, message=sub['message']))
```

### `_recurse_validation` (line 249)

Coverage ID: `proto_utils.py:249:_recurse_validation`.

Scalar → empty errors. Present singular messages recursively validate. Repeated maps recurse only protobuf-valued entries (key path field[key]); repeated messages recurse using field[index]. Unset optional messages skipped; no max-depth guard.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _recurse_validation(msg: ProtobufMessage, field: FieldDescriptor) -> list[ValidationDetail]:
    errors: list[ValidationDetail] = []
    if field.type != FieldDescriptor.TYPE_MESSAGE:
        return errors
    val = getattr(msg, field.name)
    if field.label != FieldDescriptor.LABEL_REPEATED:
        if msg.HasField(field.name):
            sub_errs = _validate_proto_required_fields_internal(val)
            _append_nested_errors(errors, field.name, sub_errs)
    elif field.message_type.GetOptions().map_entry:
        for k, v in val.items():
            if isinstance(v, ProtobufMessage):
                sub_errs = _validate_proto_required_fields_internal(v)
                _append_nested_errors(errors, f'{field.name}[{k}]', sub_errs)
    else:
        for i, item in enumerate(val):
            sub_errs = _validate_proto_required_fields_internal(item)
            _append_nested_errors(errors, f'{field.name}[{i}]', sub_errs)
    return errors
```

### `_validate_proto_required_fields_internal` (line 277)

Coverage ID: `proto_utils.py:277:_validate_proto_required_fields_internal`.

Walks every descriptor field, examines google.api.field_behavior REQUIRED extension; checks required then recursively gathers nested errors. Returns complete list; proto serialization itself does not enforce these annotations.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _validate_proto_required_fields_internal(msg: ProtobufMessage) -> list[ValidationDetail]:
    desc = msg.DESCRIPTOR
    errors: list[ValidationDetail] = []
    for field in desc.fields:
        options = field.GetOptions()
        if FieldBehavior.REQUIRED in options.Extensions[field_behavior]:
            violation = _check_required_field_violation(msg, field)
            if violation:
                errors.append(violation)
        errors.extend(_recurse_validation(msg, field))
    return errors
```

### `validate_proto_required_fields` (line 294)

Coverage ID: `proto_utils.py:294:validate_proto_required_fields`.

Runs recursive validator; nonempty errors → InvalidParamsError(message=Validation failed,data={errors:list}); valid → None. Does not mutate, repair, enforce oneof content selection absent required annotation, or validate business state.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def validate_proto_required_fields(msg: ProtobufMessage) -> None:
    errors = _validate_proto_required_fields_internal(msg)
    if errors:
        raise InvalidParamsError(message='Validation failed', data={'errors': errors})
```

### `validation_errors_to_bad_request` (line 311)

Coverage ID: `proto_utils.py:311:validation_errors_to_bad_request`.

Allocates BadRequest; each dict becomes added field_violations element with field/description. Missing keys/type issues propagate; no transport I/O.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def validation_errors_to_bad_request(errors: list[ValidationDetail]) -> error_details_pb2.BadRequest:
    bad_request = error_details_pb2.BadRequest()
    for err in errors:
        violation = bad_request.field_violations.add()
        violation.field = err['field']
        violation.description = err['message']
    return bad_request
```

### `bad_request_to_validation_errors` (line 323)

Coverage ID: `proto_utils.py:323:bad_request_to_validation_errors`.

Returns fresh list of dict field/message pairs from field_violations; discards other detail fields. Order preserved.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def bad_request_to_validation_errors(bad_request: error_details_pb2.BadRequest) -> list[ValidationDetail]:
    return [ValidationDetail(field=v.field, message=v.description) for v in bad_request.field_violations]
```
