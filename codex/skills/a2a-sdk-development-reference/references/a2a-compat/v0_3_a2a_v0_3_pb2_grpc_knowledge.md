# v0_3/a2a_v0_3_pb2_grpc.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/a2a_v0_3_pb2_grpc.py`. SHA-256: `bd39211ab6ea6c1ec4b1fbe85e77ae63c0f1a23df1a9aea48a12eb67fc44f921`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Generated RPC execution surface

The module imports grpc unconditionally; it is absent in inspected environment. `A2AServiceStub.__init__(channel)` constructs ten bound callables via channel.unary_unary or unary_stream, all with `_registered_method=True`, request SerializeToString and response FromString. These instance attributes are dynamically created APIs, not AST methods; the runtime service table below explicitly indexes them. Calling a bound callable uses channel scheduling/deadlines/metadata/credentials policy. Two RPCs are unary-stream (SendStreamingMessage, TaskSubscription); eight are unary-unary. No bidirectional/client streaming exists.

`A2AServiceServicer` contains ten defaults, each sets UNIMPLEMENTED, sets details 'Method not implemented!', then raises NotImplementedError. Override with CompatGrpcHandler for execution. `add_A2AServiceServicer_to_server(servicer,server)` binds request deserializers/response serializers and method cardinality, creates generic handler for `a2a.v1.A2AService`, calls both add_generic_rpc_handlers and add_registered_method_handlers. It registers handlers only; it does not bind ports, start server or manage shutdown.

Experimental `A2AService` static methods are genuinely mechanically identical delegates parameterized by RPC name and message/cardinality types. Each forwards request,target,options,channel_credentials,call_credentials,insecure,compression,wait_for_ready,timeout,metadata to grpc.experimental.unary_unary/unary_stream. Defaults options=(), credentials=None, insecure=False, compression/wait/timeout/metadata=None. These helpers may create/use runtime channels, and credentials go to target transport or request authorization respectively. Their lifetime/cache/TLS/retry behavior is controlled by gRPC, not guaranteed by this wrapper. Prefer an explicitly owned async channel and stub for CompatGrpcTransport.

Generated documentation's statements about cancellation ending updates are protocol intent, not enforced by generated defaults. Local server/core delegate decides actual task transitions. All methods use path `/a2a.v1.A2AService/<RPC>`; current service namespace differs. No custom domain error mapping exists in generated wrappers; compat transport/handler supplies that separately.

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
import grpc
from . import a2a_v0_3_pb2 as a2a__v0__3__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
```

## Declaration-by-declaration execution reference

### `A2AServiceStub`

Source lines 9–77; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): A2AService defines the gRPC version of the A2A protocol. This has a slightly different shape than the JSONRPC version to better conform to AIP-127, where appropriate. The nouns are AgentCard, Message, Task and TaskPushNotificationConfig. - Messages are not a standard resource so there is no get/delete/update/list interface, only a send and stream custom methods. - Tasks have a get interface and custom cancel and subscribe methods. - TaskPushNotificationConfig are a resource whose parent is a task. They have get, list and create methods. - AgentCard is a static resource with only a get method.

Declared operations: `__init__`. Each method is traced below; constructor determines retained state.

### `A2AServiceStub.__init__`

Source lines 22–77; declaration kind `FunctionDef`.

Inputs: `(self, channel)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Constructor. Args: channel: A grpc.Channel.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `self.SendMessage` from `channel.unary_unary('/a2a.v1.A2AService/SendMessage', request_serializer=a2a__v0__3__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.SendMessageResponse.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
2. Assigns `self.SendStreamingMessage` from `channel.unary_stream('/a2a.v1.A2AService/SendStreamingMessage', request_serializer=a2a__v0__3__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.StreamResponse.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
3. Assigns `self.GetTask` from `channel.unary_unary('/a2a.v1.A2AService/GetTask', request_serializer=a2a__v0__3__pb2.GetTaskRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.Task.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
4. Assigns `self.CancelTask` from `channel.unary_unary('/a2a.v1.A2AService/CancelTask', request_serializer=a2a__v0__3__pb2.CancelTaskRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.Task.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
5. Assigns `self.TaskSubscription` from `channel.unary_stream('/a2a.v1.A2AService/TaskSubscription', request_serializer=a2a__v0__3__pb2.TaskSubscriptionRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.StreamResponse.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
6. Assigns `self.CreateTaskPushNotificationConfig` from `channel.unary_unary('/a2a.v1.A2AService/CreateTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.CreateTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
7. Assigns `self.GetTaskPushNotificationConfig` from `channel.unary_unary('/a2a.v1.A2AService/GetTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
8. Assigns `self.ListTaskPushNotificationConfig` from `channel.unary_unary('/a2a.v1.A2AService/ListTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.ListTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.ListTaskPushNotificationConfigResponse.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
9. Assigns `self.GetAgentCard` from `channel.unary_unary('/a2a.v1.A2AService/GetAgentCard', request_serializer=a2a__v0__3__pb2.GetAgentCardRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.AgentCard.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.
10. Assigns `self.DeleteTaskPushNotificationConfig` from `channel.unary_unary('/a2a.v1.A2AService/DeleteTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)`; output construction/calls here execute immediately when this method runs.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `channel.unary_unary`, `channel.unary_stream`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def __init__(self, channel):
    self.SendMessage = channel.unary_unary('/a2a.v1.A2AService/SendMessage', request_serializer=a2a__v0__3__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.SendMessageResponse.FromString, _registered_method=True)
    self.SendStreamingMessage = channel.unary_stream('/a2a.v1.A2AService/SendStreamingMessage', request_serializer=a2a__v0__3__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.StreamResponse.FromString, _registered_method=True)
    self.GetTask = channel.unary_unary('/a2a.v1.A2AService/GetTask', request_serializer=a2a__v0__3__pb2.GetTaskRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.Task.FromString, _registered_method=True)
    self.CancelTask = channel.unary_unary('/a2a.v1.A2AService/CancelTask', request_serializer=a2a__v0__3__pb2.CancelTaskRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.Task.FromString, _registered_method=True)
    self.TaskSubscription = channel.unary_stream('/a2a.v1.A2AService/TaskSubscription', request_serializer=a2a__v0__3__pb2.TaskSubscriptionRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.StreamResponse.FromString, _registered_method=True)
    self.CreateTaskPushNotificationConfig = channel.unary_unary('/a2a.v1.A2AService/CreateTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.CreateTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)
    self.GetTaskPushNotificationConfig = channel.unary_unary('/a2a.v1.A2AService/GetTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)
    self.ListTaskPushNotificationConfig = channel.unary_unary('/a2a.v1.A2AService/ListTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.ListTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.ListTaskPushNotificationConfigResponse.FromString, _registered_method=True)
    self.GetAgentCard = channel.unary_unary('/a2a.v1.A2AService/GetAgentCard', request_serializer=a2a__v0__3__pb2.GetAgentCardRequest.SerializeToString, response_deserializer=a2a__v0__3__pb2.AgentCard.FromString, _registered_method=True)
    self.DeleteTaskPushNotificationConfig = channel.unary_unary('/a2a.v1.A2AService/DeleteTaskPushNotificationConfig', request_serializer=a2a__v0__3__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
```

</details>

### `A2AServiceServicer`

Source lines 80–167; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): A2AService defines the gRPC version of the A2A protocol. This has a slightly different shape than the JSONRPC version to better conform to AIP-127, where appropriate. The nouns are AgentCard, Message, Task and TaskPushNotificationConfig. - Messages are not a standard resource so there is no get/delete/update/list interface, only a send and stream custom methods. - Tasks have a get interface and custom cancel and subscribe methods. - TaskPushNotificationConfig are a resource whose parent is a task. They have get, list and create methods. - AgentCard is a static resource with only a get method.

Declared operations: `SendMessage`, `SendStreamingMessage`, `GetTask`, `CancelTask`, `TaskSubscription`, `CreateTaskPushNotificationConfig`, `GetTaskPushNotificationConfig`, `ListTaskPushNotificationConfig`, `GetAgentCard`, `DeleteTaskPushNotificationConfig`. Each method is traced below; constructor determines retained state.

### `A2AServiceServicer.SendMessage`

Source lines 93–99; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Send a message to the agent. This is a blocking call that will return the task once it is completed, or a LRO if requested.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def SendMessage(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.SendStreamingMessage`

Source lines 101–107; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: SendStreamingMessage is a streaming call that will return a stream of task update events until the Task is in an interrupted or terminal state.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def SendStreamingMessage(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.GetTask`

Source lines 109–114; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Get the current state of a task from the agent.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def GetTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.CancelTask`

Source lines 116–122; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Cancel a task from the agent. If supported one should expect no more task updates for the task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def CancelTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.TaskSubscription`

Source lines 124–132; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: TaskSubscription is a streaming call that will return a stream of task update events. This attaches the stream to an existing in process task. If the task is complete the stream will return the completed task (like GetTask) and close the stream.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def TaskSubscription(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.CreateTaskPushNotificationConfig`

Source lines 134–139; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Set a push notification config for a task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def CreateTaskPushNotificationConfig(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.GetTaskPushNotificationConfig`

Source lines 141–146; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Get a push notification config for a task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def GetTaskPushNotificationConfig(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.ListTaskPushNotificationConfig`

Source lines 148–153; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Get a list of push notifications configured for a task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def ListTaskPushNotificationConfig(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.GetAgentCard`

Source lines 155–160; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: GetAgentCard returns the agent card for the agent.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def GetAgentCard(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `A2AServiceServicer.DeleteTaskPushNotificationConfig`

Source lines 162–167; declaration kind `FunctionDef`.

Inputs: `(self, request, context)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Source intent: Delete a push notification config for a task.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Executes `context.set_code(grpc.StatusCode.UNIMPLEMENTED)`.
2. Executes `context.set_details('Method not implemented!')`.
3. Raises `NotImplementedError('Method not implemented!')`.

Explicit errors: `NotImplementedError('Method not implemented!')`. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `context.set_code`, `context.set_details`, `NotImplementedError`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def DeleteTaskPushNotificationConfig(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

</details>

### `add_A2AServiceServicer_to_server`

Source lines 170–226; declaration kind `FunctionDef`.

Inputs: `(servicer, server)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `none`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Assigns `rpc_method_handlers` from `{'SendMessage': grpc.unary_unary_rpc_method_handler(servicer.SendMessage, request_deserializer=a2a__v0__3__pb2.SendMessageRequest.FromString, response_serializer=a2a__v0__3__pb2.SendMessageResponse.SerializeToString), 'SendStreamingMessage': grpc.unary_stream_rpc_method_handler(servicer.SendStreamingMessage, request_deserializer=a2a__v0__3__pb2.SendMessageRe … (full expression in body below)`; output construction/calls here execute immediately when this method runs.
2. Assigns `generic_handler` from `grpc.method_handlers_generic_handler('a2a.v1.A2AService', rpc_method_handlers)`; output construction/calls here execute immediately when this method runs.
3. Executes `server.add_generic_rpc_handlers((generic_handler,))`.
4. Executes `server.add_registered_method_handlers('a2a.v1.A2AService', rpc_method_handlers)`.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.method_handlers_generic_handler`, `server.add_generic_rpc_handlers`, `server.add_registered_method_handlers`, `grpc.unary_unary_rpc_method_handler`, `grpc.unary_stream_rpc_method_handler`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
def add_A2AServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'SendMessage': grpc.unary_unary_rpc_method_handler(servicer.SendMessage, request_deserializer=a2a__v0__3__pb2.SendMessageRequest.FromString, response_serializer=a2a__v0__3__pb2.SendMessageResponse.SerializeToString), 'SendStreamingMessage': grpc.unary_stream_rpc_method_handler(servicer.SendStreamingMessage, request_deserializer=a2a__v0__3__pb2.SendMessageRequest.FromString, response_serializer=a2a__v0__3__pb2.StreamResponse.SerializeToString), 'GetTask': grpc.unary_unary_rpc_method_handler(servicer.GetTask, request_deserializer=a2a__v0__3__pb2.GetTaskRequest.FromString, response_serializer=a2a__v0__3__pb2.Task.SerializeToString), 'CancelTask': grpc.unary_unary_rpc_method_handler(servicer.CancelTask, request_deserializer=a2a__v0__3__pb2.CancelTaskRequest.FromString, response_serializer=a2a__v0__3__pb2.Task.SerializeToString), 'TaskSubscription': grpc.unary_stream_rpc_method_handler(servicer.TaskSubscription, request_deserializer=a2a__v0__3__pb2.TaskSubscriptionRequest.FromString, response_serializer=a2a__v0__3__pb2.StreamResponse.SerializeToString), 'CreateTaskPushNotificationConfig': grpc.unary_unary_rpc_method_handler(servicer.CreateTaskPushNotificationConfig, request_deserializer=a2a__v0__3__pb2.CreateTaskPushNotificationConfigRequest.FromString, response_serializer=a2a__v0__3__pb2.TaskPushNotificationConfig.SerializeToString), 'GetTaskPushNotificationConfig': grpc.unary_unary_rpc_method_handler(servicer.GetTaskPushNotificationConfig, request_deserializer=a2a__v0__3__pb2.GetTaskPushNotificationConfigRequest.FromString, response_serializer=a2a__v0__3__pb2.TaskPushNotificationConfig.SerializeToString), 'ListTaskPushNotificationConfig': grpc.unary_unary_rpc_method_handler(servicer.ListTaskPushNotificationConfig, request_deserializer=a2a__v0__3__pb2.ListTaskPushNotificationConfigRequest.FromString, response_serializer=a2a__v0__3__pb2.ListTaskPushNotificationConfigResponse.SerializeToString), 'GetAgentCard': grpc.unary_unary_rpc_method_handler(servicer.GetAgentCard, request_deserializer=a2a__v0__3__pb2.GetAgentCardRequest.FromString, response_serializer=a2a__v0__3__pb2.AgentCard.SerializeToString), 'DeleteTaskPushNotificationConfig': grpc.unary_unary_rpc_method_handler(servicer.DeleteTaskPushNotificationConfig, request_deserializer=a2a__v0__3__pb2.DeleteTaskPushNotificationConfigRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('a2a.v1.A2AService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('a2a.v1.A2AService', rpc_method_handlers)
```

</details>

### `A2AService`

Source lines 230–511; declaration kind `ClassDef`.

Bases: `object`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): A2AService defines the gRPC version of the A2A protocol. This has a slightly different shape than the JSONRPC version to better conform to AIP-127, where appropriate. The nouns are AgentCard, Message, Task and TaskPushNotificationConfig. - Messages are not a standard resource so there is no get/delete/update/list interface, only a send and stream custom methods. - Tasks have a get interface and custom cancel and subscribe methods. - TaskPushNotificationConfig are a resource whose parent is a task. They have get, list and create methods. - AgentCard is a static resource with only a get method.

Declared operations: `SendMessage`, `SendStreamingMessage`, `GetTask`, `CancelTask`, `TaskSubscription`, `CreateTaskPushNotificationConfig`, `GetTaskPushNotificationConfig`, `ListTaskPushNotificationConfig`, `GetAgentCard`, `DeleteTaskPushNotificationConfig`. Each method is traced below; constructor determines retained state.

### `A2AService.SendMessage`

Source lines 244–268; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/SendMessage', a2a__v0__3__pb2.SendMessageRequest.SerializeToString, a2a__v0__3__pb2.SendMessageResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def SendMessage(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/SendMessage', a2a__v0__3__pb2.SendMessageRequest.SerializeToString, a2a__v0__3__pb2.SendMessageResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.SendStreamingMessage`

Source lines 271–295; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_stream(request, target, '/a2a.v1.A2AService/SendStreamingMessage', a2a__v0__3__pb2.SendMessageRequest.SerializeToString, a2a__v0__3__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_stream`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def SendStreamingMessage(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_stream(request, target, '/a2a.v1.A2AService/SendStreamingMessage', a2a__v0__3__pb2.SendMessageRequest.SerializeToString, a2a__v0__3__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.GetTask`

Source lines 298–322; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/GetTask', a2a__v0__3__pb2.GetTaskRequest.SerializeToString, a2a__v0__3__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def GetTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/GetTask', a2a__v0__3__pb2.GetTaskRequest.SerializeToString, a2a__v0__3__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.CancelTask`

Source lines 325–349; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/CancelTask', a2a__v0__3__pb2.CancelTaskRequest.SerializeToString, a2a__v0__3__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def CancelTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/CancelTask', a2a__v0__3__pb2.CancelTaskRequest.SerializeToString, a2a__v0__3__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.TaskSubscription`

Source lines 352–376; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_stream(request, target, '/a2a.v1.A2AService/TaskSubscription', a2a__v0__3__pb2.TaskSubscriptionRequest.SerializeToString, a2a__v0__3__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_stream`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def TaskSubscription(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_stream(request, target, '/a2a.v1.A2AService/TaskSubscription', a2a__v0__3__pb2.TaskSubscriptionRequest.SerializeToString, a2a__v0__3__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.CreateTaskPushNotificationConfig`

Source lines 379–403; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/CreateTaskPushNotificationConfig', a2a__v0__3__pb2.CreateTaskPushNotificationConfigRequest.SerializeToString, a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=Tru … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def CreateTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/CreateTaskPushNotificationConfig', a2a__v0__3__pb2.CreateTaskPushNotificationConfigRequest.SerializeToString, a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.GetTaskPushNotificationConfig`

Source lines 406–430; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/GetTaskPushNotificationConfig', a2a__v0__3__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def GetTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/GetTaskPushNotificationConfig', a2a__v0__3__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, a2a__v0__3__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.ListTaskPushNotificationConfig`

Source lines 433–457; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/ListTaskPushNotificationConfig', a2a__v0__3__pb2.ListTaskPushNotificationConfigRequest.SerializeToString, a2a__v0__3__pb2.ListTaskPushNotificationConfigResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_me … (full expression in body below)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def ListTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/ListTaskPushNotificationConfig', a2a__v0__3__pb2.ListTaskPushNotificationConfigRequest.SerializeToString, a2a__v0__3__pb2.ListTaskPushNotificationConfigResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.GetAgentCard`

Source lines 460–484; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/GetAgentCard', a2a__v0__3__pb2.GetAgentCardRequest.SerializeToString, a2a__v0__3__pb2.AgentCard.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def GetAgentCard(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/GetAgentCard', a2a__v0__3__pb2.GetAgentCardRequest.SerializeToString, a2a__v0__3__pb2.AgentCard.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>

### `A2AService.DeleteTaskPushNotificationConfig`

Source lines 487–511; declaration kind `FunctionDef`.

Inputs: `(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`. Output annotation: `not annotated; see return/yield expressions`. Decorators: `staticmethod`.

Ordered implementation behavior (expressions name exact fields/delegates):

1. Returns `grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/DeleteTaskPushNotificationConfig', a2a__v0__3__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)`; this is the output/delegation boundary for this path.

Explicit errors: no explicit raise statement. Called conversion/runtime/delegate errors propagate unless the shown try clauses catch them.

Direct calls/delegation: `grpc.experimental.unary_unary`. Nested closure calls are included; branch conditions determine which execute.

<details>
<summary>Exact executable implementation (source docstrings omitted)</summary>

```python
@staticmethod
def DeleteTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/a2a.v1.A2AService/DeleteTaskPushNotificationConfig', a2a__v0__3__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

</details>
