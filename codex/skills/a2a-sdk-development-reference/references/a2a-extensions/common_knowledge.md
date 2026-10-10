# Extension requests and card lookup

Source: [common.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/extensions/common.py), a2a-sdk 1.1.4, inspected 2026-10-07.

## Definitions

**Extension declaration:** AgentExtension protobuf value inside AgentCard.capabilities.extensions, with URI, description, required flag and params. **Requested extension:** URI string found in request headers/metadata. A declaration and a request are separate values; matching them does not itself implement extension behavior or authorize a caller.

`HTTP_EXTENSION_HEADER = 'A2A-Extensions'` is the current header name. It is also used as a metadata-key identifier by server gRPC builders, which perform case-insensitive key lookup. Legacy compatibility optionally also accepts `X-A2A-Extensions`; common.py does not recognize that name itself.

## API behavior

`get_requested_extensions(values: list[str]) -> set[str]` iterates every supplied string, splits each by comma, strips whitespace on each segment, drops blank segments, returns a new set. Inputs can represent repeated HTTP header lines. Duplicate URI text is removed; order is lost. URI case/content is preserved; it performs no URL normalization, escaping/quoted-list parsing, URI validation, registry check or network retrieval. Non-string elements may fail `.split`; it is not a permissive coercer. Empty list returns empty set. It never changes the input list.

`find_extension_by_uri(card: AgentCard, uri: str) -> AgentExtension | None` scans card.capabilities.extensions in order, returns first ext.uri exactly equal to uri, else None. It does not inspect required/params, merge duplicates, or compare normalized URLs. Accessing absent capabilities on protobuf gives an empty submessage/list. Returned extension is the card's mutable protobuf object; edits can affect the original card. CopyFrom into a fresh AgentExtension to isolate changes.

## End-to-end flow

```text
HTTP repeated A2A-Extensions headers / gRPC matching metadata
  → get_requested_extensions
  → ServerCallContext.requested_extensions
  → RequestContext.requested_extensions
  → application checks declarations / activates extension behavior
```

Default HTTP builder uses header.getlist; gRPC builder collects all matching metadata values. V0.3 wrapper builders union legacy and current values. These integrations collect requests, but do not automatically enforce that required card extensions were requested or supported. Domain ExtensionSupportRequiredError exists in utils, but common.py never raises it. App-specific extension negotiation/validation belongs above these helpers.

## Usage

```python
from a2a.extensions.common import get_requested_extensions, find_extension_by_uri
from a2a.types import AgentCard, AgentCapabilities, AgentExtension

uri = "urn:example:structured-output"
card = AgentCard(capabilities=AgentCapabilities(
    extensions=[AgentExtension(uri=uri, required=True)]
))
requested = get_requested_extensions([f" {uri}, ", uri])
assert requested == {uri}
assert find_extension_by_uri(card, uri).required
assert find_extension_by_uri(card, "urn:example:absent") is None
```

Validate a required extension according to its specification and actual executor support; a requested string is not trusted configuration or permission to fetch its URI. Avoid mutating shared AgentCards during per-request checks. Preserve original card interface/version when implementing extension behavior.

## Lifecycle, failure and boundaries

Functions are synchronous and local; no I/O, retries, cache, credentials, persistence, async locks, callbacks or destructive operations. Output can be used in concurrent requests if not subsequently mutated/shared. Direct dependency is generated AgentCard/AgentExtension; protobuf handling is covered in [types reference](../a2a-types/README.md). Local checks cover repeated/blank/duplicate parsing and exact card lookup.
