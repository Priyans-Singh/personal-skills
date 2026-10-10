# v0_3/types.py execution reference

Inspected a2a-sdk **1.1.4**, **2026-10-07**. Source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/compat/v0_3/types.py`. SHA-256: `9445f481fb4cebb7dccbe2dc6ea2df055773550210cc9773b093a0f95f631a3d`. [Navigation](README.md) · [Source manifest](source_manifest.json) · [Callable index](callable_index.md).

## Model execution and public construction

`types.py` declares legacy v0.3 Pydantic schema classes and string Enums; no local validators, methods, network calls, timeouts or credential providers exist. Each class below has its exact bases, fields, annotations/defaults and source definitions. Fields without defaults (or Field(...)) are required; defaults of None are optional; Literal fields constrain kind/type/method/jsonrpc/code. Lists can be empty unless explicitly constrained; URL/timestamp/base64 fields are ordinary strings, not verified/fetched/decoded by these models. Semantic text below is source schema commentary, distinguished from executed constraints.

External A2ABaseModel body configures validate_by_name=True, validate_by_alias=True, serialize_by_alias=True and a to_camel_custom alias generator that strips trailing underscores before camelizing. Thus message_id ↔ messageId, in_ ↔ in. Its docstring claims deprecated camelCase attribute access but body has no custom get/set warning implementation. Do not rely on that docstring. Pydantic owns model_validate/model_validate_json/model_dump/model_dump_json and ValidationError behavior. Default extra handling is inherited Pydantic ignore, so undeclared tenant/unknown fields are not retained by these models.

RootModel subclasses wrap `root` internally but serialize underlying value directly. Part is text/file/data union; SecurityScheme is API key/HTTP/OAuth2/OIDC/mTLS union; A2ARequest/JSONRPCResponse and method-specific responses union valid envelopes. A2AError is a schema root, **not** a Python Exception to raise. Concrete *Error models are wire payloads; executable errors come from a2a.utils.errors. Request envelope ID correlates JSON-RPC calls; Task.id, Message.message_id, Task.context_id and PushNotificationConfig.id identify separate business objects.

TaskState contains submitted/working/input-required/completed/canceled/failed/rejected/auth-required/unknown. Role is agent/user; In is cookie/header/query; TransportProtocol is JSONRPC/GRPC/HTTP+JSON. Interface transport and preferred_transport are strings, not constrained to TransportProtocol. OAuthFlows allows multiple or zero flows even though protobuf uses oneof; converter precedence resolves that mismatch. AgentCard.protocol_version default is 0.3.0, distinct from adapter header constant 0.3. Provider/card version is application version, not SDK distribution version.

Callback configuration URL, token and authentication credentials remain in memory for model lifetime; no secret redaction, expiry or refresh is defined here. Card security schemes and requirements describe authentication but do not authenticate users. Card signatures are opaque payload fields. TaskStatusUpdateEvent.final is required, but task terminality and streaming policy are external.

```python
from a2a.compat.v0_3 import types
request = types.SendMessageRequest(id='rpc-1', params=types.MessageSendParams(
    message=types.Message(message_id='msg-1', role='user',
        parts=[types.Part(root=types.TextPart(text='hello'))])))
payload = request.model_dump(mode='json', by_alias=True, exclude_none=True)
assert payload['params']['message']['messageId'] == 'msg-1'
```

## Direct import boundaries

Imports below identify execution/type-checking dependencies. Optional try/TYPE_CHECKING guards are preserved in source bodies; importing a module does not prove every optional backend is installed. See [shared boundaries](execution_boundaries_knowledge.md).

```python
from __future__ import annotations
from enum import Enum
from typing import Any, Literal
from pydantic import Field, RootModel
from a2a._base import A2ABaseModel
```

## Declaration-by-declaration execution reference

### `A2A`

Source lines 14–15; declaration kind `ClassDef`.

Bases: `RootModel[Any]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | Any | **required / no default** |  |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: Any
```

### `In`

Source lines 18–25; declaration kind `ClassDef`.

Bases: `str, Enum`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): The location of the API key.

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
cookie = 'cookie'
header = 'header'
query = 'query'
```

### `APIKeySecurityScheme`

Source lines 28–48; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines a security scheme using an API key.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| description | str &#124; None | None | An optional description for the security scheme. |
| in_ | In | **required / no default** | The location of the API key. |
| name | str | **required / no default** | The name of the header, query, or cookie parameter to be used. |
| type | Literal['apiKey'] | 'apiKey' | The type of the security scheme. Must be 'apiKey'. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
description: str | None = None
in_: In
name: str
type: Literal['apiKey'] = 'apiKey'
```

### `AgentCardSignature`

Source lines 51–69; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): AgentCardSignature represents a JWS signature of an AgentCard. This follows the JSON format of an RFC 7515 JSON Web Signature (JWS).

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| header | dict[str, Any] &#124; None | None | The unprotected JWS header values. |
| protected | str | **required / no default** | The protected JWS header for the signature. This is a Base64url-encoded JSON object, as per RFC 7515. |
| signature | str | **required / no default** | The computed signature, Base64url-encoded. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
header: dict[str, Any] | None = None
protected: str
signature: str
```

### `AgentExtension`

Source lines 72–93; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): A declaration of a protocol extension supported by an Agent.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| description | str &#124; None | None | A human-readable description of how this agent uses the extension. |
| params | dict[str, Any] &#124; None | None | Optional, extension-specific configuration parameters. |
| required | bool &#124; None | None | If true, the client must understand and comply with the extension's requirements to interact with the agent. |
| uri | str | **required / no default** | The unique URI identifying the extension. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
description: str | None = None
params: dict[str, Any] | None = None
required: bool | None = None
uri: str
```

### `AgentInterface`

Source lines 96–116; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Declares a combination of a target URL and a transport protocol for interacting with the agent. This allows agents to expose the same functionality over multiple transport mechanisms.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| transport | str | Field(..., examples=['JSONRPC', 'GRPC', 'HTTP+JSON']) | The transport protocol supported at this URL. |
| url | str | Field(..., examples=['https://api.example.com/a2a/v1', 'https://grpc.example.com/a2a', 'https://rest.example.com/v1']) | The URL where this interface is available. Must be a valid absolute HTTPS URL in production. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
transport: str = Field(..., examples=['JSONRPC', 'GRPC', 'HTTP+JSON'])
url: str = Field(..., examples=['https://api.example.com/a2a/v1', 'https://grpc.example.com/a2a', 'https://rest.example.com/v1'])
```

### `AgentProvider`

Source lines 119–131; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents the service provider of an agent.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| organization | str | **required / no default** | The name of the agent provider's organization. |
| url | str | **required / no default** | A URL for the agent provider's website or relevant documentation. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
organization: str
url: str
```

### `AgentSkill`

Source lines 134–181; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a distinct capability or function that an agent can perform.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| description | str | **required / no default** | A detailed description of the skill, intended to help clients or users understand its purpose and functionality. |
| examples | list[str] &#124; None | Field(default=None, examples=[['I need a recipe for bread']]) | Example prompts or scenarios that this skill can handle. Provides a hint to the client on how to use the skill. |
| id | str | **required / no default** | A unique identifier for the agent's skill. |
| input_modes | list[str] &#124; None | None | The set of supported input MIME types for this skill, overriding the agent's defaults. |
| name | str | **required / no default** | A human-readable name for the skill. |
| output_modes | list[str] &#124; None | None | The set of supported output MIME types for this skill, overriding the agent's defaults. |
| security | list[dict[str, list[str]]] &#124; None | Field(default=None, examples=[[{'google': ['oidc']}]]) | Security schemes necessary for the agent to leverage this skill. As in the overall AgentCard.security, this list represents a logical OR of security requirement objects. Each object is a set of security schemes that must be used together (a logical AND). |
| tags | list[str] | Field(..., examples=[['cooking', 'customer support', 'billing']]) | A set of keywords describing the skill's capabilities. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
description: str
examples: list[str] | None = Field(default=None, examples=[['I need a recipe for bread']])
id: str
input_modes: list[str] | None = None
name: str
output_modes: list[str] | None = None
security: list[dict[str, list[str]]] | None = Field(default=None, examples=[[{'google': ['oidc']}]])
tags: list[str] = Field(..., examples=[['cooking', 'customer support', 'billing']])
```

### `AuthenticatedExtendedCardNotConfiguredError`

Source lines 184–201; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An A2A-specific error indicating that the agent does not have an Authenticated Extended Card configured

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32007] | -32007 | The error code for when an authenticated extended card is not configured. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Authenticated Extended Card is not configured' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32007] = -32007
data: Any | None = None
message: str | None = 'Authenticated Extended Card is not configured'
```

### `AuthorizationCodeOAuthFlow`

Source lines 204–228; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines configuration details for the OAuth 2.0 Authorization Code flow.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| authorization_url | str | **required / no default** | The authorization URL to be used for this flow. This MUST be a URL and use TLS. |
| refresh_url | str &#124; None | None | The URL to be used for obtaining refresh tokens. This MUST be a URL and use TLS. |
| scopes | dict[str, str] | **required / no default** | The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. |
| token_url | str | **required / no default** | The token URL to be used for this flow. This MUST be a URL and use TLS. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
authorization_url: str
refresh_url: str | None = None
scopes: dict[str, str]
token_url: str
```

### `ClientCredentialsOAuthFlow`

Source lines 231–248; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines configuration details for the OAuth 2.0 Client Credentials flow.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| refresh_url | str &#124; None | None | The URL to be used for obtaining refresh tokens. This MUST be a URL. |
| scopes | dict[str, str] | **required / no default** | The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. |
| token_url | str | **required / no default** | The token URL to be used for this flow. This MUST be a URL. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
refresh_url: str | None = None
scopes: dict[str, str]
token_url: str
```

### `ContentTypeNotSupportedError`

Source lines 251–269; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An A2A-specific error indicating an incompatibility between the requested content types and the agent's capabilities.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32005] | -32005 | The error code for an unsupported content type. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Incompatible content types' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32005] = -32005
data: Any | None = None
message: str | None = 'Incompatible content types'
```

### `DataPart`

Source lines 272–288; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a structured data segment (e.g., JSON) within a message or artifact.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| data | dict[str, Any] | **required / no default** | The structured data content. |
| kind | Literal['data'] | 'data' | The type of this part, used as a discriminator. Always 'data'. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with this part. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
data: dict[str, Any]
kind: Literal['data'] = 'data'
metadata: dict[str, Any] | None = None
```

### `DeleteTaskPushNotificationConfigParams`

Source lines 291–307; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines parameters for deleting a specific push notification configuration for a task.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str | **required / no default** | The unique identifier (e.g. UUID) of the task. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with the request. |
| push_notification_config_id | str | **required / no default** | The ID of the push notification configuration to delete. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str
metadata: dict[str, Any] | None = None
push_notification_config_id: str
```

### `DeleteTaskPushNotificationConfigRequest`

Source lines 310–332; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `tasks/pushNotificationConfig/delete` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['tasks/pushNotificationConfig/delete'] | 'tasks/pushNotificationConfig/delete' | The method name. Must be 'tasks/pushNotificationConfig/delete'. |
| params | DeleteTaskPushNotificationConfigParams | **required / no default** | The parameters identifying the push notification configuration to delete. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['tasks/pushNotificationConfig/delete'] = 'tasks/pushNotificationConfig/delete'
params: DeleteTaskPushNotificationConfigParams
```

### `DeleteTaskPushNotificationConfigSuccessResponse`

Source lines 335–351; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `tasks/pushNotificationConfig/delete` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | None | **required / no default** | The result is null on successful deletion. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: None
```

### `FileBase`

Source lines 354–366; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines base properties for a file.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| mime_type | str &#124; None | None | The MIME type of the file (e.g., "application/pdf"). |
| name | str &#124; None | None | An optional name for the file (e.g., "document.pdf"). |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
mime_type: str | None = None
name: str | None = None
```

### `FileWithBytes`

Source lines 369–385; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a file with its content provided directly as a base64-encoded string.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| bytes | str | **required / no default** | The base64-encoded content of the file. |
| mime_type | str &#124; None | None | The MIME type of the file (e.g., "application/pdf"). |
| name | str &#124; None | None | An optional name for the file (e.g., "document.pdf"). |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
bytes: str
mime_type: str | None = None
name: str | None = None
```

### `FileWithUri`

Source lines 388–404; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a file with its content located at a specific URI.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| mime_type | str &#124; None | None | The MIME type of the file (e.g., "application/pdf"). |
| name | str &#124; None | None | An optional name for the file (e.g., "document.pdf"). |
| uri | str | **required / no default** | A URL pointing to the file's content. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
mime_type: str | None = None
name: str | None = None
uri: str
```

### `GetAuthenticatedExtendedCardRequest`

Source lines 407–425; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `agent/getAuthenticatedExtendedCard` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['agent/getAuthenticatedExtendedCard'] | 'agent/getAuthenticatedExtendedCard' | The method name. Must be 'agent/getAuthenticatedExtendedCard'. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['agent/getAuthenticatedExtendedCard'] = 'agent/getAuthenticatedExtendedCard'
```

### `GetTaskPushNotificationConfigParams`

Source lines 428–444; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines parameters for fetching a specific push notification configuration for a task.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str | **required / no default** | The unique identifier (e.g. UUID) of the task. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with the request. |
| push_notification_config_id | str &#124; None | None | The ID of the push notification configuration to retrieve. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str
metadata: dict[str, Any] | None = None
push_notification_config_id: str | None = None
```

### `HTTPAuthSecurityScheme`

Source lines 447–470; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines a security scheme using HTTP authentication.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| bearer_format | str &#124; None | None | A hint to the client to identify how the bearer token is formatted (e.g., "JWT"). This is primarily for documentation purposes. |
| description | str &#124; None | None | An optional description for the security scheme. |
| scheme | str | **required / no default** | The name of the HTTP Authentication scheme to be used in the Authorization header, as defined in RFC7235 (e.g., "Bearer"). This value should be registered in the IANA Authentication Scheme registry. |
| type | Literal['http'] | 'http' | The type of the security scheme. Must be 'http'. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
bearer_format: str | None = None
description: str | None = None
scheme: str
type: Literal['http'] = 'http'
```

### `ImplicitOAuthFlow`

Source lines 473–490; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines configuration details for the OAuth 2.0 Implicit flow.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| authorization_url | str | **required / no default** | The authorization URL to be used for this flow. This MUST be a URL. |
| refresh_url | str &#124; None | None | The URL to be used for obtaining refresh tokens. This MUST be a URL. |
| scopes | dict[str, str] | **required / no default** | The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
authorization_url: str
refresh_url: str | None = None
scopes: dict[str, str]
```

### `InternalError`

Source lines 493–510; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An error indicating an internal error on the server.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32603] | -32603 | The error code for an internal server error. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Internal error' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32603] = -32603
data: Any | None = None
message: str | None = 'Internal error'
```

### `InvalidAgentResponseError`

Source lines 513–531; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An A2A-specific error indicating that the agent returned a response that does not conform to the specification for the current method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32006] | -32006 | The error code for an invalid agent response. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Invalid agent response' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32006] = -32006
data: Any | None = None
message: str | None = 'Invalid agent response'
```

### `InvalidParamsError`

Source lines 534–551; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An error indicating that the method parameters are invalid.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32602] | -32602 | The error code for an invalid parameters error. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Invalid parameters' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32602] = -32602
data: Any | None = None
message: str | None = 'Invalid parameters'
```

### `InvalidRequestError`

Source lines 554–571; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An error indicating that the JSON sent is not a valid Request object.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32600] | -32600 | The error code for an invalid request. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Request payload validation error' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32600] = -32600
data: Any | None = None
message: str | None = 'Request payload validation error'
```

### `JSONParseError`

Source lines 574–591; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An error indicating that the server received invalid JSON.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32700] | -32700 | The error code for a JSON parse error. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Invalid JSON payload' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32700] = -32700
data: Any | None = None
message: str | None = 'Invalid JSON payload'
```

### `JSONRPCError`

Source lines 594–611; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC 2.0 Error object, included in an error response.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | int | **required / no default** | A number that indicates the error type that occurred. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str | **required / no default** | A string providing a short description of the error. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: int
data: Any | None = None
message: str
```

### `JSONRPCMessage`

Source lines 614–627; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines the base structure for any JSON-RPC 2.0 request, response, or notification.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | A unique identifier established by the client. It must be a String, a Number, or null. The server must reply with the same value in the response. This property is omitted for notifications. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
```

### `JSONRPCRequest`

Source lines 630–651; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC 2.0 Request object.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | A unique identifier established by the client. It must be a String, a Number, or null. The server must reply with the same value in the response. This property is omitted for notifications. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | str | **required / no default** | A string containing the name of the method to be invoked. |
| params | dict[str, Any] &#124; None | None | A structured value holding the parameter values to be used during the method invocation. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
method: str
params: dict[str, Any] | None = None
```

### `JSONRPCSuccessResponse`

Source lines 654–670; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC 2.0 Response object.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | Any | **required / no default** | The value of this member is determined by the method invoked on the Server. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: Any
```

### `ListTaskPushNotificationConfigParams`

Source lines 673–685; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines parameters for listing all push notification configurations associated with a task.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str | **required / no default** | The unique identifier (e.g. UUID) of the task. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with the request. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str
metadata: dict[str, Any] | None = None
```

### `ListTaskPushNotificationConfigRequest`

Source lines 688–710; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `tasks/pushNotificationConfig/list` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['tasks/pushNotificationConfig/list'] | 'tasks/pushNotificationConfig/list' | The method name. Must be 'tasks/pushNotificationConfig/list'. |
| params | ListTaskPushNotificationConfigParams | **required / no default** | The parameters identifying the task whose configurations are to be listed. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['tasks/pushNotificationConfig/list'] = 'tasks/pushNotificationConfig/list'
params: ListTaskPushNotificationConfigParams
```

### `Role`

Source lines 713–719; declaration kind `ClassDef`.

Bases: `str, Enum`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Identifies the sender of the message. `user` for the client, `agent` for the service.

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
agent = 'agent'
user = 'user'
```

### `MethodNotFoundError`

Source lines 722–739; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An error indicating that the requested method does not exist or is not available.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32601] | -32601 | The error code for a method not found error. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Method not found' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32601] = -32601
data: Any | None = None
message: str | None = 'Method not found'
```

### `MutualTLSSecurityScheme`

Source lines 742–754; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines a security scheme using mTLS authentication.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| description | str &#124; None | None | An optional description for the security scheme. |
| type | Literal['mutualTLS'] | 'mutualTLS' | The type of the security scheme. Must be 'mutualTLS'. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
description: str | None = None
type: Literal['mutualTLS'] = 'mutualTLS'
```

### `OpenIdConnectSecurityScheme`

Source lines 757–773; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines a security scheme using OpenID Connect.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| description | str &#124; None | None | An optional description for the security scheme. |
| open_id_connect_url | str | **required / no default** | The OpenID Connect Discovery URL for the OIDC provider's metadata. |
| type | Literal['openIdConnect'] | 'openIdConnect' | The type of the security scheme. Must be 'openIdConnect'. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
description: str | None = None
open_id_connect_url: str
type: Literal['openIdConnect'] = 'openIdConnect'
```

### `PartBase`

Source lines 776–784; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines base properties common to all message or artifact parts.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with this part. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
metadata: dict[str, Any] | None = None
```

### `PasswordOAuthFlow`

Source lines 787–804; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines configuration details for the OAuth 2.0 Resource Owner Password flow.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| refresh_url | str &#124; None | None | The URL to be used for obtaining refresh tokens. This MUST be a URL. |
| scopes | dict[str, str] | **required / no default** | The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. |
| token_url | str | **required / no default** | The token URL to be used for this flow. This MUST be a URL. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
refresh_url: str | None = None
scopes: dict[str, str]
token_url: str
```

### `PushNotificationAuthenticationInfo`

Source lines 807–819; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines authentication details for a push notification endpoint.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| credentials | str &#124; None | None | Optional credentials required by the push notification endpoint. |
| schemes | list[str] | **required / no default** | A list of supported authentication schemes (e.g., 'Basic', 'Bearer'). |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
credentials: str | None = None
schemes: list[str]
```

### `PushNotificationConfig`

Source lines 822–843; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines the configuration for setting up push notifications for task updates.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| authentication | PushNotificationAuthenticationInfo &#124; None | None | Optional authentication details for the agent to use when calling the notification URL. |
| id | str &#124; None | None | A unique identifier (e.g. UUID) for the push notification configuration, set by the client to support multiple notification callbacks. |
| token | str &#124; None | None | A unique token for this task or session to validate incoming push notifications. |
| url | str | **required / no default** | The callback URL where the agent should send push notifications. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
authentication: PushNotificationAuthenticationInfo | None = None
id: str | None = None
token: str | None = None
url: str
```

### `PushNotificationNotSupportedError`

Source lines 846–863; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An A2A-specific error indicating that the agent does not support push notifications.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32003] | -32003 | The error code for when push notifications are not supported. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Push Notification is not supported' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32003] = -32003
data: Any | None = None
message: str | None = 'Push Notification is not supported'
```

### `SecuritySchemeBase`

Source lines 866–874; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines base properties shared by all security scheme objects.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| description | str &#124; None | None | An optional description for the security scheme. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
description: str | None = None
```

### `TaskIdParams`

Source lines 877–889; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines parameters containing a task ID, used for simple task operations.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str | **required / no default** | The unique identifier (e.g. UUID) of the task. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with the request. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str
metadata: dict[str, Any] | None = None
```

### `TaskNotCancelableError`

Source lines 892–909; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An A2A-specific error indicating that the task is in a state where it cannot be canceled.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32002] | -32002 | The error code for a task that cannot be canceled. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Task cannot be canceled' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32002] = -32002
data: Any | None = None
message: str | None = 'Task cannot be canceled'
```

### `TaskNotFoundError`

Source lines 912–929; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An A2A-specific error indicating that the requested task ID was not found.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32001] | -32001 | The error code for a task not found error. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'Task not found' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32001] = -32001
data: Any | None = None
message: str | None = 'Task not found'
```

### `TaskPushNotificationConfig`

Source lines 932–944; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): A container associating a push notification configuration with a specific task.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| push_notification_config | PushNotificationConfig | **required / no default** | The push notification configuration for this task. |
| task_id | str | **required / no default** | The unique identifier (e.g. UUID) of the task. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
push_notification_config: PushNotificationConfig
task_id: str
```

### `TaskQueryParams`

Source lines 947–963; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines parameters for querying a task, with an option to limit history length.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| history_length | int &#124; None | None | The number of most recent messages from the task's history to retrieve. |
| id | str | **required / no default** | The unique identifier (e.g. UUID) of the task. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with the request. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
history_length: int | None = None
id: str
metadata: dict[str, Any] | None = None
```

### `TaskResubscriptionRequest`

Source lines 966–986; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `tasks/resubscribe` method, used to resume a streaming connection.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['tasks/resubscribe'] | 'tasks/resubscribe' | The method name. Must be 'tasks/resubscribe'. |
| params | TaskIdParams | **required / no default** | The parameters identifying the task to resubscribe to. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['tasks/resubscribe'] = 'tasks/resubscribe'
params: TaskIdParams
```

### `TaskState`

Source lines 989–1002; declaration kind `ClassDef`.

Bases: `str, Enum`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines the lifecycle states of a Task.

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
submitted = 'submitted'
working = 'working'
input_required = 'input-required'
completed = 'completed'
canceled = 'canceled'
failed = 'failed'
rejected = 'rejected'
auth_required = 'auth-required'
unknown = 'unknown'
```

### `TextPart`

Source lines 1005–1021; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a text segment within a message or artifact.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| kind | Literal['text'] | 'text' | The type of this part, used as a discriminator. Always 'text'. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with this part. |
| text | str | **required / no default** | The string content of the text part. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
kind: Literal['text'] = 'text'
metadata: dict[str, Any] | None = None
text: str
```

### `TransportProtocol`

Source lines 1024–1031; declaration kind `ClassDef`.

Bases: `str, Enum`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Supported A2A transport protocols.

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
jsonrpc = 'JSONRPC'
grpc = 'GRPC'
http_json = 'HTTP+JSON'
```

### `UnsupportedOperationError`

Source lines 1034–1051; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An A2A-specific error indicating that the requested operation is not supported by the agent.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| code | Literal[-32004] | -32004 | The error code for an unsupported operation. |
| data | Any &#124; None | None | A primitive or structured value containing additional information about the error. This may be omitted. |
| message | str &#124; None | 'This operation is not supported' | The error message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
code: Literal[-32004] = -32004
data: Any | None = None
message: str | None = 'This operation is not supported'
```

### `A2AError`

Source lines 1054–1086; declaration kind `ClassDef`.

Bases: `RootModel[JSONParseError | InvalidRequestError | MethodNotFoundError | InvalidParamsError | InternalError | TaskNotFoundError | TaskNotCancelableError | PushNotificationNotSupportedError | UnsupportedOperationError | ContentTypeNotSupportedError | InvalidAgentResponseError | AuthenticatedExtendedCardNotConfiguredError]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONParseError &#124; InvalidRequestError &#124; MethodNotFoundError &#124; InvalidParamsError &#124; InternalError &#124; TaskNotFoundError &#124; TaskNotCancelableError &#124; PushNotificationNotSupportedError &#124; UnsupportedOperationError &#124; ContentTypeNotSupportedError &#124; InvalidAgentResponseError &#124; AuthenticatedExtendedCardNotConfiguredError | **required / no default** | A discriminated union of all standard JSON-RPC and A2A-specific error types. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONParseError | InvalidRequestError | MethodNotFoundError | InvalidParamsError | InternalError | TaskNotFoundError | TaskNotCancelableError | PushNotificationNotSupportedError | UnsupportedOperationError | ContentTypeNotSupportedError | InvalidAgentResponseError | AuthenticatedExtendedCardNotConfiguredError
```

### `AgentCapabilities`

Source lines 1089–1109; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines optional capabilities supported by an agent.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| extensions | list[AgentExtension] &#124; None | None | A list of protocol extensions supported by the agent. |
| push_notifications | bool &#124; None | None | Indicates if the agent supports sending push notifications for asynchronous task updates. |
| state_transition_history | bool &#124; None | None | Indicates if the agent provides a history of state transitions for a task. |
| streaming | bool &#124; None | None | Indicates if the agent supports Server-Sent Events (SSE) for streaming responses. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
extensions: list[AgentExtension] | None = None
push_notifications: bool | None = None
state_transition_history: bool | None = None
streaming: bool | None = None
```

### `CancelTaskRequest`

Source lines 1112–1132; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `tasks/cancel` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['tasks/cancel'] | 'tasks/cancel' | The method name. Must be 'tasks/cancel'. |
| params | TaskIdParams | **required / no default** | The parameters identifying the task to cancel. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['tasks/cancel'] = 'tasks/cancel'
params: TaskIdParams
```

### `FilePart`

Source lines 1135–1152; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a file segment within a message or artifact. The file content can be provided either directly as bytes or as a URI.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| file | FileWithBytes &#124; FileWithUri | **required / no default** | The file content, represented as either a URI or as base64-encoded bytes. |
| kind | Literal['file'] | 'file' | The type of this part, used as a discriminator. Always 'file'. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata associated with this part. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
file: FileWithBytes | FileWithUri
kind: Literal['file'] = 'file'
metadata: dict[str, Any] | None = None
```

### `GetTaskPushNotificationConfigRequest`

Source lines 1155–1177; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `tasks/pushNotificationConfig/get` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['tasks/pushNotificationConfig/get'] | 'tasks/pushNotificationConfig/get' | The method name. Must be 'tasks/pushNotificationConfig/get'. |
| params | TaskIdParams &#124; GetTaskPushNotificationConfigParams | **required / no default** | The parameters for getting a push notification configuration. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['tasks/pushNotificationConfig/get'] = 'tasks/pushNotificationConfig/get'
params: TaskIdParams | GetTaskPushNotificationConfigParams
```

### `GetTaskPushNotificationConfigSuccessResponse`

Source lines 1180–1196; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `tasks/pushNotificationConfig/get` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | TaskPushNotificationConfig | **required / no default** | The result, containing the requested push notification configuration. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: TaskPushNotificationConfig
```

### `GetTaskRequest`

Source lines 1199–1219; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `tasks/get` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['tasks/get'] | 'tasks/get' | The method name. Must be 'tasks/get'. |
| params | TaskQueryParams | **required / no default** | The parameters for querying a task. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['tasks/get'] = 'tasks/get'
params: TaskQueryParams
```

### `JSONRPCErrorResponse`

Source lines 1222–1252; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC 2.0 Error Response object.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| error | JSONRPCError &#124; JSONParseError &#124; InvalidRequestError &#124; MethodNotFoundError &#124; InvalidParamsError &#124; InternalError &#124; TaskNotFoundError &#124; TaskNotCancelableError &#124; PushNotificationNotSupportedError &#124; UnsupportedOperationError &#124; ContentTypeNotSupportedError &#124; InvalidAgentResponseError &#124; AuthenticatedExtendedCardNotConfiguredError | **required / no default** | An object describing the error that occurred. |
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
error: JSONRPCError | JSONParseError | InvalidRequestError | MethodNotFoundError | InvalidParamsError | InternalError | TaskNotFoundError | TaskNotCancelableError | PushNotificationNotSupportedError | UnsupportedOperationError | ContentTypeNotSupportedError | InvalidAgentResponseError | AuthenticatedExtendedCardNotConfiguredError
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
```

### `ListTaskPushNotificationConfigSuccessResponse`

Source lines 1255–1271; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `tasks/pushNotificationConfig/list` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | list[TaskPushNotificationConfig] | **required / no default** | The result, containing an array of all push notification configurations for the task. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: list[TaskPushNotificationConfig]
```

### `MessageSendConfiguration`

Source lines 1274–1294; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines configuration options for a `message/send` or `message/stream` request.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| accepted_output_modes | list[str] &#124; None | None | A list of output MIME types the client is prepared to accept in the response. |
| blocking | bool &#124; None | None | If true, the client will wait for the task to complete. The server may reject this if the task is long-running. |
| history_length | int &#124; None | None | The number of most recent messages from the task's history to retrieve in the response. |
| push_notification_config | PushNotificationConfig &#124; None | None | Configuration for the agent to send push notifications for updates after the initial response. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
accepted_output_modes: list[str] | None = None
blocking: bool | None = None
history_length: int | None = None
push_notification_config: PushNotificationConfig | None = None
```

### `OAuthFlows`

Source lines 1297–1317; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines the configuration for the supported OAuth 2.0 flows.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| authorization_code | AuthorizationCodeOAuthFlow &#124; None | None | Configuration for the OAuth Authorization Code flow. Previously called accessCode in OpenAPI 2.0. |
| client_credentials | ClientCredentialsOAuthFlow &#124; None | None | Configuration for the OAuth Client Credentials flow. Previously called application in OpenAPI 2.0. |
| implicit | ImplicitOAuthFlow &#124; None | None | Configuration for the OAuth Implicit flow. |
| password | PasswordOAuthFlow &#124; None | None | Configuration for the OAuth Resource Owner Password flow. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
authorization_code: AuthorizationCodeOAuthFlow | None = None
client_credentials: ClientCredentialsOAuthFlow | None = None
implicit: ImplicitOAuthFlow | None = None
password: PasswordOAuthFlow | None = None
```

### `Part`

Source lines 1320–1325; declaration kind `ClassDef`.

Bases: `RootModel[TextPart | FilePart | DataPart]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | TextPart &#124; FilePart &#124; DataPart | **required / no default** | A discriminated union representing a part of a message or artifact, which can be text, a file, or structured data. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: TextPart | FilePart | DataPart
```

### `SetTaskPushNotificationConfigRequest`

Source lines 1328–1350; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `tasks/pushNotificationConfig/set` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['tasks/pushNotificationConfig/set'] | 'tasks/pushNotificationConfig/set' | The method name. Must be 'tasks/pushNotificationConfig/set'. |
| params | TaskPushNotificationConfig | **required / no default** | The parameters for setting the push notification configuration. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['tasks/pushNotificationConfig/set'] = 'tasks/pushNotificationConfig/set'
params: TaskPushNotificationConfig
```

### `SetTaskPushNotificationConfigSuccessResponse`

Source lines 1353–1369; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `tasks/pushNotificationConfig/set` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | TaskPushNotificationConfig | **required / no default** | The result, containing the configured push notification settings. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: TaskPushNotificationConfig
```

### `Artifact`

Source lines 1372–1400; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a file, data structure, or other resource generated by an agent during a task.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| artifact_id | str | **required / no default** | A unique identifier (e.g. UUID) for the artifact within the scope of the task. |
| description | str &#124; None | None | An optional, human-readable description of the artifact. |
| extensions | list[str] &#124; None | None | The URIs of extensions that are relevant to this artifact. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata for extensions. The key is an extension-specific identifier. |
| name | str &#124; None | None | An optional, human-readable name for the artifact. |
| parts | list[Part] | **required / no default** | An array of content parts that make up the artifact. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
artifact_id: str
description: str | None = None
extensions: list[str] | None = None
metadata: dict[str, Any] | None = None
name: str | None = None
parts: list[Part]
```

### `DeleteTaskPushNotificationConfigResponse`

Source lines 1403–1411; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | DeleteTaskPushNotificationConfigSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; DeleteTaskPushNotificationConfigSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `tasks/pushNotificationConfig/delete` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | DeleteTaskPushNotificationConfigSuccessResponse
```

### `GetTaskPushNotificationConfigResponse`

Source lines 1414–1422; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | GetTaskPushNotificationConfigSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; GetTaskPushNotificationConfigSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `tasks/pushNotificationConfig/get` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | GetTaskPushNotificationConfigSuccessResponse
```

### `ListTaskPushNotificationConfigResponse`

Source lines 1425–1433; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | ListTaskPushNotificationConfigSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; ListTaskPushNotificationConfigSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `tasks/pushNotificationConfig/list` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | ListTaskPushNotificationConfigSuccessResponse
```

### `Message`

Source lines 1436–1477; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a single message in the conversation between a user and an agent.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| context_id | str &#124; None | None | The context ID for this message, used to group related interactions. |
| extensions | list[str] &#124; None | None | The URIs of extensions that are relevant to this message. |
| kind | Literal['message'] | 'message' | The type of this object, used as a discriminator. Always 'message' for a Message. |
| message_id | str | **required / no default** | A unique identifier for the message, typically a UUID, generated by the sender. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata for extensions. The key is an extension-specific identifier. |
| parts | list[Part] | **required / no default** | An array of content parts that form the message body. A message can be composed of multiple parts of different types (e.g., text and files). |
| reference_task_ids | list[str] &#124; None | None | A list of other task IDs that this message references for additional context. |
| role | Role | **required / no default** | Identifies the sender of the message. `user` for the client, `agent` for the service. |
| task_id | str &#124; None | None | The ID of the task this message is part of. Can be omitted for the first message of a new task. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
context_id: str | None = None
extensions: list[str] | None = None
kind: Literal['message'] = 'message'
message_id: str
metadata: dict[str, Any] | None = None
parts: list[Part]
reference_task_ids: list[str] | None = None
role: Role
task_id: str | None = None
```

### `MessageSendParams`

Source lines 1480–1497; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines the parameters for a request to send a message to an agent. This can be used to create a new task, continue an existing one, or restart a task.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| configuration | MessageSendConfiguration &#124; None | None | Optional configuration for the send request. |
| message | Message | **required / no default** | The message object being sent to the agent. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata for extensions. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
configuration: MessageSendConfiguration | None = None
message: Message
metadata: dict[str, Any] | None = None
```

### `OAuth2SecurityScheme`

Source lines 1500–1521; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Defines a security scheme using OAuth 2.0.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| description | str &#124; None | None | An optional description for the security scheme. |
| flows | OAuthFlows | **required / no default** | An object containing configuration information for the supported OAuth 2.0 flows. |
| oauth2_metadata_url | str &#124; None | None | URL to the oauth2 authorization server metadata [RFC8414](https://datatracker.ietf.org/doc/html/rfc8414). TLS is required. |
| type | Literal['oauth2'] | 'oauth2' | The type of the security scheme. Must be 'oauth2'. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
description: str | None = None
flows: OAuthFlows
oauth2_metadata_url: str | None = None
type: Literal['oauth2'] = 'oauth2'
```

### `SecurityScheme`

Source lines 1524–1543; declaration kind `ClassDef`.

Bases: `RootModel[APIKeySecurityScheme | HTTPAuthSecurityScheme | OAuth2SecurityScheme | OpenIdConnectSecurityScheme | MutualTLSSecurityScheme]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | APIKeySecurityScheme &#124; HTTPAuthSecurityScheme &#124; OAuth2SecurityScheme &#124; OpenIdConnectSecurityScheme &#124; MutualTLSSecurityScheme | **required / no default** | Defines a security scheme that can be used to secure an agent's endpoints. This is a discriminated union type based on the OpenAPI 3.0 Security Scheme Object. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: APIKeySecurityScheme | HTTPAuthSecurityScheme | OAuth2SecurityScheme | OpenIdConnectSecurityScheme | MutualTLSSecurityScheme
```

### `SendMessageRequest`

Source lines 1546–1566; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `message/send` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['message/send'] | 'message/send' | The method name. Must be 'message/send'. |
| params | MessageSendParams | **required / no default** | The parameters for sending a message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['message/send'] = 'message/send'
params: MessageSendParams
```

### `SendStreamingMessageRequest`

Source lines 1569–1589; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a JSON-RPC request for the `message/stream` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int | **required / no default** | The identifier for this request. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| method | Literal['message/stream'] | 'message/stream' | The method name. Must be 'message/stream'. |
| params | MessageSendParams | **required / no default** | The parameters for sending a message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int
jsonrpc: Literal['2.0'] = '2.0'
method: Literal['message/stream'] = 'message/stream'
params: MessageSendParams
```

### `SetTaskPushNotificationConfigResponse`

Source lines 1592–1600; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | SetTaskPushNotificationConfigSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; SetTaskPushNotificationConfigSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `tasks/pushNotificationConfig/set` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | SetTaskPushNotificationConfigSuccessResponse
```

### `TaskArtifactUpdateEvent`

Source lines 1603–1636; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An event sent by the agent to notify the client that an artifact has been generated or updated. This is typically used in streaming models.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| append | bool &#124; None | None | If true, the content of this artifact should be appended to a previously sent artifact with the same ID. |
| artifact | Artifact | **required / no default** | The artifact that was generated or updated. |
| context_id | str | **required / no default** | The context ID associated with the task. |
| kind | Literal['artifact-update'] | 'artifact-update' | The type of this event, used as a discriminator. Always 'artifact-update'. |
| last_chunk | bool &#124; None | None | If true, this is the final chunk of the artifact. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata for extensions. |
| task_id | str | **required / no default** | The ID of the task this artifact belongs to. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
append: bool | None = None
artifact: Artifact
context_id: str
kind: Literal['artifact-update'] = 'artifact-update'
last_chunk: bool | None = None
metadata: dict[str, Any] | None = None
task_id: str
```

### `TaskStatus`

Source lines 1639–1657; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents the status of a task at a specific point in time.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| message | Message &#124; None | None | An optional, human-readable message providing more details about the current status. |
| state | TaskState | **required / no default** | The current state of the task's lifecycle. |
| timestamp | str &#124; None | Field(default=None, examples=['2023-10-27T10:00:00Z']) | An ISO 8601 datetime string indicating when this status was recorded. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
message: Message | None = None
state: TaskState
timestamp: str | None = Field(default=None, examples=['2023-10-27T10:00:00Z'])
```

### `TaskStatusUpdateEvent`

Source lines 1660–1689; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): An event sent by the agent to notify the client of a change in a task's status. This is typically used in streaming or subscription models.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| context_id | str | **required / no default** | The context ID associated with the task. |
| final | bool | **required / no default** | If true, this is the final event in the stream for this interaction. |
| kind | Literal['status-update'] | 'status-update' | The type of this event, used as a discriminator. Always 'status-update'. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata for extensions. |
| status | TaskStatus | **required / no default** | The new status of the task. |
| task_id | str | **required / no default** | The ID of the task that was updated. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
context_id: str
final: bool
kind: Literal['status-update'] = 'status-update'
metadata: dict[str, Any] | None = None
status: TaskStatus
task_id: str
```

### `A2ARequest`

Source lines 1692–1720; declaration kind `ClassDef`.

Bases: `RootModel[SendMessageRequest | SendStreamingMessageRequest | GetTaskRequest | CancelTaskRequest | SetTaskPushNotificationConfigRequest | GetTaskPushNotificationConfigRequest | TaskResubscriptionRequest | ListTaskPushNotificationConfigRequest | DeleteTaskPushNotificationConfigRequest | GetAuthenticatedExtendedCardRequest]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | SendMessageRequest &#124; SendStreamingMessageRequest &#124; GetTaskRequest &#124; CancelTaskRequest &#124; SetTaskPushNotificationConfigRequest &#124; GetTaskPushNotificationConfigRequest &#124; TaskResubscriptionRequest &#124; ListTaskPushNotificationConfigRequest &#124; DeleteTaskPushNotificationConfigRequest &#124; GetAuthenticatedExtendedCardRequest | **required / no default** | A discriminated union representing all possible JSON-RPC 2.0 requests supported by the A2A specification. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: SendMessageRequest | SendStreamingMessageRequest | GetTaskRequest | CancelTaskRequest | SetTaskPushNotificationConfigRequest | GetTaskPushNotificationConfigRequest | TaskResubscriptionRequest | ListTaskPushNotificationConfigRequest | DeleteTaskPushNotificationConfigRequest | GetAuthenticatedExtendedCardRequest
```

### `AgentCard`

Source lines 1723–1833; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): The AgentCard is a self-describing manifest for an agent. It provides essential metadata including the agent's identity, capabilities, skills, supported communication methods, and security requirements.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| additional_interfaces | list[AgentInterface] &#124; None | None | A list of additional supported interfaces (transport and URL combinations). This allows agents to expose multiple transports, potentially at different URLs. Best practices: - SHOULD include all supported transports for completeness - SHOULD include an entry matching the main 'url' and 'preferredTransport' - MAY reuse URLs if multiple transports are available at the same endpoint - MUST accurately declare the transport available at each URL Clients can select any interface from this list based on their transport capabilities and preferences. This enables transport negotiation and fallback scenarios. |
| capabilities | AgentCapabilities | **required / no default** | A declaration of optional capabilities supported by the agent. |
| default_input_modes | list[str] | **required / no default** | Default set of supported input MIME types for all skills, which can be overridden on a per-skill basis. |
| default_output_modes | list[str] | **required / no default** | Default set of supported output MIME types for all skills, which can be overridden on a per-skill basis. |
| description | str | Field(..., examples=['Agent that helps users with recipes and cooking.']) | A human-readable description of the agent, assisting users and other agents in understanding its purpose. |
| documentation_url | str &#124; None | None | An optional URL to the agent's documentation. |
| icon_url | str &#124; None | None | An optional URL to an icon for the agent. |
| name | str | Field(..., examples=['Recipe Agent']) | A human-readable name for the agent. |
| preferred_transport | str &#124; None | Field(default='JSONRPC', examples=['JSONRPC', 'GRPC', 'HTTP+JSON']) | The transport protocol for the preferred endpoint (the main 'url' field). If not specified, defaults to 'JSONRPC'. IMPORTANT: The transport specified here MUST be available at the main 'url'. This creates a binding between the main URL and its supported transport protocol. Clients should prefer this transport and URL combination when both are supported. |
| protocol_version | str &#124; None | '0.3.0' | The version of the A2A protocol this agent supports. |
| provider | AgentProvider &#124; None | None | Information about the agent's service provider. |
| security | list[dict[str, list[str]]] &#124; None | Field(default=None, examples=[[{'oauth': ['read']}, {'api-key': [], 'mtls': []}]]) | A list of security requirement objects that apply to all agent interactions. Each object lists security schemes that can be used. Follows the OpenAPI 3.0 Security Requirement Object. This list can be seen as an OR of ANDs. Each object in the list describes one possible set of security requirements that must be present on a request. This allows specifying, for example, "callers must either use OAuth OR an API Key AND mTLS." |
| security_schemes | dict[str, SecurityScheme] &#124; None | None | A declaration of the security schemes available to authorize requests. The key is the scheme name. Follows the OpenAPI 3.0 Security Scheme Object. |
| signatures | list[AgentCardSignature] &#124; None | None | JSON Web Signatures computed for this AgentCard. |
| skills | list[AgentSkill] | **required / no default** | The set of skills, or distinct capabilities, that the agent can perform. |
| supports_authenticated_extended_card | bool &#124; None | None | If true, the agent can provide an extended agent card with additional details to authenticated users. Defaults to false. |
| url | str | Field(..., examples=['https://api.example.com/a2a/v1']) | The preferred endpoint URL for interacting with the agent. This URL MUST support the transport specified by 'preferredTransport'. |
| version | str | Field(..., examples=['1.0.0']) | The agent's own version number. The format is defined by the provider. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
additional_interfaces: list[AgentInterface] | None = None
capabilities: AgentCapabilities
default_input_modes: list[str]
default_output_modes: list[str]
description: str = Field(..., examples=['Agent that helps users with recipes and cooking.'])
documentation_url: str | None = None
icon_url: str | None = None
name: str = Field(..., examples=['Recipe Agent'])
preferred_transport: str | None = Field(default='JSONRPC', examples=['JSONRPC', 'GRPC', 'HTTP+JSON'])
protocol_version: str | None = '0.3.0'
provider: AgentProvider | None = None
security: list[dict[str, list[str]]] | None = Field(default=None, examples=[[{'oauth': ['read']}, {'api-key': [], 'mtls': []}]])
security_schemes: dict[str, SecurityScheme] | None = None
signatures: list[AgentCardSignature] | None = None
skills: list[AgentSkill]
supports_authenticated_extended_card: bool | None = None
url: str = Field(..., examples=['https://api.example.com/a2a/v1'])
version: str = Field(..., examples=['1.0.0'])
```

### `GetAuthenticatedExtendedCardSuccessResponse`

Source lines 1836–1852; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `agent/getAuthenticatedExtendedCard` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | AgentCard | **required / no default** | The result is an Agent Card object. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: AgentCard
```

### `Task`

Source lines 1855–1887; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a single, stateful operation or conversation between a client and an agent.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| artifacts | list[Artifact] &#124; None | None | A collection of artifacts generated by the agent during the execution of the task. |
| context_id | str | **required / no default** | A server-generated unique identifier (e.g. UUID) for maintaining context across multiple related tasks or interactions. |
| history | list[Message] &#124; None | None | An array of messages exchanged during the task, representing the conversation history. |
| id | str | **required / no default** | A unique identifier (e.g. UUID) for the task, generated by the server for a new task. |
| kind | Literal['task'] | 'task' | The type of this object, used as a discriminator. Always 'task' for a Task. |
| metadata | dict[str, Any] &#124; None | None | Optional metadata for extensions. The key is an extension-specific identifier. |
| status | TaskStatus | **required / no default** | The current status of the task, including its state and a descriptive message. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
artifacts: list[Artifact] | None = None
context_id: str
history: list[Message] | None = None
id: str
kind: Literal['task'] = 'task'
metadata: dict[str, Any] | None = None
status: TaskStatus
```

### `CancelTaskSuccessResponse`

Source lines 1890–1906; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `tasks/cancel` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | Task | **required / no default** | The result, containing the final state of the canceled Task object. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: Task
```

### `GetAuthenticatedExtendedCardResponse`

Source lines 1909–1917; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | GetAuthenticatedExtendedCardSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; GetAuthenticatedExtendedCardSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `agent/getAuthenticatedExtendedCard` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | GetAuthenticatedExtendedCardSuccessResponse
```

### `GetTaskSuccessResponse`

Source lines 1920–1936; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `tasks/get` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | Task | **required / no default** | The result, containing the requested Task object. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: Task
```

### `SendMessageSuccessResponse`

Source lines 1939–1955; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `message/send` method.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | Task &#124; Message | **required / no default** | The result, which can be a direct reply Message or the initial Task object. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: Task | Message
```

### `SendStreamingMessageSuccessResponse`

Source lines 1958–1975; declaration kind `ClassDef`.

Bases: `A2ABaseModel`. Decorators: `none`.

Source definition/intent (executed behavior is determined by fields and methods): Represents a successful JSON-RPC response for the `message/stream` method. The server may send multiple response objects for a single request.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| id | str &#124; int &#124; None | None | The identifier established by the client. |
| jsonrpc | Literal['2.0'] | '2.0' | The version of the JSON-RPC protocol. MUST be exactly "2.0". |
| result | Task &#124; Message &#124; TaskStatusUpdateEvent &#124; TaskArtifactUpdateEvent | **required / no default** | The result, which can be a Message, Task, or a streaming update event. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
id: str | int | None = None
jsonrpc: Literal['2.0'] = '2.0'
result: Task | Message | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
```

### `CancelTaskResponse`

Source lines 1978–1984; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | CancelTaskSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; CancelTaskSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `tasks/cancel` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | CancelTaskSuccessResponse
```

### `GetTaskResponse`

Source lines 1987–1991; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | GetTaskSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; GetTaskSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `tasks/get` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | GetTaskSuccessResponse
```

### `JSONRPCResponse`

Source lines 1994–2023; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | SendMessageSuccessResponse | SendStreamingMessageSuccessResponse | GetTaskSuccessResponse | CancelTaskSuccessResponse | SetTaskPushNotificationConfigSuccessResponse | GetTaskPushNotificationConfigSuccessResponse | ListTaskPushNotificationConfigSuccessResponse | DeleteTaskPushNotificationConfigSuccessResponse | GetAuthenticatedExtendedCardSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; SendMessageSuccessResponse &#124; SendStreamingMessageSuccessResponse &#124; GetTaskSuccessResponse &#124; CancelTaskSuccessResponse &#124; SetTaskPushNotificationConfigSuccessResponse &#124; GetTaskPushNotificationConfigSuccessResponse &#124; ListTaskPushNotificationConfigSuccessResponse &#124; DeleteTaskPushNotificationConfigSuccessResponse &#124; GetAuthenticatedExtendedCardSuccessResponse | **required / no default** | A discriminated union representing all possible JSON-RPC 2.0 responses for the A2A specification methods. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | SendMessageSuccessResponse | SendStreamingMessageSuccessResponse | GetTaskSuccessResponse | CancelTaskSuccessResponse | SetTaskPushNotificationConfigSuccessResponse | GetTaskPushNotificationConfigSuccessResponse | ListTaskPushNotificationConfigSuccessResponse | DeleteTaskPushNotificationConfigSuccessResponse | GetAuthenticatedExtendedCardSuccessResponse
```

### `SendMessageResponse`

Source lines 2026–2032; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | SendMessageSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; SendMessageSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `message/send` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | SendMessageSuccessResponse
```

### `SendStreamingMessageResponse`

Source lines 2035–2041; declaration kind `ClassDef`.

Bases: `RootModel[JSONRPCErrorResponse | SendStreamingMessageSuccessResponse]`. Decorators: `none`.

| Field | Input/type | Default/required | Source meaning |
|---|---|---|---|
| root | JSONRPCErrorResponse &#124; SendStreamingMessageSuccessResponse | **required / no default** | Represents a JSON-RPC response for the `message/stream` method. |

Execution: schema/enum construction only; inherited base supplies validation/serialization. No local method, I/O, retry or cancellation behavior.

```python
root: JSONRPCErrorResponse | SendStreamingMessageSuccessResponse
```
