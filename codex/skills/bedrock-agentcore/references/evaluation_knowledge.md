# Bedrock AgentCore Evaluation Knowledge

Last updated: 2026-07-13

This file is a project-neutral handbook for using the evaluation features exposed through `bedrock_agentcore.evaluation` and the AgentCore CLI. It is intended for teams to copy across projects and adapt by replacing placeholders such as `<runtime-name>`, `<region>`, `<session-id>`, and `<dataset-name>`.

Sources used:

- Local SDK package shape: `bedrock_agentcore/evaluation/`
- Installed AgentCore CLI help: `agentcore run eval --help`, `agentcore run batch-evaluation --help`
- AgentCore docs MCP: AgentCore Evaluation Quickstart

Important version note: some public quickstart material may show commands as `agentcore eval ...`. The CLI shape verified for this environment is `agentcore run eval` and `agentcore run batch-evaluation`. Always check the installed CLI in your project.

## Core Mental Model

Evaluation is span-based.

```text
Agent interaction
  -> runtime session ID
  -> traces/spans emitted to CloudWatch
  -> evaluation service reads spans
  -> evaluator scores at SESSION, TRACE, or TOOL_CALL level
  -> result contains score/value, label, explanation, and token usage where available
```

Operational rule: no spans means no evaluation. A deployed agent must have observability enabled and must have at least one completed session whose spans have reached CloudWatch.

CloudWatch ingestion delay is normal. AgentCore docs call out a typical delay of 2-5 minutes after invocation before spans are available.

## Values To Collect Per Project

Before running evaluations, each team should identify:

```text
AWS region: <region>
Runtime name from agentcore.json: <runtime-name>
Runtime ID: <runtime-id>
Runtime ARN: arn:aws:bedrock-agentcore:<region>:<account-id>:runtime/<runtime-id>
Runtime endpoint: DEFAULT unless using named endpoints
CloudWatch log group: /aws/bedrock-agentcore/runtimes/<runtime-id>-<endpoint>
Known session ID: <session-id>
Known trace ID, optional: <trace-id>
Dataset names, optional: <dataset-name>
Evaluator IDs: Builtin.* or custom evaluator ARNs
```

Recommended discovery commands:

```bash
agentcore status
agentcore traces list --runtime <runtime-name> --limit 20
agentcore evals history --runtime <runtime-name>
```



## Evaluator Levels

Evaluator levels control the `evaluationTarget` sent to the evaluation API.

### SESSION

Evaluates the whole conversation/session.

Typical examples:

- Goal completion
- Overall task success
- Multi-turn quality

SDK behavior:

- No `evaluationTarget` is added.
- Full `evaluationInput.sessionSpans` is evaluated.
- Session-level reference inputs can include assertions and expected tool trajectory.



### TRACE

Evaluates one or more individual traces/responses.

Typical examples:

- Helpfulness
- Correctness
- Relevance
- Faithfulness

SDK behavior:

- Adds `evaluationTarget: {"traceIds": [...]}`.
- If no explicit trace is supplied, all trace IDs are extracted from spans and batched.
- Batching limit is 10 target IDs per API request.
- Expected response ground truth is attached to a specific trace.



### TOOL_CALL

Evaluates individual tool executions.

Typical examples:

- Tool choice
- Tool parameters
- Tool-use correctness

SDK behavior:

- Adds `evaluationTarget: {"spanIds": [...]}`.
- Tool spans are detected by attributes:
  - `gen_ai.operation.name == "execute_tool"`
  - `openinference.span.kind == "TOOL"`
  - `traceloop.span.kind == "tool"`
- Batching limit is 10 target IDs per API request.



## Common Built-In Evaluators

The official quickstart shows built-in evaluators such as:

- `Builtin.GoalSuccessRate`: SESSION level, task completion / goal success
- `Builtin.Helpfulness`: TRACE level, response usefulness
- `Builtin.Correctness`: TRACE level, factual correctness

The exact available evaluator set can change. Use the installed CLI or SDK to list evaluators in the target account/region.

## CLI Usage



### On-Demand Evaluation

Check installed help:

```bash
agentcore run eval --help
```

Important flags:

```text
-r, --runtime <name>           Runtime name from project config
--runtime-arn <arn>            Runtime ARN for standalone mode
-e, --evaluator <names...>     Builtin.* IDs or project evaluator names
--evaluator-arn <arns...>      Evaluator ARNs for standalone mode
--region <region>              AWS region
-s, --session-id <id>          Specific session
-t, --trace-id <id>            Specific trace
--endpoint <name>              Runtime endpoint, default DEFAULT
--days <days>                  Lookback window, default 7
-A, --assertion <text...>      Ground truth assertions
--expected-trajectory <names>  Comma-separated expected tool call names
--expected-response <text>     Ground truth response text
--output <path>                Save output file
--dataset <name>               Invoke dataset scenarios instead of historical traces
--dataset-version <version>    Dataset version, or local file when omitted
--json                         JSON output
```

Evaluate a known session:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --session-id <session-id> \
  --evaluator Builtin.Helpfulness
```

Evaluate a specific trace:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --session-id <session-id> \
  --trace-id <trace-id> \
  --evaluator Builtin.Helpfulness
```

Evaluate with ground truth:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --session-id <session-id> \
  --evaluator Builtin.Helpfulness \
  --assertion "The response should answer the user's request clearly." \
  --expected-response "The response should be accurate, grounded, and concise."
```

Run dataset-backed evaluation:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --dataset <dataset-name> \
  --evaluator Builtin.Helpfulness
```

For a managed dataset version:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --dataset <dataset-name> \
  --dataset-version DRAFT \
  --evaluator Builtin.Helpfulness
```

Save JSON output:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --session-id <session-id> \
  --evaluator Builtin.Helpfulness \
  --json \
  --output eval-result.json
```



### Batch Evaluation

Check installed help:

```bash
agentcore run batch-evaluation --help
```

Important flags:

```text
-r, --runtime <name>         Runtime name from project config
-e, --evaluator <ids...>     Builtin.* evaluator IDs
--evaluator-arn <arns...>    Evaluator ARNs
-n, --name <name>            Batch evaluation job name
-d, --lookback-days <days>   Lookback window
-s, --session-ids <ids...>   Specific sessions
-g, --ground-truth <path>    JSON ground truth file
--region <region>            AWS region
--endpoint <name>            Runtime endpoint
--dataset <name>             Invoke dataset scenarios first
--dataset-version <version>  Dataset version
--kms-key <arn>              KMS key for encryption
--wait                       Block until terminal state
--json                       JSON output
```

Batch evaluate a known session:

```bash
agentcore run batch-evaluation \
  --runtime <runtime-name> \
  --region <region> \
  --session-ids <session-id> \
  --evaluator Builtin.Helpfulness \
  --name <batch-evaluation-name> \
  --wait
```

Batch evaluate a dataset:

```bash
agentcore run batch-evaluation \
  --runtime <runtime-name> \
  --region <region> \
  --dataset <dataset-name> \
  --evaluator Builtin.Helpfulness \
  --name <batch-evaluation-name> \
  --wait
```



### Viewing Results

On-demand eval history:

```bash
agentcore evals history --runtime <runtime-name>
agentcore evals history --runtime <runtime-name> --json
```

Trace discovery:

```bash
agentcore traces list --runtime <runtime-name> --limit 20
agentcore traces get <trace-id>
```



## Python SDK Public Exports

The package exports these major groups from `bedrock_agentcore.evaluation`:

- `EvaluationClient`
- `ReferenceInputs`
- `DatasetClient`



- Dataset models:
  - `Dataset`
  - `Scenario`
  - `PredefinedScenario`
  - `SimulatedScenario`
  - `Turn`
  - `ActorProfile`
  - `SimulationConfig`
- Dataset providers:
  - `FileDatasetProvider`
  - `DatasetManagementServiceProvider`
- Invocation types:
  - `AgentInvokerInput`
  - `AgentInvokerOutput`
  - `AgentInvokerFn`
- On-demand runner:
  - `OnDemandEvaluationDatasetRunner`
  - `EvaluationRunConfig`
  - `EvaluatorConfig`
  - `EvaluationResult`
  - `ScenarioResult`
  - `EvaluatorResult`
  - `CloudWatchAgentSpanCollector`
- Batch runner:
  - `BatchEvaluationRunner`
  - `BatchEvaluationRunConfig`
  - `BatchEvaluatorConfig`
  - `CloudWatchDataSourceConfig`
  - `OnlineEvaluationDataSourceConfig`
  - `BatchEvaluationResult`
- Custom code-based evaluator helpers:
  - `custom_code_based_evaluator`
  - `EvaluatorInput`
  - `EvaluatorOutput`
  - `ReferenceInput`
- Strands helpers:
  - `convert_strands_to_adot`
  - `create_strands_evaluator`
  - `StrandsEvalsAgentCoreEvaluator`
- CloudWatch helper:
  - `fetch_spans_from_cloudwatch`



## SDK Path 1: Evaluate Existing Session

Use `EvaluationClient` when the agent has already run and spans are already in CloudWatch.

Flow:

1. Resolve region.
2. Use `agent_id` to derive log group, or accept explicit `log_group_name`.
3. Query CloudWatch spans through `CloudWatchAgentSpanCollector`.
4. Build `evaluationInput: {"sessionSpans": spans}`.
5. Optionally attach `evaluationReferenceInputs`.
6. For each evaluator, call control plane `get_evaluator` to discover level.
7. Build level-aware targets:
  - SESSION: no target
  - TRACE: `traceIds`
  - TOOL_CALL: `spanIds`
8. Call data plane `evaluate`.
9. Return combined `evaluationResults`.

Example:

```python
from datetime import timedelta
from bedrock_agentcore.evaluation import EvaluationClient, ReferenceInputs

client = EvaluationClient(region_name="<region>")

results = client.run(
    evaluator_ids=["Builtin.Helpfulness"],
    session_id="<session-id>",
    log_group_name="/aws/bedrock-agentcore/runtimes/<runtime-id>-DEFAULT",
    look_back_time=timedelta(days=7),
    reference_inputs=ReferenceInputs(
        assertions=["The response should answer the user request clearly."],
        expected_response="The response should be accurate, grounded, and concise.",
        expected_trajectory=["<expected-tool-name>"],
    ),
)

for result in results:
    print(result)
```

Trace-specific evaluation:

```python
results = client.run(
    evaluator_ids=["Builtin.Helpfulness"],
    session_id="<session-id>",
    log_group_name="/aws/bedrock-agentcore/runtimes/<runtime-id>-DEFAULT",
    trace_id="<trace-id>",
)
```

Reference input behavior:

- `assertions` become a session-level object:
  - `{"context": {"spanContext": {"sessionId": ...}}, "assertions": [{"text": ...}]}`
- `expected_trajectory` becomes session-level:
  - `{"expectedTrajectory": {"toolNames": [...]}}`
- `expected_response` as a string maps to:
  - explicit `trace_id` if provided
  - otherwise the last extracted trace
- `expected_response` as a dict maps each `trace_id -> expected response`.

Important: if no spans are found, `EvaluationClient.run()` returns an empty list.

## SDK Path 2: On-Demand Dataset Runner

Use `OnDemandEvaluationDatasetRunner` when you want to run scenarios first, then collect spans and evaluate them.

Flow:

1. Run all scenarios concurrently.
2. Wait `evaluation_delay_seconds` for CloudWatch ingestion.
3. Collect spans for each successful scenario.
4. Build level-aware evaluator requests.
5. Run evaluators and group results by evaluator.

Configuration:

```python
from bedrock_agentcore.evaluation import EvaluationRunConfig, EvaluatorConfig

config = EvaluationRunConfig(
    evaluator_config=EvaluatorConfig(evaluator_ids=["Builtin.Helpfulness"]),
    evaluation_delay_seconds=180,
    max_concurrent_scenarios=5,
)
```

Dataset:

```python
from bedrock_agentcore.evaluation import Dataset, PredefinedScenario, Turn

dataset = Dataset(
    scenarios=[
        PredefinedScenario(
            scenario_id="basic_policy_question",
            turns=[
                Turn(
                    input={"prompt": "What is the relevant policy?"},
                    expected_response="The response should accurately explain the relevant policy.",
                )
            ],
            assertions=[
                "The response should be grounded in available source data.",
                "The response should not invent details.",
            ],
            expected_trajectory=["<expected-tool-name>"],
        )
    ]
)
```

Agent invoker contract:

```python
from bedrock_agentcore.evaluation import AgentInvokerInput, AgentInvokerOutput

def invoke_agent(input: AgentInvokerInput) -> AgentInvokerOutput:
    # input.payload is the scenario turn input.
    # input.session_id is generated by the runner and stable for all turns in the scenario.
    response = call_agent(payload=input.payload, session_id=input.session_id)
    return AgentInvokerOutput(agent_output=response)
```

The runner itself does not know how to call your agent. You must provide `agent_invoker`.

For deployed AgentCore Runtime agents, preserve the runner-generated session ID by passing it to runtime invocation as the runtime session ID. The exact payload shape should match your agent entrypoint.

Collector:

```python
from bedrock_agentcore.evaluation import CloudWatchAgentSpanCollector

collector = CloudWatchAgentSpanCollector(
    log_group_name="/aws/bedrock-agentcore/runtimes/<runtime-id>-DEFAULT",
    region="<region>",
    max_wait_seconds=300,
    poll_interval_seconds=30,
)
```

Run:

```python
from bedrock_agentcore.evaluation import OnDemandEvaluationDatasetRunner

runner = OnDemandEvaluationDatasetRunner(region="<region>")
result = runner.run(
    config=config,
    dataset=dataset,
    agent_invoker=invoke_agent,
    span_collector=collector,
)
```

Predefined scenario execution details:

- `PredefinedScenarioExecutor` generates session IDs as `<scenario_id>-<uuid>`.
- All turns in the same scenario use the same session ID.
- The return value of `agent_invoker` is not used for scoring directly by the runner; scoring happens from spans.
- Per-turn `expected_response` is matched to extracted trace IDs by turn index.



## SDK Path 3: Batch Evaluation Runner

Use `BatchEvaluationRunner` when evaluation should be submitted as an asynchronous AgentCore batch job.

Flow:

1. Execute scenarios in parallel through `agent_invoker`.
2. Transform scenario ground truth into batch `evaluationMetadata.sessionMetadata`.
3. Call `data_source.pre_evaluation_run_hook()`.
4. Start a batch evaluation job with `start_batch_evaluation`.
5. Poll `get_batch_evaluation` until terminal state.
6. Return `BatchEvaluationResult`.
7. Optionally call `fetch_evaluation_events(result)` for per-turn events.

Terminal states:

```text
Successful: COMPLETED, COMPLETED_WITH_ERRORS
Terminal: COMPLETED, COMPLETED_WITH_ERRORS, FAILED, STOPPED, DELETING
Running: PENDING, IN_PROGRESS, STOPPING
```

CloudWatch data source:

```python
from bedrock_agentcore.evaluation import CloudWatchDataSourceConfig

data_source = CloudWatchDataSourceConfig(
    service_names=["<service-name>"],
    log_group_names=[
        "/aws/bedrock-agentcore/runtimes/<runtime-id>-DEFAULT"
    ],
    ingestion_delay_seconds=180,
)
```

Constraints from local model:

- `service_names`: list length exactly 1.
- `log_group_names`: list length 1 to 5.
- `ingestion_delay_seconds`: integer >= 0.

Run:

```python
from bedrock_agentcore.evaluation import (
    BatchEvaluationRunner,
    BatchEvaluationRunConfig,
    BatchEvaluatorConfig,
)

runner = BatchEvaluationRunner(region="<region>")

result = runner.run_dataset_evaluation(
    config=BatchEvaluationRunConfig(
        batch_evaluation_name="<batch-evaluation-name>",
        evaluator_config=BatchEvaluatorConfig(
            evaluator_ids=["Builtin.Helpfulness"]
        ),
        data_source=data_source,
        max_concurrent_scenarios=5,
        polling_timeout_seconds=1800,
        polling_interval_seconds=30,
    ),
    dataset=dataset,
    agent_invoker=invoke_agent,
)
```

Fetch detailed per-turn result events:

```python
events = runner.fetch_evaluation_events(result)
for event in events:
    print(event)
```

`fetch_evaluation_events` reads JSON events from the CloudWatch log group/stream returned in `result.output_data_config`.

## Dataset Types



### PredefinedScenario

Schema type:

```text
AGENTCORE_EVALUATION_PREDEFINED_V1
```

Fields:

```python
PredefinedScenario(
    scenario_id="unique-id",
    turns=[
        Turn(input="...", expected_response="..."),
    ],
    assertions=["..."],
    expected_trajectory=["tool1", "tool2"],
    metadata={...},
)
```

Validation:

- `turns` must not be empty.
- Dataset scenario IDs must be unique.

JSONL example:

```json
{"scenario_id":"policy-question","turns":[{"input":{"prompt":"What is the policy?"},"expected_response":"The answer should explain the policy."}],"assertions":["Agent should use source facts"],"expected_trajectory":["lookup_policy"]}
```

Note: the local SDK `FileDatasetProvider` reads `expected_response` in JSONL `turns`. If your CLI or service accepts camelCase `expectedResponse`, verify that path separately before using the same file through the Python SDK provider.

### SimulatedScenario

Schema type:

```text
AGENTCORE_EVALUATION_SIMULATED_V1
```

Fields:

```python
SimulatedScenario(
    scenario_id="unique-id",
    scenario_description="...",
    actor_profile=ActorProfile(
        traits={"personality": "..."},
        context="...",
        goal="...",
    ),
    input="initial user message",
    max_turns=10,
    assertions=["..."],
    metadata={...},
)
```

Validation:

- `max_turns` must be >= 1.
- Required JSON fields for parser when no `turns` are present:
  - `scenario_id`
  - `actor_profile`
  - `input`

Runtime behavior:

- Uses `SimulatedScenarioExecutor`.
- Requires optional Strands Evals simulation dependencies.
- Imports `strands_evals.simulation.tools.goal_completion`.
- If missing, raises an ImportError instructing installation of `bedrock-agentcore[simulation]`.

Simulation config:

```python
SimulationConfig(
    model_id=None,
    system_prompt_template=None,
    input_type=None,
    output_type=None,
)
```

The actor simulator uses a dynamic Pydantic response model. If `input_type` is set, the actor's next message is schema-constrained to that type. If `output_type` is set, agent outputs are validated before being passed back to the actor.

## Dataset Providers



### FileDatasetProvider

Loads local JSON or JSONL into `Dataset`.

Behavior:

- `.jsonl`: one scenario JSON object per line.
- other extension: JSON object containing `{"scenarios": [...]}`.
- If raw scenario has `turns`, parses as `PredefinedScenario`.
- Otherwise parses as `SimulatedScenario`.

Example:

```python
from bedrock_agentcore.evaluation import FileDatasetProvider

dataset = FileDatasetProvider("agentcore/datasets/<dataset-file>.jsonl").get_dataset()
```



### DatasetManagementServiceProvider

Loads a managed AgentCore dataset by `dataset_id` and optional version.

Behavior:

- Calls `DatasetClient.get_dataset`.
- Checks `schemaType` is supported:
  - `AGENTCORE_EVALUATION_PREDEFINED_V1`
  - `AGENTCORE_EVALUATION_SIMULATED_V1`
- Requires `downloadUrl` in service response.
- Downloads JSONL content with `requests`.
- Requires the `datasets` extra if `requests` is not installed.

Example:

```python
from bedrock_agentcore.evaluation import DatasetManagementServiceProvider

dataset = DatasetManagementServiceProvider(
    dataset_id="<dataset-id>",
    version_id="DRAFT",
).get_dataset()
```



## DatasetClient

Purpose: manage evaluation datasets through the `bedrock-agentcore-control` service.

Pass-through methods:

- `create_dataset`
- `get_dataset`
- `list_datasets`
- `update_dataset`
- `delete_dataset`
- `create_dataset_version`
- `list_dataset_versions`
- `add_dataset_examples`
- `update_dataset_examples`
- `delete_dataset_examples`
- `list_dataset_examples`

Wait helpers:

- `create_dataset_and_wait`
- `delete_dataset_and_wait`
- `create_dataset_version_and_wait`
- `add_examples_and_wait`
- `update_examples_and_wait`
- `delete_examples_and_wait`

Example:

```python
from bedrock_agentcore.evaluation import DatasetClient

client = DatasetClient(region_name="<region>")
dataset = client.create_dataset_and_wait(
    datasetName="<dataset-name>",
    schemaType="AGENTCORE_EVALUATION_PREDEFINED_V1",
    source={"inlineExamples": {"examples": []}},
)
```



## Span Collection

`CloudWatchAgentSpanCollector` collects spans after an agent invocation.

Constructor:

```python
CloudWatchAgentSpanCollector(
    log_group_name="...",
    region="<region>",
    max_wait_seconds=300,
    poll_interval_seconds=30,
)
```

Collection behavior:

- Adds a 60 second buffer to `end_time`.
- Polls until spans appear or timeout.
- Queries both:
  - `aws/spans`
  - configured event log group
- Uses a CloudWatch Logs Insights query filtering:
  - `attributes.session.id = "<session_id>"`
  - `ispresent(scope.name)`
  - `ispresent(traceId)`
  - `ispresent(spanId)`
- Sorts results by `endTimeUnixNano`.

If no spans are found before timeout, returns an empty list.

Convenience function:

```python
from bedrock_agentcore.evaluation import fetch_spans_from_cloudwatch

spans = fetch_spans_from_cloudwatch(
    session_id="<session-id>",
    event_log_group="/aws/bedrock-agentcore/runtimes/<runtime-id>-DEFAULT",
    start_time=start_time,
    end_time=end_time,
    region="<region>",
)
```



## Custom Evaluators

The package supports code-based evaluator Lambda handlers.

Decorator:

```python
from bedrock_agentcore.evaluation import (
    custom_code_based_evaluator,
    EvaluatorInput,
    EvaluatorOutput,
)

@custom_code_based_evaluator()
def handler(input: EvaluatorInput, context) -> EvaluatorOutput:
    return EvaluatorOutput(
        value=1.0,
        label="Pass",
        explanation="The response meets the evaluation requirement.",
    )
```

The decorator:

- Reads raw Lambda event.
- Extracts `evaluationLevel`.
- Extracts `evaluationInput.sessionSpans`.
- Extracts first target trace ID or span ID from `evaluationTarget`.
- Parses `evaluationReferenceInputs`.
- Calls the wrapped function with typed `EvaluatorInput`.
- Requires the wrapped function to return `EvaluatorOutput`.
- Serializes output with `model_dump()`.

`EvaluatorInput` fields:

```text
evaluation_level: SESSION | TRACE | TOOL_CALL
session_spans: raw ADOT span dicts
target_trace_id: set for TRACE target
target_span_id: set for TOOL_CALL target
schema_version: default 1.0
evaluator_id
evaluator_name
reference_inputs
```

`EvaluatorOutput` fields:

```text
value: numeric score
label: required for success
explanation
errorCode
errorMessage
```

Validation rule: a success response must include `label`; if no label is provided, set `errorCode` to return an error response.

Domain-specific custom evaluator ideas:

- Grounding: response must cite or reflect known source data.
- No invention: response must not introduce unsupported facts.
- Safety: response must avoid unsafe or disallowed content.
- Privacy: response must not reveal sensitive data to the wrong user.
- Escalation: response must route high-risk cases to the correct human process.
- Tool trajectory: response should use expected tools for specific task classes.



## Creating Evaluators Through SDK

`EvaluationClient` forwards selected control plane evaluator methods:

- `create_evaluator`
- `get_evaluator`
- `list_evaluators`
- `update_evaluator`
- `delete_evaluator`
- `create_online_evaluation_config`
- `get_online_evaluation_config`
- `list_online_evaluation_configs`
- `update_online_evaluation_config`
- `delete_online_evaluation_config`

It also provides wait helpers:

- `create_evaluator_and_wait`
- `update_evaluator_and_wait`
- `delete_evaluator_and_wait`
- `create_online_evaluation_config_and_wait`
- `update_online_evaluation_config_and_wait`
- `delete_online_evaluation_config_and_wait`

Example shape:

```python
from bedrock_agentcore.evaluation import EvaluationClient

client = EvaluationClient(region_name="<region>")

evaluator = client.create_evaluator_and_wait(
    evaluatorName="<custom-evaluator-name>",
    level="TRACE",
    # additional service-specific evaluator config here
)
```

Use exact service API fields from current boto3/AgentCore docs when creating real evaluators.

## Online Evaluation

Online evaluation is continuous evaluation of sampled live traffic.

Concept:

- Create an online evaluation config.
- Attach evaluator IDs.
- Set sampling rate.
- AgentCore evaluates sampled production sessions.
- Results are visible in CloudWatch / GenAI Observability / Bedrock AgentCore.

Docs command shape:

```bash
agentcore eval online create \
  --name <online-eval-config-name> \
  --sampling-rate 1.0 \
  --evaluator "Builtin.GoalSuccessRate" \
  --evaluator "Builtin.Helpfulness" \
  --description "Production evaluation for this agent"
```

Important: confirm exact command syntax against the installed CLI before use, because CLI command groups can differ by toolkit version.

The SDK exposes control plane pass-through methods for online evaluation configs through `EvaluationClient`.

## Strands Integration

Purpose: use AgentCore evaluation from Strands Evals workflows.

### Span Conversion

`convert_strands_to_adot(raw_spans)` converts raw OpenTelemetry spans from Strands to ADOT-formatted span/log documents.

It parses Strands event names:

- `gen_ai.user.message`
- `gen_ai.assistant.message`
- `gen_ai.tool.message`
- `gen_ai.choice`

It builds:

- ADOT span document
- conversation log record
- tool execution log record when `gen_ai.operation.name == "execute_tool"`

Example:

```python
from bedrock_agentcore.evaluation import convert_strands_to_adot

raw_spans = list(telemetry.in_memory_exporter.get_finished_spans())
adot_docs = convert_strands_to_adot(raw_spans)
```



### Strands Evals Adapter

`create_strands_evaluator(evaluator_id, **kwargs)` returns a Strands-compatible evaluator.

Behavior:

- If trajectory is already ADOT dicts, uses them as-is.
- If trajectory is raw OTel spans, validates and converts them.
- Calls `bedrock-agentcore.evaluate`.
- Produces Strands `EvaluationOutput` with:
  - `score`
  - `test_pass`
  - `reason`
- `test_pass` is `score >= test_pass_score`.

Example:

```python
from bedrock_agentcore.evaluation import create_strands_evaluator

evaluator = create_strands_evaluator(
    "Builtin.Helpfulness",
    region="<region>",
    test_pass_score=0.7,
)
```

The optional symbols are lazy-imported. If `strands-agents-evals` extra is missing, importing `create_strands_evaluator` or `StrandsEvalsAgentCoreEvaluator` raises an ImportError instructing installation of `bedrock-agentcore[strands-agents-evals]`.

## Invoking A Deployed Runtime For Dataset Evaluation

For dataset runners, your `agent_invoker` must call the test subject and preserve the runner-generated session ID.

For AgentCore Runtime agents, inspect the installed boto3 service model if in doubt. Current parameters for `InvokeAgentRuntime` include:

```text
agentRuntimeArn: required
payload: required blob
runtimeSessionId: optional
qualifier: optional endpoint
contentType: optional
accept: optional
```

Example invoker shape:

```python
import json
import boto3
from bedrock_agentcore.evaluation import AgentInvokerInput, AgentInvokerOutput

client = boto3.client("bedrock-agentcore", region_name="<region>")
runtime_arn = "arn:aws:bedrock-agentcore:<region>:<account-id>:runtime/<runtime-id>"

def invoke_agent(input: AgentInvokerInput) -> AgentInvokerOutput:
    payload = input.payload
    if isinstance(payload, str):
        payload = {"prompt": payload}

    response = client.invoke_agent_runtime(
        agentRuntimeArn=runtime_arn,
        qualifier="DEFAULT",
        runtimeSessionId=input.session_id,
        contentType="application/json",
        accept="application/json",
        payload=json.dumps(payload).encode("utf-8"),
    )

    body = response.get("response")
    if hasattr(body, "read"):
        body = body.read()
    if isinstance(body, bytes):
        body = body.decode("utf-8")

    return AgentInvokerOutput(agent_output=body)
```

Adjust the payload wrapper to match your agent entrypoint. Some agents expect `{"prompt": ...}`, others expect `{"input": ...}`, `{"messages": ...}`, or a domain-specific schema.

## Troubleshooting



### No spans found

Likely causes:

- CloudWatch ingestion delay.
- Wrong session ID.
- Wrong log group.
- Session outside lookback window.
- Observability was not enabled when session ran.
- Agent invocation failed before spans were emitted.

Actions:

```bash
agentcore traces list --runtime <runtime-name> --limit 20 --since 2h
agentcore run eval --runtime <runtime-name> --session-id <session-id> --days 30 --evaluator Builtin.Helpfulness
```

Wait 2-5 minutes after a fresh invocation before evaluating.

### Trace evaluator returns no results

Likely causes:

- No trace IDs extracted from spans.
- Wrong `trace_id`.
- Evaluator level is not TRACE.

Actions:

- Run session-level evaluation first.
- Use `agentcore traces list` to find trace IDs.
- Avoid `--trace-id` until the broad session evaluation works.



### Tool evaluator returns no results

Likely causes:

- No tool spans emitted.
- Tool attributes do not match supported markers.
- Question did not require a tool call.

Actions:

- Ask a prompt that definitely requires a tool.
- Verify spans include `gen_ai.operation.name == "execute_tool"` or another supported tool marker.



### Dataset runner produces failed scenarios

Likely causes:

- `agent_invoker` raised an exception.
- Payload shape does not match the agent entrypoint.
- Runtime invocation did not pass `runtimeSessionId`.
- Optional simulated scenario dependencies are missing.

Actions:

- Test `agent_invoker` with one payload outside the runner.
- Ensure payload shape matches your agent.
- For simulated scenarios, install required `bedrock-agentcore[simulation]` extras if needed.



### Batch evaluation starts but detailed events are missing

Likely causes:

- `result.output_data_config` is absent.
- CloudWatch result stream not written yet.
- CloudWatch log stream is not available immediately.

Actions:

- Check `result.status`.
- Retry `fetch_evaluation_events(result)` after a short delay.
- If `output_data_config` is `None`, the service did not return a CloudWatch destination for that job.



### CLI command mismatch

Official docs may show:

```bash
agentcore eval run
```

Some installed versions use:

```bash
agentcore run eval
```

Always check:

```bash
agentcore --help
agentcore run eval --help
agentcore run batch-evaluation --help
```



## Suggested Evaluation Use Cases

1. Policy or documentation QA
  - Evaluators: `Builtin.Helpfulness`, `Builtin.Correctness`
  - Expected trajectory: retrieval/search tool
  - Assertions:
    - Response uses source facts.
    - Response does not invent details.
    - Response handles missing information honestly.
2. Account or record lookup
  - Evaluators: `Builtin.Correctness`
  - Expected trajectory: lookup tool
  - Assertions:
    - Response uses the lookup result.
    - Response does not expose unrelated user data.
3. Transactional workflow
  - Evaluators: `Builtin.GoalSuccessRate`, custom SESSION evaluator
  - Expected trajectory: validate -> execute -> confirm
  - Assertions:
    - Agent asks for missing required fields.
    - Agent confirms action outcome.
4. Sensitive or escalated support issue
  - Evaluators: custom TRACE or SESSION evaluator
  - Assertions:
    - Response acknowledges concern.
    - Response routes to the correct human or policy process.
    - Response avoids unsafe claims.
5. Multi-turn simulated user
  - Dataset type: `AGENTCORE_EVALUATION_SIMULATED_V1`
  - Goal: user tries to complete a workflow across follow-ups.
  - Assertions:
    - Agent does not lose track of the issue.
    - Agent asks for missing details.
    - Agent does not close prematurely.



## Safe Defaults

For demos:

```text
Evaluator: Builtin.Helpfulness
Endpoint: DEFAULT
Lookback: 7 days, increase to 30 if needed
Wait after invocation: 2-5 minutes
Dataset concurrency: low, e.g. 1-3, to avoid noisy failures/cost surprises
```

For CI or repeatable checks:

- Keep datasets small and deterministic.
- Prefer predefined scenarios first.
- Add simulated scenarios later.
- Pin evaluator IDs.
- Save JSON outputs.
- Treat score thresholds as policy decisions, not universal truth.



## Quick Reference

Historical session CLI:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --session-id <session-id> \
  --evaluator Builtin.Helpfulness \
  --json
```

Dataset CLI:

```bash
agentcore run eval \
  --runtime <runtime-name> \
  --region <region> \
  --dataset <dataset-name> \
  --evaluator Builtin.Helpfulness \
  --json
```

Batch CLI:

```bash
agentcore run batch-evaluation \
  --runtime <runtime-name> \
  --region <region> \
  --dataset <dataset-name> \
  --evaluator Builtin.Helpfulness \
  --name <batch-evaluation-name> \
  --wait \
  --json
```

Python existing session:

```python
from datetime import timedelta
from bedrock_agentcore.evaluation import EvaluationClient

client = EvaluationClient(region_name="<region>")
results = client.run(
    evaluator_ids=["Builtin.Helpfulness"],
    session_id="<session-id>",
    log_group_name="/aws/bedrock-agentcore/runtimes/<runtime-id>-DEFAULT",
    look_back_time=timedelta(days=7),
)
```

Python load local dataset:

```python
from bedrock_agentcore.evaluation import FileDatasetProvider

dataset = FileDatasetProvider("agentcore/datasets/<dataset-file>.jsonl").get_dataset()
```

Python span collector:

```python
from bedrock_agentcore.evaluation import CloudWatchAgentSpanCollector

collector = CloudWatchAgentSpanCollector(
    log_group_name="/aws/bedrock-agentcore/runtimes/<runtime-id>-DEFAULT",
    region="<region>",
)
```

