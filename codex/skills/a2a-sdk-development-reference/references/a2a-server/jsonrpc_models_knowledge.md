# JSON-RPC error values

Source: [`server/jsonrpc_models.py`](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py).

These are **Pydantic payload models**, distinct from `a2a.utils.errors` exceptions. They are passed to serializers, not raised as Python exceptions. No declared methods; inherited Pydantic parsing/dumping provides validation.

`JSONRPCBaseModel` allows extra fields, population by field name, and arbitrary types. `JSONRPCError` requires integer `code` and string `message`, with optional arbitrary `data` defaulting to None.

| Subclass | Fixed code | Default message |
|---|---:|---|
| `JSONParseError` | -32700 | Parse error |
| `InvalidRequestError` | -32600 | Invalid Request |
| `MethodNotFoundError` | -32601 | Method not found |
| `InvalidParamsError` | -32602 | Invalid params |
| `InternalError` | -32603 | Internal error |

Codes in subclasses use Literal types, so supplying another code is a validation error. Construction does not send a response. `build_error_response` in response_helpers combines the model with a JSON-RPC request ID and excludes None fields. Semantic A2A exceptions use their own error mapping, with extra Google RPC error details.

Alias imports when both model and exception names are needed (`JSONRPCInternalError` versus domain `InternalError`) to avoid raising a model or serializing the wrong representation. Error data must be JSON-serializable at the transport boundary despite arbitrary-types allowance.
