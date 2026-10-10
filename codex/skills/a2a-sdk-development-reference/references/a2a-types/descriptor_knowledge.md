# Generated descriptor execution catalog

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

All descriptor messages, including synthetic nested map entries, fields, oneofs, enums, services and options. REQUIRED is google.api metadata enforced only when utility validator is called; proto3 construction/serialization accepts omissions. Field numbers are the binary wire identity; JSON aliases are separate. Defaults shown below are runtime defaults.

## File metadata

Name `a2a.proto`; package `lf.a2a.v1`; syntax `proto3`.

```json
{
  "javaPackage": "com.lf.a2a.v1",
  "javaOuterClassname": "A2aProto",
  "javaMultipleFiles": true,
  "goPackage": "google.golang.org/lf/a2a/v1",
  "objcClassPrefix": "LAX",
  "csharpNamespace": "Lf.A2a.V1",
  "phpNamespace": "Lf\\A2a\\V1",
  "phpMetadataNamespace": "Lf\\A2a\\V1\\GPBMetadata",
  "rubyPackage": "Lf::A2a::V1"
}
```

Imports: `google/api/annotations.proto`, `google/api/client.proto`, `google/api/field_behavior.proto`, `google/protobuf/empty.proto`, `google/protobuf/struct.proto`, `google/protobuf/timestamp.proto`

## `lf.a2a.v1.SendMessageConfiguration`

Execution hints attached to send requests: output MIME preferences, push configuration, optional history limit, immediate-return flag. No scheduling is performed here.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `accepted_output_modes` / `acceptedOutputModes` | 1 | `string` | repeated | False / `—` | `[]` | ; `` |
| `task_push_notification_config` / `taskPushNotificationConfig` | 2 | `lf.a2a.v1.TaskPushNotificationConfig` | singular | True / `—` | `None` | ; `` |
| `history_length` / `historyLength` | 3 | `int32` | singular | True / `_history_length` | `0` | ; `` |
| `return_immediately` / `returnImmediately` | 4 | `bool` | singular | False / `—` | `False` | ; `` |

Oneofs: `_history_length` = `history_length`.

## `lf.a2a.v1.Task`

Task resource snapshot: id identifies task; context_id groups conversation; status is current state; artifacts are outputs and history is messages. Mutating snapshot does not update a task store.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `id` / `id` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `context_id` / `contextId` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `status` / `status` | 3 | `lf.a2a.v1.TaskStatus` | singular | True / `—` | `None` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `artifacts` / `artifacts` | 4 | `lf.a2a.v1.Artifact` | repeated | False / `—` | `[]` | ; `` |
| `history` / `history` | 5 | `lf.a2a.v1.Message` | repeated | False / `—` | `[]` | ; `` |
| `metadata` / `metadata` | 6 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.TaskStatus`

State plus optional agent/user message and protobuf Timestamp. Enum assignment is not a state-machine transition.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `state` / `state` | 1 | `lf.a2a.v1.TaskState` | singular | False / `—` | `0` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `message` / `message` | 2 | `lf.a2a.v1.Message` | singular | True / `—` | `None` | ; `` |
| `timestamp` / `timestamp` | 3 | `google.protobuf.Timestamp` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.Part`

One content alternative: text, raw bytes, URL reference, or arbitrary protobuf Value; metadata/filename/media_type annotate it. URL construction does not fetch content.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `text` / `text` | 1 | `string` | singular | True / `content` | `''` | ; `` |
| `raw` / `raw` | 2 | `bytes` | singular | True / `content` | `b''` | ; `` |
| `url` / `url` | 3 | `string` | singular | True / `content` | `''` | ; `` |
| `data` / `data` | 4 | `google.protobuf.Value` | singular | True / `content` | `None` | ; `` |
| `metadata` / `metadata` | 5 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |
| `filename` / `filename` | 6 | `string` | singular | False / `—` | `''` | ; `` |
| `media_type` / `mediaType` | 7 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: `content` = `text`, `raw`, `url`, `data`.

## `lf.a2a.v1.Message`

Message identity, task/context linkage, role, required repeated Parts; metadata/extensions/reference task IDs carry context. IDs are supplied by caller, never generated here.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `message_id` / `messageId` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `context_id` / `contextId` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `task_id` / `taskId` | 3 | `string` | singular | False / `—` | `''` | ; `` |
| `role` / `role` | 4 | `lf.a2a.v1.Role` | singular | False / `—` | `0` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `parts` / `parts` | 5 | `lf.a2a.v1.Part` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `metadata` / `metadata` | 6 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |
| `extensions` / `extensions` | 7 | `string` | repeated | False / `—` | `[]` | ; `` |
| `reference_task_ids` / `referenceTaskIds` | 8 | `string` | repeated | False / `—` | `[]` | ; `` |

Oneofs: none.

## `lf.a2a.v1.Artifact`

Output identified by artifact_id with required Parts and optional descriptive fields; no file write or remote object exists from construction.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `artifact_id` / `artifactId` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `name` / `name` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `description` / `description` | 3 | `string` | singular | False / `—` | `''` | ; `` |
| `parts` / `parts` | 4 | `lf.a2a.v1.Part` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `metadata` / `metadata` | 5 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |
| `extensions` / `extensions` | 6 | `string` | repeated | False / `—` | `[]` | ; `` |

Oneofs: none.

## `lf.a2a.v1.TaskStatusUpdateEvent`

Task/context identity plus replacement status and metadata; no final flag in this version.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `task_id` / `taskId` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `context_id` / `contextId` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `status` / `status` | 3 | `lf.a2a.v1.TaskStatus` | singular | True / `—` | `None` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `metadata` / `metadata` | 4 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.TaskArtifactUpdateEvent`

Task/context identity plus artifact and append/last_chunk flags. Consumer implements merge/assembly; generated class does not append to Task.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `task_id` / `taskId` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `context_id` / `contextId` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `artifact` / `artifact` | 3 | `lf.a2a.v1.Artifact` | singular | True / `—` | `None` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `append` / `append` | 4 | `bool` | singular | False / `—` | `False` | ; `` |
| `last_chunk` / `lastChunk` | 5 | `bool` | singular | False / `—` | `False` | ; `` |
| `metadata` / `metadata` | 6 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.AuthenticationInfo`

Callback authentication declaration with scheme and credentials string. Sensitive data may be serialized; no encryption, expiry, credential refresh, or authorization enforcement.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `scheme` / `scheme` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `credentials` / `credentials` | 2 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.AgentInterface`

Agent endpoint URL plus binding, optional tenant and required protocol_version; discovery/routing data, not live connection.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `url` / `url` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `protocol_binding` / `protocolBinding` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `tenant` / `tenant` | 3 | `string` | singular | False / `—` | `''` | ; `` |
| `protocol_version` / `protocolVersion` | 4 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.AgentCard`

Discovery document with capabilities/interfaces/provider/skills/security definitions and signatures. version is agent version; interface protocol_version is distinct. No implicit endpoint probe.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `name` / `name` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `description` / `description` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `supported_interfaces` / `supportedInterfaces` | 3 | `lf.a2a.v1.AgentInterface` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `provider` / `provider` | 4 | `lf.a2a.v1.AgentProvider` | singular | True / `—` | `None` | ; `` |
| `version` / `version` | 5 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `documentation_url` / `documentationUrl` | 6 | `string` | singular | True / `_documentation_url` | `''` | ; `` |
| `capabilities` / `capabilities` | 7 | `lf.a2a.v1.AgentCapabilities` | singular | True / `—` | `None` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `security_schemes` / `securitySchemes` | 8 | `lf.a2a.v1.AgentCard.SecuritySchemesEntry` | map | False / `—` | `[]` | ; `` |
| `security_requirements` / `securityRequirements` | 9 | `lf.a2a.v1.SecurityRequirement` | repeated | False / `—` | `[]` | ; `` |
| `default_input_modes` / `defaultInputModes` | 10 | `string` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `default_output_modes` / `defaultOutputModes` | 11 | `string` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `skills` / `skills` | 12 | `lf.a2a.v1.AgentSkill` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `signatures` / `signatures` | 13 | `lf.a2a.v1.AgentCardSignature` | repeated | False / `—` | `[]` | ; `` |
| `icon_url` / `iconUrl` | 14 | `string` | singular | True / `_icon_url` | `''` | ; `` |

Oneofs: `_documentation_url` = `documentation_url`; `_icon_url` = `icon_url`.

## `lf.a2a.v1.AgentCard.SecuritySchemesEntry`

Synthetic nested map-entry: key/value transport representation. Parent exposes a mapping container, not a repeated list of entry objects.

Map entry: `True`. Options: `map_entry: true `.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `key` / `key` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `value` / `value` | 2 | `lf.a2a.v1.SecurityScheme` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.AgentProvider`

Organization and URL identity metadata, not authenticated principal.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `url` / `url` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `organization` / `organization` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.AgentCapabilities`

Optional booleans distinguish absent from explicit false, plus extension declarations; no capability implementation is created.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `streaming` / `streaming` | 1 | `bool` | singular | True / `_streaming` | `False` | ; `` |
| `push_notifications` / `pushNotifications` | 2 | `bool` | singular | True / `_push_notifications` | `False` | ; `` |
| `extensions` / `extensions` | 3 | `lf.a2a.v1.AgentExtension` | repeated | False / `—` | `[]` | ; `` |
| `extended_agent_card` / `extendedAgentCard` | 4 | `bool` | singular | True / `_extended_agent_card` | `False` | ; `` |

Oneofs: `_streaming` = `streaming`; `_push_notifications` = `push_notifications`; `_extended_agent_card` = `extended_agent_card`.

## `lf.a2a.v1.AgentExtension`

Extension URI/description/required flag plus arbitrary Struct parameters; untrusted params can nest and impact signing depth.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `uri` / `uri` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `description` / `description` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `required` / `required` | 3 | `bool` | singular | False / `—` | `False` | ; `` |
| `params` / `params` | 4 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.AgentSkill`

Skill identifier/documentation/tags/examples and optional MIME/security requirements. Generated class does not enforce selection or execute skill.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `id` / `id` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `name` / `name` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `description` / `description` | 3 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `tags` / `tags` | 4 | `string` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `examples` / `examples` | 5 | `string` | repeated | False / `—` | `[]` | ; `` |
| `input_modes` / `inputModes` | 6 | `string` | repeated | False / `—` | `[]` | ; `` |
| `output_modes` / `outputModes` | 7 | `string` | repeated | False / `—` | `[]` | ; `` |
| `security_requirements` / `securityRequirements` | 8 | `lf.a2a.v1.SecurityRequirement` | repeated | False / `—` | `[]` | ; `` |

Oneofs: none.

## `lf.a2a.v1.AgentCardSignature`

Detached JWS protected header and signature base64url strings, plus unprotected Struct header. Payload comes from canonicalized AgentCard without signatures.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `protected` / `protected` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `signature` / `signature` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `header` / `header` | 3 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.TaskPushNotificationConfig`

Configuration resource keyed by tenant/task_id/id; callback url/token/authentication stored as proto values. Credentials/token destination is callback consumer/sender integration, not agent-card public security scheme. Model imposes no lifetime, revocation, persistence, or outbound HTTP.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `id` / `id` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `task_id` / `taskId` | 3 | `string` | singular | False / `—` | `''` | ; `` |
| `url` / `url` | 4 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `token` / `token` | 5 | `string` | singular | False / `—` | `''` | ; `` |
| `authentication` / `authentication` | 6 | `lf.a2a.v1.AuthenticationInfo` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.StringList`

Repeated string wrapper enabling protobuf map values of scope lists.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `list` / `list` | 1 | `string` | repeated | False / `—` | `[]` | ; `` |

Oneofs: none.

## `lf.a2a.v1.SecurityRequirement`

Map security scheme names to StringList scope requirements. Schema data; no matching, AND/OR evaluation, credential acquisition, or enforcement occurs here.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `schemes` / `schemes` | 1 | `lf.a2a.v1.SecurityRequirement.SchemesEntry` | map | False / `—` | `[]` | ; `` |

Oneofs: none.

## `lf.a2a.v1.SecurityRequirement.SchemesEntry`

Synthetic nested map-entry: key/value transport representation. Parent exposes a mapping container, not a repeated list of entry objects.

Map entry: `True`. Options: `map_entry: true `.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `key` / `key` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `value` / `value` | 2 | `lf.a2a.v1.StringList` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.SecurityScheme`

Oneof union of API key, HTTP auth, OAuth2, OIDC, mutual TLS definitions; switching scheme clears previous choice.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `api_key_security_scheme` / `apiKeySecurityScheme` | 1 | `lf.a2a.v1.APIKeySecurityScheme` | singular | True / `scheme` | `None` | ; `` |
| `http_auth_security_scheme` / `httpAuthSecurityScheme` | 2 | `lf.a2a.v1.HTTPAuthSecurityScheme` | singular | True / `scheme` | `None` | ; `` |
| `oauth2_security_scheme` / `oauth2SecurityScheme` | 3 | `lf.a2a.v1.OAuth2SecurityScheme` | singular | True / `scheme` | `None` | ; `` |
| `open_id_connect_security_scheme` / `openIdConnectSecurityScheme` | 4 | `lf.a2a.v1.OpenIdConnectSecurityScheme` | singular | True / `scheme` | `None` | ; `` |
| `mtls_security_scheme` / `mtlsSecurityScheme` | 5 | `lf.a2a.v1.MutualTlsSecurityScheme` | singular | True / `scheme` | `None` | ; `` |

Oneofs: `scheme` = `api_key_security_scheme`, `http_auth_security_scheme`, `oauth2_security_scheme`, `open_id_connect_security_scheme`, `mtls_security_scheme`.

## `lf.a2a.v1.APIKeySecurityScheme`

API key description/location/name describes credential destination (header/query/cookie convention is consumer responsibility). Stores no actual key.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `description` / `description` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `location` / `location` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `name` / `name` | 3 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.HTTPAuthSecurityScheme`

HTTP scheme and bearer-format hint; no bearer token acquisition/validation.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `description` / `description` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `scheme` / `scheme` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `bearer_format` / `bearerFormat` | 3 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.OAuth2SecurityScheme`

OAuth flows and optional metadata URL; no discovery fetch or token exchange.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `description` / `description` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `flows` / `flows` | 2 | `lf.a2a.v1.OAuthFlows` | singular | True / `—` | `None` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `oauth2_metadata_url` / `oauth2MetadataUrl` | 3 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.OpenIdConnectSecurityScheme`

Discovery URL metadata; no network request or ID-token validation.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `description` / `description` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `open_id_connect_url` / `openIdConnectUrl` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.MutualTlsSecurityScheme`

mTLS description; no certificate/key or TLS configuration.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `description` / `description` | 1 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.OAuthFlows`

Oneof flow: authorization_code, client_credentials, implicit, password, device_code. Unlike an arbitrary multi-flow mapping, only one can be selected at once. implicit/password descriptor fields are deprecated.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `authorization_code` / `authorizationCode` | 1 | `lf.a2a.v1.AuthorizationCodeOAuthFlow` | singular | True / `flow` | `None` | ; `` |
| `client_credentials` / `clientCredentials` | 2 | `lf.a2a.v1.ClientCredentialsOAuthFlow` | singular | True / `flow` | `None` | ; `` |
| `implicit` / `implicit` | 3 | `lf.a2a.v1.ImplicitOAuthFlow` | singular | True / `flow` | `None` | ; `deprecated: true ` |
| `password` / `password` | 4 | `lf.a2a.v1.PasswordOAuthFlow` | singular | True / `flow` | `None` | ; `deprecated: true ` |
| `device_code` / `deviceCode` | 5 | `lf.a2a.v1.DeviceCodeOAuthFlow` | singular | True / `flow` | `None` | ; `` |

Oneofs: `flow` = `authorization_code`, `client_credentials`, `implicit`, `password`, `device_code`.

## `lf.a2a.v1.AuthorizationCodeOAuthFlow`

Authorization/token/refresh endpoints, scope descriptions, PKCE-required flag. Describes token destinations, does not generate verifier/challenge or store tokens.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `authorization_url` / `authorizationUrl` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `token_url` / `tokenUrl` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `refresh_url` / `refreshUrl` | 3 | `string` | singular | False / `—` | `''` | ; `` |
| `scopes` / `scopes` | 4 | `lf.a2a.v1.AuthorizationCodeOAuthFlow.ScopesEntry` | map | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `pkce_required` / `pkceRequired` | 5 | `bool` | singular | False / `—` | `False` | ; `` |

Oneofs: none.

## `lf.a2a.v1.AuthorizationCodeOAuthFlow.ScopesEntry`

Synthetic nested map-entry: key/value transport representation. Parent exposes a mapping container, not a repeated list of entry objects.

Map entry: `True`. Options: `map_entry: true `.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `key` / `key` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `value` / `value` | 2 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.ClientCredentialsOAuthFlow`

Token/refresh endpoints and scope descriptions; no client secret storage or issuance.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `token_url` / `tokenUrl` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `refresh_url` / `refreshUrl` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `scopes` / `scopes` | 3 | `lf.a2a.v1.ClientCredentialsOAuthFlow.ScopesEntry` | map | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.ClientCredentialsOAuthFlow.ScopesEntry`

Synthetic nested map-entry: key/value transport representation. Parent exposes a mapping container, not a repeated list of entry objects.

Map entry: `True`. Options: `map_entry: true `.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `key` / `key` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `value` / `value` | 2 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.ImplicitOAuthFlow`

Deprecated flow metadata; authorization/refresh URLs and scopes, no browser redirect.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `authorization_url` / `authorizationUrl` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `refresh_url` / `refreshUrl` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `scopes` / `scopes` | 3 | `lf.a2a.v1.ImplicitOAuthFlow.ScopesEntry` | map | False / `—` | `[]` | ; `` |

Oneofs: none.

## `lf.a2a.v1.ImplicitOAuthFlow.ScopesEntry`

Synthetic nested map-entry: key/value transport representation. Parent exposes a mapping container, not a repeated list of entry objects.

Map entry: `True`. Options: `map_entry: true `.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `key` / `key` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `value` / `value` | 2 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.PasswordOAuthFlow`

Deprecated flow metadata; token/refresh URLs and scopes, no password collection.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `token_url` / `tokenUrl` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `refresh_url` / `refreshUrl` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `scopes` / `scopes` | 3 | `lf.a2a.v1.PasswordOAuthFlow.ScopesEntry` | map | False / `—` | `[]` | ; `` |

Oneofs: none.

## `lf.a2a.v1.PasswordOAuthFlow.ScopesEntry`

Synthetic nested map-entry: key/value transport representation. Parent exposes a mapping container, not a repeated list of entry objects.

Map entry: `True`. Options: `map_entry: true `.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `key` / `key` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `value` / `value` | 2 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.DeviceCodeOAuthFlow`

Device authorization/token/refresh URLs and scopes; no polling loop, expiry/retry intervals, or user-code generation.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `device_authorization_url` / `deviceAuthorizationUrl` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `token_url` / `tokenUrl` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `refresh_url` / `refreshUrl` | 3 | `string` | singular | False / `—` | `''` | ; `` |
| `scopes` / `scopes` | 4 | `lf.a2a.v1.DeviceCodeOAuthFlow.ScopesEntry` | map | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.DeviceCodeOAuthFlow.ScopesEntry`

Synthetic nested map-entry: key/value transport representation. Parent exposes a mapping container, not a repeated list of entry objects.

Map entry: `True`. Options: `map_entry: true `.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `key` / `key` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `value` / `value` | 2 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.SendMessageRequest`

Tenant routing scope, required Message, optional configuration/metadata; used by unary and server-streaming send.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `message` / `message` | 2 | `lf.a2a.v1.Message` | singular | True / `—` | `None` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `configuration` / `configuration` | 3 | `lf.a2a.v1.SendMessageConfiguration` | singular | True / `—` | `None` | ; `` |
| `metadata` / `metadata` | 4 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.GetTaskRequest`

Tenant and required task id, optional history_length with explicit-zero presence semantics.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `id` / `id` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `history_length` / `historyLength` | 3 | `int32` | singular | True / `_history_length` | `0` | ; `` |

Oneofs: `_history_length` = `history_length`.

## `lf.a2a.v1.ListTasksRequest`

Tenant/context/status/time filters, optional page size/history/include_artifacts and cursor. No filter application, snapshot consistency, ordering, or page defaulting occurs here.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `context_id` / `contextId` | 2 | `string` | singular | False / `—` | `''` | ; `` |
| `status` / `status` | 3 | `lf.a2a.v1.TaskState` | singular | False / `—` | `0` | ; `` |
| `page_size` / `pageSize` | 4 | `int32` | singular | True / `_page_size` | `0` | ; `` |
| `page_token` / `pageToken` | 5 | `string` | singular | False / `—` | `''` | ; `` |
| `history_length` / `historyLength` | 6 | `int32` | singular | True / `_history_length` | `0` | ; `` |
| `status_timestamp_after` / `statusTimestampAfter` | 7 | `google.protobuf.Timestamp` | singular | True / `—` | `None` | ; `` |
| `include_artifacts` / `includeArtifacts` | 8 | `bool` | singular | True / `_include_artifacts` | `False` | ; `` |

Oneofs: `_page_size` = `page_size`; `_history_length` = `history_length`; `_include_artifacts` = `include_artifacts`.

## `lf.a2a.v1.ListTasksResponse`

Tasks page plus next cursor/page size/total size. REQUIRED annotations on empty cursor/numeric zero can conflict with business meaning when generic required validator is applied; generated serializer permits them.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tasks` / `tasks` | 1 | `lf.a2a.v1.Task` | repeated | False / `—` | `[]` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `next_page_token` / `nextPageToken` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `page_size` / `pageSize` | 3 | `int32` | singular | False / `—` | `0` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `total_size` / `totalSize` | 4 | `int32` | singular | False / `—` | `0` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.CancelTaskRequest`

Tenant/task id plus metadata; serializing this does not cancel work. Remote handler owns cancelability and races.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `id` / `id` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `metadata` / `metadata` | 3 | `google.protobuf.Struct` | singular | True / `—` | `None` | ; `` |

Oneofs: none.

## `lf.a2a.v1.GetTaskPushNotificationConfigRequest`

Tenant/task_id/config id lookup; identifiers are separate scalar values, not parsed resource paths.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `task_id` / `taskId` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `id` / `id` | 3 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.DeleteTaskPushNotificationConfigRequest`

Tenant/task_id/config id deletion request. No local delete side effect; remote call requires caller authorization.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `task_id` / `taskId` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `id` / `id` | 3 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.SubscribeToTaskRequest`

Tenant/task id subscription request; no iterator/state replay/cursor exists until transport is invoked.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |
| `id` / `id` | 2 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |

Oneofs: none.

## `lf.a2a.v1.ListTaskPushNotificationConfigsRequest`

Task-scoped listing with page size/cursor; page_size is nonpresence scalar (absent vs zero indistinguishable). Tenant field number is 4.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 4 | `string` | singular | False / `—` | `''` | ; `` |
| `task_id` / `taskId` | 1 | `string` | singular | False / `—` | `''` | REQUIRED; `[google.api.field_behavior]: REQUIRED ` |
| `page_size` / `pageSize` | 2 | `int32` | singular | False / `—` | `0` | ; `` |
| `page_token` / `pageToken` | 3 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.GetExtendedAgentCardRequest`

Tenant-only request; generated type does not prove authentication or authorization.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `tenant` / `tenant` | 1 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## `lf.a2a.v1.SendMessageResponse`

Oneof payload returns Task snapshot or direct Message; empty response is constructible.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `task` / `task` | 1 | `lf.a2a.v1.Task` | singular | True / `payload` | `None` | ; `` |
| `message` / `message` | 2 | `lf.a2a.v1.Message` | singular | True / `payload` | `None` | ; `` |

Oneofs: `payload` = `task`, `message`.

## `lf.a2a.v1.StreamResponse`

Oneof payload with Task/Message/status/artifact updates. Not a Python async iterator; each wire stream item is one envelope.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `task` / `task` | 1 | `lf.a2a.v1.Task` | singular | True / `payload` | `None` | ; `` |
| `message` / `message` | 2 | `lf.a2a.v1.Message` | singular | True / `payload` | `None` | ; `` |
| `status_update` / `statusUpdate` | 3 | `lf.a2a.v1.TaskStatusUpdateEvent` | singular | True / `payload` | `None` | ; `` |
| `artifact_update` / `artifactUpdate` | 4 | `lf.a2a.v1.TaskArtifactUpdateEvent` | singular | True / `payload` | `None` | ; `` |

Oneofs: `payload` = `task`, `message`, `status_update`, `artifact_update`.

## `lf.a2a.v1.ListTaskPushNotificationConfigsResponse`

Repeated callback configurations plus next page token; sensitive callback configuration fields remain serializable.

Map entry: `False`. Options: ``.

| Python field / JSON name | Wire # | Type | Cardinality | Presence / oneof | Default | Field behavior/options |
|---|---|---|---|---|---|---|
| `configs` / `configs` | 1 | `lf.a2a.v1.TaskPushNotificationConfig` | repeated | False / `—` | `[]` | ; `` |
| `next_page_token` / `nextPageToken` | 2 | `string` | singular | False / `—` | `''` | ; `` |

Oneofs: none.

## Enum `lf.a2a.v1.TaskState`

| Name | Integer |
|---|---|
| `TASK_STATE_UNSPECIFIED` | 0 |
| `TASK_STATE_SUBMITTED` | 1 |
| `TASK_STATE_WORKING` | 2 |
| `TASK_STATE_COMPLETED` | 3 |
| `TASK_STATE_FAILED` | 4 |
| `TASK_STATE_CANCELED` | 5 |
| `TASK_STATE_INPUT_REQUIRED` | 6 |
| `TASK_STATE_REJECTED` | 7 |
| `TASK_STATE_AUTH_REQUIRED` | 8 |

Runtime EnumTypeWrapper supports Name(value), Value(name), keys(), values(), items(); invalid lookup errors propagate. Constants are integers; enums do not enforce task transitions.

## Enum `lf.a2a.v1.Role`

| Name | Integer |
|---|---|
| `ROLE_UNSPECIFIED` | 0 |
| `ROLE_USER` | 1 |
| `ROLE_AGENT` | 2 |

Runtime EnumTypeWrapper supports Name(value), Value(name), keys(), values(), items(); invalid lookup errors propagate. Constants are integers; enums do not enforce task transitions.

## Service `lf.a2a.v1.A2AService`

All RPCs are client-unary; two are server-streaming. HTTP annotation is schema routing intent, not an installed HTTP router.

| RPC/path | Input | Output | Server stream |
|---|---|---|---|
| `/lf.a2a.v1.A2AService/SendMessage` | `lf.a2a.v1.SendMessageRequest` | `lf.a2a.v1.SendMessageResponse` | False |
| `/lf.a2a.v1.A2AService/SendStreamingMessage` | `lf.a2a.v1.SendMessageRequest` | `lf.a2a.v1.StreamResponse` | True |
| `/lf.a2a.v1.A2AService/GetTask` | `lf.a2a.v1.GetTaskRequest` | `lf.a2a.v1.Task` | False |
| `/lf.a2a.v1.A2AService/ListTasks` | `lf.a2a.v1.ListTasksRequest` | `lf.a2a.v1.ListTasksResponse` | False |
| `/lf.a2a.v1.A2AService/CancelTask` | `lf.a2a.v1.CancelTaskRequest` | `lf.a2a.v1.Task` | False |
| `/lf.a2a.v1.A2AService/SubscribeToTask` | `lf.a2a.v1.SubscribeToTaskRequest` | `lf.a2a.v1.StreamResponse` | True |
| `/lf.a2a.v1.A2AService/CreateTaskPushNotificationConfig` | `lf.a2a.v1.TaskPushNotificationConfig` | `lf.a2a.v1.TaskPushNotificationConfig` | False |
| `/lf.a2a.v1.A2AService/GetTaskPushNotificationConfig` | `lf.a2a.v1.GetTaskPushNotificationConfigRequest` | `lf.a2a.v1.TaskPushNotificationConfig` | False |
| `/lf.a2a.v1.A2AService/ListTaskPushNotificationConfigs` | `lf.a2a.v1.ListTaskPushNotificationConfigsRequest` | `lf.a2a.v1.ListTaskPushNotificationConfigsResponse` | False |
| `/lf.a2a.v1.A2AService/GetExtendedAgentCard` | `lf.a2a.v1.GetExtendedAgentCardRequest` | `lf.a2a.v1.AgentCard` | False |
| `/lf.a2a.v1.A2AService/DeleteTaskPushNotificationConfig` | `lf.a2a.v1.DeleteTaskPushNotificationConfigRequest` | `google.protobuf.Empty` | False |

### `SendMessage` HTTP/service metadata

```json
{
  "[google.api.http]": {
    "post": "/message:send",
    "body": "*",
    "additional_bindings": [
      {
        "post": "/{tenant}/message:send",
        "body": "*"
      }
    ]
  }
}
```

### `SendStreamingMessage` HTTP/service metadata

```json
{
  "[google.api.http]": {
    "post": "/message:stream",
    "body": "*",
    "additional_bindings": [
      {
        "post": "/{tenant}/message:stream",
        "body": "*"
      }
    ]
  }
}
```

### `GetTask` HTTP/service metadata

```json
{
  "[google.api.method_signature]": [
    "id"
  ],
  "[google.api.http]": {
    "get": "/tasks/{id=*}",
    "additional_bindings": [
      {
        "get": "/{tenant}/tasks/{id=*}"
      }
    ]
  }
}
```

### `ListTasks` HTTP/service metadata

```json
{
  "[google.api.http]": {
    "get": "/tasks",
    "additional_bindings": [
      {
        "get": "/{tenant}/tasks"
      }
    ]
  }
}
```

### `CancelTask` HTTP/service metadata

```json
{
  "[google.api.http]": {
    "post": "/tasks/{id=*}:cancel",
    "body": "*",
    "additional_bindings": [
      {
        "post": "/{tenant}/tasks/{id=*}:cancel",
        "body": "*"
      }
    ]
  }
}
```

### `SubscribeToTask` HTTP/service metadata

```json
{
  "[google.api.http]": {
    "get": "/tasks/{id=*}:subscribe",
    "additional_bindings": [
      {
        "get": "/{tenant}/tasks/{id=*}:subscribe"
      }
    ]
  }
}
```

### `CreateTaskPushNotificationConfig` HTTP/service metadata

```json
{
  "[google.api.method_signature]": [
    "task_id,config"
  ],
  "[google.api.http]": {
    "post": "/tasks/{task_id=*}/pushNotificationConfigs",
    "body": "*",
    "additional_bindings": [
      {
        "post": "/{tenant}/tasks/{task_id=*}/pushNotificationConfigs",
        "body": "*"
      }
    ]
  }
}
```

### `GetTaskPushNotificationConfig` HTTP/service metadata

```json
{
  "[google.api.method_signature]": [
    "task_id,id"
  ],
  "[google.api.http]": {
    "get": "/tasks/{task_id=*}/pushNotificationConfigs/{id=*}",
    "additional_bindings": [
      {
        "get": "/{tenant}/tasks/{task_id=*}/pushNotificationConfigs/{id=*}"
      }
    ]
  }
}
```

### `ListTaskPushNotificationConfigs` HTTP/service metadata

```json
{
  "[google.api.method_signature]": [
    "task_id"
  ],
  "[google.api.http]": {
    "get": "/tasks/{task_id=*}/pushNotificationConfigs",
    "additional_bindings": [
      {
        "get": "/{tenant}/tasks/{task_id=*}/pushNotificationConfigs"
      }
    ]
  }
}
```

### `GetExtendedAgentCard` HTTP/service metadata

```json
{
  "[google.api.http]": {
    "get": "/extendedAgentCard",
    "additional_bindings": [
      {
        "get": "/{tenant}/extendedAgentCard"
      }
    ]
  }
}
```

### `DeleteTaskPushNotificationConfig` HTTP/service metadata

```json
{
  "[google.api.method_signature]": [
    "task_id,id"
  ],
  "[google.api.http]": {
    "delete": "/tasks/{task_id=*}/pushNotificationConfigs/{id=*}",
    "additional_bindings": [
      {
        "delete": "/{tenant}/tasks/{task_id=*}/pushNotificationConfigs/{id=*}"
      }
    ]
  }
}
```
