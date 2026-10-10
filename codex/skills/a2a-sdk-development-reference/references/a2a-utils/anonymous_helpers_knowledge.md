# Anonymous helpers and typed entries

a2a-sdk 1.1.4, inspected 2026-10-07. Two lambdas exist in all 14 utils files; both occur in `_jcs.py` and are explicitly recorded in annotation_and_lambda_inventory.json with lexical scope/line.

| Helper | Inputs → output | Errors/delegation/lifetime |
|---|---|---|
| `_sorted_items` lambda, line 158 | `(key,value)` tuple → key encoded as UTF-16 big-endian bytes | Called by sorted for ordering dictionary items. Invalid key/surrogate errors are transformed by enclosing helper; no state retained beyond sort. |
| `_quote` regex replacement lambda, line 169 | Regex match → `_ESCAPE_MAP[matched_character]` string | Called by compiled regex substitution only for escaped/control characters. Map built at import includes every C0 character/backslash/quote; no mutation/network. |

The 26 annotated entries include protocol fields, TypedDict fields, exception data/message, named-tuple fields, mapping declarations and local variable annotations. These describe static types; they do not introduce extra runtime validation or constructor behavior. Their exact scoped source is preserved in JSON inventory and each file implementation excerpt. Duplicate `create_async_queue` declarations are distinct version branches, not overwritten coverage IDs.
