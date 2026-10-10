# Utilities: mental model, flows, operational use

Inspected a2a-sdk 1.1.4, 2026-10-07; source `.venv/lib/python3.11/site-packages/a2a/utils`. Utilities are distinct local policies, not a global validation/authorization pipeline. Public package imports only constants, proto_utils and to_stream_response. Import signing/telemetry/errors/decorators from their submodules explicitly; package __all__ does not expose every helper.

## Execution paths

**REST request:** handler supplies QueryParams and an existing proto → parse_params uses descriptor JSON/camelcase field names, coalesces repeated values, converts booleans, delegates ParseDict → caller invokes validate_proto_required_fields → descriptor REQUIRED annotations and nested messages generate field-path violations → InvalidParamsError.data['errors'] → build_error_details emits ErrorInfo plus BadRequest → build_rest_error_payload chooses transport mapping → _create_error_response constructs Starlette JSONResponse. Parsing/required validation are separate opt-in calls. They do not check tenant authorization, IDs against stores, task transition, or URL safety. Unknown query keys ignored. Bool 'anything other than true' becomes false. Malformed inputs can fail after mutation; use a fresh proto.

**Streaming response:** executor emits Task/Message/update event → to_stream_response copies into payload oneof → consumer serializes envelope via protobuf JSON/binary → manual streaming JSON uses json_utils.dumps for literal Unicode. rest_stream_error_handler catches construction errors into HTTP JSON responses; after headers/iteration start it logs and rethrows. Only async-generator body_iterator is replaced. Transport owns termination/cancellation/reconnect; utility has no replay buffer, retry, or persistence. Unknown event types yield an empty envelope, so validate event type at integration boundary.

**Task retrieval/page cursor:** caller validates history_length/page_size separately → apply_history_length either returns original identity or copies/truncates newest message suffix → encode_page_token creates reversible base64 ID → decode_page_token repairs padding and decodes. Cursor exposes ID, is unsigned and has no expiration; authorization/filter/snapshot consistency must come from store/handler. Never mutate returned Task on assumption it is always a copy. Negative history is not rejected by apply_history_length.

**Card signing:** MessageToDict → remove signatures → remove empty values → canonical JCS → PyJWT compact JWS → append detached protected/signature fields. Returned signer mutates same card. Verify computes same payload once, feeds untrusted kid/jku to key_provider, accepts first allowed-algorithm valid signature. Only PyJWTError causes trying another signature; malformed protected JSON/provider errors can abort. Key provider owns trust, cache/network/rotation. Signing key remains in closure for signer lifetime; verification keys are local provider return values. No token expiry, fetch, credential transmission or revocation is implemented here. AgentCardSignature unprotected header is outside protected JWS bytes. Avoid treating successful signature as endpoint authorization.

**Version routing:** context.state['headers'] → standard/lowercase A2A-Version, empty/missing defaults 0.3 → packaging.Version compatibility. Implementation compares major only; 1.0 and 1.9 pass. Missing context passes expected version. Expected invalid version only exact match. Generator wrapper validates at iterator construction, coroutine wrapper at await. Do not rely on this decorator for strict minor-version negotiation.

**Tracing:** import-time OTEL_INSTRUMENTATION_A2A_SDK_ENABLED equals true case-insensitively → real trace API or absorbing no-op. trace_function opens span per invocation and forwards result/errors; async cancellation and queue shutdown recorded but not explicitly marked ERROR. Extractor runs finally and errors are swallowed/logged. No-op tracing still wraps calls. Async-generator work is outside sync wrapper span. trace_class modifies eligible function attributes, including inherited functions; descriptor-sensitive methods need care. Export destination/lifetime/provider are externally configured, so avoid placing raw tokens, private keys or sensitive data in attributes/extractor/logs.

**Push URL screening:** parse scheme/host/port → event-loop DNS resolve → reject any nonpublic IP. No outbound HTTP is performed by validator, but DNS is I/O. It does not pin IP for later sender, evaluate redirects, strip userinfo, or configure egress. Inference: resolution/fetch races remain possible; deployment egress policy must own the actual connection. Do not run URL examples against live hosts merely to test documentation.

## Optional dependencies and supporting boundaries

Inspected environment has PyJWT, Starlette, opentelemetry.trace, culsans, packaging, protobuf/google API and RPC descriptors; **grpc is absent**. grpc_status imports without grpc but functions raise explicit ImportError. Generated a2a_pb2_grpc fails import without grpc. signing raises actionable ImportError at import if PyJWT absent. Starlette helper imports fall back to Any for source/type availability, not usable HTTP response behavior. Telemetry has no-op when absent/disabled; Python 3.11 queue compatibility still requires culsans.

Direct supporting source: types supplies all message/event classes and descriptor options; server.context.ServerCallContext supplies mutable state/user/tenant/requested_extensions; auth.user supplies default unauthenticated user. Version helper only reads headers from state, not user/tenant. Server transport/store/executor provide actual I/O, auth, consistency, event/state lifetimes; parent/sibling references document them. google.protobuf JSON/descriptor/RPC BadRequest dependencies implement coercion and typed error transport. packaging implements version parsing; ipaddress classifications depend on Python version. No module here silently persists task history, rotates credentials, retries RPCs, or issues cancellation requests.

## Error mapping and exposure

errors.py tables map exact classes to JSON-RPC codes, HTTP/gRPC codes/reasons. A2A_REST_ERROR_MAPPING aliases same dictionary, not a copy. A2A_ERROR_REASONS and inverse are snapshots built at import, so mutating mapping later does not refresh them. JSONParseError has JSON-RPC entry but no A2A_ERROR_MAPPING entry: REST sees default INTERNAL and UNKNOWN_ERROR unless actual protobuf ParseError is used. ContentTypeNotSupportedError and ExtendedAgentCardNotConfiguredError exist but are omitted from errors.__all__; they are re-exported by a2a.types. Unknown subclass of known error can use fallback mapping due exact-type lookup. A2AError.data is exposed to clients and logs unaltered: use field-validation details, never credentials or internal traces. Public builder functions can raise on malformed metadata, so error shaping is not guaranteed total.

## Pure examples

```python
from a2a.types import GetTaskRequest, Task, Message
from a2a.utils.task import apply_history_length, encode_page_token, decode_page_token
from a2a.utils._jcs import canonicalize
from a2a.utils.proto_utils import normalize_large_integers_to_strings
from a2a.utils.error_handlers import build_rest_error_payload
from a2a.utils.errors import InvalidParamsError

original = Task(id='t1', history=[Message(message_id='a'), Message(message_id='b')])
assert apply_history_length(original, GetTaskRequest()) is original
short = apply_history_length(original, GetTaskRequest(history_length=1))
assert short is not original and short.history[0].message_id == 'b'
assert decode_page_token(encode_page_token('t1')) == 't1'
assert canonicalize({'z': -0.0, 'a': 'é'}) == '{"a":"é","z":0}'
assert normalize_large_integers_to_strings({'id':10**16}) == {'id':str(10**16)}
payload = build_rest_error_payload(InvalidParamsError(data={'errors':[{'field':'id','message':'missing'}]}))
assert payload['error']['code'] == 400
assert len(payload['error']['details']) == 2
```

See every per-file guide for exact signatures, private closures, behavior, errors and implementation evidence. Source excerpts are retained as reviewable evidence alongside authored execution descriptions; mechanical checks do not treat mere name presence as sufficient.
