# `langchain/embeddings`

`__init__.py` exports Core `Embeddings` and `init_embeddings`; `base.py` holds a lazy registry factory. It does not embed or make network calls by itself.

`init_embeddings(model, provider=None, **kwargs)` requires a nonblank model. If provider is omitted it parses `provider:model`; otherwise it validates and normalizes the explicit provider. It then lazy-imports the selected integration and instantiates it. Invalid format/provider produces `ValueError`; an absent integration gives install guidance in `ImportError`.

Built-ins are Azure AI, Azure OpenAI, Bedrock, Cohere, Google GenAI, Google Vertex AI, Hugging Face, Mistral, Ollama, and OpenAI. Bedrock maps model to `model_id`; Hugging Face maps it to `model_name`; most pass `model`. The returned integration’s `embed_query` and `embed_documents` own credentials, batching, retry, and remote I/O. Prefer explicit provider when a model name is ambiguous.
