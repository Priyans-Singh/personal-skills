# `grpc.py`: current gRPC transport

Source: a2a-sdk 1.1.4. Import requires gRPC plus Google RPC protobuf dependencies. Missing grpc raises installation-advice ImportError; factory/transports import guards can expose unavailable transport as None.

## Construction and encoding

`GrpcTransport.__init__(channel,agent_card)` retains channel/card and constructs generated `a2a_pb2_grpc.A2AServiceStub(channel)`. `create(card,url,config)` requires `grpc_channel_factory`, calls it with selected URL, returns transport. No default TLS/channel policy is created; the caller's factory controls channel security and transport options.

`_get_grpc_metadata(context)` starts `[('a2a-version','1.0')]`, appends lower-cased context parameter names and unchanged values. A supplied version parameter creates a duplicate entry, rather than replacing the mandatory one. `_get_grpc_timeout(context)` returns timeout or None. `context.state` remains local.

`_call_grpc(method,request,context,**kwargs)` passes protobuf request directly with metadata, deadline and any extra kwargs, awaits method and returns generated protobuf result. Serialization is performed by generated stub's `SerializeToString`/`FromString` callbacks.

## Operation delegates

`send_message`, `get_task`, `list_tasks`, `cancel_task`, `create_task_push_notification_config`, `get_task_push_notification_config`, `list_task_push_notification_configs`, `delete_task_push_notification_config` call `_call_grpc` with matching stub method from [wire map](transport_knowledge.md). Inputs/results follow core contracts, except **delete returns the generated `google.protobuf.Empty` object**, despite annotation `None`, because it returns `_call_grpc` unchanged. BaseClient/tenant delegates preserve that result.

`get_extended_agent_card` returns retained card if present and capability false; otherwise calls stub `GetExtendedAgentCard` through `_call_grpc`. Does not update transport card reference.

`send_message_streaming` and `subscribe` call `_call_grpc_stream` with stub `SendStreamingMessage` and `SubscribeToTask`, forwarding events. `_call_grpc_stream` creates the call with metadata/deadline, repeatedly awaits `stream.read`, stops on `grpc.aio.EOF`, yields each response. It does not buffer or reconnect. No explicit `stream.cancel()` finally block exists here for early iterator abandonment.

`close` awaits channel.close. There is no channel ownership flag or shared-channel reference count.

## Error conversion

`_handle_grpc_exception(func)` returns nested async `wrapper`, preserving metadata via `wraps`; it awaits func and catches only `grpc.aio.AioRpcError`, forwarding to `_map_grpc_error`. `_handle_grpc_stream_exception` returns nested async-generator `wrapper`, catches that error while iterating, and maps it. Every public ordinary/stream operation above uses the appropriate decorator. Close/helper errors are not independently normalized by these decorators.

`_map_grpc_error(e)`:

1. DEADLINE_EXCEEDED -> `A2AClientTimeoutError` with cause.
2. Calls `status_from_call` to extract Google `Status` from `grpc-status-details-bin` trailing metadata.
3. Iterates details: ErrorInfo domain exactly `a2a-protocol.org` selects mapped class from reason; BadRequest converts field violations to `{'errors':[{'field':..., 'message':...}]}`. This is validation data, not preserved ErrorInfo metadata.
4. If a mapped class is selected, raises it with status.message and collected validation data.
5. Otherwise raises generic `A2AClientError` containing status-code name/details.

`status_from_call` validates proto code/message against call code/details; mismatches raise ValueError and malformed binary can raise decoding errors. These are not converted by `_map_grpc_error`. Multiple ErrorInfo/BadRequest details can replace earlier selected class/data as iteration proceeds. Hook exceptions and locally malformed protobufs are outside the AioRpcError catch.

Tracing is supplied by `trace_class(kind=CLIENT)`. There is no automatic retry, token refresh or local consistency mechanism. gRPC library/channel settings may add behavior outside what this source establishes.
