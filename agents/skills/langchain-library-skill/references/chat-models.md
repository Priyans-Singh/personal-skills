# `langchain/chat_models`

`__init__.py` exports Core `BaseChatModel` and local `init_chat_model`; `base.py` contains the factory and `_ConfigurableModel` proxy, not provider implementations.

`init_chat_model` returns a concrete integration instance for a fixed model, or `_ConfigurableModel` if no model or `configurable_fields` was given. Fixed model identity comes from `provider:model`, explicit `model_provider`, or best-effort inference; provider names normalize hyphens to underscores. Provider classes import lazily, and absent optional packages cause actionable `ImportError` only when selected.

`_ConfigurableModel` reads `configurable_` runtime settings, then constructs/delegates at invoke, async invoke, stream, batch, event/log, tool-binding, or structured-output binding time. A finite configurable-field allowlist constrains runtime override. `"any"` permits sensitive fields such as API key/base URL, so do not provide it to untrusted callers.

No provider request occurs during factory construction. Authentication, serialization, streaming, retries, and provider-specific exceptions belong to the integration package/Core. Notable adapters include Hugging Face `from_model_id`, IBM `model_id`, LangSmith Gateway setup/Responses API, and a backwards-compatible Ollama fallback.
