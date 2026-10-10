# BedrockAgentCoreApp Exploration & Insights

## Overview

`BedrockAgentCoreApp` is a Starlette-based web framework for deploying AI agents to AWS Bedrock AgentCore. This document explores how it works internally and how execution flows through your application.

---

## What BedrockAgentCoreApp Actually Is

### Core Identity

`BedrockAgentCoreApp` **is a subclass of Starlette**, not a custom runner or framework. Starlette is an ASGI (Asynchronous Server Gateway Interface) web framework, the same foundation used by FastAPI.

```python
class BedrockAgentCoreApp(Starlette):
    def __init__(self, debug=False, lifespan=None, middleware=None):
        routes = [
            Route("/invocations", self._handle_invocation, methods=["POST"]),
            Route("/ping", self._handle_ping, methods=["GET"]),
            WebSocketRoute("/ws", self._handle_websocket),
        ]
        super().__init__(routes=routes, ...)
```

**What this means:**

- When you instantiate `app = BedrockAgentCoreApp()`, you're creating a full HTTP server with pre-configured routes
- These routes are **already registered** at instantiation time
- The server itself is **NOT running yet** — only when you call `app.run()` does it start

---

## How Server Creation Works: Step by Step

### Step 1: Module Initialization

When you create the app at module level:

```python
app = BedrockAgentCoreApp()
log = app.logger
```

Python executes this immediately (before any function is called). At this point:

- A Starlette ASGI application object is created
- Three HTTP routes are registered (`/invocations`, `/ping`, `/ws`)
- A logger is initialized
- Internal state (handlers dict, task tracking, etc.) is initialized
- **No HTTP server is listening yet**

### Step 2: The @app.entrypoint Decorator

```python
@app.entrypoint
async def invoke(payload, context):
    # ... your agent logic ...
    yield event
```

This decorator **only stores the function reference**. It does NOT execute your code:

```python
def entrypoint(self, func: Callable) -> Callable:
    self.handlers["main"] = func  # ← Just saves it
    func.run = lambda port=8080, host=None: self.run(port, host)
    return func
```

Your `invoke()` async generator sits dormant in `self.handlers["main"]`, waiting to be called.

### Step 3: Server Startup - app.run()

```python
if __name__ == "__main__":
    app.run()
```

This calls:

```python
def run(self, port: int = 8080, host: Optional[str] = None, **kwargs):
    import uvicorn
    
    if host is None:
        if os.path.exists("/.dockerenv"):
            host = "0.0.0.0"  # Docker
        else:
            host = "127.0.0.1"  # localhost
    
    uvicorn.run(self, host=host, port=port, ...)
```

**This launches uvicorn**, a production-grade ASGI server. Your Starlette app instance becomes the ASGI application, and the server now listens for HTTP requests.

---

## Execution Flow of `uv run opentelemetry-instrument python3 main.py`

### The Complete Picture

```
Terminal Command: uv run opentelemetry-instrument python3 main.py
                    │
                    ├─ uv resolves and runs the command
                    │opentelemetry-instrument [wraps the execution]
                    └─ 
                        │
                        ├─ Patches sys.meta_path with OTel hooks
                        ├─ Installs instrumentation for:
                        │   - httpx, requests (HTTP clients)
                        │   - boto3, botocore (AWS SDK)
                        │   - starlette (your web framework)
                        │   - asyncio (async runtime)
                        ├─ Initializes TraceProvider globally
                        ├─ Initializes MeterProvider globally
                        │
                        └─ Spawns: python3 main.py
                            │
                            └─ Executes main.py LINE BY LINE (top to bottom)
```

### Python Line-by-Line Execution in main.py


| #   | Line(s) | Code                                                               | Execution Timing | What Happens                                                                                                                   |
| --- | ------- | ------------------------------------------------------------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1   | 1-8     | Import statements                                                  | **Immediately**  | Modules loaded, classes/functions imported                                                                                     |
| 2   | 17      | `app = BedrockAgentCoreApp()`                                      | **Immediately**  | Starlette app instance created with 3 routes registered. Logger initialized. Internal state set up. **Server NOT running yet** |
| 3   | 18      | `log = app.logger`                                                 | **Immediately**  | Logger reference stored                                                                                                        |
| 4   | 24-25   | `print(f"OTEL_EXPORTER...")`                                       | **Immediately**  | Debug prints execute                                                                                                           |
| 5   | 27      | `mcp_clients = [...]`                                              | **Immediately**  | MCP client objects created and stored                                                                                          |
| 6   | 38-42   | `@tool def add_numbers(...)`                                       | **Immediately**  | Tool registered                                                                                                                |
| 7   | 46-48   | `for mcp_client in mcp_clients:`                                   | **Immediately**  | Loop executes, MCP clients appended to tools list                                                                              |
| 8   | 51-65   | `def agent_factory():` and `get_or_create_agent = agent_factory()` | **Immediately**  | Factory function defined and called, closure created                                                                           |
| 9   | 68-82   | `@app.entrypoint async def invoke(...)`                            | **Immediately**  | `invoke` function stored in `app.handlers["main"]`. **NOT called or awaited**                                                  |
| 10  | 85      | `if __name__ == "__main__":`                                       | **Evaluated**    | Python sets `__name__` to `"__main__"` for the script entry point. This evaluates to **True**                                  |
| 11  | 86      | `app.run()`                                                        | **Called NOW**   | uvicorn.run(app) starts. HTTP server binds to 127.0.0.1:8080 and **blocks forever**, waiting for requests                      |


### Important: The `__name__` Variable

```python
if __name__ == "__main__":
    app.run()
```

This is **standard Python**, not AgentCore magic:

- When a `.py` file is run directly as the main script: `__name__` is set to `"__main__"` → condition is **True**
- When a `.py` file is imported as a module: `__name__` is set to the module name (e.g., `"main"`) → condition is **False**

This prevents `app.run()` from executing when someone does `from main import app` in another script.

---

## What Happens During an HTTP Request

### The Request Flow

```
curl -X POST http://127.0.0.1:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, agent!"}'

                    ↓
            uvicorn receives HTTP request
                    ↓
        Starlette routes to /invocations handler
                    ↓
            BedrockAgentCoreApp._handle_invocation()
                    │
                    ├─ Parse JSON payload
                    ├─ Build request context (session ID, headers, etc.)
                    ├─ Lookup self.handlers["main"] (your invoke function)
                    ├─ Call invoke(payload, context)
                    │   ├─ Create or retrieve agent from cache
                    │   ├─ Stream from agent.stream_async()
                    │   └─ Yield events
                    │
                    ├─ Detect return type:
                    │   ├─ If async generator → StreamingResponse
                    │   ├─ If regular return → JSONResponse
                    │
                    └─ Send back to client
```

### Your `invoke()` Function Only Runs When Called

```python
@app.entrypoint
async def invoke(payload, context):  # ← Only executes when POST /invocations arrives
    log.info("Invoking Agent.....")
    
    session_id = getattr(context, 'session_id', 'default-session')
    user_id = getattr(context, 'user_id', 'default-user')
    agent = get_or_create_agent(session_id, user_id)
    
    stream = agent.stream_async(payload.get("prompt"))
    
    async for event in stream:
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]
```

- **Before** the request: Your `invoke` function sits dormant in memory
- **During** the request: The function executes asynchronously on uvicorn's event loop
- **After** the response: The function completes, generator closes

---

## How OpenTelemetry Integration Works

### Auto-Instrumentation with `opentelemetry-instrument`

The `opentelemetry-instrument` command is a wrapper that pre-patches your application:

```bash
opentelemetry-instrument python3 main.py
```

**What happens BEFORE main.py runs:**

1. **Import sys.meta_path hooks** — allows OTel to intercept module imports
2. **Patch AWS SDK** — boto3/botocore calls generate spans
3. **Patch HTTP libraries** — requests, httpx generate spans
4. **Patch Starlette** — your ASGI app's request handlers generate spans
5. **Patch asyncio** — async operations generate spans
6. **Initialize TracerProvider** — OTEL_EXPORTER_OTLP_ENDPOINT is used to send traces
7. **Initialize MeterProvider** — Metrics are collected and exported

**Then** your `main.py` starts executing with OTel already active.

### Why Traces Appear

When your code runs:

```python
app = BedrockAgentCoreApp()  # ← Creates a Starlette app
```

The `__init__` method calls:

```python
_ensure_baggage_processor_registered()  # ← Registers OTel processors
```

At this point, **OTel is already initialized** (by `opentelemetry-instrument`), so the processor is registered to the real `TracerProvider`, not a no-op one.

When a request arrives and your `invoke()` runs, OTel captures:

- HTTP request/response metadata
- Boto3 API calls (if you use Bedrock, S3, etc.)
- Your custom spans (if you add `@tracer.start_as_current_span()`)
- Timing and errors

These spans are batched and sent to `OTEL_EXPORTER_OTLP_ENDPOINT`.

---

## Key Invariants & Mental Model

### 1. Module-Level Code = Startup Time

Everything outside a function/class runs **once** when the module loads:

```python
app = BedrockAgentCoreApp()  # ← Runs at startup
print("OTEL_EXPORTER...")   # ← Runs at startup
mcp_clients = [...]          # ← Runs at startup
```

### 2. Decorated Functions = Storage, Not Execution

```python
@app.entrypoint
async def invoke(payload, context):
    # ← This code does NOT run at decoration time
    # ← It only runs when POST /invocations arrives
```

### 3. Server Blocks Until Shutdown

Once `app.run()` is called:

```python
app.run()  # ← Blocks forever
# Code here never runs (unless app.run() raises an exception)
```

The process stays alive, listening for HTTP requests indefinitely.

### 4. Thread Isolation for Long-Running Handlers

BedrockAgentCoreApp creates a **dedicated worker event loop** in a background thread for async handlers:

```python
_worker_loop = asyncio.new_event_loop()  # Created in background thread
```

This ensures blocking handlers don't prevent `/ping` health checks from responding. It's part of the managed runtime's health probing mechanism.

---

## HTTP Headers: Complete Analysis

### The Journey of a Header (from curl to your `invoke` function)

```
curl -X POST http://localhost:8080/invocations \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: session-abc"
  -H "Authorization: Bearer my-token"
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Custom-User-Name: priyans"
        │
        ↓
_handle_invocation(request)
        │
        ↓
_build_request_context(request)
        │
        ├─ Reads specific headers → sets them as ContextVars
        ├─ Filters remaining headers → stores in request_headers dict
        │
        ↓
RequestContext(session_id=..., request_headers={...})
        │
        ↓
invoke(payload, context)   ← context IS the RequestContext object
```

### What is `context` in Your `invoke` Function?

```python
@app.entrypoint
async def invoke(payload, context):
```

`context` is a `RequestContext` Pydantic model:

```python
class RequestContext(BaseModel):
    session_id: Optional[str]               # ← from SESSION_HEADER
    request_headers: Optional[Dict[str, str]] # ← filtered forwardable headers
    request: Optional[Any]                   # ← raw Starlette Request object
```

That's it — **three fields**. Other values like `request_id`, `workload_access_token`, and `oauth2_callback_url` are stored in `BedrockAgentCoreContext` ContextVars, not in the context object.

### System-Managed Headers

These are set **by the AgentCore Runtime infrastructure** when deployed. Simulate them locally for testing.

#### `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id`

**What it does:** Identifies a unique conversation/session. Groups multiple turns of a conversation together.

**How it flows:**

```python
session_id = headers.get(SESSION_HEADER)
BedrockAgentCoreContext.set_request_context(request_id, session_id)
# → stored in RequestContext.session_id AND as ContextVar
```

**Access in `invoke`:**

```python
@app.entrypoint
async def invoke(payload, context):
    session_id = context.session_id   # ← from RequestContext
    # OR globally:
    session_id = BedrockAgentCoreContext.get_session_id()
```

**Send as:**

```bash
-H "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: my-session-123"
```

---

#### `X-Amzn-Bedrock-AgentCore-Runtime-Request-Id`

**What it does:** Unique ID for this specific HTTP request (not the session). Auto-generated if absent. Used for distributed tracing and log correlation.

**How it flows:**

```python
request_id = headers.get(REQUEST_ID_HEADER)
if not request_id:
    request_id = str(uuid.uuid4())   # ← auto-generated if missing
BedrockAgentCoreContext.set_request_context(request_id, session_id)
```

**Access in `invoke`:**

```python
# Accessed globally via ContextVar (NOT in context object):
request_id = BedrockAgentCoreContext.get_request_id()
```

Appears automatically in every structured log entry via `RequestContextFormatter`.

**Send as:**

```bash
-H "X-Amzn-Bedrock-AgentCore-Runtime-Request-Id: req-123-abc"
```

---

#### `WorkloadAccessToken`

**What it does:** The **agent identity token** — a short-lived credential issued by AgentCore Runtime. Lets your agent call other AWS services on its behalf with proper IAM authorization. Think of it as proof of identity for service-to-service calls.

**How it flows:**

```python
agent_identity_token = headers.get(ACCESS_TOKEN_HEADER)
if agent_identity_token:
    BedrockAgentCoreContext.set_workload_access_token(agent_identity_token)
```

**Access in `invoke`:**

```python
token = BedrockAgentCoreContext.get_workload_access_token()
# Use this to authenticate downstream AWS service calls
```

**Note:** Not in the `context` object directly. Use the class method.

---

#### `OAuth2CallbackUrl`

**What it does:** Provides the callback URL when your agent needs to perform OAuth2 flows (e.g., user login to Google/GitHub). After user authorization, they're redirected to this URL for completion.

**How it flows:**

```python
oauth2_callback_url = headers.get(OAUTH2_CALLBACK_URL_HEADER)
if oauth2_callback_url:
    BedrockAgentCoreContext.set_oauth2_callback_url(oauth2_callback_url)
```

**Access in `invoke`:**

```python
callback_url = BedrockAgentCoreContext.get_oauth2_callback_url()
# Redirect user to: {oauth_provider}/auth?redirect_uri={callback_url}
```

**Note:** Set by AWS Runtime only, not accessible in local testing.

---

#### `Authorization`

**What it does:** Standard HTTP `Authorization` header (e.g., `Bearer <token>`, `Basic <base64>`). Specially handled — **case-normalized** regardless of HTTP version:

```python
for header_name, header_value in headers.items():
    if header_name.lower() == _AUTHORIZATION_HEADER_LOWER:
        request_headers[AUTHORIZATION_HEADER] = header_value  # Always "Authorization"
```

**Access in `invoke`:**

```python
auth = context.request_headers.get("Authorization")
# e.g., "Bearer eyJhbGci..."
```

**Send as:**

```bash
-H "Authorization: Bearer my-token"
# OR
-H "Authorization: Basic dXNlcjpwYXNz"
```

---

### Custom Headers — What You Control

```python
CUSTOM_HEADER_PREFIX = "X-Amzn-Bedrock-AgentCore-Runtime-Custom-"
```

**This is the recommended way to pass arbitrary data to your agent.**

The forwarding rule from `is_forwardable_header()`:

```python
def is_forwardable_header(header_name: str) -> bool:
    lower = header_name.lower()
    if lower in RESTRICTED_HEADERS:       # blocked
        return False
    if lower.startswith("x-amz-"):        # blocked (AWS SigV4)
        return False
    if lower.startswith("x-amzn-") and not lower.startswith(_CUSTOM_HEADER_PREFIX_LOWER):
        return False                       # blocked (reserved for AWS)
    return True                            # ← everything else passes through
```

So the `X-Amzn-Bedrock-AgentCore-Runtime-Custom-*` namespace is **explicitly whitelisted** in an otherwise-blocked `x-amzn-`* namespace.

**Example:**

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Custom-User-Id: user-priyans" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Tenant-Id: tenant-456" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Feature-Flag: dark-mode" \
  -d '{"prompt": "Hello"}'
```

**Reading in `invoke`:**

```python
@app.entrypoint
async def invoke(payload, context):
    headers = context.request_headers or {}
    user_id = headers.get("X-Amzn-Bedrock-AgentCore-Runtime-Custom-User-Id")  # "user-priyans"
    tenant = headers.get("X-Amzn-Bedrock-AgentCore-Runtime-Custom-Tenant-Id")  # "tenant-456"
    flag = headers.get("X-Amzn-Bedrock-AgentCore-Runtime-Custom-Feature-Flag")  # "dark-mode"
```

---

### Blocked Headers (Will NOT reach your function)

A `RESTRICTED_HEADERS` frozenset blocks headers in these categories:


| Category            | Examples                                   | Reason Blocked               |
| ------------------- | ------------------------------------------ | ---------------------------- |
| Content negotiation | `Content-Type`, `Accept`, `Content-Length` | Infrastructure concern       |
| Caching             | `Cache-Control`, `ETag`, `Expires`         | HTTP infrastructure          |
| Security            | `X-Frame-Options`, `CSP`, `CORS headers`   | Security layer handles these |
| Cookies             | `Cookie`, `Set-Cookie`                     | Security boundary            |
| Proxy/CDN           | `X-Forwarded-For`, `CF-Ray`, `X-Real-IP`   | Can be spoofed               |
| AWS internal        | `x-amz-*`                                  | Reserved for SigV4 signing   |
| AWS internal        | `x-amzn-*` (except Custom prefix)          | Reserved for AWS services    |
| HTTP/2 pseudo       | `:method`, `:path`                         | Protocol-level headers       |


---

### Header Summary Table


| Header Name                                   | Constant                     | Who Sets It                     | Where It Ends Up                           | How to Access                                                      |
| --------------------------------------------- | ---------------------------- | ------------------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` | `SESSION_HEADER`             | AWS Runtime / you               | `context.session_id` + ContextVar          | `context.session_id` or `BedrockAgentCoreContext.get_session_id()` |
| `X-Amzn-Bedrock-AgentCore-Runtime-Request-Id` | `REQUEST_ID_HEADER`          | AWS Runtime / you (or auto-gen) | ContextVar only                            | `BedrockAgentCoreContext.get_request_id()`                         |
| `WorkloadAccessToken`                         | `ACCESS_TOKEN_HEADER`        | AWS Runtime only                | ContextVar only                            | `BedrockAgentCoreContext.get_workload_access_token()`              |
| `OAuth2CallbackUrl`                           | `OAUTH2_CALLBACK_URL_HEADER` | AWS Runtime only                | ContextVar only                            | `BedrockAgentCoreContext.get_oauth2_callback_url()`                |
| `Authorization`                               | `AUTHORIZATION_HEADER`       | You / client                    | `context.request_headers["Authorization"]` | `context.request_headers.get("Authorization")`                     |
| `X-Amzn-Bedrock-AgentCore-Runtime-Custom-*`   | `CUSTOM_HEADER_PREFIX`       | You / client                    | `context.request_headers[header_name]`     | `context.request_headers.get("X-Amzn-...Custom-Foo")`              |
| Any other non-restricted header               | —                            | You / client                    | `context.request_headers[header_name]`     | `context.request_headers.get(name)`                                |


---

### Complete Example for Local Testing

```bash
curl -X POST http://127.0.0.1:8080/invocations \
  -H "Content-Type: application/json" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: session-priyans-001" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Request-Id: req-debug-123" \
  -H "Authorization: Bearer my-test-token" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Custom-User-Id: priyans" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Debug-Mode: true" \
  -d '{"prompt": "What is 2+2?"}'
```

In your `invoke`:

```python
@app.entrypoint
async def invoke(payload, context):
    # From RequestContext object:
    session_id  = context.session_id           # "session-priyans-001"
    headers     = context.request_headers or {}
    auth        = headers.get("Authorization") # "Bearer my-test-token"
    user_id     = headers.get("X-Amzn-Bedrock-AgentCore-Runtime-Custom-User-Id")  # "priyans"
    debug_mode  = headers.get("X-Amzn-Bedrock-AgentCore-Runtime-Custom-Debug-Mode")  # "true"
    
    # From ContextVars:
    request_id  = BedrockAgentCoreContext.get_request_id()  # "req-debug-123"
    
    log.info(f"Session: {session_id}, Request: {request_id}, User: {user_id}")
    
    # ... your logic ...
    yield {"response": "4"}
```

---

## Debugging Checklist

If your agent isn't behaving as expected:

- **Decorator applied?** Check `@app.entrypoint` is present and decorates an `async def` or `async def` generator
- **Function signature correct?** Should be `async def invoke(payload, context):` or just `async def invoke(payload):`
- **app.run() called?** Must be in `if __name__ == "__main__":` block
- **Yielding vs returning?** Generators (with `yield`) stream; regular returns get JSONResponse
- **OTel env vars set?** `OTEL_EXPORTER_OTLP_ENDPOINT` must point to a valid collector
- **Serving locally?** Try `curl -X POST http://127.0.0.1:8080/invocations -H "Content-Type: application/json" -d '{"prompt":"test"}'`

---

## References

- **Starlette**: [https://www.starlette.io/](https://www.starlette.io/)
- **Uvicorn**: [https://www.uvicorn.org/](https://www.uvicorn.org/)
- **OpenTelemetry**: [https://opentelemetry.io/](https://opentelemetry.io/)
- **BedrockAgentCore SDK**: [https://github.com/aws/bedrock-agentcore-sdk-python](https://github.com/aws/bedrock-agentcore-sdk-python)

