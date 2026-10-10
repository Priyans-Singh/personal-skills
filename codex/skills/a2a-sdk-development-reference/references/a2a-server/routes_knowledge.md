# HTTP routes, dispatch, SSE, and FastAPI schemas

Sources: `server/routes/`, a2a-sdk 1.1.4. These modules adapt HTTP to RequestHandler; no executor/LLM implementation belongs here.

## `__init__.py`

Exports route factories, FastAPI helper, ServerCallContextBuilder and default builder. Dispatchers/schema helpers require defining-module imports. Factories return Starlette routes; they do not run uvicorn or attach a shutdown hook.

## `common.py`

`serialize_list_tasks_response(response, include_artifacts)` calls MessageToDict with default-valued nonpresence fields printed. If artifacts excluded, removes artifacts keys from each serialized task. Ensures empty list/page fields remain visible without returning empty artifact arrays unnecessarily.

`StarletteUser.__init__` retains framework user; is_authenticated delegates, user_name returns display_name. `ServerCallContextBuilder.build` is abstract sync contract. `DefaultServerCallContextBuilder.build` records available request.auth, copies headers into state, constructs user through build_user, parses all A2A-Extensions headers. `build_user` adapts request.user when scope contains it, otherwise UnauthenticatedUser. Authentication middleware is not installed here. Headers in context can contain secrets; avoid logging the mapping.

## `agent_card_routes.py`

`create_agent_card_routes(agent_card, card_modifier=None, card_url='/.well-known/agent-card.json')` guards Starlette availability and returns a GET route. Nested `_get_agent_card` uses shared card, optionally awaits modifier(card), then JSONResponse(agent_card_to_dict). Modifier receives no caller context/request argument. No signature creation, cache policy, authentication gate, or persistence. Copy shared card before mutation; advertise URLs/capabilities actually served.

## `rest_routes.py`

`create_rest_routes(handler, context_builder=None, enable_v0_3_compat=False, path_prefix='')` builds RestDispatcher, optionally adds `/v1/...` compatibility routes, creates base routes below, and adds `Mount('/{tenant}', routes=base_route_objects)`. Prefix is prepended to child/base paths; tenant mount itself stays `/{tenant}`. This is version-sensitive if composing prefixes/mounts.

| Route | HTTP | Dispatcher / effect |
|---|---|---|
| `/message:send` | POST | on_message_send: request body → SendMessageResponse |
| `/message:stream` | POST | on_message_send_stream: body → SSE StreamResponse events |
| `/tasks/{id}:cancel` | POST | on_cancel_task: path ID → Task |
| `/tasks/{id}:subscribe` | GET/POST | on_subscribe_to_task: path ID → SSE |
| `/tasks/{id}` | GET | on_get_task: query options + authoritative path ID |
| `/tasks` | GET | list_tasks: query filters/pagination → task list |
| `/tasks/{id}/pushNotificationConfigs` | POST/GET | set_push_notification / list_push_notifications |
| `/tasks/{id}/pushNotificationConfigs/{push_id}` | GET/DELETE | get_push_notification / delete_push_notification |
| `/extendedAgentCard` | GET | handle_authenticated_agent_card |

No public Task deletion endpoint is created. `TaskStore.delete` is an application operation. Enabling compatibility does not infer card interfaces or install authentication.

## `rest_dispatcher.py`

`RestDispatcher.__init__` requires Starlette/SSE availability and stores handler/default context builder. `_build_call_context` copies tenant path value if present. `_handle_non_streaming` builds context then awaits handler closure.

Every endpoint has nested `_handler` with validate_version('1.0'). With request context but no A2A-Version header, validator defaults to 0.3 and rejects current endpoints. Same-major versions are accepted; strict OpenAPI enum is narrower than runtime compatibility. Context builder must preserve state['headers'] for version validation.

Distinct endpoint parsing:

- on_message_send/stream: protobuf Parse of body to SendMessageRequest; unknown/malformed fields raise parse errors. Unary wraps Task or Message; stream wraps each event.
- on_cancel_task: constructs CancelTaskRequest from path; body is not mapped to request metadata.
- on_subscribe_to_task: constructs SubscribeToTaskRequest from path; no history/query mapping here.
- on_get_task: proto_utils.parse_params(query), overrides id from path, rejects handler None.
- get_push_notification: constructs task/config IDs from path.
- delete_push_notification: invokes handler then returns `{}` JSON, not a 204.
- set_push_notification: parses body as TaskPushNotificationConfig, overrides task_id from path.
- list_push_notifications: parses query, overrides task_id.
- list_tasks: parses query, passes include_artifacts to special serialization.
- handle_authenticated_agent_card: empty GetExtendedAgentCardRequest, serializes card directly with MessageToDict. Its name does not install an authentication check.

`_handle_streaming` **pre-reads request.body** before SSE starts to avoid competing receive/body reads. Read errors ValueError/RuntimeError/OSError become InvalidRequestError. Builds context, obtains iterator, eagerly awaits first item; empty stream returns empty EventSourceResponse. Errors before first item go through outer REST error decorator with HTTP status. Nested event_generator yields first item then subsequent JSON serialized ServerSentEvents; subsequent exceptions log and yield event='error' with REST payload. After response begins, HTTP status cannot represent that later failure.

Unary endpoints use rest_error_handler; streams use rest_stream_error_handler. Neither is a retry mechanism. Generator wrappers do not universally explicitly aclose every nested underlying iterator; preserve closure behavior and test disconnects if customizing. JSON SSE uses ensure_ascii=False.

## `jsonrpc_routes.py`

`create_jsonrpc_routes(handler, rpc_url, context_builder=None, enable_v0_3_compat=False)` returns one POST route bound to JsonRpcDispatcher.handle_requests. rpc_url is required despite a constants module default RPC path elsewhere. No tenant mount automatically added; tenant comes from parsed protobuf request.

## `jsonrpc_dispatcher.py`

`__init__` validates dependencies, stores builder/handler, optionally builds JSONRPC03Adapter. METHOD_TO_MODEL maps **PascalCase current method names** to protobuf classes: SendMessage, SendStreamingMessage, GetTask, ListTasks, CancelTask, Create/Get/List/DeleteTaskPushNotificationConfig, SubscribeToTask, GetExtendedAgentCard. Legacy slash names require compatibility flag.

`handle_requests` reads JSON, sanitizes request ID type (str/int/None), validates JSONRPC20Request and exact jsonrpc='2.0', rejects batches, requires method, optionally dispatches recognized v0.3 method, maps unknown method→MethodNotFoundError, ParseDicts params, builds caller context, copies model tenant, inserts method/request_id into state, then chooses unary/stream processing. Current processing validates version header.

Invalid JSON→JSONParseError (also traceback printed); bad envelope/batch→InvalidRequestError; parameter parse→InvalidParamsError. Domain errors build protocol error envelope. Payload-too-large HTTPException maps InvalidRequestError; other HTTPExceptions re-raise. Unexpected exceptions log and become InternalError with str(exception). `_generate_error_response` normalizes error/model, logs warning/error by code, returns HTTP **200** JSON error. Clients must inspect body, not HTTP code only.

`_process_non_streaming_request` matches state method and delegates private `_handle_*` functions. Send wraps protobuf SendMessageResponse; get/cancel reject None; list uses special list serializer; config create/get/list and extended card convert protobuf dict; delete awaits side effect and returns None (JSON-RPC result null). These helpers do not create independent tasks or retry I/O.

`_process_streaming_request` selects handler generator for send/subscription, raises unsupported if none, eagerly gets first event. Nested `_wrap_stream` and `_map_event` convert StreamResponse to JSONRPC20Response with request ID; A2A errors during iteration yield protocol error envelope. Other errors are caught by `_create_response`'s nested event_generator. It adds event='error' for error envelopes, catches unexpected failures and emits InternalError envelope, uses json_utils.dumps, then EventSourceResponse. Unary results use JSONResponse. Initial stream errors return ordinary JSON envelopes; later errors are SSE events.

## `_proto_schema.py`

REST_BODY_TYPES maps send/stream and config-create POST suffixes to protobuf classes. `_is_required` reads google.api REQUIRED annotation. `field_schema` maps protobuf scalars (64-bit ints are JSON strings, bytes base64), enum names/examples, repeated arrays, map entries, optional message refs with null, and recursive message schemas. It mutates shared components dictionary.

`message_schema` returns inline schemas for well-known Timestamp/Duration/Struct/Value/ListValue/Empty/Any/FieldMask. Other descriptors use simple message-name component keys, insert placeholder before recursion, and return $ref. Multi-field oneofs get exactly-one constraints; proto optional synthetic oneofs are ignored. Base fields are emitted using **snake_case field.name**, while MessageToDict wire serialization uses camelCase json_name. Non-oneof REQUIRED annotations are not comprehensively emitted into message-level required arrays. Therefore generated OpenAPI is helpful discovery, not authoritative validation/wire schema. Component name collisions across protobuf packages are possible with simple names.

## `_jsonrpc_schema.py`

METHOD_TYPES mirrors current method→request mapping. `envelope_schema(components)` generates unique request type refs, adds A2ARequest object requiring jsonrpc and method, with ID union and params.oneOf. Does not enforce correspondence between a particular method value and a particular params schema. DESCRIPTION documents methods. Actual dispatcher/required-field validation remains authoritative.

## `fastapi_routes.py`

Optional import defines `_A2ARoute(APIRoute)`; its __init__ runs parent then replaces app with Starlette request_response(endpoint), so existing Request→Response dispatchers remain usable instead of FastAPI treating their signatures as ordinary dependency/body APIs.

`_request_body_extra` constructs OpenAPI JSON requestBody. `_rest_body_extra` matches route suffix and method to body schema. `_attach_route` appends non-Route/mount unchanged; normal Route becomes _A2ARoute without HEAD, tagged by transport, with optional version-header parameters. It does not invoke FastAPI dependency injection to authenticate these wrapped endpoints.

`add_a2a_routes_to_fastapi(app, agent_card_routes=None, jsonrpc_routes=None, rest_routes=None)` generates all components/extras, attaches routes, captures original app.openapi, and replaces it with nested `_openapi`. New wrapper returns existing app.openapi_schema if truthy; otherwise calls original and setdefault-merges components. Existing cached schema can omit newly attached routes/components: install routes before first OpenAPI generation or deliberately reset cache. Repeated helper calls can chain wrappers; keep setup simple. Runtime route behavior still belongs to Starlette dispatchers.

## Practices

Match card's binding/version/URL to mounted routes; send A2A-Version for current HTTP operations; use protobuf constructors/helpers instead of guessing dict field names. Require real authentication separately for task/extended-card access. Test both first-event and midstream errors, tenant prefix composition, non-ASCII SSE, and disconnect cleanup. Consult protobuf descriptors/source when OpenAPI names/constraints disagree with actual wire behavior.

### JSON-RPC unary helper index

The private operation helpers are separate call boundaries, not additional protocol methods:

| Helper | Delegation and normalization |
|---|---|
| `_handle_send_message` | on_message_send → SendMessageResponse oneof → dict |
| `_handle_cancel_task` | on_cancel_task → Task dict; None raises TaskNotFoundError |
| `_handle_get_task` | on_get_task → Task dict; None raises TaskNotFoundError |
| `_handle_list_tasks` | on_list_tasks → serialize_list_tasks_response respecting include_artifacts |
| `_handle_create_task_push_notification_config` | on_create_task_push_notification_config → config dict |
| `_handle_get_task_push_notification_config` | on_get_task_push_notification_config → config dict |
| `_handle_list_task_push_notification_configs` | on_list_task_push_notification_configs → response dict |
| `_handle_delete_task_push_notification_config` | on_delete_task_push_notification_config → no value |
| `_handle_get_extended_agent_card` | on_get_extended_agent_card → card dict |
