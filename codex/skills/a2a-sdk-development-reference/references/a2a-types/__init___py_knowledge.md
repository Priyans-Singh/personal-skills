# `types/__init__.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/types/__init__.py`. SHA-256: `d8e0b9a3928f7b6a6982c58a2af2c312039ba7aa993326d5cbe50ada008dc542`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
from a2a.types.a2a_pb2 import APIKeySecurityScheme, AgentCapabilities, AgentCard, AgentCardSignature, AgentExtension, AgentInterface, AgentProvider, AgentSkill, Artifact, AuthenticationInfo, AuthorizationCodeOAuthFlow, CancelTaskRequest, ClientCredentialsOAuthFlow, DeleteTaskPushNotificationConfigRequest, DeviceCodeOAuthFlow, GetExtendedAgentCardRequest, GetTaskPushNotificationConfigRequest, GetTaskRequest, HTTPAuthSecurityScheme, ImplicitOAuthFlow, ListTaskPushNotificationConfigsRequest, ListTaskPushNotificationConfigsResponse, ListTasksRequest, ListTasksResponse, Message, MutualTlsSecurityScheme, OAuth2SecurityScheme, OAuthFlows, OpenIdConnectSecurityScheme, Part, PasswordOAuthFlow, Role, SecurityRequirement, SecurityScheme, SendMessageConfiguration, SendMessageRequest, SendMessageResponse, StreamResponse, StringList, SubscribeToTaskRequest, Task, TaskArtifactUpdateEvent, TaskPushNotificationConfig, TaskState, TaskStatus, TaskStatusUpdateEvent
from a2a.utils.errors import ContentTypeNotSupportedError, ExtendedAgentCardNotConfiguredError, ExtensionSupportRequiredError, InternalError, InvalidAgentResponseError, InvalidParamsError, InvalidRequestError, MethodNotFoundError, PushNotificationNotSupportedError, TaskNotCancelableError, TaskNotFoundError, UnsupportedOperationError, VersionNotSupportedError
```

This package re-exports generated message classes and SDK error classes; no gRPC import or connection is required. A2ARequest is a union alias, not validation/dispatch. Its members omit ListTasksRequest and DeleteTaskPushNotificationConfigRequest even though both are exported. Enum value constants are accessible through a2a_pb2, not all re-exported here.

## Public/constants/type aliases and module initialization

```python
A2ARequest = SendMessageRequest | GetTaskRequest | CancelTaskRequest | TaskPushNotificationConfig | GetTaskPushNotificationConfigRequest | SubscribeToTaskRequest | GetExtendedAgentCardRequest | ListTaskPushNotificationConfigsRequest
```

```python
__all__ = ['A2ARequest', 'APIKeySecurityScheme', 'AgentCapabilities', 'AgentCard', 'AgentCardSignature', 'AgentExtension', 'AgentInterface', 'AgentProvider', 'AgentSkill', 'Artifact', 'AuthenticationInfo', 'AuthorizationCodeOAuthFlow', 'CancelTaskRequest', 'ClientCredentialsOAuthFlow', 'ContentTypeNotSupportedError', 'DeleteTaskPushNotificationConfigRequest', 'DeviceCodeOAuthFlow', 'ExtendedAgentCardNotConfiguredError', 'ExtensionSupportRequiredError', 'GetExtendedAgentCardRequest', 'GetTaskPushNotificationConfigRequest', 'GetTaskRequest', 'HTTPAuthSecurityScheme', 'ImplicitOAuthFlow', 'InternalError', 'InvalidAgentResponseError', 'InvalidParamsError', 'InvalidRequestError', 'ListTaskPushNotificationConfigsRequest', 'ListTaskPushNotificationConfigsResponse', 'ListTasksRequest', 'ListTasksResponse', 'Message', 'MethodNotFoundError', 'MutualTlsSecurityScheme', 'OAuth2SecurityScheme', 'OAuthFlows', 'OpenIdConnectSecurityScheme', 'Part', 'PasswordOAuthFlow', 'PushNotificationNotSupportedError', 'Role', 'SecurityRequirement', 'SecurityScheme', 'SendMessageConfiguration', 'SendMessageRequest', 'SendMessageResponse', 'StreamResponse', 'StringList', 'SubscribeToTaskRequest', 'Task', 'TaskArtifactUpdateEvent', 'TaskNotCancelableError', 'TaskNotFoundError', 'TaskPushNotificationConfig', 'TaskState', 'TaskStatus', 'TaskStatusUpdateEvent', 'UnsupportedOperationError', 'VersionNotSupportedError']
```

## Declarations and execution
