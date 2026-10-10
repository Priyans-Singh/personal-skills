# Bedrock AgentCore Knowledge Base Knowledge

This guide describes every installed file and callable in `bedrock_agentcore.knowledge_base`:

```text
knowledge_base/
├── __init__.py       public export: KnowledgeBaseClient
└── client.py         KnowledgeBaseClient and its direct/polling operations
```

It is a thin, synchronous convenience layer over two boto3 services. It does not chunk documents, create embeddings, choose a vector store, or answer questions locally; those actions occur in the Bedrock service after this client submits an API request.

## Mental model

```text
control plane: bedrock-agent
  Knowledge base ──contains──> data source ──feeds──> ingestion/indexing
       │                                         │
       └── document-management APIs <────────────┘

data plane: bedrock-agent-runtime
  indexed knowledge base ──> retrieve / rerank / generate-query
                              retrieve-and-generate / streaming retrieval
```

Use the control plane to configure resources and load content. Use the data plane only after content has been indexed. `KnowledgeBaseClient` owns one boto3 client for each plane and exposes a deliberately small allowlist from each.

## `__init__.py`: public import boundary

`from bedrock_agentcore.knowledge_base import KnowledgeBaseClient` is the supported import. The module imports that class from `client.py` and declares it in `__all__`; it has no setup side effects.

## `client.py`: `KnowledgeBaseClient`

### Construction: `KnowledgeBaseClient.__init__(region_name=None, integration_source=None, boto3_session=None)`

The constructor chooses `boto3_session` when supplied, otherwise creates `boto3.Session()`. Region precedence is explicit argument, then the session's configured region, then the SDK fallback `us-west-2`. A named profile, assumed-role credentials, retry configuration, and credential refresh should therefore be configured on the supplied session, not on this wrapper.

It constructs:

- `cp_client`: `session.client("bedrock-agent", ...)`, the knowledge-base control plane.
- `dp_client`: `session.client("bedrock-agent-runtime", ...)`, the retrieval/generation data plane.

Both clients receive `botocore.config.Config(user_agent_extra=...)`. `integration_source` is telemetry only: the shared helper adds an AgentCore SDK suffix and sanitizes it to lower-case alphanumeric, `-`, and `_`; it does not select a service or change authorization. The instance retains `region_name` and `integration_source` as attributes.

Construction creates clients but makes no AWS API call. Credential errors generally surface on the first request.

### Keyword convention used everywhere

Forwarded methods are wrapped with `accept_snake_case_kwargs`; the convenience methods call `convert_kwargs` before calling boto3 directly. Consequently both `knowledge_base_id=` and AWS's `knowledgeBaseId=` work, but only for top-level argument names. Nested request dictionaries are passed through unchanged and must use the AWS service shape.

Never supply both spellings of one top-level key (`knowledge_base_id` and `knowledgeBaseId`): the forwarding wrapper detects the collision and raises `TypeError`. Underscored malformed names also raise `ValueError`. Responses remain boto3/AWS camelCase responses.

### Dynamic API surface: `KnowledgeBaseClient.__getattr__(name)`

There are no concrete Python methods named `retrieve` or `create_data_source`. Attribute lookup reaches `__getattr__`, which forwards only names in the following allowlists to the underlying boto3 client, then returns a fresh keyword-normalizing wrapper around that boto3 method. Any other missing name raises `AttributeError`; it cannot accidentally expose arbitrary boto3 operations.

Control-plane (`cp_client`) pass-throughs:

| Group | Callable | Purpose |
|---|---|---|
| Knowledge base | `create_knowledge_base`, `get_knowledge_base`, `update_knowledge_base`, `delete_knowledge_base`, `list_knowledge_bases` | Define, inspect, modify, remove, or enumerate a knowledge base. Creation/update returns before the resource is necessarily usable. |
| Data source | `create_data_source`, `get_data_source`, `update_data_source`, `delete_data_source`, `list_data_sources` | Manage a source attached to a specific knowledge base. The source configuration determines where service ingestion reads from. |
| Ingestion job | `start_ingestion_job`, `get_ingestion_job`, `stop_ingestion_job`, `list_ingestion_jobs` | Start or control asynchronous sync/index work for a data source. |
| Direct documents | `ingest_knowledge_base_documents`, `get_knowledge_base_documents`, `delete_knowledge_base_documents`, `list_knowledge_base_documents` | Put, inspect, delete, or enumerate documents through the custom-data-source document APIs. These are distinct from source-wide ingestion jobs. |
| Tags | `tag_resource`, `untag_resource`, `list_tags_for_resource` | Apply, remove, or read resource tags. |

Data-plane (`dp_client`) pass-throughs:

| Callable | Purpose |
|---|---|
| `retrieve` | Return retrieved chunks/metadata for a query; the caller generates an answer. |
| `retrieve_and_generate` | Ask the service to retrieve and produce a grounded generated response in one non-streaming call. |
| `retrieve_and_generate_stream` | Streaming version of the preceding operation. Consume the boto3 event stream and close it on cancellation/error. |
| `generate_query` | Have the service turn a natural-language prompt into a structured query for a configured knowledge base. |
| `rerank` | Reorder supplied retrieval candidates according to a reranking configuration. It does not fetch documents itself. |
| `agentic_retrieve_stream` | Stream agentic retrieval events; it is a runtime event stream, not a Python async generator supplied by this SDK. |

For request/response members and service validation, consult the boto3 model for the installed version. This wrapper does no local schema validation, pagination, retries, or exception translation.

## Wait helpers: lifecycle behavior in detail

All `*_and_wait` methods are synchronous and block the calling thread. They accept `WaitConfig(max_wait=300, poll_interval=10)` by default. The shared config rejects either value below one second. Polling makes an immediate get call, then sleeps between later calls; timeout is measured from the start, so actual return can slightly exceed `max_wait` by one API call.

The common `wait_until` returns the exact response object from the successful poll. A status in its failed set raises `RuntimeError` with the configured reason field; an unrecognized perpetual status times out. `wait_until_deleted` treats boto3 `ClientError` with code `ResourceNotFoundException` as deletion success; any other AWS exception propagates.

### `create_knowledge_base_and_wait(wait_config=None, **kwargs)`

Calls `cp_client.create_knowledge_base(**converted_kwargs)`, reads `response["knowledgeBase"]["knowledgeBaseId"]`, then repeatedly calls `get_knowledge_base(knowledgeBaseId=...)` and polls its nested `"knowledgeBase"` object. It returns that object when `status == "ACTIVE"`.

`FAILED` is terminal and produces `RuntimeError`; missing IDs/keys and AWS errors propagate as-is. This is appropriate when a following operation needs an active resource, rather than merely an accepted create request.

### `update_knowledge_base_and_wait(wait_config=None, **kwargs)`

Same mechanics as creation, except the first request is `update_knowledge_base`. It waits for the returned knowledge-base ID to become `ACTIVE`, and treats `FAILED` as terminal. This does not verify that an ingestion job has re-indexed content after a configuration update.

### `delete_knowledge_base_and_wait(wait_config=None, **kwargs)`

Calls `delete_knowledge_base`, obtains the top-level `response["knowledgeBaseId"]`, and polls `get_knowledge_base(...)["knowledgeBase"]` until the get operation returns `ResourceNotFoundException`. `DELETE_UNSUCCESSFUL` or `FAILED` becomes `RuntimeError`, using `failureReasons` instead of the generic `statusReasons`. It returns `None`, not a deletion response.

Deletion can fail when dependent resources or service constraints remain. Do not treat an accepted delete response as completed deletion; use this method if an immediate recreation with the same identity matters.

### `start_ingestion_job_and_wait(wait_config=None, **kwargs)`

Calls `start_ingestion_job`, extracts `knowledgeBaseId`, `dataSourceId`, and `ingestionJobId` from `response["ingestionJob"]`, then polls the exact job with all three identifiers. It returns `response["ingestionJob"]` when `status == "COMPLETE"`.

`FAILED` and `STOPPED` raise `RuntimeError`, taking details from `failureReasons`. Explicitly stopping a job is therefore a failure outcome for this convenience method, even though it may be intentional operationally. It does not inspect partial indexing counters: inspect the returned job details when completeness matters.

### `ingest_knowledge_base_documents_and_wait(wait_config=None, **kwargs)`

This is a document-status polling loop rather than the shared `wait_until` helper:

1. Converts top-level keywords and calls `ingest_knowledge_base_documents`.
2. Splits initial `documentDetails` into `IGNORED` documents and documents whose status is exactly `STARTING`.
3. If there are no `STARTING` documents, immediately returns the original ingestion response.
4. Otherwise, gets the knowledge-base/data-source IDs from the original request and polls `get_knowledge_base_documents` for the accepted documents' `identifier` values.
5. Returns a final poll response once every returned detail is terminal, appending initially ignored details to `documentDetails`.

Terminal success statuses are `INDEXED`, `PARTIALLY_INDEXED`, and `METADATA_PARTIALLY_INDEXED`; terminal failed statuses are `FAILED`, `METADATA_UPDATE_FAILED`, `NOT_FOUND`, and `IGNORED`. Unlike the other wait helpers, failures do **not** raise `RuntimeError`: the caller must examine each final `documentDetails[*].status` and failure information. `PARTIALLY_INDEXED` is similarly returned, not escalated.

Important edge cases:

- The method only polls documents initially marked `STARTING`. An initial non-ignored/non-starting status is not added to the tracking list; preserve and inspect the original response if that distinction matters.
- Python `all([])` is true. If a poll response omits all requested details, this implementation will consider it terminal and return it; callers requiring strict document accounting should compare requested identifiers with returned identifiers.
- It uses `time.time()` and `time.sleep()`, so it blocks a thread and has no cancellation API beyond the surrounding process/thread strategy.
- It needs `knowledgeBaseId`, `dataSourceId`, and documents because those fields are read locally after the request. Missing fields lead to ordinary `KeyError`, while AWS-side shape errors remain boto3 errors.

## Practical flows

### Create, source, index, retrieve

```python
from bedrock_agentcore.knowledge_base import KnowledgeBaseClient
from bedrock_agentcore._utils.config import WaitConfig

kb = KnowledgeBaseClient(region_name="us-west-2")
active = kb.create_knowledge_base_and_wait(
    name="support-kb",
    role_arn="<bedrock-kb-role-arn>",
    knowledge_base_configuration={"type": "VECTOR", "vectorKnowledgeBaseConfiguration": {...}},
    storage_configuration={...},
)
source = kb.create_data_source(knowledge_base_id=active["knowledgeBaseId"], name="manuals", dataSourceConfiguration={...})
job = kb.start_ingestion_job_and_wait(
    knowledge_base_id=active["knowledgeBaseId"],
    data_source_id=source["dataSource"]["dataSourceId"],
    wait_config=WaitConfig(max_wait=1800, poll_interval=15),
)
hits = kb.retrieve(knowledge_base_id=active["knowledgeBaseId"], retrieval_query={"text": "How do I reset access?"})
```

The example intentionally uses snake case only at the top level. `dataSourceConfiguration`, `vectorKnowledgeBaseConfiguration`, and other nested API shapes are not converted by the wrapper.

### Direct document ingestion

```python
final = kb.ingest_knowledge_base_documents_and_wait(
    knowledge_base_id="KB123",
    data_source_id="DS456",
    documents=[...],
)
failed = [d for d in final.get("documentDetails", []) if d.get("status") not in {
    "INDEXED", "PARTIALLY_INDEXED", "METADATA_PARTIALLY_INDEXED",
}]
```

Use direct document APIs only with a data source that supports them. Source-wide `start_ingestion_job` and direct document ingestion solve different ingestion paths; do not run both against the same content unless duplicate/version semantics are understood.

## Failure, correctness, and ownership rules

- IAM must authorize the caller separately for control-plane and runtime calls; constructing this client proves neither permission.
- A knowledge base being `ACTIVE` means its resource lifecycle completed, not necessarily that a new source has finished indexing. Wait for the relevant ingestion job/document statuses before retrieval.
- Retrieval can legitimately return no relevant chunks; it is not a service failure. Treat citation/score thresholds as application policy.
- Boto3 returns AWS exceptions (`ClientError`, validation, throttling, credential errors) unchanged. Build retries/idempotency and logging around business operations according to the service's request-token support.
- `__getattr__` only normalizes keyword spelling. It does not make a non-idempotent API idempotent or paginate list calls. Follow `nextToken` yourself for each forwarded `list_*` API.

## Callable coverage checklist

Public class and concrete methods: `KnowledgeBaseClient`, `__init__`, `__getattr__`, `create_knowledge_base_and_wait`, `update_knowledge_base_and_wait`, `delete_knowledge_base_and_wait`, `start_ingestion_job_and_wait`, `ingest_knowledge_base_documents_and_wait`.

Dynamic allowlisted callables: `create_knowledge_base`, `get_knowledge_base`, `update_knowledge_base`, `delete_knowledge_base`, `list_knowledge_bases`, `create_data_source`, `get_data_source`, `update_data_source`, `delete_data_source`, `list_data_sources`, `start_ingestion_job`, `get_ingestion_job`, `stop_ingestion_job`, `list_ingestion_jobs`, `ingest_knowledge_base_documents`, `get_knowledge_base_documents`, `delete_knowledge_base_documents`, `list_knowledge_base_documents`, `tag_resource`, `untag_resource`, `list_tags_for_resource`, `retrieve`, `retrieve_and_generate`, `retrieve_and_generate_stream`, `generate_query`, `rerank`, `agentic_retrieve_stream`.

`__init__.py` adds no callable beyond exporting `KnowledgeBaseClient`.
