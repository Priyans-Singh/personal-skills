# `callbacks.py`

Graph lifecycle callback surface. Subclass `GraphCallbackHandler` and supply it in invocation callbacks to receive interrupt/resume events carrying run, status, checkpoint/namespace, and payload information. Ordinary LangChain handlers do not automatically receive these LangGraph-specific events.
