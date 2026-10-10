# AgentCore Configuration Bundle — working knowledge

Configuration bundles are versioned control-plane configuration documents selected per inbound request through W3C OpenTelemetry baggage. This SDK portion is preview; treat both wire keys and behavior as subject to change.

## Request-to-configuration flow

1. An upstream caller sends one or more `baggage` headers with `aws.agentcore.configbundle_arn` and `aws.agentcore.configbundle_version`.
2. `_extract_baggage(headers)` consumes a duplicate-preserving Starlette-like headers object or `(name, value)` tuples. It matches header names case-insensitively, splits comma-separated entries, strips `;` properties, percent-decodes values, preserves encounter order, and accumulates duplicate keys. A plain dict loses duplicate header values and is unsuitable. Malformed/empty entries are warned and skipped.
3. `_parse_config_bundle_baggage(all_baggage)` uses only the first ARN/version, warns if multiples exist, returns `None` if either is absent or invalid, otherwise creates `ConfigBundleRef`.
4. Application code uses `ConfigBundleClient.get_configuration_bundle_version(...)` to fetch the selected version and applies its component configuration. Parsing does not fetch or apply anything itself.

## Reference model: `bundle.py`

`ConfigBundleComponents` is the type alias `dict[component_id, {'configuration': document}]`; it describes component-specific configuration payloads.

`ConfigBundleRef(bundle_arn, bundle_version)` is frozen, so a parsed selection cannot be mutated under a request. Its post-init requires non-empty ARN/version and an ARN containing a non-empty final `/` segment. Invalid inputs raise `ValueError`. Its `bundle_id` property returns precisely that final ARN path segment; it is convenience extraction, not ARN validation.

## Control-plane façade: `client.py`

`ConfigBundleClient(region_name=None, boto3_session=None)` saves a region (default shared SDK region) and optional boto3 session, but creates `bedrock-agentcore-control` lazily and lock-protected on first operation. Create once at startup; request paths without bundle baggage pay no client construction cost.

It deliberately exposes only these forwarded boto3 calls via `__getattr__`: `create_configuration_bundle`, `delete_configuration_bundle`, `get_configuration_bundle`, `get_configuration_bundle_version`, `list_configuration_bundle_versions`, `list_configuration_bundles`, and `update_configuration_bundle`. Anything else produces `AttributeError`, even if the underlying boto3 client implements it. Calls retain boto3's native request/response schema, pagination and exceptions; this class does not translate names, validate documents, or wait for completion. Its endpoint is `get_control_plane_endpoint(region)`, including safe configured override behavior.

## Operational rules

- Baggage is untrusted routing input: parsing fails closed to `None`, but authorization to read/use a bundle remains the application's and AWS IAM's responsibility.
- Do not assume a repeat key means multiple bundles: the SDK selects first ARN and first version independently. Normalize upstream propagation if atomic pairing matters.
- Carry the immutable `ConfigBundleRef` with request context, then fetch the exact version; never silently substitute “latest.”

## Coverage ledger

All files/callables: `__init__.py`; `baggage._extract_baggage`, `baggage._parse_config_bundle_baggage`; `bundle.ConfigBundleComponents`, `ConfigBundleRef` including `bundle_id`; `client.ConfigBundleClient` including lazy `_get_client` and forwarded allowlist.
