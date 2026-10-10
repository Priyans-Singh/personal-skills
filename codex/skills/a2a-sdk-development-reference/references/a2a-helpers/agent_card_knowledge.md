# `agent_card.py`: human-readable card output

Source: [agent_card.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/helpers/agent_card.py), a2a-sdk 1.1.4, 2026-10-07.

`display_agent_card(card: AgentCard) -> None` builds a list of strings, joins with newline, and prints once to stdout. Returns None; does not alter card, serialize a protocol response, discover/fetch a card, verify signatures, or resolve security credentials.

Output begins/ends with 52-character '=' separators. General section includes name/description/version; documentation/icon URL appear if truthy; provider appears when protobuf HasField('provider') and optional URL suffix. Interfaces enumerate URLs with protocol binding/version and optional tenant. Capabilities prints streaming/push/extended booleans. I/O modes join lists or show '(none)'. Skills section prints ID/name/description/tags/examples, or '(none)'. Skill input/output/security requirements, card signatures/security schemes/requirements and extension parameters are not exhaustively displayed.

Width does not truncate or wrap long values. Arbitrary card strings are printed without control-character escaping or redaction. Inference: treat untrusted card display cautiously in terminals/logs, and don't embed secrets in URLs/descriptions. Generated default/absent fields can produce blanks/False; the output is a summary, not evidence of valid REQUIRED fields or actual endpoint capability.

Direct dependency is generated AgentCard; print can raise standard stdout/write/type errors, none caught. No cache, retries, background work or credential forwarding. Use `from a2a.helpers import display_agent_card`; capture stdout when testing/report generation. For canonical wire JSON use protobuf MessageToDict, and for validation use the relevant protocol/card checks rather than this formatter.
