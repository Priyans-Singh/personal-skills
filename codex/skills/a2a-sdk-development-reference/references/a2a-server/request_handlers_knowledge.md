# Request handlers and gRPC

Sources: `server/request_handlers/`. Handlers accept protobuf request values plus ServerCallContext and produce protocol objects/events; HTTP/gRPC adapters perform transport parsing/serialization.

## `__init__.py`

Exports RequestHandler, parameter-validation decorator, response helpers, LegacyRequestHandler, DefaultRequestHandlerV2, optional gRPC classes. **DefaultRequestHandler = DefaultRequestHandlerV2**. `validate` requires its defining module. Dependency placeholders are described in [initializer](init_knowledge.md).

## `request_handler.py`: interface and decorators

`RequestHandler` declares on_get_task, on_list_tasks, on_cancel_task, on_message_send, on_message_send_stream, on_create_task_push_notification_config, on_get_task_push_notification_config, on_subscribe_to_task, on_list_task_push_notification_configs, on_delete_task_push_notification_config, on_get_extended_agent_card. Abstract get/cancel annotations allow None but adapters translate it to not-found. Abstract stream methods are async generators whose body raises UnsupportedOperationError. See operation table below for parameters/results of concrete handlers.

`validate_request_params(method)` detects async-generator versus coroutine. Its async_gen_wrapper validates protobuf REQUIRED annotations before iteration, yields inner items, and finally awaits inner.aclose. async_wrapper validates then awaits method. None parameters skip validation; it does not parse dicts or validate arbitrary agent output. Validation details include nested field paths.

`validate(expression, error_message=None, error_type=UnsupportedOperationError)` returns decorator selecting async_gen_wrapper, async_wrapper, or sync_wrapper. Each evaluates expression(self), logs/raises configured error on False, otherwise delegates; generator wrapper closes inner generator on exit. Predicate exceptions propagate. These gates test advertised capability, not caller authorization. Private nested wrappers are covered in the index.

## `default_request_handler_v2.py`: constructor/setup

`DefaultRequestHandlerV2.__init__` requires executor, TaskStore and AgentCard. Optional sender/config store, builder, extended card/modifier, URL validator are recorded. Default builder does not populate referred tasks. Constructs ActiveTaskRegistry; `_background_tasks` is initialized but is not the V2 lifecycle mechanism. Any queue_manager argument warns and is ignored.

`_reject_unsafe_push_url` returns without screening when validator None, else awaits bool and raises InvalidParamsError for False; validator exceptions propagate. `aclose` closes registry, not engines/HTTP client/executor's own resources.

`_setup_active_task` validates configuration history_length, reads original IDs, requires any explicitly supplied task ID to be caller-readable, builds context with **task=None**, takes resulting IDs, stores inline config if store present and submessage exists, then gets/creates active object with creation allowed and initial message. Inline registration is not gated by the same capability decorators as explicit config API. No config store means inline config is ignored; absent sender means stored config won't deliver. This method does not validate accepted_output_modes against card or enforce caller role independently.

Existing snapshot is read for existence but not passed to builder; producer later sets current_task. Missing continuation context ID can generate a new ID despite existing task. Supply both IDs or implement a builder that derives correct context under ownership constraints.

`_validate_task_id_match` logs mismatched agent IDs and raises InternalError. This handler-level check occurs for emitted/full Tasks in relevant paths; TaskManager has additional event ID checks. Do not infer that every output field is independently validated.

## Operation table: concrete handlers

Both V2/legacy implement these methods. Common access and payload behavior is genuinely equivalent; lifecycle differences follow separately.

| Method | Request → response | Behavior / failures |
|---|---|---|
| `on_get_task` | GetTaskRequest → Task | Required fields, nonnegative history; owner get; None→TaskNotFoundError; trims returned history only |
| `on_list_tasks` | ListTasksRequest → ListTasksResponse | Validates history and explicit page size; store.list; clears artifacts if not requested, trims task histories |
| `on_cancel_task` | CancelTaskRequest → Task | Owned-task cancellation; different execution semantics below |
| `on_message_send` | SendMessageRequest → Message or Task | Starts/continues execution, aggregates unary result; honors return_immediately |
| `on_message_send_stream` | SendMessageRequest → async events | Requires card.capabilities.streaming; execution plus live output |
| `on_subscribe_to_task` | SubscribeToTaskRequest → async events | Requires streaming; initial owned snapshot plus future queue events |
| `on_create_task_push_notification_config` | TaskPushNotificationConfig → same input object | Requires advertised push capability, config store, caller-readable Task; validates URL then set_info |
| `on_get_task_push_notification_config` | GetTaskPushNotificationConfigRequest → config | Same capability/store/task checks; scans owner's configs for exact ID; absent config→TaskNotFoundError |
| `on_list_task_push_notification_configs` | ListTaskPushNotificationConfigsRequest → configs response | Capability/store/task checks; owner config list; no page slicing implemented here |
| `on_delete_task_push_notification_config` | DeleteTaskPushNotificationConfigRequest → None | Capability/store/task checks; deletes config by ID; store missing-config delete is a logged no-op |
| `on_get_extended_agent_card` | GetExtendedAgentCardRequest → AgentCard | Requires advertised extended-card capability and configured card; optional async modifier(card, context); missing→ExtendedAgentCardNotConfiguredError |

Extended-card handler checks capability/configuration, **not** context.user.is_authenticated. Application middleware/custom handling must enforce access. Modifier receives shared configured protobuf card; copy before per-user modifications to avoid leaking mutations across requests.

## V2 send, stream, subscribe, cancel

`on_message_send` subscribes with status updates replaced by Task snapshots. It selects first Task on return_immediately or terminal/interrupted state. For FAILED in blocking mode it retains result but keeps consuming, allowing execution errors to surface. Messages become result while iteration continues through completion. If no selected result, awaits active_task.get_task. Applies history trimming to Task result. Returning immediately still waits for first relevant output; it is not a precreated task acknowledgment before executor emits anything.

`on_message_send_stream` performs setup, yields events; full Task IDs checked and history trimmed, other updates yielded unchanged. Subscription is tied to invocation completion, not merely task terminal state. A request may return for input-required while ActiveTask remains ready for continuation.

`on_subscribe_to_task` calls get_or_create(create_task_if_missing=False), then subscribe(include_initial_task=True). Can construct an idle coordinator from a nonterminal snapshot when no coordinator exists. This supplies no replay/resumption; observer may wait for a future send on that process. Terminal snapshot start raises InvalidParamsError.

`on_cancel_task` gets/creates owned coordinator, awaits cancel, maps InvalidParamsError to TaskNotCancelableError, rejects impossible Message result as InternalError. Missing owned Task remains TaskNotFoundError. Cancellation/shutdown hook order and failure details are in [execution](agent_execution_knowledge.md).

## `default_request_handler.py`: LegacyRequestHandler

Constructor takes same dependencies but actively uses supplied QueueManager or local InMemoryQueueManager. Holds running producer map with RLock and background task set.

`_setup_message_execution` creates per-request TaskManager, reads prior Task, rejects terminal state, adds new user message to cached history, rejects supplied nonexistent ID, builds context with prior Task, stores inline config, obtains create_or_tap queue, creates ResultAggregator, starts producer, registers it. Unlike V2 it does not use one serialized ActiveTask request loop; same-task requests can interact via taps/producers with weaker coordination. Builder receives existing Task; context consistency still depends on supplied IDs and constructor path.

`_run_event_stream` awaits executor.execute then graceful queue.close. Unhandled errors escape producer and are captured by consumer callback. `_register_producer` overwrites task-ID handle under lock; a custom distributed QueueManager does not make this map distributed.

`on_message_send` validates history, sets consumer callback, computes blocking from return_immediately, and uses consume_and_break_on_interrupt. Nested push_notification_callback calls `_send_push_notification_if_needed`. Background consumption and cleanup tasks are tracked. Exceptions cancel producer/re-raise. Result absent→InternalError; Task IDs checked/history trimmed. `_cleanup_producer` awaits producer (suppresses only cancellation), closes manager queue, then removes running map; other producer/close errors can interrupt map cleanup.

`on_message_send_stream` processes/persists and emits events with optional push; on CancelledError/GeneratorExit schedules consume_all in background so execution can continue, then re-raises. Cleanup always scheduled. Background continuation there has no push callback. Streaming history behavior differs from unary/V2; this method does not apply history trimming on each Task.

`on_subscribe_to_task` owner-loads snapshot, rejects terminal with UnsupportedOperationError, yields initial Task, requires existing tapped queue, then applies ResultAggregator while yielding. Unlike V2, tap absence is TaskNotFoundError after the initial yield.

`on_cancel_task` loads owned snapshot, rejects terminal, builds manager/aggregator, taps queue or creates legacy queue, awaits cancel hook, cancels tracked producer, consumes result, requires Task AND CANCELED; otherwise InternalError/TaskNotCancelableError. No V2 fallback forcing canceled snapshot.

`_send_push_notification_if_needed` sends only task-family events with sender present. `_track_background_task` records task and adds `_on_done` callback: calls result(), logs errors/cancellation, always removes set entry. No public legacy aclose drains this set. `_reject_unsafe_push_url` and `_validate_task_id_match` mirror V2. Shared CRUD/extended-card methods follow operation table.

## `response_helpers.py`

`agent_card_to_dict(card)` first serializes current protobuf; attempts to_compat_agent_card, swallowing only VersionNotSupportedError. Removes falsy legacy supportsAuthenticatedExtendedCard. Nested `merge` fills only missing keys, recursively merges dictionaries and same-index dict elements in overlapping list lengths. Existing core values win; it does not append extra compat list items. Discovery card can therefore include legacy fields when a compatible interface exists.

`build_error_response(request_id, error)` passes through JSONRPCError model, or maps exact A2A exception class to code/model and Google RPC details. Unrecognized errors use InternalError; subclass matching is not hierarchical. Serializes excluding None and wraps JSONRPC20Response.

`prepare_response_object(request_id, response, success_response_types)` accepts caller-provided allowed classes, converts protobuf to camelCase dict, wraps success. Domain/model errors produce error envelope; unexpected output type→InvalidAgentResponseError. It does not recursively convert arbitrary lists of protobuf values. Used as helper/compatibility API; modern dispatchers also build direct envelopes.

## `grpc_handler.py`

Requires grpcio; source subclasses generated A2AServiceServicer. `GrpcServerCallContextBuilder.build` is abstract. Default builder creates state['grpc_context'], unauthenticated user, extensions parsed from metadata. `build_user` always unauthenticated; customize to use verified credentials. `_get_metadata_value` matches key case-insensitively, decodes bytes as UTF-8; decode errors propagate.

`GrpcHandler.__init__` records RequestHandler/default builder. `_build_call_context` builds then copies request.tenant if present. `_handle_unary` / `_handle_stream` build context, invoke closure, and catch only A2AError to abort; unexpected exceptions remain gRPC/framework errors. Default response values are fallback after abort paths, not substitutes for domain success.

RPC wrappers are mechanical binding conversions with distinct results:

- `SendMessage`: handler Task/Message → SendMessageResponse oneof.
- `SendStreamingMessage`, `SubscribeToTask`: each event → StreamResponse through proto_utils.
- `GetTask`, `CancelTask`: None→TaskNotFoundError; otherwise Task.
- `CreateTaskPushNotificationConfig`, `GetTaskPushNotificationConfig`, `ListTaskPushNotificationConfigs`: delegate corresponding protobuf response.
- `DeleteTaskPushNotificationConfig`: None → google.protobuf.Empty.
- `ListTasks`: handler's ListTasksResponse.
- `GetExtendedAgentCard`: AgentCard.

Each has a nested `_handler` captured request closure. `abort_context` maps exact domain class to gRPC status, builds ErrorInfo reason/domain, optionally BadRequest field violations, serializes Status into grpc-status-details-bin, preserves existing trailing metadata, then aborts. Unknown class→UNKNOWN. No HTTP version decorator here; protobuf-native binding/version negotiation is separate from REST/JSON-RPC header validation. Transport identity defaults are not authentication.

The default gRPC builder's exact class name is `DefaultGrpcServerCallContextBuilder`; override its `build_user` or replace the builder to supply authenticated identity.
