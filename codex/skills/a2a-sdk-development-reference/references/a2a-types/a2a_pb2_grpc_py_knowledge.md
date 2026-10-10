# `types/a2a_pb2_grpc.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/types/a2a_pb2_grpc.py`. SHA-256: `401e653ec5e4261bf29fb91839a54341b97162f4e701a45085accea06067b49e`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import grpc
from . import a2a_pb2 as a2a__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
```

Generated transport wiring requires grpc at import; grpc is absent in the inspected environment. AST and descriptors were inspected without importing this file or contacting a server. A2AServiceStub construction binds channel callable attributes; no RPC is issued until caller invokes one. A2AServiceServicer methods are unimplemented; registration installs handlers on an already-created server. Experimental A2AService static methods initiate RPCs by delegating to grpc.experimental.

The wrapper does not authorize tenants, fetch secrets, retry, persist tasks, or implement cancellation rules. Channel credentials secure target transport; call_credentials/metadata are forwarded to target per RPC, with lifetime controlled by gRPC/channel and caller. timeout/deadline, compression, wait_for_ready and options pass through. Streaming has no local resume/replay loop or consistency guarantee. Use an appropriate sync or grpc.aio channel and caller deadlines/cancellation; awaitability comes from chosen channel, not this module.

## Public/constants/type aliases and module initialization

## Declarations and execution

### `A2AServiceStub` (line 9)

Coverage ID: `a2a_pb2_grpc.py:9:A2AServiceStub`.

Binds all 11 callable RPC attributes on provided channel; mapping below specifies distinct input/output and streaming cardinality.

```python
class A2AServiceStub(object):

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendMessage = channel.unary_unary('/lf.a2a.v1.A2AService/SendMessage', request_serializer=a2a__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__pb2.SendMessageResponse.FromString, _registered_method=True)
        self.SendStreamingMessage = channel.unary_stream('/lf.a2a.v1.A2AService/SendStreamingMessage', request_serializer=a2a__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__pb2.StreamResponse.FromString, _registered_method=True)
        self.GetTask = channel.unary_unary('/lf.a2a.v1.A2AService/GetTask', request_serializer=a2a__pb2.GetTaskRequest.SerializeToString, response_deserializer=a2a__pb2.Task.FromString, _registered_method=True)
        self.ListTasks = channel.unary_unary('/lf.a2a.v1.A2AService/ListTasks', request_serializer=a2a__pb2.ListTasksRequest.SerializeToString, response_deserializer=a2a__pb2.ListTasksResponse.FromString, _registered_method=True)
        self.CancelTask = channel.unary_unary('/lf.a2a.v1.A2AService/CancelTask', request_serializer=a2a__pb2.CancelTaskRequest.SerializeToString, response_deserializer=a2a__pb2.Task.FromString, _registered_method=True)
        self.SubscribeToTask = channel.unary_stream('/lf.a2a.v1.A2AService/SubscribeToTask', request_serializer=a2a__pb2.SubscribeToTaskRequest.SerializeToString, response_deserializer=a2a__pb2.StreamResponse.FromString, _registered_method=True)
        self.CreateTaskPushNotificationConfig = channel.unary_unary('/lf.a2a.v1.A2AService/CreateTaskPushNotificationConfig', request_serializer=a2a__pb2.TaskPushNotificationConfig.SerializeToString, response_deserializer=a2a__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)
        self.GetTaskPushNotificationConfig = channel.unary_unary('/lf.a2a.v1.A2AService/GetTaskPushNotificationConfig', request_serializer=a2a__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)
        self.ListTaskPushNotificationConfigs = channel.unary_unary('/lf.a2a.v1.A2AService/ListTaskPushNotificationConfigs', request_serializer=a2a__pb2.ListTaskPushNotificationConfigsRequest.SerializeToString, response_deserializer=a2a__pb2.ListTaskPushNotificationConfigsResponse.FromString, _registered_method=True)
        self.GetExtendedAgentCard = channel.unary_unary('/lf.a2a.v1.A2AService/GetExtendedAgentCard', request_serializer=a2a__pb2.GetExtendedAgentCardRequest.SerializeToString, response_deserializer=a2a__pb2.AgentCard.FromString, _registered_method=True)
        self.DeleteTaskPushNotificationConfig = channel.unary_unary('/lf.a2a.v1.A2AService/DeleteTaskPushNotificationConfig', request_serializer=a2a__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
```

### `A2AServiceStub.__init__` (line 13)

Coverage ID: `a2a_pb2_grpc.py:13:A2AServiceStub.__init__`.

For each RPC creates unary_unary or unary_stream callable using exact service path, request SerializeToString, response FromString, _registered_method=True; stores callable on self. Does not own channel lifecycle or close it.

```python
def __init__(self, channel):
    self.SendMessage = channel.unary_unary('/lf.a2a.v1.A2AService/SendMessage', request_serializer=a2a__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__pb2.SendMessageResponse.FromString, _registered_method=True)
    self.SendStreamingMessage = channel.unary_stream('/lf.a2a.v1.A2AService/SendStreamingMessage', request_serializer=a2a__pb2.SendMessageRequest.SerializeToString, response_deserializer=a2a__pb2.StreamResponse.FromString, _registered_method=True)
    self.GetTask = channel.unary_unary('/lf.a2a.v1.A2AService/GetTask', request_serializer=a2a__pb2.GetTaskRequest.SerializeToString, response_deserializer=a2a__pb2.Task.FromString, _registered_method=True)
    self.ListTasks = channel.unary_unary('/lf.a2a.v1.A2AService/ListTasks', request_serializer=a2a__pb2.ListTasksRequest.SerializeToString, response_deserializer=a2a__pb2.ListTasksResponse.FromString, _registered_method=True)
    self.CancelTask = channel.unary_unary('/lf.a2a.v1.A2AService/CancelTask', request_serializer=a2a__pb2.CancelTaskRequest.SerializeToString, response_deserializer=a2a__pb2.Task.FromString, _registered_method=True)
    self.SubscribeToTask = channel.unary_stream('/lf.a2a.v1.A2AService/SubscribeToTask', request_serializer=a2a__pb2.SubscribeToTaskRequest.SerializeToString, response_deserializer=a2a__pb2.StreamResponse.FromString, _registered_method=True)
    self.CreateTaskPushNotificationConfig = channel.unary_unary('/lf.a2a.v1.A2AService/CreateTaskPushNotificationConfig', request_serializer=a2a__pb2.TaskPushNotificationConfig.SerializeToString, response_deserializer=a2a__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)
    self.GetTaskPushNotificationConfig = channel.unary_unary('/lf.a2a.v1.A2AService/GetTaskPushNotificationConfig', request_serializer=a2a__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=a2a__pb2.TaskPushNotificationConfig.FromString, _registered_method=True)
    self.ListTaskPushNotificationConfigs = channel.unary_unary('/lf.a2a.v1.A2AService/ListTaskPushNotificationConfigs', request_serializer=a2a__pb2.ListTaskPushNotificationConfigsRequest.SerializeToString, response_deserializer=a2a__pb2.ListTaskPushNotificationConfigsResponse.FromString, _registered_method=True)
    self.GetExtendedAgentCard = channel.unary_unary('/lf.a2a.v1.A2AService/GetExtendedAgentCard', request_serializer=a2a__pb2.GetExtendedAgentCardRequest.SerializeToString, response_deserializer=a2a__pb2.AgentCard.FromString, _registered_method=True)
    self.DeleteTaskPushNotificationConfig = channel.unary_unary('/lf.a2a.v1.A2AService/DeleteTaskPushNotificationConfig', request_serializer=a2a__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
```

### `A2AServiceServicer` (line 76)

Coverage ID: `a2a_pb2_grpc.py:76:A2AServiceServicer`.

Base service skeleton, every RPC method marks UNIMPLEMENTED then raises; subclass must implement operational behavior.

```python
class A2AServiceServicer(object):

    def SendMessage(self, request, context):
        """Sends a message to an agent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendStreamingMessage(self, request, context):
        """Sends a streaming message to an agent, allowing for real-time interaction and status updates.
        Streaming version of `SendMessage`
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTask(self, request, context):
        """Gets the latest state of a task.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListTasks(self, request, context):
        """Lists tasks that match the specified filter.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelTask(self, request, context):
        """Cancels a task in progress.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeToTask(self, request, context):
        """Subscribes to task updates for tasks not in a terminal state.
        Returns `UnsupportedOperationError` if the task is already in a terminal state (completed, failed, canceled, rejected).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateTaskPushNotificationConfig(self, request, context):
        """(-- api-linter: client-libraries::4232::required-fields=disabled
        api-linter: core::0133::method-signature=disabled
        api-linter: core::0133::request-message-name=disabled
        aip.dev/not-precedent: method_signature preserved for backwards compatibility --)
        Creates a push notification config for a task.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTaskPushNotificationConfig(self, request, context):
        """Gets a push notification config for a task.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListTaskPushNotificationConfigs(self, request, context):
        """Get a list of push notifications configured for a task.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetExtendedAgentCard(self, request, context):
        """Gets the extended agent card for the authenticated agent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTaskPushNotificationConfig(self, request, context):
        """Deletes a push notification config for a task.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.SendMessage` (line 80)

Coverage ID: `a2a_pb2_grpc.py:80:A2AServiceServicer.SendMessage`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def SendMessage(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.SendStreamingMessage` (line 87)

Coverage ID: `a2a_pb2_grpc.py:87:A2AServiceServicer.SendStreamingMessage`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def SendStreamingMessage(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.GetTask` (line 95)

Coverage ID: `a2a_pb2_grpc.py:95:A2AServiceServicer.GetTask`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def GetTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.ListTasks` (line 102)

Coverage ID: `a2a_pb2_grpc.py:102:A2AServiceServicer.ListTasks`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def ListTasks(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.CancelTask` (line 109)

Coverage ID: `a2a_pb2_grpc.py:109:A2AServiceServicer.CancelTask`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def CancelTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.SubscribeToTask` (line 116)

Coverage ID: `a2a_pb2_grpc.py:116:A2AServiceServicer.SubscribeToTask`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def SubscribeToTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.CreateTaskPushNotificationConfig` (line 124)

Coverage ID: `a2a_pb2_grpc.py:124:A2AServiceServicer.CreateTaskPushNotificationConfig`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def CreateTaskPushNotificationConfig(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.GetTaskPushNotificationConfig` (line 135)

Coverage ID: `a2a_pb2_grpc.py:135:A2AServiceServicer.GetTaskPushNotificationConfig`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def GetTaskPushNotificationConfig(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.ListTaskPushNotificationConfigs` (line 142)

Coverage ID: `a2a_pb2_grpc.py:142:A2AServiceServicer.ListTaskPushNotificationConfigs`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def ListTaskPushNotificationConfigs(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.GetExtendedAgentCard` (line 149)

Coverage ID: `a2a_pb2_grpc.py:149:A2AServiceServicer.GetExtendedAgentCard`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def GetExtendedAgentCard(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `A2AServiceServicer.DeleteTaskPushNotificationConfig` (line 156)

Coverage ID: `a2a_pb2_grpc.py:156:A2AServiceServicer.DeleteTaskPushNotificationConfig`.

Accepts request and context. Sets grpc.StatusCode.UNIMPLEMENTED and details Method not implemented!, then raises NotImplementedError. Documented task semantics in generated docstrings are protocol intent; skeleton does not implement them.

```python
def DeleteTaskPushNotificationConfig(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

### `add_A2AServiceServicer_to_server` (line 164)

Coverage ID: `a2a_pb2_grpc.py:164:add_A2AServiceServicer_to_server`.

Builds handler dictionary keyed by RPC method; chooses unary_unary or unary_stream, deserializes request FromString, serializes response SerializeToString. Registers generic handler tuple and registered method handlers on server under lf.a2a.v1.A2AService. Mutates server registration; starts no server and executes no request.

```python
def add_A2AServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'SendMessage': grpc.unary_unary_rpc_method_handler(servicer.SendMessage, request_deserializer=a2a__pb2.SendMessageRequest.FromString, response_serializer=a2a__pb2.SendMessageResponse.SerializeToString), 'SendStreamingMessage': grpc.unary_stream_rpc_method_handler(servicer.SendStreamingMessage, request_deserializer=a2a__pb2.SendMessageRequest.FromString, response_serializer=a2a__pb2.StreamResponse.SerializeToString), 'GetTask': grpc.unary_unary_rpc_method_handler(servicer.GetTask, request_deserializer=a2a__pb2.GetTaskRequest.FromString, response_serializer=a2a__pb2.Task.SerializeToString), 'ListTasks': grpc.unary_unary_rpc_method_handler(servicer.ListTasks, request_deserializer=a2a__pb2.ListTasksRequest.FromString, response_serializer=a2a__pb2.ListTasksResponse.SerializeToString), 'CancelTask': grpc.unary_unary_rpc_method_handler(servicer.CancelTask, request_deserializer=a2a__pb2.CancelTaskRequest.FromString, response_serializer=a2a__pb2.Task.SerializeToString), 'SubscribeToTask': grpc.unary_stream_rpc_method_handler(servicer.SubscribeToTask, request_deserializer=a2a__pb2.SubscribeToTaskRequest.FromString, response_serializer=a2a__pb2.StreamResponse.SerializeToString), 'CreateTaskPushNotificationConfig': grpc.unary_unary_rpc_method_handler(servicer.CreateTaskPushNotificationConfig, request_deserializer=a2a__pb2.TaskPushNotificationConfig.FromString, response_serializer=a2a__pb2.TaskPushNotificationConfig.SerializeToString), 'GetTaskPushNotificationConfig': grpc.unary_unary_rpc_method_handler(servicer.GetTaskPushNotificationConfig, request_deserializer=a2a__pb2.GetTaskPushNotificationConfigRequest.FromString, response_serializer=a2a__pb2.TaskPushNotificationConfig.SerializeToString), 'ListTaskPushNotificationConfigs': grpc.unary_unary_rpc_method_handler(servicer.ListTaskPushNotificationConfigs, request_deserializer=a2a__pb2.ListTaskPushNotificationConfigsRequest.FromString, response_serializer=a2a__pb2.ListTaskPushNotificationConfigsResponse.SerializeToString), 'GetExtendedAgentCard': grpc.unary_unary_rpc_method_handler(servicer.GetExtendedAgentCard, request_deserializer=a2a__pb2.GetExtendedAgentCardRequest.FromString, response_serializer=a2a__pb2.AgentCard.SerializeToString), 'DeleteTaskPushNotificationConfig': grpc.unary_unary_rpc_method_handler(servicer.DeleteTaskPushNotificationConfig, request_deserializer=a2a__pb2.DeleteTaskPushNotificationConfigRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('lf.a2a.v1.A2AService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('lf.a2a.v1.A2AService', rpc_method_handlers)
```

### `A2AService` (line 229)

Coverage ID: `a2a_pb2_grpc.py:229:A2AService`.

Experimental static RPC entry points with identical forwarding family; individual methods below preserve distinct request/response serializers and service paths.

```python
class A2AService(object):

    @staticmethod
    def SendMessage(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/SendMessage', a2a__pb2.SendMessageRequest.SerializeToString, a2a__pb2.SendMessageResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def SendStreamingMessage(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_stream(request, target, '/lf.a2a.v1.A2AService/SendStreamingMessage', a2a__pb2.SendMessageRequest.SerializeToString, a2a__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/GetTask', a2a__pb2.GetTaskRequest.SerializeToString, a2a__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListTasks(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/ListTasks', a2a__pb2.ListTasksRequest.SerializeToString, a2a__pb2.ListTasksResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CancelTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/CancelTask', a2a__pb2.CancelTaskRequest.SerializeToString, a2a__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def SubscribeToTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_stream(request, target, '/lf.a2a.v1.A2AService/SubscribeToTask', a2a__pb2.SubscribeToTaskRequest.SerializeToString, a2a__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CreateTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/CreateTaskPushNotificationConfig', a2a__pb2.TaskPushNotificationConfig.SerializeToString, a2a__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/GetTaskPushNotificationConfig', a2a__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, a2a__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListTaskPushNotificationConfigs(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/ListTaskPushNotificationConfigs', a2a__pb2.ListTaskPushNotificationConfigsRequest.SerializeToString, a2a__pb2.ListTaskPushNotificationConfigsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetExtendedAgentCard(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/GetExtendedAgentCard', a2a__pb2.GetExtendedAgentCardRequest.SerializeToString, a2a__pb2.AgentCard.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/DeleteTaskPushNotificationConfig', a2a__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.SendMessage` (line 234)

Coverage ID: `a2a_pb2_grpc.py:234:A2AService.SendMessage`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def SendMessage(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/SendMessage', a2a__pb2.SendMessageRequest.SerializeToString, a2a__pb2.SendMessageResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.SendStreamingMessage` (line 261)

Coverage ID: `a2a_pb2_grpc.py:261:A2AService.SendStreamingMessage`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def SendStreamingMessage(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_stream(request, target, '/lf.a2a.v1.A2AService/SendStreamingMessage', a2a__pb2.SendMessageRequest.SerializeToString, a2a__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.GetTask` (line 288)

Coverage ID: `a2a_pb2_grpc.py:288:A2AService.GetTask`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def GetTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/GetTask', a2a__pb2.GetTaskRequest.SerializeToString, a2a__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.ListTasks` (line 315)

Coverage ID: `a2a_pb2_grpc.py:315:A2AService.ListTasks`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def ListTasks(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/ListTasks', a2a__pb2.ListTasksRequest.SerializeToString, a2a__pb2.ListTasksResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.CancelTask` (line 342)

Coverage ID: `a2a_pb2_grpc.py:342:A2AService.CancelTask`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def CancelTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/CancelTask', a2a__pb2.CancelTaskRequest.SerializeToString, a2a__pb2.Task.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.SubscribeToTask` (line 369)

Coverage ID: `a2a_pb2_grpc.py:369:A2AService.SubscribeToTask`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def SubscribeToTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_stream(request, target, '/lf.a2a.v1.A2AService/SubscribeToTask', a2a__pb2.SubscribeToTaskRequest.SerializeToString, a2a__pb2.StreamResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.CreateTaskPushNotificationConfig` (line 396)

Coverage ID: `a2a_pb2_grpc.py:396:A2AService.CreateTaskPushNotificationConfig`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def CreateTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/CreateTaskPushNotificationConfig', a2a__pb2.TaskPushNotificationConfig.SerializeToString, a2a__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.GetTaskPushNotificationConfig` (line 423)

Coverage ID: `a2a_pb2_grpc.py:423:A2AService.GetTaskPushNotificationConfig`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def GetTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/GetTaskPushNotificationConfig', a2a__pb2.GetTaskPushNotificationConfigRequest.SerializeToString, a2a__pb2.TaskPushNotificationConfig.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.ListTaskPushNotificationConfigs` (line 450)

Coverage ID: `a2a_pb2_grpc.py:450:A2AService.ListTaskPushNotificationConfigs`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def ListTaskPushNotificationConfigs(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/ListTaskPushNotificationConfigs', a2a__pb2.ListTaskPushNotificationConfigsRequest.SerializeToString, a2a__pb2.ListTaskPushNotificationConfigsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.GetExtendedAgentCard` (line 477)

Coverage ID: `a2a_pb2_grpc.py:477:A2AService.GetExtendedAgentCard`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def GetExtendedAgentCard(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/GetExtendedAgentCard', a2a__pb2.GetExtendedAgentCardRequest.SerializeToString, a2a__pb2.AgentCard.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```

### `A2AService.DeleteTaskPushNotificationConfig` (line 504)

Coverage ID: `a2a_pb2_grpc.py:504:A2AService.DeleteTaskPushNotificationConfig`.

Returns grpc.experimental unary_unary/unary_stream result for corresponding RPC path. Passes request,target, serializers,options,channel_credentials,insecure,call_credentials,compression,wait_for_ready,timeout,metadata and _registered_method=True. External gRPC errors/deadline/cancellation propagate; no local catch/retry. This is the point that can issue network I/O, unlike stub construction.

```python
@staticmethod
def DeleteTaskPushNotificationConfig(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
    return grpc.experimental.unary_unary(request, target, '/lf.a2a.v1.A2AService/DeleteTaskPushNotificationConfig', a2a__pb2.DeleteTaskPushNotificationConfigRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
```
