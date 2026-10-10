# Complete callable and class index

Generated from the inspected AST, including conditional declarations, properties/setters, private methods, and nested closures. Entries are keyed by source path, line, and lexical name to distinguish duplicate names. Each source section links its manually written behavioral guide; implementation discussion there takes precedence over a source docstring when they differ. The brief summaries below are labeled source-docstring excerpts, not independent verification of behavior. Signatures exclude decorators; source links retain those details. No-callable initializers are also listed.

## `__init__.py`

Behavior: [init_knowledge.md](init_knowledge.md). Source: [__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/__init__.py).

No declared classes/functions/methods. Import and export behavior is documented in the linked guide.

## `agent_execution/__init__.py`

Behavior: [agent_execution_knowledge.md](agent_execution_knowledge.md). Source: [agent_execution/__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/__init__.py).

No declared classes/functions/methods. Import and export behavior is documented in the linked guide.

## `agent_execution/active_task.py`

Behavior: [agent_execution_knowledge.md](agent_execution_knowledge.md). Source: [agent_execution/active_task.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py).

<!-- declaration:agent_execution/active_task.py:95:_RequestStarted -->
### `_RequestStarted` — line 95

```python
class _RequestStarted()
```

Source: [_RequestStarted](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:95).

Source-docstring summary: No class docstring; role and value/constructor semantics are covered in the linked behavioral guide.

<!-- declaration:agent_execution/active_task.py:96:_RequestStarted.__init__ -->
### `_RequestStarted.__init__` — line 96

```python
def __init__(self, request_id: uuid.UUID, request_context: RequestContext)
```

Source: [_RequestStarted.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:96).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:agent_execution/active_task.py:101:_RequestCompleted -->
### `_RequestCompleted` — line 101

```python
class _RequestCompleted()
```

Source: [_RequestCompleted](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:101).

Source-docstring summary: No class docstring; role and value/constructor semantics are covered in the linked behavioral guide.

<!-- declaration:agent_execution/active_task.py:102:_RequestCompleted.__init__ -->
### `_RequestCompleted.__init__` — line 102

```python
def __init__(self, request_id: uuid.UUID)
```

Source: [_RequestCompleted.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:102).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:agent_execution/active_task.py:106:EventConsumer -->
### `EventConsumer` — line 106

```python
class EventConsumer()
```

Source: [EventConsumer](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:106).

Source-docstring summary: Consumes events from the agent and updates system state.

<!-- declaration:agent_execution/active_task.py:109:EventConsumer.__init__ -->
### `EventConsumer.__init__` — line 109

```python
def __init__(self, active_task: ActiveTask) -> None
```

Source: [EventConsumer.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:109).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:agent_execution/active_task.py:114:EventConsumer.run -->
### `EventConsumer.run` — line 114

```python
async def run(self) -> None
```

Source: [EventConsumer.run](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:114).

Source-docstring summary: Consumes events from the agent and updates system state.

<!-- declaration:agent_execution/active_task.py:156:EventConsumer._process_event -->
### `EventConsumer._process_event` — line 156

```python
async def _process_event(self, event: Event) -> None
```

Source: [EventConsumer._process_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:156).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:196:EventConsumer._handle_message_event -->
### `EventConsumer._handle_message_event` — line 196

```python
def _handle_message_event(self, event: Message) -> None
```

Source: [EventConsumer._handle_message_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:196).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:207:EventConsumer._handle_task_event -->
### `EventConsumer._handle_task_event` — line 207

```python
async def _handle_task_event(self, event: Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent | PushNotificationEvent) -> Task
```

Source: [EventConsumer._handle_task_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:207).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:230:EventConsumer._handle_initial_task -->
### `EventConsumer._handle_initial_task` — line 230

```python
async def _handle_initial_task(self, event: Task) -> None
```

Source: [EventConsumer._handle_initial_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:230).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:241:EventConsumer._handle_task_modification_event -->
### `EventConsumer._handle_task_modification_event` — line 241

```python
async def _handle_task_modification_event(self, event: TaskStatusUpdateEvent | TaskArtifactUpdateEvent | PushNotificationEvent) -> None
```

Source: [EventConsumer._handle_task_modification_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:241).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:282:EventConsumer._update_task_state -->
### `EventConsumer._update_task_state` — line 282

```python
async def _update_task_state(self, updated_task: Task, event: Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent | PushNotificationEvent) -> None
```

Source: [EventConsumer._update_task_state](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:282).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:308:EventConsumer._handle_terminal_state -->
### `EventConsumer._handle_terminal_state` — line 308

```python
async def _handle_terminal_state(self, updated_task: Task) -> None
```

Source: [EventConsumer._handle_terminal_state](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:308).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:317:EventConsumer._enqueue_to_subscribers -->
### `EventConsumer._enqueue_to_subscribers` — line 317

```python
async def _enqueue_to_subscribers(self, event: Event, updated_task: Task | None) -> None
```

Source: [EventConsumer._enqueue_to_subscribers](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:317).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:339:ActiveTask -->
### `ActiveTask` — line 339

```python
class ActiveTask()
```

Source: [ActiveTask](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:339).

Source-docstring summary: Manages the lifecycle and execution of an active A2A task.

<!-- declaration:agent_execution/active_task.py:357:ActiveTask.__init__ -->
### `ActiveTask.__init__` — line 357

```python
def __init__(self, agent_executor: AgentExecutor, task_id: str, task_manager: TaskManager, push_sender: PushNotificationSender | None=None, on_cleanup: Callable[[ActiveTask], None] | None=None) -> None
```

Source: [ActiveTask.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:357).

Source-docstring summary: Initializes the ActiveTask.

<!-- declaration:agent_execution/active_task.py:418:ActiveTask.task_id -->
### `ActiveTask.task_id` — line 418

```python
def task_id(self) -> str
```

Source: [ActiveTask.task_id](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:418).

Source-docstring summary: The ID of the task.

<!-- declaration:agent_execution/active_task.py:422:ActiveTask.enqueue_request -->
### `ActiveTask.enqueue_request` — line 422

```python
async def enqueue_request(self, request_context: RequestContext) -> uuid.UUID
```

Source: [ActiveTask.enqueue_request](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:422).

Source-docstring summary: Enqueues a request for the active task to process.

<!-- declaration:agent_execution/active_task.py:430:ActiveTask.start -->
### `ActiveTask.start` — line 430

```python
async def start(self, call_context: ServerCallContext, create_task_if_missing: bool=False) -> None
```

Source: [ActiveTask.start](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:430).

Source-docstring summary: Starts the active task background processes.

<!-- declaration:agent_execution/active_task.py:500:ActiveTask._run_producer -->
### `ActiveTask._run_producer` — line 500

```python
async def _run_producer(self) -> None
```

Source: [ActiveTask._run_producer](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:500).

Source-docstring summary: Executes the agent logic.

<!-- declaration:agent_execution/active_task.py:582:ActiveTask._run_consumer -->
### `ActiveTask._run_consumer` — line 582

```python
async def _run_consumer(self) -> None
```

Source: [ActiveTask._run_consumer](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:582).

Source-docstring summary: Consumes events from the agent and updates system state.

<!-- declaration:agent_execution/active_task.py:608:ActiveTask.subscribe -->
### `ActiveTask.subscribe` — line 608

```python
async def subscribe(self, *, request: RequestContext | None=None, include_initial_task: bool=False, replace_status_update_with_task: bool=False) -> AsyncGenerator[Event, None]
```

Source: [ActiveTask.subscribe](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:608).

Source-docstring summary: Creates a queue tap and yields events as they are produced.

<!-- declaration:agent_execution/active_task.py:711:ActiveTask.cancel -->
### `ActiveTask.cancel` — line 711

```python
async def cancel(self, call_context: ServerCallContext) -> Task
```

Source: [ActiveTask.cancel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:711).

Source-docstring summary: Cancels the running active task.

<!-- declaration:agent_execution/active_task.py:809:ActiveTask.aclose -->
### `ActiveTask.aclose` — line 809

```python
async def aclose(self) -> None
```

Source: [ActiveTask.aclose](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:809).

Source-docstring summary: Force-closes the task's queues and drains its background tasks.

<!-- declaration:agent_execution/active_task.py:851:ActiveTask._maybe_cleanup -->
### `ActiveTask._maybe_cleanup` — line 851

```python
async def _maybe_cleanup(self) -> None
```

Source: [ActiveTask._maybe_cleanup](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:851).

Source-docstring summary: Triggers cleanup if task is finished and has no subscribers.

<!-- declaration:agent_execution/active_task.py:874:ActiveTask._mark_task_as_failed -->
### `ActiveTask._mark_task_as_failed` — line 874

```python
async def _mark_task_as_failed(self, exception: Exception) -> Task | None
```

Source: [ActiveTask._mark_task_as_failed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:874).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task.py:894:ActiveTask.get_task -->
### `ActiveTask.get_task` — line 894

```python
async def get_task(self) -> Task
```

Source: [ActiveTask.get_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task.py:894).

Source-docstring summary: Get task from db.

## `agent_execution/active_task_registry.py`

Behavior: [agent_execution_knowledge.md](agent_execution_knowledge.md). Source: [agent_execution/active_task_registry.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py).

<!-- declaration:agent_execution/active_task_registry.py:25:ActiveTaskRegistry -->
### `ActiveTaskRegistry` — line 25

```python
class ActiveTaskRegistry()
```

Source: [ActiveTaskRegistry](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py:25).

Source-docstring summary: A registry for active ActiveTask instances.

<!-- declaration:agent_execution/active_task_registry.py:28:ActiveTaskRegistry.__init__ -->
### `ActiveTaskRegistry.__init__` — line 28

```python
def __init__(self, agent_executor: AgentExecutor, task_store: TaskStore, push_sender: PushNotificationSender | None=None)
```

Source: [ActiveTaskRegistry.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py:28).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:agent_execution/active_task_registry.py:42:ActiveTaskRegistry.get_or_create -->
### `ActiveTaskRegistry.get_or_create` — line 42

```python
async def get_or_create(self, task_id: str, call_context: ServerCallContext, context_id: str | None=None, create_task_if_missing: bool=False, initial_message: Message | None=None) -> ActiveTask
```

Source: [ActiveTaskRegistry.get_or_create](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py:42).

Source-docstring summary: Retrieves an existing ActiveTask or creates a new one.

<!-- declaration:agent_execution/active_task_registry.py:99:ActiveTaskRegistry._on_active_task_cleanup -->
### `ActiveTaskRegistry._on_active_task_cleanup` — line 99

```python
def _on_active_task_cleanup(self, active_task: ActiveTask) -> None
```

Source: [ActiveTaskRegistry._on_active_task_cleanup](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py:99).

Source-docstring summary: Called by ActiveTask when it's finished and has no subscribers.

<!-- declaration:agent_execution/active_task_registry.py:106:ActiveTaskRegistry._remove_task -->
### `ActiveTaskRegistry._remove_task` — line 106

```python
async def _remove_task(self, task_id: str) -> None
```

Source: [ActiveTaskRegistry._remove_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py:106).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:agent_execution/active_task_registry.py:111:ActiveTaskRegistry.get -->
### `ActiveTaskRegistry.get` — line 111

```python
async def get(self, task_id: str) -> ActiveTask | None
```

Source: [ActiveTaskRegistry.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py:111).

Source-docstring summary: Retrieves an existing task.

<!-- declaration:agent_execution/active_task_registry.py:116:ActiveTaskRegistry.aclose -->
### `ActiveTaskRegistry.aclose` — line 116

```python
async def aclose(self) -> None
```

Source: [ActiveTaskRegistry.aclose](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/active_task_registry.py:116).

Source-docstring summary: Closes the registry and drains all active tasks.

## `agent_execution/agent_executor.py`

Behavior: [agent_execution_knowledge.md](agent_execution_knowledge.md). Source: [agent_execution/agent_executor.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/agent_executor.py).

<!-- declaration:agent_execution/agent_executor.py:7:AgentExecutor -->
### `AgentExecutor` — line 7

```python
class AgentExecutor(ABC)
```

Source: [AgentExecutor](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/agent_executor.py:7).

Source-docstring summary: Agent Executor interface.

<!-- declaration:agent_execution/agent_executor.py:15:AgentExecutor.execute -->
### `AgentExecutor.execute` — line 15

```python
async def execute(self, context: RequestContext, event_queue: EventQueue) -> None
```

Source: [AgentExecutor.execute](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/agent_executor.py:15).

Source-docstring summary: Execute the agent's logic for a given request context.

<!-- declaration:agent_execution/agent_executor.py:70:AgentExecutor.cancel -->
### `AgentExecutor.cancel` — line 70

```python
async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None
```

Source: [AgentExecutor.cancel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/agent_executor.py:70).

Source-docstring summary: Request the agent to cancel an ongoing task.

## `agent_execution/context.py`

Behavior: [agent_execution_knowledge.md](agent_execution_knowledge.md). Source: [agent_execution/context.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py).

<!-- declaration:agent_execution/context.py:21:RequestContext -->
### `RequestContext` — line 21

```python
class RequestContext()
```

Source: [RequestContext](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:21).

Source-docstring summary: Request Context.

<!-- declaration:agent_execution/context.py:29:RequestContext.__init__ -->
### `RequestContext.__init__` — line 29

```python
def __init__(self, call_context: ServerCallContext, request: SendMessageRequest | None=None, task_id: str | None=None, context_id: str | None=None, task: Task | None=None, related_tasks: list[Task] | None=None, task_id_generator: IDGenerator | None=None, context_id_generator: IDGenerator | None=None)
```

Source: [RequestContext.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:29).

Source-docstring summary: Initializes the RequestContext.

<!-- declaration:agent_execution/context.py:82:RequestContext.get_user_input -->
### `RequestContext.get_user_input` — line 82

```python
def get_user_input(self, delimiter: str='\n') -> str
```

Source: [RequestContext.get_user_input](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:82).

Source-docstring summary: Extracts text content from the user's message parts.

<!-- declaration:agent_execution/context.py:98:RequestContext.attach_related_task -->
### `RequestContext.attach_related_task` — line 98

```python
def attach_related_task(self, task: Task) -> None
```

Source: [RequestContext.attach_related_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:98).

Source-docstring summary: Attaches a related task to the context.

<!-- declaration:agent_execution/context.py:110:RequestContext.message -->
### `RequestContext.message` — line 110

```python
def message(self) -> Message | None
```

Source: [RequestContext.message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:110).

Source-docstring summary: The incoming `Message` object from the request, if available.

<!-- declaration:agent_execution/context.py:115:RequestContext.related_tasks -->
### `RequestContext.related_tasks` — line 115

```python
def related_tasks(self) -> list[Task]
```

Source: [RequestContext.related_tasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:115).

Source-docstring summary: A list of tasks related to the current request.

<!-- declaration:agent_execution/context.py:120:RequestContext.current_task -->
### `RequestContext.current_task` — line 120

```python
def current_task(self) -> Task | None
```

Source: [RequestContext.current_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:120).

Source-docstring summary: The current `Task` object being processed.

<!-- declaration:agent_execution/context.py:125:RequestContext.current_task -->
### `RequestContext.current_task` — line 125

```python
def current_task(self, task: Task | None) -> None
```

Source: [RequestContext.current_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:125).

Source-docstring summary: Sets the current task object.

<!-- declaration:agent_execution/context.py:130:RequestContext.task_id -->
### `RequestContext.task_id` — line 130

```python
def task_id(self) -> str | None
```

Source: [RequestContext.task_id](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:130).

Source-docstring summary: The ID of the task associated with this context.

<!-- declaration:agent_execution/context.py:135:RequestContext.context_id -->
### `RequestContext.context_id` — line 135

```python
def context_id(self) -> str | None
```

Source: [RequestContext.context_id](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:135).

Source-docstring summary: The ID of the conversation context associated with this task.

<!-- declaration:agent_execution/context.py:140:RequestContext.configuration -->
### `RequestContext.configuration` — line 140

```python
def configuration(self) -> SendMessageConfiguration | None
```

Source: [RequestContext.configuration](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:140).

Source-docstring summary: The `SendMessageConfiguration` from the request, if available.

<!-- declaration:agent_execution/context.py:145:RequestContext.call_context -->
### `RequestContext.call_context` — line 145

```python
def call_context(self) -> ServerCallContext
```

Source: [RequestContext.call_context](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:145).

Source-docstring summary: The server call context associated with this request.

<!-- declaration:agent_execution/context.py:150:RequestContext.metadata -->
### `RequestContext.metadata` — line 150

```python
def metadata(self) -> dict[str, Any]
```

Source: [RequestContext.metadata](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:150).

Source-docstring summary: Metadata associated with the request, if available.

<!-- declaration:agent_execution/context.py:159:RequestContext.tenant -->
### `RequestContext.tenant` — line 159

```python
def tenant(self) -> str
```

Source: [RequestContext.tenant](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:159).

Source-docstring summary: The tenant associated with this request.

<!-- declaration:agent_execution/context.py:164:RequestContext.requested_extensions -->
### `RequestContext.requested_extensions` — line 164

```python
def requested_extensions(self) -> set[str]
```

Source: [RequestContext.requested_extensions](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:164).

Source-docstring summary: Extensions that the client requested for this interaction.

<!-- declaration:agent_execution/context.py:168:RequestContext._check_or_generate_task_id -->
### `RequestContext._check_or_generate_task_id` — line 168

```python
def _check_or_generate_task_id(self) -> None
```

Source: [RequestContext._check_or_generate_task_id](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:168).

Source-docstring summary: Ensures a task ID is present, generating one if necessary.

<!-- declaration:agent_execution/context.py:180:RequestContext._check_or_generate_context_id -->
### `RequestContext._check_or_generate_context_id` — line 180

```python
def _check_or_generate_context_id(self) -> None
```

Source: [RequestContext._check_or_generate_context_id](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/context.py:180).

Source-docstring summary: Ensures a context ID is present, generating one if necessary.

## `agent_execution/request_context_builder.py`

Behavior: [agent_execution_knowledge.md](agent_execution_knowledge.md). Source: [agent_execution/request_context_builder.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/request_context_builder.py).

<!-- declaration:agent_execution/request_context_builder.py:8:RequestContextBuilder -->
### `RequestContextBuilder` — line 8

```python
class RequestContextBuilder(ABC)
```

Source: [RequestContextBuilder](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/request_context_builder.py:8).

Source-docstring summary: Builds request context to be supplied to agent executor.

<!-- declaration:agent_execution/request_context_builder.py:12:RequestContextBuilder.build -->
### `RequestContextBuilder.build` — line 12

```python
async def build(self, context: ServerCallContext, params: SendMessageRequest | None=None, task_id: str | None=None, context_id: str | None=None, task: Task | None=None) -> RequestContext
```

Source: [RequestContextBuilder.build](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/request_context_builder.py:12).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

## `agent_execution/simple_request_context_builder.py`

Behavior: [agent_execution_knowledge.md](agent_execution_knowledge.md). Source: [agent_execution/simple_request_context_builder.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/simple_request_context_builder.py).

<!-- declaration:agent_execution/simple_request_context_builder.py:10:SimpleRequestContextBuilder -->
### `SimpleRequestContextBuilder` — line 10

```python
class SimpleRequestContextBuilder(RequestContextBuilder)
```

Source: [SimpleRequestContextBuilder](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/simple_request_context_builder.py:10).

Source-docstring summary: Builds request context and populates referred tasks.

<!-- declaration:agent_execution/simple_request_context_builder.py:13:SimpleRequestContextBuilder.__init__ -->
### `SimpleRequestContextBuilder.__init__` — line 13

```python
def __init__(self, should_populate_referred_tasks: bool=False, task_store: TaskStore | None=None, task_id_generator: IDGenerator | None=None, context_id_generator: IDGenerator | None=None) -> None
```

Source: [SimpleRequestContextBuilder.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/simple_request_context_builder.py:13).

Source-docstring summary: Initializes the SimpleRequestContextBuilder.

<!-- declaration:agent_execution/simple_request_context_builder.py:36:SimpleRequestContextBuilder.build -->
### `SimpleRequestContextBuilder.build` — line 36

```python
async def build(self, context: ServerCallContext, params: SendMessageRequest | None=None, task_id: str | None=None, context_id: str | None=None, task: Task | None=None) -> RequestContext
```

Source: [SimpleRequestContextBuilder.build](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/agent_execution/simple_request_context_builder.py:36).

Source-docstring summary: Builds the request context for an agent execution.

## `context.py`

Behavior: [context_knowledge.md](context_knowledge.md). Source: [context.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/context.py).

<!-- declaration:context.py:14:ServerCallContext -->
### `ServerCallContext` — line 14

```python
class ServerCallContext(BaseModel)
```

Source: [ServerCallContext](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/context.py:14).

Source-docstring summary: A context passed when calling a server method.

## `events/__init__.py`

Behavior: [events_knowledge.md](events_knowledge.md). Source: [events/__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/__init__.py).

No declared classes/functions/methods. Import and export behavior is documented in the linked guide.

## `events/event_consumer.py`

Behavior: [events_knowledge.md](events_knowledge.md). Source: [events/event_consumer.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_consumer.py).

<!-- declaration:events/event_consumer.py:22:EventConsumer -->
### `EventConsumer` — line 22

```python
class EventConsumer()
```

Source: [EventConsumer](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_consumer.py:22).

Source-docstring summary: Consumer to read events from the agent event queue.

<!-- declaration:events/event_consumer.py:25:EventConsumer.__init__ -->
### `EventConsumer.__init__` — line 25

```python
def __init__(self, queue: EventQueueLegacy)
```

Source: [EventConsumer.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_consumer.py:25).

Source-docstring summary: Initializes the EventConsumer.

<!-- declaration:events/event_consumer.py:36:EventConsumer.consume_all -->
### `EventConsumer.consume_all` — line 36

```python
async def consume_all(self) -> AsyncGenerator[Event]
```

Source: [EventConsumer.consume_all](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_consumer.py:36).

Source-docstring summary: Consume all the generated streaming events from the agent.

<!-- declaration:events/event_consumer.py:112:EventConsumer.agent_task_callback -->
### `EventConsumer.agent_task_callback` — line 112

```python
def agent_task_callback(self, agent_task: asyncio.Task[None]) -> None
```

Source: [EventConsumer.agent_task_callback](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_consumer.py:112).

Source-docstring summary: Callback to handle exceptions from the agent's execution task.

## `events/event_queue.py`

Behavior: [events_knowledge.md](events_knowledge.md). Source: [events/event_queue.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py).

<!-- declaration:events/event_queue.py:34:EventQueue -->
### `EventQueue` — line 34

```python
class EventQueue(ABC)
```

Source: [EventQueue](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:34).

Source-docstring summary: Producer-side interface passed to `AgentExecutor.execute`/`cancel`.

<!-- declaration:events/event_queue.py:46:EventQueue.__new__ -->
### `EventQueue.__new__` — line 46

```python
def __new__(cls, *args: Any, **kwargs: Any) -> Self
```

Source: [EventQueue.__new__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:46).

Source-docstring summary: Deprecated: redirects bare `EventQueue(...)` to `EventQueueLegacy(...)`.

<!-- declaration:events/event_queue.py:63:EventQueue.enqueue_event -->
### `EventQueue.enqueue_event` — line 63

```python
async def enqueue_event(self, event: Event) -> None
```

Source: [EventQueue.enqueue_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:63).

Source-docstring summary: Pushes an event into the queue.

<!-- declaration:events/event_queue.py:71:EventQueueLegacy -->
### `EventQueueLegacy` — line 71

```python
class EventQueueLegacy(EventQueue)
```

Source: [EventQueueLegacy](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:71).

Source-docstring summary: Event queue for A2A responses from agent.

<!-- declaration:events/event_queue.py:79:EventQueueLegacy.__init__ -->
### `EventQueueLegacy.__init__` — line 79

```python
def __init__(self, max_queue_size: int=DEFAULT_MAX_QUEUE_SIZE) -> None
```

Source: [EventQueueLegacy.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:79).

Source-docstring summary: Initializes the EventQueue.

<!-- declaration:events/event_queue.py:96:EventQueueLegacy.queue -->
### `EventQueueLegacy.queue` — line 96

```python
def queue(self) -> AsyncQueue[Event]
```

Source: [EventQueueLegacy.queue](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:96).

Source-docstring summary: [DEPRECATED] Returns the underlying asyncio.Queue.

<!-- declaration:events/event_queue.py:100:EventQueueLegacy.__aenter__ -->
### `EventQueueLegacy.__aenter__` — line 100

```python
async def __aenter__(self) -> Self
```

Source: [EventQueueLegacy.__aenter__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:100).

Source-docstring summary: Enters the async context manager, returning the queue itself.

<!-- declaration:events/event_queue.py:104:EventQueueLegacy.__aexit__ -->
### `EventQueueLegacy.__aexit__` — line 104

```python
async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None
```

Source: [EventQueueLegacy.__aexit__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:104).

Source-docstring summary: Exits the async context manager, ensuring close() is called.

<!-- declaration:events/event_queue.py:113:EventQueueLegacy.enqueue_event -->
### `EventQueueLegacy.enqueue_event` — line 113

```python
async def enqueue_event(self, event: Event) -> None
```

Source: [EventQueueLegacy.enqueue_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:113).

Source-docstring summary: Enqueues an event to this queue and all its children.

<!-- declaration:events/event_queue.py:135:EventQueueLegacy.dequeue_event -->
### `EventQueueLegacy.dequeue_event` — line 135

```python
async def dequeue_event(self) -> Event
```

Source: [EventQueueLegacy.dequeue_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:135).

Source-docstring summary: Dequeues an event from the queue.

<!-- declaration:events/event_queue.py:166:EventQueueLegacy.task_done -->
### `EventQueueLegacy.task_done` — line 166

```python
def task_done(self) -> None
```

Source: [EventQueueLegacy.task_done](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:166).

Source-docstring summary: Signals that a formerly enqueued task is complete.

<!-- declaration:events/event_queue.py:174:EventQueueLegacy.tap -->
### `EventQueueLegacy.tap` — line 174

```python
async def tap(self, max_queue_size: int=DEFAULT_MAX_QUEUE_SIZE) -> 'EventQueueLegacy'
```

Source: [EventQueueLegacy.tap](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:174).

Source-docstring summary: Taps the event queue to create a new child queue that receives future events.

<!-- declaration:events/event_queue.py:188:EventQueueLegacy.close -->
### `EventQueueLegacy.close` — line 188

```python
async def close(self, immediate: bool=False) -> None
```

Source: [EventQueueLegacy.close](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:188).

Source-docstring summary: Closes the queue for future push events and also closes all child queues.

<!-- declaration:events/event_queue.py:212:EventQueueLegacy.is_closed -->
### `EventQueueLegacy.is_closed` — line 212

```python
def is_closed(self) -> bool
```

Source: [EventQueueLegacy.is_closed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue.py:212).

Source-docstring summary: Checks if the queue is closed.

## `events/event_queue_v2.py`

Behavior: [events_knowledge.md](events_knowledge.md). Source: [events/event_queue_v2.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py).

<!-- declaration:events/event_queue_v2.py:24:EventQueueSource -->
### `EventQueueSource` — line 24

```python
class EventQueueSource(EventQueue)
```

Source: [EventQueueSource](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:24).

Source-docstring summary: The Parent EventQueue.

<!-- declaration:events/event_queue_v2.py:31:EventQueueSource.__init__ -->
### `EventQueueSource.__init__` — line 31

```python
def __init__(self, max_queue_size: int=DEFAULT_MAX_QUEUE_SIZE, create_default_sink: bool=True) -> None
```

Source: [EventQueueSource.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:31).

Source-docstring summary: Initializes the EventQueueSource.

<!-- declaration:events/event_queue_v2.py:64:EventQueueSource.queue -->
### `EventQueueSource.queue` — line 64

```python
def queue(self) -> AsyncQueue[Event]
```

Source: [EventQueueSource.queue](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:64).

Source-docstring summary: Returns the underlying asyncio.Queue of the default sink.

<!-- declaration:events/event_queue_v2.py:70:EventQueueSource._deliver_to_sink -->
### `EventQueueSource._deliver_to_sink` — line 70

```python
async def _deliver_to_sink(self, sink: 'EventQueueSink', event: Event) -> None
```

Source: [EventQueueSource._deliver_to_sink](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:70).

Source-docstring summary: Puts one event into one sink, evicting an evict-on-full sink if full.

<!-- declaration:events/event_queue_v2.py:114:EventQueueSource._dispatch_loop -->
### `EventQueueSource._dispatch_loop` — line 114

```python
async def _dispatch_loop(self) -> None
```

Source: [EventQueueSource._dispatch_loop](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:114).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:events/event_queue_v2.py:169:EventQueueSource._join_incoming_queue -->
### `EventQueueSource._join_incoming_queue` — line 169

```python
async def _join_incoming_queue(self) -> None
```

Source: [EventQueueSource._join_incoming_queue](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:169).

Source-docstring summary: Helper to wait for join() while monitoring the dispatcher task.

<!-- declaration:events/event_queue_v2.py:210:EventQueueSource.tap -->
### `EventQueueSource.tap` — line 210

```python
async def tap(self, max_queue_size: int=DEFAULT_MAX_QUEUE_SIZE, evict_on_full: bool=False) -> 'EventQueueSink'
```

Source: [EventQueueSource.tap](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:210).

Source-docstring summary: Taps the event queue to create a new child queue that receives future events.

<!-- declaration:events/event_queue_v2.py:243:EventQueueSource.remove_sink -->
### `EventQueueSource.remove_sink` — line 243

```python
async def remove_sink(self, sink: 'EventQueueSink') -> None
```

Source: [EventQueueSource.remove_sink](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:243).

Source-docstring summary: Removes a sink from the source's internal list if present.

<!-- declaration:events/event_queue_v2.py:248:EventQueueSource.enqueue_event -->
### `EventQueueSource.enqueue_event` — line 248

```python
async def enqueue_event(self, event: Event) -> None
```

Source: [EventQueueSource.enqueue_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:248).

Source-docstring summary: Enqueues an event to this queue and all its children.

<!-- declaration:events/event_queue_v2.py:257:EventQueueSource.dequeue_event -->
### `EventQueueSource.dequeue_event` — line 257

```python
async def dequeue_event(self) -> Event
```

Source: [EventQueueSource.dequeue_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:257).

Source-docstring summary: Pulls an event from the default internal sink queue.

<!-- declaration:events/event_queue_v2.py:263:EventQueueSource.task_done -->
### `EventQueueSource.task_done` — line 263

```python
def task_done(self) -> None
```

Source: [EventQueueSource.task_done](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:263).

Source-docstring summary: Signals that a work on dequeued event is complete via the default internal sink queue.

<!-- declaration:events/event_queue_v2.py:269:EventQueueSource.close -->
### `EventQueueSource.close` — line 269

```python
async def close(self, immediate: bool=False) -> None
```

Source: [EventQueueSource.close](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:269).

Source-docstring summary: Closes the queue and all its child sinks.

<!-- declaration:events/event_queue_v2.py:319:EventQueueSource.is_closed -->
### `EventQueueSource.is_closed` — line 319

```python
def is_closed(self) -> bool
```

Source: [EventQueueSource.is_closed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:319).

Source-docstring summary: [DEPRECATED] Checks if the queue is closed.

<!-- declaration:events/event_queue_v2.py:328:EventQueueSource.test_only_join_incoming_queue -->
### `EventQueueSource.test_only_join_incoming_queue` — line 328

```python
async def test_only_join_incoming_queue(self) -> None
```

Source: [EventQueueSource.test_only_join_incoming_queue](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:328).

Source-docstring summary: Wait for incoming queue to be fully processed.

<!-- declaration:events/event_queue_v2.py:332:EventQueueSource.__aenter__ -->
### `EventQueueSource.__aenter__` — line 332

```python
async def __aenter__(self) -> Self
```

Source: [EventQueueSource.__aenter__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:332).

Source-docstring summary: Enters the async context manager, returning the queue itself.

<!-- declaration:events/event_queue_v2.py:340:EventQueueSource.__aexit__ -->
### `EventQueueSource.__aexit__` — line 340

```python
async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None
```

Source: [EventQueueSource.__aexit__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:340).

Source-docstring summary: Exits the async context manager, ensuring close() is called.

<!-- declaration:events/event_queue_v2.py:356:EventQueueSink -->
### `EventQueueSink` — line 356

```python
class EventQueueSink(EventQueue)
```

Source: [EventQueueSink](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:356).

Source-docstring summary: The Child EventQueue.

<!-- declaration:events/event_queue_v2.py:363:EventQueueSink.__init__ -->
### `EventQueueSink.__init__` — line 363

```python
def __init__(self, parent: EventQueueSource, max_queue_size: int=DEFAULT_MAX_QUEUE_SIZE, evict_on_full: bool=False) -> None
```

Source: [EventQueueSink.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:363).

Source-docstring summary: Initializes the EventQueueSink.

<!-- declaration:events/event_queue_v2.py:391:EventQueueSink.queue -->
### `EventQueueSink.queue` — line 391

```python
def queue(self) -> AsyncQueue[Event]
```

Source: [EventQueueSink.queue](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:391).

Source-docstring summary: Returns the underlying asyncio.Queue of this sink.

<!-- declaration:events/event_queue_v2.py:395:EventQueueSink._put_internal -->
### `EventQueueSink._put_internal` — line 395

```python
async def _put_internal(self, event: Event) -> None
```

Source: [EventQueueSink._put_internal](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:395).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:events/event_queue_v2.py:399:EventQueueSink.enqueue_event -->
### `EventQueueSink.enqueue_event` — line 399

```python
async def enqueue_event(self, event: Event) -> None
```

Source: [EventQueueSink.enqueue_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:399).

Source-docstring summary: Sinks are read-only and cannot have events directly enqueued to them.

<!-- declaration:events/event_queue_v2.py:403:EventQueueSink.dequeue_event -->
### `EventQueueSink.dequeue_event` — line 403

```python
async def dequeue_event(self) -> Event
```

Source: [EventQueueSink.dequeue_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:403).

Source-docstring summary: Pulls an event from the sink queue.

<!-- declaration:events/event_queue_v2.py:410:EventQueueSink.task_done -->
### `EventQueueSink.task_done` — line 410

```python
def task_done(self) -> None
```

Source: [EventQueueSink.task_done](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:410).

Source-docstring summary: Signals that a work on dequeued event is complete in this sink queue.

<!-- declaration:events/event_queue_v2.py:415:EventQueueSink.tap -->
### `EventQueueSink.tap` — line 415

```python
async def tap(self, max_queue_size: int=DEFAULT_MAX_QUEUE_SIZE, evict_on_full: bool=False) -> 'EventQueueSink'
```

Source: [EventQueueSink.tap](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:415).

Source-docstring summary: Creates a child queue that receives future events.

<!-- declaration:events/event_queue_v2.py:430:EventQueueSink.close -->
### `EventQueueSink.close` — line 430

```python
async def close(self, immediate: bool=False) -> None
```

Source: [EventQueueSink.close](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:430).

Source-docstring summary: Closes the child sink queue.

<!-- declaration:events/event_queue_v2.py:447:EventQueueSink.is_closed -->
### `EventQueueSink.is_closed` — line 447

```python
def is_closed(self) -> bool
```

Source: [EventQueueSink.is_closed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:447).

Source-docstring summary: [DEPRECATED] Checks if the queue is closed.

<!-- declaration:events/event_queue_v2.py:456:EventQueueSink.__aenter__ -->
### `EventQueueSink.__aenter__` — line 456

```python
async def __aenter__(self) -> Self
```

Source: [EventQueueSink.__aenter__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:456).

Source-docstring summary: Enters the async context manager, returning the queue itself.

<!-- declaration:events/event_queue_v2.py:464:EventQueueSink.__aexit__ -->
### `EventQueueSink.__aexit__` — line 464

```python
async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None
```

Source: [EventQueueSink.__aexit__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/event_queue_v2.py:464).

Source-docstring summary: Exits the async context manager, ensuring close() is called.

## `events/in_memory_queue_manager.py`

Behavior: [events_knowledge.md](events_knowledge.md). Source: [events/in_memory_queue_manager.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py).

<!-- declaration:events/in_memory_queue_manager.py:13:InMemoryQueueManager -->
### `InMemoryQueueManager` — line 13

```python
class InMemoryQueueManager(QueueManager)
```

Source: [InMemoryQueueManager](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py:13).

Source-docstring summary: InMemoryQueueManager is used for a single binary management.

<!-- declaration:events/in_memory_queue_manager.py:24:InMemoryQueueManager.__init__ -->
### `InMemoryQueueManager.__init__` — line 24

```python
def __init__(self) -> None
```

Source: [InMemoryQueueManager.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py:24).

Source-docstring summary: Initializes the InMemoryQueueManager.

<!-- declaration:events/in_memory_queue_manager.py:29:InMemoryQueueManager.add -->
### `InMemoryQueueManager.add` — line 29

```python
async def add(self, task_id: str, queue: EventQueueLegacy) -> None
```

Source: [InMemoryQueueManager.add](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py:29).

Source-docstring summary: Adds a new event queue for a task ID.

<!-- declaration:events/in_memory_queue_manager.py:40:InMemoryQueueManager.get -->
### `InMemoryQueueManager.get` — line 40

```python
async def get(self, task_id: str) -> EventQueueLegacy | None
```

Source: [InMemoryQueueManager.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py:40).

Source-docstring summary: Retrieves the event queue for a task ID.

<!-- declaration:events/in_memory_queue_manager.py:49:InMemoryQueueManager.tap -->
### `InMemoryQueueManager.tap` — line 49

```python
async def tap(self, task_id: str) -> EventQueueLegacy | None
```

Source: [InMemoryQueueManager.tap](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py:49).

Source-docstring summary: Taps the event queue for a task ID to create a child queue.

<!-- declaration:events/in_memory_queue_manager.py:61:InMemoryQueueManager.close -->
### `InMemoryQueueManager.close` — line 61

```python
async def close(self, task_id: str) -> None
```

Source: [InMemoryQueueManager.close](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py:61).

Source-docstring summary: Closes and removes the event queue for a task ID.

<!-- declaration:events/in_memory_queue_manager.py:73:InMemoryQueueManager.create_or_tap -->
### `InMemoryQueueManager.create_or_tap` — line 73

```python
async def create_or_tap(self, task_id: str) -> EventQueueLegacy
```

Source: [InMemoryQueueManager.create_or_tap](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/in_memory_queue_manager.py:73).

Source-docstring summary: Creates a new event queue for a task ID if one doesn't exist, otherwise taps the existing one.

## `events/queue_manager.py`

Behavior: [events_knowledge.md](events_knowledge.md). Source: [events/queue_manager.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py).

<!-- declaration:events/queue_manager.py:6:QueueManager -->
### `QueueManager` — line 6

```python
class QueueManager(ABC)
```

Source: [QueueManager](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:6).

Source-docstring summary: Interface for managing the event queue lifecycles per task.

<!-- declaration:events/queue_manager.py:10:QueueManager.add -->
### `QueueManager.add` — line 10

```python
async def add(self, task_id: str, queue: EventQueueLegacy) -> None
```

Source: [QueueManager.add](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:10).

Source-docstring summary: Adds a new event queue associated with a task ID.

<!-- declaration:events/queue_manager.py:14:QueueManager.get -->
### `QueueManager.get` — line 14

```python
async def get(self, task_id: str) -> EventQueueLegacy | None
```

Source: [QueueManager.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:14).

Source-docstring summary: Retrieves the event queue for a task ID.

<!-- declaration:events/queue_manager.py:18:QueueManager.tap -->
### `QueueManager.tap` — line 18

```python
async def tap(self, task_id: str) -> EventQueueLegacy | None
```

Source: [QueueManager.tap](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:18).

Source-docstring summary: Creates a child event queue (tap) for an existing task ID.

<!-- declaration:events/queue_manager.py:22:QueueManager.close -->
### `QueueManager.close` — line 22

```python
async def close(self, task_id: str) -> None
```

Source: [QueueManager.close](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:22).

Source-docstring summary: Closes and removes the event queue for a task ID.

<!-- declaration:events/queue_manager.py:26:QueueManager.create_or_tap -->
### `QueueManager.create_or_tap` — line 26

```python
async def create_or_tap(self, task_id: str) -> EventQueueLegacy
```

Source: [QueueManager.create_or_tap](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:26).

Source-docstring summary: Creates a queue if one doesn't exist, otherwise taps the existing one.

<!-- declaration:events/queue_manager.py:30:TaskQueueExists -->
### `TaskQueueExists` — line 30

```python
class TaskQueueExists(Exception)
```

Source: [TaskQueueExists](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:30).

Source-docstring summary: Exception raised when attempting to add a queue for a task ID that already exists.

<!-- declaration:events/queue_manager.py:34:NoTaskQueue -->
### `NoTaskQueue` — line 34

```python
class NoTaskQueue(Exception)
```

Source: [NoTaskQueue](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/events/queue_manager.py:34).

Source-docstring summary: Exception raised when attempting to access or close a queue for a task ID that does not exist.

## `id_generator.py`

Behavior: [id_generator_knowledge.md](id_generator_knowledge.md). Source: [id_generator.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/id_generator.py).

<!-- declaration:id_generator.py:8:IDGeneratorContext -->
### `IDGeneratorContext` — line 8

```python
class IDGeneratorContext(BaseModel)
```

Source: [IDGeneratorContext](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/id_generator.py:8).

Source-docstring summary: Context for providing additional information to ID generators.

<!-- declaration:id_generator.py:15:IDGenerator -->
### `IDGenerator` — line 15

```python
class IDGenerator(ABC)
```

Source: [IDGenerator](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/id_generator.py:15).

Source-docstring summary: Interface for generating unique identifiers.

<!-- declaration:id_generator.py:19:IDGenerator.generate -->
### `IDGenerator.generate` — line 19

```python
def generate(self, context: IDGeneratorContext) -> str
```

Source: [IDGenerator.generate](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/id_generator.py:19).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:id_generator.py:23:UUIDGenerator -->
### `UUIDGenerator` — line 23

```python
class UUIDGenerator(IDGenerator)
```

Source: [UUIDGenerator](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/id_generator.py:23).

Source-docstring summary: UUID implementation of the IDGenerator interface.

<!-- declaration:id_generator.py:26:UUIDGenerator.generate -->
### `UUIDGenerator.generate` — line 26

```python
def generate(self, context: IDGeneratorContext) -> str
```

Source: [UUIDGenerator.generate](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/id_generator.py:26).

Source-docstring summary: Generates a random UUID, ignoring the context.

## `jsonrpc_models.py`

Behavior: [jsonrpc_models_knowledge.md](jsonrpc_models_knowledge.md). Source: [jsonrpc_models.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py).

<!-- declaration:jsonrpc_models.py:6:JSONRPCBaseModel -->
### `JSONRPCBaseModel` — line 6

```python
class JSONRPCBaseModel(BaseModel)
```

Source: [JSONRPCBaseModel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py:6).

Source-docstring summary: Base model for JSON-RPC objects.

<!-- declaration:jsonrpc_models.py:16:JSONRPCError -->
### `JSONRPCError` — line 16

```python
class JSONRPCError(JSONRPCBaseModel)
```

Source: [JSONRPCError](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py:16).

Source-docstring summary: Base model for JSON-RPC error objects.

<!-- declaration:jsonrpc_models.py:24:JSONParseError -->
### `JSONParseError` — line 24

```python
class JSONParseError(JSONRPCError)
```

Source: [JSONParseError](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py:24).

Source-docstring summary: Error raised when invalid JSON was received by the server.

<!-- declaration:jsonrpc_models.py:31:InvalidRequestError -->
### `InvalidRequestError` — line 31

```python
class InvalidRequestError(JSONRPCError)
```

Source: [InvalidRequestError](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py:31).

Source-docstring summary: Error raised when the JSON sent is not a valid Request object.

<!-- declaration:jsonrpc_models.py:38:MethodNotFoundError -->
### `MethodNotFoundError` — line 38

```python
class MethodNotFoundError(JSONRPCError)
```

Source: [MethodNotFoundError](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py:38).

Source-docstring summary: Error raised when the method does not exist / is not available.

<!-- declaration:jsonrpc_models.py:45:InvalidParamsError -->
### `InvalidParamsError` — line 45

```python
class InvalidParamsError(JSONRPCError)
```

Source: [InvalidParamsError](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py:45).

Source-docstring summary: Error raised when invalid method parameter(s).

<!-- declaration:jsonrpc_models.py:52:InternalError -->
### `InternalError` — line 52

```python
class InternalError(JSONRPCError)
```

Source: [InternalError](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/jsonrpc_models.py:52).

Source-docstring summary: Error raised when internal JSON-RPC error.

## `models.py`

Behavior: [models_knowledge.md](models_knowledge.md). Source: [models.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py).

<!-- declaration:models.py:9:override -->
### `override` — line 9

```python
def override(func)
```

Source: [override](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:9).

Source-docstring summary: Override decorator.

<!-- declaration:models.py:37:Base -->
### `Base` — line 37

```python
class Base(DeclarativeBase)
```

Source: [Base](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:37).

Source-docstring summary: Base class for declarative models in A2A SDK.

<!-- declaration:models.py:42:TaskMixin -->
### `TaskMixin` — line 42

```python
class TaskMixin()
```

Source: [TaskMixin](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:42).

Source-docstring summary: Mixin providing standard task columns with proper type handling.

<!-- declaration:models.py:66:TaskMixin.task_metadata -->
### `TaskMixin.task_metadata` — line 66

```python
def task_metadata(cls) -> Mapped[dict[str, Any] | None]
```

Source: [TaskMixin.task_metadata](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:66).

Source-docstring summary: Define the 'metadata' column, avoiding name conflicts with Pydantic.

<!-- declaration:models.py:71:TaskMixin.__repr__ -->
### `TaskMixin.__repr__` — line 71

```python
def __repr__(self) -> str
```

Source: [TaskMixin.__repr__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:71).

Source-docstring summary: Return a string representation of the task.

<!-- declaration:models.py:80:TaskMixin.__table_args__ -->
### `TaskMixin.__table_args__` — line 80

```python
def __table_args__(cls) -> tuple[Any, ...]
```

Source: [TaskMixin.__table_args__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:80).

Source-docstring summary: Define a composite index (owner, last_updated) for each table that uses the mixin.

<!-- declaration:models.py:90:create_task_model -->
### `create_task_model` — line 90

```python
def create_task_model(table_name: str='tasks', base: type[DeclarativeBase]=Base) -> type
```

Source: [create_task_model](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:90).

Source-docstring summary: Create a TaskModel class with a configurable table name.

<!-- declaration:models.py:117:create_task_model.TaskModel -->
### `create_task_model.TaskModel` — line 117

```python
class TaskModel(TaskMixin, base)
```

Source: [create_task_model.TaskModel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:117).

Source-docstring summary: No class docstring; role and value/constructor semantics are covered in the linked behavioral guide.

<!-- declaration:models.py:121:create_task_model.TaskModel.__repr__ -->
### `create_task_model.TaskModel.__repr__` — line 121

```python
def __repr__(self) -> str
```

Source: [create_task_model.TaskModel.__repr__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:121).

Source-docstring summary: Return a string representation of the task.

<!-- declaration:models.py:136:TaskModel -->
### `TaskModel` — line 136

```python
class TaskModel(TaskMixin, Base)
```

Source: [TaskModel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:136).

Source-docstring summary: Default task model with standard table name.

<!-- declaration:models.py:143:PushNotificationConfigMixin -->
### `PushNotificationConfigMixin` — line 143

```python
class PushNotificationConfigMixin()
```

Source: [PushNotificationConfigMixin](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:143).

Source-docstring summary: Mixin providing standard push notification config columns.

<!-- declaration:models.py:155:PushNotificationConfigMixin.__repr__ -->
### `PushNotificationConfigMixin.__repr__` — line 155

```python
def __repr__(self) -> str
```

Source: [PushNotificationConfigMixin.__repr__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:155).

Source-docstring summary: Return a string representation of the push notification config.

<!-- declaration:models.py:163:create_push_notification_config_model -->
### `create_push_notification_config_model` — line 163

```python
def create_push_notification_config_model(table_name: str='push_notification_configs', base: type[DeclarativeBase]=Base) -> type
```

Source: [create_push_notification_config_model](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:163).

Source-docstring summary: Create a PushNotificationConfigModel class with a configurable table name.

<!-- declaration:models.py:169:create_push_notification_config_model.PushNotificationConfigModel -->
### `create_push_notification_config_model.PushNotificationConfigModel` — line 169

```python
class PushNotificationConfigModel(PushNotificationConfigMixin, base)
```

Source: [create_push_notification_config_model.PushNotificationConfigModel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:169).

Source-docstring summary: No class docstring; role and value/constructor semantics are covered in the linked behavioral guide.

<!-- declaration:models.py:173:create_push_notification_config_model.PushNotificationConfigModel.__repr__ -->
### `create_push_notification_config_model.PushNotificationConfigModel.__repr__` — line 173

```python
def __repr__(self) -> str
```

Source: [create_push_notification_config_model.PushNotificationConfigModel.__repr__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:173).

Source-docstring summary: Return a string representation of the push notification config.

<!-- declaration:models.py:191:PushNotificationConfigModel -->
### `PushNotificationConfigModel` — line 191

```python
class PushNotificationConfigModel(PushNotificationConfigMixin, Base)
```

Source: [PushNotificationConfigModel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/models.py:191).

Source-docstring summary: Default push notification config model with standard table name.

## `owner_resolver.py`

Behavior: [owner_resolver_knowledge.md](owner_resolver_knowledge.md). Source: [owner_resolver.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/owner_resolver.py).

<!-- declaration:owner_resolver.py:11:resolve_user_scope -->
### `resolve_user_scope` — line 11

```python
def resolve_user_scope(context: ServerCallContext) -> str
```

Source: [resolve_user_scope](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/owner_resolver.py:11).

Source-docstring summary: Resolves the owner scope based on the user in the context.

## `request_handlers/__init__.py`

Behavior: [request_handlers_knowledge.md](request_handlers_knowledge.md). Source: [request_handlers/__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/__init__.py).

<!-- declaration:request_handlers/__init__.py:36:GrpcHandler -->
### `GrpcHandler` — line 36

```python
class GrpcHandler()
```

Source: [GrpcHandler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/__init__.py:36).

Source-docstring summary: Placeholder for GrpcHandler when dependencies are not installed.

<!-- declaration:request_handlers/__init__.py:39:GrpcHandler.__init__ -->
### `GrpcHandler.__init__` — line 39

```python
def __init__(self, *args, **kwargs)
```

Source: [GrpcHandler.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/__init__.py:39).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

## `request_handlers/default_request_handler.py`

Behavior: [request_handlers_knowledge.md](request_handlers_knowledge.md). Source: [request_handlers/default_request_handler.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py).

<!-- declaration:request_handlers/default_request_handler.py:81:LegacyRequestHandler -->
### `LegacyRequestHandler` — line 81

```python
class LegacyRequestHandler(RequestHandler)
```

Source: [LegacyRequestHandler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:81).

Source-docstring summary: Default request handler for all incoming requests.

<!-- declaration:request_handlers/default_request_handler.py:92:LegacyRequestHandler.__init__ -->
### `LegacyRequestHandler.__init__` — line 92

```python
def __init__(self, agent_executor: AgentExecutor, task_store: TaskStore, agent_card: AgentCard, queue_manager: QueueManager | None=None, push_config_store: PushNotificationConfigStore | None=None, push_sender: PushNotificationSender | None=None, request_context_builder: RequestContextBuilder | None=None, extended_agent_card: AgentCard | None=None, extended_card_modifier: Callable[[AgentCard, ServerCallContext], Awaitable[AgentCard]] | None=None, push_url_validator: Callable[[str], Awaitable[bool]] | None=None) -> None
```

Source: [LegacyRequestHandler.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:92).

Source-docstring summary: Initializes the DefaultRequestHandler.

<!-- declaration:request_handlers/default_request_handler.py:149:LegacyRequestHandler._reject_unsafe_push_url -->
### `LegacyRequestHandler._reject_unsafe_push_url` — line 149

```python
async def _reject_unsafe_push_url(self, url: str) -> None
```

Source: [LegacyRequestHandler._reject_unsafe_push_url](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:149).

Source-docstring summary: Apply the configured push-URL policy, if any.

<!-- declaration:request_handlers/default_request_handler.py:157:LegacyRequestHandler.on_get_task -->
### `LegacyRequestHandler.on_get_task` — line 157

```python
async def on_get_task(self, params: GetTaskRequest, context: ServerCallContext) -> Task | None
```

Source: [LegacyRequestHandler.on_get_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:157).

Source-docstring summary: Default handler for 'tasks/get'.

<!-- declaration:request_handlers/default_request_handler.py:173:LegacyRequestHandler.on_list_tasks -->
### `LegacyRequestHandler.on_list_tasks` — line 173

```python
async def on_list_tasks(self, params: ListTasksRequest, context: ServerCallContext) -> ListTasksResponse
```

Source: [LegacyRequestHandler.on_list_tasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:173).

Source-docstring summary: Default handler for 'tasks/list'.

<!-- declaration:request_handlers/default_request_handler.py:195:LegacyRequestHandler.on_cancel_task -->
### `LegacyRequestHandler.on_cancel_task` — line 195

```python
async def on_cancel_task(self, params: CancelTaskRequest, context: ServerCallContext) -> Task | None
```

Source: [LegacyRequestHandler.on_cancel_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:195).

Source-docstring summary: Default handler for 'tasks/cancel'.

<!-- declaration:request_handlers/default_request_handler.py:256:LegacyRequestHandler._run_event_stream -->
### `LegacyRequestHandler._run_event_stream` — line 256

```python
async def _run_event_stream(self, request: RequestContext, queue: EventQueueLegacy) -> None
```

Source: [LegacyRequestHandler._run_event_stream](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:256).

Source-docstring summary: Runs the agent's `execute` method and closes the queue afterwards.

<!-- declaration:request_handlers/default_request_handler.py:268:LegacyRequestHandler._setup_message_execution -->
### `LegacyRequestHandler._setup_message_execution` — line 268

```python
async def _setup_message_execution(self, params: SendMessageRequest, context: ServerCallContext) -> tuple[TaskManager, str, EventQueueLegacy, ResultAggregator, asyncio.Task]
```

Source: [LegacyRequestHandler._setup_message_execution](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:268).

Source-docstring summary: Common setup logic for both streaming and non-streaming message handling.

<!-- declaration:request_handlers/default_request_handler.py:341:LegacyRequestHandler._validate_task_id_match -->
### `LegacyRequestHandler._validate_task_id_match` — line 341

```python
def _validate_task_id_match(self, task_id: str, event_task_id: str) -> None
```

Source: [LegacyRequestHandler._validate_task_id_match](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:341).

Source-docstring summary: Validates that agent-generated task ID matches the expected task ID.

<!-- declaration:request_handlers/default_request_handler.py:351:LegacyRequestHandler._send_push_notification_if_needed -->
### `LegacyRequestHandler._send_push_notification_if_needed` — line 351

```python
async def _send_push_notification_if_needed(self, task_id: str, event: Event) -> None
```

Source: [LegacyRequestHandler._send_push_notification_if_needed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:351).

Source-docstring summary: Sends push notification if configured.

<!-- declaration:request_handlers/default_request_handler.py:363:LegacyRequestHandler.on_message_send -->
### `LegacyRequestHandler.on_message_send` — line 363

```python
async def on_message_send(self, params: SendMessageRequest, context: ServerCallContext) -> Message | Task
```

Source: [LegacyRequestHandler.on_message_send](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:363).

Source-docstring summary: Default handler for 'message/send' interface (non-streaming).

<!-- declaration:request_handlers/default_request_handler.py:391:LegacyRequestHandler.on_message_send.push_notification_callback -->
### `LegacyRequestHandler.on_message_send.push_notification_callback` — line 391

```python
async def push_notification_callback(event: Event) -> None
```

Source: [LegacyRequestHandler.on_message_send.push_notification_callback](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:391).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler.py:437:LegacyRequestHandler.on_message_send_stream -->
### `LegacyRequestHandler.on_message_send_stream` — line 437

```python
async def on_message_send_stream(self, params: SendMessageRequest, context: ServerCallContext) -> AsyncGenerator[Event]
```

Source: [LegacyRequestHandler.on_message_send_stream](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:437).

Source-docstring summary: Default handler for 'message/stream' (streaming).

<!-- declaration:request_handlers/default_request_handler.py:479:LegacyRequestHandler._register_producer -->
### `LegacyRequestHandler._register_producer` — line 479

```python
async def _register_producer(self, task_id: str, producer_task: asyncio.Task) -> None
```

Source: [LegacyRequestHandler._register_producer](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:479).

Source-docstring summary: Registers the agent execution task with the handler.

<!-- declaration:request_handlers/default_request_handler.py:486:LegacyRequestHandler._track_background_task -->
### `LegacyRequestHandler._track_background_task` — line 486

```python
def _track_background_task(self, task: asyncio.Task) -> None
```

Source: [LegacyRequestHandler._track_background_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:486).

Source-docstring summary: Tracks a background task and logs exceptions on completion.

<!-- declaration:request_handlers/default_request_handler.py:494:LegacyRequestHandler._track_background_task._on_done -->
### `LegacyRequestHandler._track_background_task._on_done` — line 494

```python
def _on_done(completed: asyncio.Task) -> None
```

Source: [LegacyRequestHandler._track_background_task._on_done](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:494).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler.py:509:LegacyRequestHandler._cleanup_producer -->
### `LegacyRequestHandler._cleanup_producer` — line 509

```python
async def _cleanup_producer(self, producer_task: asyncio.Task, task_id: str) -> None
```

Source: [LegacyRequestHandler._cleanup_producer](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:509).

Source-docstring summary: Cleans up the agent execution task and queue manager entry.

<!-- declaration:request_handlers/default_request_handler.py:531:LegacyRequestHandler.on_create_task_push_notification_config -->
### `LegacyRequestHandler.on_create_task_push_notification_config` — line 531

```python
async def on_create_task_push_notification_config(self, params: TaskPushNotificationConfig, context: ServerCallContext) -> TaskPushNotificationConfig
```

Source: [LegacyRequestHandler.on_create_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:531).

Source-docstring summary: Default handler for 'tasks/pushNotificationConfig/create'.

<!-- declaration:request_handlers/default_request_handler.py:564:LegacyRequestHandler.on_get_task_push_notification_config -->
### `LegacyRequestHandler.on_get_task_push_notification_config` — line 564

```python
async def on_get_task_push_notification_config(self, params: GetTaskPushNotificationConfigRequest, context: ServerCallContext) -> TaskPushNotificationConfig
```

Source: [LegacyRequestHandler.on_get_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:564).

Source-docstring summary: Default handler for 'tasks/pushNotificationConfig/get'.

<!-- declaration:request_handlers/default_request_handler.py:597:LegacyRequestHandler.on_subscribe_to_task -->
### `LegacyRequestHandler.on_subscribe_to_task` — line 597

```python
async def on_subscribe_to_task(self, params: SubscribeToTaskRequest, context: ServerCallContext) -> AsyncGenerator[Event, None]
```

Source: [LegacyRequestHandler.on_subscribe_to_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:597).

Source-docstring summary: Default handler for 'SubscribeToTask'.

<!-- declaration:request_handlers/default_request_handler.py:645:LegacyRequestHandler.on_list_task_push_notification_configs -->
### `LegacyRequestHandler.on_list_task_push_notification_configs` — line 645

```python
async def on_list_task_push_notification_configs(self, params: ListTaskPushNotificationConfigsRequest, context: ServerCallContext) -> ListTaskPushNotificationConfigsResponse
```

Source: [LegacyRequestHandler.on_list_task_push_notification_configs](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:645).

Source-docstring summary: Default handler for 'ListTaskPushNotificationConfigs'.

<!-- declaration:request_handlers/default_request_handler.py:676:LegacyRequestHandler.on_delete_task_push_notification_config -->
### `LegacyRequestHandler.on_delete_task_push_notification_config` — line 676

```python
async def on_delete_task_push_notification_config(self, params: DeleteTaskPushNotificationConfigRequest, context: ServerCallContext) -> None
```

Source: [LegacyRequestHandler.on_delete_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:676).

Source-docstring summary: Default handler for 'tasks/pushNotificationConfig/delete'.

<!-- declaration:request_handlers/default_request_handler.py:701:LegacyRequestHandler.on_get_extended_agent_card -->
### `LegacyRequestHandler.on_get_extended_agent_card` — line 701

```python
async def on_get_extended_agent_card(self, params: GetExtendedAgentCardRequest, context: ServerCallContext) -> AgentCard
```

Source: [LegacyRequestHandler.on_get_extended_agent_card](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler.py:701).

Source-docstring summary: Default handler for 'GetExtendedAgentCard'.

## `request_handlers/default_request_handler_v2.py`

Behavior: [request_handlers_knowledge.md](request_handlers_knowledge.md). Source: [request_handlers/default_request_handler_v2.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py).

<!-- declaration:request_handlers/default_request_handler_v2.py:76:DefaultRequestHandlerV2 -->
### `DefaultRequestHandlerV2` — line 76

```python
class DefaultRequestHandlerV2(RequestHandler)
```

Source: [DefaultRequestHandlerV2](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:76).

Source-docstring summary: Default request handler for all incoming requests.

<!-- declaration:request_handlers/default_request_handler_v2.py:87:DefaultRequestHandlerV2.__init__ -->
### `DefaultRequestHandlerV2.__init__` — line 87

```python
def __init__(self, agent_executor: AgentExecutor, task_store: TaskStore, agent_card: AgentCard, queue_manager: Any | None=None, push_config_store: PushNotificationConfigStore | None=None, push_sender: PushNotificationSender | None=None, request_context_builder: RequestContextBuilder | None=None, extended_agent_card: AgentCard | None=None, extended_card_modifier: Callable[[AgentCard, ServerCallContext], Awaitable[AgentCard]] | None=None, push_url_validator: Callable[[str], Awaitable[bool]] | None=None) -> None
```

Source: [DefaultRequestHandlerV2.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:87).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:request_handlers/default_request_handler_v2.py:136:DefaultRequestHandlerV2._reject_unsafe_push_url -->
### `DefaultRequestHandlerV2._reject_unsafe_push_url` — line 136

```python
async def _reject_unsafe_push_url(self, url: str) -> None
```

Source: [DefaultRequestHandlerV2._reject_unsafe_push_url](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:136).

Source-docstring summary: Apply the configured push-URL policy, if any.

<!-- declaration:request_handlers/default_request_handler_v2.py:143:DefaultRequestHandlerV2.aclose -->
### `DefaultRequestHandlerV2.aclose` — line 143

```python
async def aclose(self) -> None
```

Source: [DefaultRequestHandlerV2.aclose](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:143).

Source-docstring summary: Shuts down the handler, draining all active tasks.

<!-- declaration:request_handlers/default_request_handler_v2.py:153:DefaultRequestHandlerV2.on_get_task -->
### `DefaultRequestHandlerV2.on_get_task` — line 153

```python
async def on_get_task(self, params: GetTaskRequest, context: ServerCallContext) -> Task | None
```

Source: [DefaultRequestHandlerV2.on_get_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:153).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:168:DefaultRequestHandlerV2.on_list_tasks -->
### `DefaultRequestHandlerV2.on_list_tasks` — line 168

```python
async def on_list_tasks(self, params: ListTasksRequest, context: ServerCallContext) -> ListTasksResponse
```

Source: [DefaultRequestHandlerV2.on_list_tasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:168).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:189:DefaultRequestHandlerV2.on_cancel_task -->
### `DefaultRequestHandlerV2.on_cancel_task` — line 189

```python
async def on_cancel_task(self, params: CancelTaskRequest, context: ServerCallContext) -> Task | None
```

Source: [DefaultRequestHandlerV2.on_cancel_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:189).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:211:DefaultRequestHandlerV2._validate_task_id_match -->
### `DefaultRequestHandlerV2._validate_task_id_match` — line 211

```python
def _validate_task_id_match(self, task_id: str, event_task_id: str) -> None
```

Source: [DefaultRequestHandlerV2._validate_task_id_match](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:211).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:220:DefaultRequestHandlerV2._setup_active_task -->
### `DefaultRequestHandlerV2._setup_active_task` — line 220

```python
async def _setup_active_task(self, params: SendMessageRequest, call_context: ServerCallContext) -> tuple[ActiveTask, RequestContext]
```

Source: [DefaultRequestHandlerV2._setup_active_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:220).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:271:DefaultRequestHandlerV2.on_message_send -->
### `DefaultRequestHandlerV2.on_message_send` — line 271

```python
async def on_message_send(self, params: SendMessageRequest, context: ServerCallContext) -> Message | Task
```

Source: [DefaultRequestHandlerV2.on_message_send](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:271).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:340:DefaultRequestHandlerV2.on_message_send_stream -->
### `DefaultRequestHandlerV2.on_message_send_stream` — line 340

```python
async def on_message_send_stream(self, params: SendMessageRequest, context: ServerCallContext) -> AsyncGenerator[Event, None]
```

Source: [DefaultRequestHandlerV2.on_message_send_stream](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:340).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:373:DefaultRequestHandlerV2.on_create_task_push_notification_config -->
### `DefaultRequestHandlerV2.on_create_task_push_notification_config` — line 373

```python
async def on_create_task_push_notification_config(self, params: TaskPushNotificationConfig, context: ServerCallContext) -> TaskPushNotificationConfig
```

Source: [DefaultRequestHandlerV2.on_create_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:373).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:402:DefaultRequestHandlerV2.on_get_task_push_notification_config -->
### `DefaultRequestHandlerV2.on_get_task_push_notification_config` — line 402

```python
async def on_get_task_push_notification_config(self, params: GetTaskPushNotificationConfigRequest, context: ServerCallContext) -> TaskPushNotificationConfig
```

Source: [DefaultRequestHandlerV2.on_get_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:402).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:431:DefaultRequestHandlerV2.on_subscribe_to_task -->
### `DefaultRequestHandlerV2.on_subscribe_to_task` — line 431

```python
async def on_subscribe_to_task(self, params: SubscribeToTaskRequest, context: ServerCallContext) -> AsyncGenerator[Event, None]
```

Source: [DefaultRequestHandlerV2.on_subscribe_to_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:431).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:453:DefaultRequestHandlerV2.on_list_task_push_notification_configs -->
### `DefaultRequestHandlerV2.on_list_task_push_notification_configs` — line 453

```python
async def on_list_task_push_notification_configs(self, params: ListTaskPushNotificationConfigsRequest, context: ServerCallContext) -> ListTaskPushNotificationConfigsResponse
```

Source: [DefaultRequestHandlerV2.on_list_task_push_notification_configs](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:453).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:480:DefaultRequestHandlerV2.on_delete_task_push_notification_config -->
### `DefaultRequestHandlerV2.on_delete_task_push_notification_config` — line 480

```python
async def on_delete_task_push_notification_config(self, params: DeleteTaskPushNotificationConfigRequest, context: ServerCallContext) -> None
```

Source: [DefaultRequestHandlerV2.on_delete_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:480).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/default_request_handler_v2.py:501:DefaultRequestHandlerV2.on_get_extended_agent_card -->
### `DefaultRequestHandlerV2.on_get_extended_agent_card` — line 501

```python
async def on_get_extended_agent_card(self, params: GetExtendedAgentCardRequest, context: ServerCallContext) -> AgentCard
```

Source: [DefaultRequestHandlerV2.on_get_extended_agent_card](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/default_request_handler_v2.py:501).

Source-docstring summary: Default handler for 'GetExtendedAgentCard'.

## `request_handlers/grpc_handler.py`

Behavior: [request_handlers_knowledge.md](request_handlers_knowledge.md). Source: [request_handlers/grpc_handler.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py).

<!-- declaration:request_handlers/grpc_handler.py:42:GrpcServerCallContextBuilder -->
### `GrpcServerCallContextBuilder` — line 42

```python
class GrpcServerCallContextBuilder(ABC)
```

Source: [GrpcServerCallContextBuilder](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:42).

Source-docstring summary: Interface for building ServerCallContext from gRPC context.

<!-- declaration:request_handlers/grpc_handler.py:46:GrpcServerCallContextBuilder.build -->
### `GrpcServerCallContextBuilder.build` — line 46

```python
def build(self, context: grpc.aio.ServicerContext) -> ServerCallContext
```

Source: [GrpcServerCallContextBuilder.build](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:46).

Source-docstring summary: Builds a ServerCallContext from a gRPC ServicerContext.

<!-- declaration:request_handlers/grpc_handler.py:50:DefaultGrpcServerCallContextBuilder -->
### `DefaultGrpcServerCallContextBuilder` — line 50

```python
class DefaultGrpcServerCallContextBuilder(GrpcServerCallContextBuilder)
```

Source: [DefaultGrpcServerCallContextBuilder](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:50).

Source-docstring summary: Default implementation of GrpcServerCallContextBuilder.

<!-- declaration:request_handlers/grpc_handler.py:53:DefaultGrpcServerCallContextBuilder.build -->
### `DefaultGrpcServerCallContextBuilder.build` — line 53

```python
def build(self, context: grpc.aio.ServicerContext) -> ServerCallContext
```

Source: [DefaultGrpcServerCallContextBuilder.build](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:53).

Source-docstring summary: Builds a ServerCallContext from a gRPC ServicerContext.

<!-- declaration:request_handlers/grpc_handler.py:64:DefaultGrpcServerCallContextBuilder.build_user -->
### `DefaultGrpcServerCallContextBuilder.build_user` — line 64

```python
def build_user(self, context: grpc.aio.ServicerContext) -> User
```

Source: [DefaultGrpcServerCallContextBuilder.build_user](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:64).

Source-docstring summary: Builds a User from a gRPC ServicerContext.

<!-- declaration:request_handlers/grpc_handler.py:69:_get_metadata_value -->
### `_get_metadata_value` — line 69

```python
def _get_metadata_value(context: grpc.aio.ServicerContext, key: str) -> list[str]
```

Source: [_get_metadata_value](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:69).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/grpc_handler.py:104:GrpcHandler -->
### `GrpcHandler` — line 104

```python
class GrpcHandler(a2a_grpc.A2AServiceServicer)
```

Source: [GrpcHandler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:104).

Source-docstring summary: Maps incoming gRPC requests to the appropriate request handler method.

<!-- declaration:request_handlers/grpc_handler.py:107:GrpcHandler.__init__ -->
### `GrpcHandler.__init__` — line 107

```python
def __init__(self, request_handler: RequestHandler, context_builder: GrpcServerCallContextBuilder | None=None)
```

Source: [GrpcHandler.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:107).

Source-docstring summary: Initializes the GrpcHandler.

<!-- declaration:request_handlers/grpc_handler.py:126:GrpcHandler._handle_unary -->
### `GrpcHandler._handle_unary` — line 126

```python
async def _handle_unary(self, request: message.Message, context: grpc.aio.ServicerContext, handler_func: Callable[[ServerCallContext], Awaitable[TResponse]], default_response: TResponse) -> TResponse
```

Source: [GrpcHandler._handle_unary](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:126).

Source-docstring summary: Centralized error handling and context management for unary calls.

<!-- declaration:request_handlers/grpc_handler.py:143:GrpcHandler._handle_stream -->
### `GrpcHandler._handle_stream` — line 143

```python
async def _handle_stream(self, request: message.Message, context: grpc.aio.ServicerContext, handler_func: Callable[[ServerCallContext], AsyncIterable[TResponse]]) -> AsyncIterable[TResponse]
```

Source: [GrpcHandler._handle_stream](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:143).

Source-docstring summary: Centralized error handling and context management for streaming calls.

<!-- declaration:request_handlers/grpc_handler.py:157:GrpcHandler.SendMessage -->
### `GrpcHandler.SendMessage` — line 157

```python
async def SendMessage(self, request: a2a_pb2.SendMessageRequest, context: grpc.aio.ServicerContext) -> a2a_pb2.SendMessageResponse
```

Source: [GrpcHandler.SendMessage](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:157).

Source-docstring summary: Handles the 'SendMessage' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:164:GrpcHandler.SendMessage._handler -->
### `GrpcHandler.SendMessage._handler` — line 164

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.SendMessageResponse
```

Source: [GrpcHandler.SendMessage._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:164).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:178:GrpcHandler.SendStreamingMessage -->
### `GrpcHandler.SendStreamingMessage` — line 178

```python
async def SendStreamingMessage(self, request: a2a_pb2.SendMessageRequest, context: grpc.aio.ServicerContext) -> AsyncIterable[a2a_pb2.StreamResponse]
```

Source: [GrpcHandler.SendStreamingMessage](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:178).

Source-docstring summary: Handles the 'StreamMessage' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:185:GrpcHandler.SendStreamingMessage._handler -->
### `GrpcHandler.SendStreamingMessage._handler` — line 185

```python
async def _handler(server_context: ServerCallContext) -> AsyncIterable[a2a_pb2.StreamResponse]
```

Source: [GrpcHandler.SendStreamingMessage._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:185).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:196:GrpcHandler.CancelTask -->
### `GrpcHandler.CancelTask` — line 196

```python
async def CancelTask(self, request: a2a_pb2.CancelTaskRequest, context: grpc.aio.ServicerContext) -> a2a_pb2.Task
```

Source: [GrpcHandler.CancelTask](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:196).

Source-docstring summary: Handles the 'CancelTask' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:203:GrpcHandler.CancelTask._handler -->
### `GrpcHandler.CancelTask._handler` — line 203

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.Task
```

Source: [GrpcHandler.CancelTask._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:203).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:215:GrpcHandler.SubscribeToTask -->
### `GrpcHandler.SubscribeToTask` — line 215

```python
async def SubscribeToTask(self, request: a2a_pb2.SubscribeToTaskRequest, context: grpc.aio.ServicerContext) -> AsyncIterable[a2a_pb2.StreamResponse]
```

Source: [GrpcHandler.SubscribeToTask](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:215).

Source-docstring summary: Handles the 'SubscribeToTask' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:222:GrpcHandler.SubscribeToTask._handler -->
### `GrpcHandler.SubscribeToTask._handler` — line 222

```python
async def _handler(server_context: ServerCallContext) -> AsyncIterable[a2a_pb2.StreamResponse]
```

Source: [GrpcHandler.SubscribeToTask._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:222).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:233:GrpcHandler.GetTaskPushNotificationConfig -->
### `GrpcHandler.GetTaskPushNotificationConfig` — line 233

```python
async def GetTaskPushNotificationConfig(self, request: a2a_pb2.GetTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext) -> a2a_pb2.TaskPushNotificationConfig
```

Source: [GrpcHandler.GetTaskPushNotificationConfig](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:233).

Source-docstring summary: Handles the 'GetTaskPushNotificationConfig' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:240:GrpcHandler.GetTaskPushNotificationConfig._handler -->
### `GrpcHandler.GetTaskPushNotificationConfig._handler` — line 240

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.TaskPushNotificationConfig
```

Source: [GrpcHandler.GetTaskPushNotificationConfig._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:240).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:253:GrpcHandler.CreateTaskPushNotificationConfig -->
### `GrpcHandler.CreateTaskPushNotificationConfig` — line 253

```python
async def CreateTaskPushNotificationConfig(self, request: a2a_pb2.TaskPushNotificationConfig, context: grpc.aio.ServicerContext) -> a2a_pb2.TaskPushNotificationConfig
```

Source: [GrpcHandler.CreateTaskPushNotificationConfig](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:253).

Source-docstring summary: Handles the 'CreateTaskPushNotificationConfig' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:260:GrpcHandler.CreateTaskPushNotificationConfig._handler -->
### `GrpcHandler.CreateTaskPushNotificationConfig._handler` — line 260

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.TaskPushNotificationConfig
```

Source: [GrpcHandler.CreateTaskPushNotificationConfig._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:260).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:271:GrpcHandler.ListTaskPushNotificationConfigs -->
### `GrpcHandler.ListTaskPushNotificationConfigs` — line 271

```python
async def ListTaskPushNotificationConfigs(self, request: a2a_pb2.ListTaskPushNotificationConfigsRequest, context: grpc.aio.ServicerContext) -> a2a_pb2.ListTaskPushNotificationConfigsResponse
```

Source: [GrpcHandler.ListTaskPushNotificationConfigs](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:271).

Source-docstring summary: Handles the 'ListTaskPushNotificationConfig' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:278:GrpcHandler.ListTaskPushNotificationConfigs._handler -->
### `GrpcHandler.ListTaskPushNotificationConfigs._handler` — line 278

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.ListTaskPushNotificationConfigsResponse
```

Source: [GrpcHandler.ListTaskPushNotificationConfigs._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:278).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:292:GrpcHandler.DeleteTaskPushNotificationConfig -->
### `GrpcHandler.DeleteTaskPushNotificationConfig` — line 292

```python
async def DeleteTaskPushNotificationConfig(self, request: a2a_pb2.DeleteTaskPushNotificationConfigRequest, context: grpc.aio.ServicerContext) -> empty_pb2.Empty
```

Source: [GrpcHandler.DeleteTaskPushNotificationConfig](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:292).

Source-docstring summary: Handles the 'DeleteTaskPushNotificationConfig' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:299:GrpcHandler.DeleteTaskPushNotificationConfig._handler -->
### `GrpcHandler.DeleteTaskPushNotificationConfig._handler` — line 299

```python
async def _handler(server_context: ServerCallContext) -> empty_pb2.Empty
```

Source: [GrpcHandler.DeleteTaskPushNotificationConfig._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:299).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:311:GrpcHandler.GetTask -->
### `GrpcHandler.GetTask` — line 311

```python
async def GetTask(self, request: a2a_pb2.GetTaskRequest, context: grpc.aio.ServicerContext) -> a2a_pb2.Task
```

Source: [GrpcHandler.GetTask](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:311).

Source-docstring summary: Handles the 'GetTask' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:318:GrpcHandler.GetTask._handler -->
### `GrpcHandler.GetTask._handler` — line 318

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.Task
```

Source: [GrpcHandler.GetTask._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:318).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:330:GrpcHandler.ListTasks -->
### `GrpcHandler.ListTasks` — line 330

```python
async def ListTasks(self, request: a2a_pb2.ListTasksRequest, context: grpc.aio.ServicerContext) -> a2a_pb2.ListTasksResponse
```

Source: [GrpcHandler.ListTasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:330).

Source-docstring summary: Handles the 'ListTasks' gRPC method.

<!-- declaration:request_handlers/grpc_handler.py:337:GrpcHandler.ListTasks._handler -->
### `GrpcHandler.ListTasks._handler` — line 337

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.ListTasksResponse
```

Source: [GrpcHandler.ListTasks._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:337).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:348:GrpcHandler.GetExtendedAgentCard -->
### `GrpcHandler.GetExtendedAgentCard` — line 348

```python
async def GetExtendedAgentCard(self, request: a2a_pb2.GetExtendedAgentCardRequest, context: grpc.aio.ServicerContext) -> a2a_pb2.AgentCard
```

Source: [GrpcHandler.GetExtendedAgentCard](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:348).

Source-docstring summary: Get the extended agent card for the agent served.

<!-- declaration:request_handlers/grpc_handler.py:355:GrpcHandler.GetExtendedAgentCard._handler -->
### `GrpcHandler.GetExtendedAgentCard._handler` — line 355

```python
async def _handler(server_context: ServerCallContext) -> a2a_pb2.AgentCard
```

Source: [GrpcHandler.GetExtendedAgentCard._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:355).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:request_handlers/grpc_handler.py:366:GrpcHandler.abort_context -->
### `GrpcHandler.abort_context` — line 366

```python
async def abort_context(self, error: A2AError, context: grpc.aio.ServicerContext) -> None
```

Source: [GrpcHandler.abort_context](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:366).

Source-docstring summary: Sets the grpc errors appropriately in the context.

<!-- declaration:request_handlers/grpc_handler.py:421:GrpcHandler._build_call_context -->
### `GrpcHandler._build_call_context` — line 421

```python
def _build_call_context(self, context: grpc.aio.ServicerContext, request: message.Message) -> ServerCallContext
```

Source: [GrpcHandler._build_call_context](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/grpc_handler.py:421).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

## `request_handlers/request_handler.py`

Behavior: [request_handlers_knowledge.md](request_handlers_knowledge.md). Source: [request_handlers/request_handler.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py).

<!-- declaration:request_handlers/request_handler.py:34:RequestHandler -->
### `RequestHandler` — line 34

```python
class RequestHandler(ABC)
```

Source: [RequestHandler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:34).

Source-docstring summary: A2A request handler interface.

<!-- declaration:request_handlers/request_handler.py:42:RequestHandler.on_get_task -->
### `RequestHandler.on_get_task` — line 42

```python
async def on_get_task(self, params: GetTaskRequest, context: ServerCallContext) -> Task | None
```

Source: [RequestHandler.on_get_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:42).

Source-docstring summary: Handles the 'tasks/get' method.

<!-- declaration:request_handlers/request_handler.py:60:RequestHandler.on_list_tasks -->
### `RequestHandler.on_list_tasks` — line 60

```python
async def on_list_tasks(self, params: ListTasksRequest, context: ServerCallContext) -> ListTasksResponse
```

Source: [RequestHandler.on_list_tasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:60).

Source-docstring summary: Handles the tasks/list method.

<!-- declaration:request_handlers/request_handler.py:77:RequestHandler.on_cancel_task -->
### `RequestHandler.on_cancel_task` — line 77

```python
async def on_cancel_task(self, params: CancelTaskRequest, context: ServerCallContext) -> Task | None
```

Source: [RequestHandler.on_cancel_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:77).

Source-docstring summary: Handles the 'tasks/cancel' method.

<!-- declaration:request_handlers/request_handler.py:95:RequestHandler.on_message_send -->
### `RequestHandler.on_message_send` — line 95

```python
async def on_message_send(self, params: SendMessageRequest, context: ServerCallContext) -> Task | Message
```

Source: [RequestHandler.on_message_send](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:95).

Source-docstring summary: Handles the 'message/send' method (non-streaming).

<!-- declaration:request_handlers/request_handler.py:114:RequestHandler.on_message_send_stream -->
### `RequestHandler.on_message_send_stream` — line 114

```python
async def on_message_send_stream(self, params: SendMessageRequest, context: ServerCallContext) -> AsyncGenerator[Event]
```

Source: [RequestHandler.on_message_send_stream](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:114).

Source-docstring summary: Handles the 'message/stream' method (streaming).

<!-- declaration:request_handlers/request_handler.py:136:RequestHandler.on_create_task_push_notification_config -->
### `RequestHandler.on_create_task_push_notification_config` — line 136

```python
async def on_create_task_push_notification_config(self, params: TaskPushNotificationConfig, context: ServerCallContext) -> TaskPushNotificationConfig
```

Source: [RequestHandler.on_create_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:136).

Source-docstring summary: Handles the 'tasks/pushNotificationConfig/create' method.

<!-- declaration:request_handlers/request_handler.py:154:RequestHandler.on_get_task_push_notification_config -->
### `RequestHandler.on_get_task_push_notification_config` — line 154

```python
async def on_get_task_push_notification_config(self, params: GetTaskPushNotificationConfigRequest, context: ServerCallContext) -> TaskPushNotificationConfig
```

Source: [RequestHandler.on_get_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:154).

Source-docstring summary: Handles the 'tasks/pushNotificationConfig/get' method.

<!-- declaration:request_handlers/request_handler.py:172:RequestHandler.on_subscribe_to_task -->
### `RequestHandler.on_subscribe_to_task` — line 172

```python
async def on_subscribe_to_task(self, params: SubscribeToTaskRequest, context: ServerCallContext) -> AsyncGenerator[Event]
```

Source: [RequestHandler.on_subscribe_to_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:172).

Source-docstring summary: Handles the 'SubscribeToTask' method.

<!-- declaration:request_handlers/request_handler.py:192:RequestHandler.on_list_task_push_notification_configs -->
### `RequestHandler.on_list_task_push_notification_configs` — line 192

```python
async def on_list_task_push_notification_configs(self, params: ListTaskPushNotificationConfigsRequest, context: ServerCallContext) -> ListTaskPushNotificationConfigsResponse
```

Source: [RequestHandler.on_list_task_push_notification_configs](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:192).

Source-docstring summary: Handles the 'ListTaskPushNotificationConfigs' method.

<!-- declaration:request_handlers/request_handler.py:210:RequestHandler.on_delete_task_push_notification_config -->
### `RequestHandler.on_delete_task_push_notification_config` — line 210

```python
async def on_delete_task_push_notification_config(self, params: DeleteTaskPushNotificationConfigRequest, context: ServerCallContext) -> None
```

Source: [RequestHandler.on_delete_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:210).

Source-docstring summary: Handles the 'tasks/pushNotificationConfig/delete' method.

<!-- declaration:request_handlers/request_handler.py:228:RequestHandler.on_get_extended_agent_card -->
### `RequestHandler.on_get_extended_agent_card` — line 228

```python
async def on_get_extended_agent_card(self, params: GetExtendedAgentCardRequest, context: ServerCallContext) -> AgentCard
```

Source: [RequestHandler.on_get_extended_agent_card](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:228).

Source-docstring summary: Handles the 'GetExtendedAgentCard' method.

<!-- declaration:request_handlers/request_handler.py:247:validate_request_params -->
### `validate_request_params` — line 247

```python
def validate_request_params(method: Callable) -> Callable
```

Source: [validate_request_params](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:247).

Source-docstring summary: Decorator for RequestHandler methods to validate required fields on incoming requests.

<!-- declaration:request_handlers/request_handler.py:252:validate_request_params.async_gen_wrapper -->
### `validate_request_params.async_gen_wrapper` — line 252

```python
async def async_gen_wrapper(self: RequestHandler, params: ProtoMessage, context: ServerCallContext, *args: Any, **kwargs: Any) -> Any
```

Source: [validate_request_params.async_gen_wrapper](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:252).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/request_handler.py:276:validate_request_params.async_wrapper -->
### `validate_request_params.async_wrapper` — line 276

```python
async def async_wrapper(self: RequestHandler, params: ProtoMessage, context: ServerCallContext, *args: Any, **kwargs: Any) -> Any
```

Source: [validate_request_params.async_wrapper](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:276).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/request_handler.py:290:validate -->
### `validate` — line 290

```python
def validate(expression: Callable[[Any], bool], error_message: str | None=None, error_type: type[Exception]=UnsupportedOperationError) -> Callable
```

Source: [validate](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:290).

Source-docstring summary: Decorator that validates if a given expression evaluates to True.

<!-- declaration:request_handlers/request_handler.py:366:validate.decorator -->
### `validate.decorator` — line 366

```python
def decorator(function: Callable) -> Callable
```

Source: [validate.decorator](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:366).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/request_handler.py:370:validate.decorator.async_gen_wrapper -->
### `validate.decorator.async_gen_wrapper` — line 370

```python
async def async_gen_wrapper(self: Any, *args, **kwargs) -> Any
```

Source: [validate.decorator.async_gen_wrapper](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:370).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/request_handler.py:389:validate.decorator.async_wrapper -->
### `validate.decorator.async_wrapper` — line 389

```python
async def async_wrapper(self: Any, *args, **kwargs) -> Any
```

Source: [validate.decorator.async_wrapper](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:389).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/request_handler.py:401:validate.decorator.sync_wrapper -->
### `validate.decorator.sync_wrapper` — line 401

```python
def sync_wrapper(self: Any, *args, **kwargs) -> Any
```

Source: [validate.decorator.sync_wrapper](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/request_handler.py:401).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

## `request_handlers/response_helpers.py`

Behavior: [request_handlers_knowledge.md](request_handlers_knowledge.md). Source: [request_handlers/response_helpers.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/response_helpers.py).

<!-- declaration:request_handlers/response_helpers.py:87:agent_card_to_dict -->
### `agent_card_to_dict` — line 87

```python
def agent_card_to_dict(card: AgentCard) -> dict[str, Any]
```

Source: [agent_card_to_dict](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/response_helpers.py:87).

Source-docstring summary: Convert AgentCard to dict and inject backward compatibility fields.

<!-- declaration:request_handlers/response_helpers.py:101:agent_card_to_dict.merge -->
### `agent_card_to_dict.merge` — line 101

```python
def merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]
```

Source: [agent_card_to_dict.merge](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/response_helpers.py:101).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:request_handlers/response_helpers.py:116:build_error_response -->
### `build_error_response` — line 116

```python
def build_error_response(request_id: str | int | None, error: A2AError | JSONRPCError) -> dict[str, Any]
```

Source: [build_error_response](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/response_helpers.py:116).

Source-docstring summary: Build a JSON-RPC error response dict.

<!-- declaration:request_handlers/response_helpers.py:148:prepare_response_object -->
### `prepare_response_object` — line 148

```python
def prepare_response_object(request_id: str | int | None, response: EventTypes, success_response_types: tuple[type, ...]) -> dict[str, Any]
```

Source: [prepare_response_object](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/request_handlers/response_helpers.py:148).

Source-docstring summary: Build a JSON-RPC response dict from handler output.

## `routes/__init__.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/__init__.py).

No declared classes/functions/methods. Import and export behavior is documented in the linked guide.

## `routes/_jsonrpc_schema.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/_jsonrpc_schema.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/_jsonrpc_schema.py).

<!-- declaration:routes/_jsonrpc_schema.py:56:envelope_schema -->
### `envelope_schema` — line 56

```python
def envelope_schema(components: dict[str, Any]) -> dict[str, Any]
```

Source: [envelope_schema](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/_jsonrpc_schema.py:56).

Source-docstring summary: Builds the A2ARequest JSON-RPC envelope schema with a oneOf over all method params.

## `routes/_proto_schema.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/_proto_schema.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/_proto_schema.py).

<!-- declaration:routes/_proto_schema.py:38:_is_required -->
### `_is_required` — line 38

```python
def _is_required(field: FieldDescriptor) -> bool
```

Source: [_is_required](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/_proto_schema.py:38).

Source-docstring summary: Returns True if the field carries google.api.field_behavior = REQUIRED.

<!-- declaration:routes/_proto_schema.py:55:field_schema -->
### `field_schema` — line 55

```python
def field_schema(field: FieldDescriptor, components: dict[str, Any]) -> dict[str, Any]
```

Source: [field_schema](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/_proto_schema.py:55).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/_proto_schema.py:110:message_schema -->
### `message_schema` — line 110

```python
def message_schema(descriptor: Descriptor | Any, components: dict[str, Any]) -> dict[str, Any]
```

Source: [message_schema](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/_proto_schema.py:110).

Source-docstring summary: Returns a $ref to descriptor's schema, registering it in components if needed.

## `routes/agent_card_routes.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/agent_card_routes.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/agent_card_routes.py).

<!-- declaration:routes/agent_card_routes.py:31:create_agent_card_routes -->
### `create_agent_card_routes` — line 31

```python
def create_agent_card_routes(agent_card: AgentCard, card_modifier: Callable[[AgentCard], Awaitable[AgentCard]] | None=None, card_url: str=AGENT_CARD_WELL_KNOWN_PATH) -> list['Route']
```

Source: [create_agent_card_routes](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/agent_card_routes.py:31).

Source-docstring summary: Creates the Starlette Route for the A2A protocol agent card endpoint.

<!-- declaration:routes/agent_card_routes.py:43:create_agent_card_routes._get_agent_card -->
### `create_agent_card_routes._get_agent_card` — line 43

```python
async def _get_agent_card(request: Request) -> Response
```

Source: [create_agent_card_routes._get_agent_card](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/agent_card_routes.py:43).

Source-docstring summary: Returns the public AgentCard describing this agent's capabilities, supported transports, and skills.

## `routes/common.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/common.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py).

<!-- declaration:routes/common.py:28:serialize_list_tasks_response -->
### `serialize_list_tasks_response` — line 28

```python
def serialize_list_tasks_response(response: ListTasksResponse, include_artifacts: bool) -> dict[str, Any]
```

Source: [serialize_list_tasks_response](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:28).

Source-docstring summary: Serializes a ListTasks response according to artifact semantics.

<!-- declaration:routes/common.py:43:StarletteUser -->
### `StarletteUser` — line 43

```python
class StarletteUser(User)
```

Source: [StarletteUser](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:43).

Source-docstring summary: Adapts a Starlette BaseUser to the A2A User interface.

<!-- declaration:routes/common.py:46:StarletteUser.__init__ -->
### `StarletteUser.__init__` — line 46

```python
def __init__(self, user: BaseUser)
```

Source: [StarletteUser.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:46).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:routes/common.py:50:StarletteUser.is_authenticated -->
### `StarletteUser.is_authenticated` — line 50

```python
def is_authenticated(self) -> bool
```

Source: [StarletteUser.is_authenticated](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:50).

Source-docstring summary: Returns whether the current user is authenticated.

<!-- declaration:routes/common.py:55:StarletteUser.user_name -->
### `StarletteUser.user_name` — line 55

```python
def user_name(self) -> str
```

Source: [StarletteUser.user_name](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:55).

Source-docstring summary: Returns the user name of the current user.

<!-- declaration:routes/common.py:60:ServerCallContextBuilder -->
### `ServerCallContextBuilder` — line 60

```python
class ServerCallContextBuilder(ABC)
```

Source: [ServerCallContextBuilder](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:60).

Source-docstring summary: A class for building ServerCallContexts using the Starlette Request.

<!-- declaration:routes/common.py:64:ServerCallContextBuilder.build -->
### `ServerCallContextBuilder.build` — line 64

```python
def build(self, request: Request) -> ServerCallContext
```

Source: [ServerCallContextBuilder.build](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:64).

Source-docstring summary: Builds a ServerCallContext from a Starlette Request.

<!-- declaration:routes/common.py:68:DefaultServerCallContextBuilder -->
### `DefaultServerCallContextBuilder` — line 68

```python
class DefaultServerCallContextBuilder(ServerCallContextBuilder)
```

Source: [DefaultServerCallContextBuilder](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:68).

Source-docstring summary: A default implementation of ServerCallContextBuilder.

<!-- declaration:routes/common.py:71:DefaultServerCallContextBuilder.build -->
### `DefaultServerCallContextBuilder.build` — line 71

```python
def build(self, request: Request) -> ServerCallContext
```

Source: [DefaultServerCallContextBuilder.build](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:71).

Source-docstring summary: Builds a ServerCallContext from a Starlette Request.

<!-- declaration:routes/common.py:93:DefaultServerCallContextBuilder.build_user -->
### `DefaultServerCallContextBuilder.build_user` — line 93

```python
def build_user(self, request: Request) -> User
```

Source: [DefaultServerCallContextBuilder.build_user](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/common.py:93).

Source-docstring summary: Builds a User from a Starlette Request.

## `routes/fastapi_routes.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/fastapi_routes.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py).

<!-- declaration:routes/fastapi_routes.py:29:_A2ARoute -->
### `_A2ARoute` — line 29

```python
class _A2ARoute(APIRoute)
```

Source: [_A2ARoute](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py:29).

Source-docstring summary: APIRoute that uses Starlette's request_response to bypass FastAPI middleware scope requirements.

<!-- declaration:routes/fastapi_routes.py:32:_A2ARoute.__init__ -->
### `_A2ARoute.__init__` — line 32

```python
def __init__(self, *args: Any, **kwargs: Any) -> None
```

Source: [_A2ARoute.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py:32).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:routes/fastapi_routes.py:57:_request_body_extra -->
### `_request_body_extra` — line 57

```python
def _request_body_extra(ref: dict[str, Any], description: str) -> dict[str, Any]
```

Source: [_request_body_extra](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py:57).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/fastapi_routes.py:69:_rest_body_extra -->
### `_rest_body_extra` — line 69

```python
def _rest_body_extra(route: 'Route', rest_bodies: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any] | None
```

Source: [_rest_body_extra](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py:69).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/fastapi_routes.py:79:_attach_route -->
### `_attach_route` — line 79

```python
def _attach_route(app: 'FastAPI', route: 'BaseRoute', tag: str, openapi_extra: dict[str, Any] | None, require_version_header: bool=False) -> None
```

Source: [_attach_route](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py:79).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/fastapi_routes.py:106:add_a2a_routes_to_fastapi -->
### `add_a2a_routes_to_fastapi` — line 106

```python
def add_a2a_routes_to_fastapi(app: 'FastAPI', *, agent_card_routes: 'Sequence[BaseRoute] | None'=None, jsonrpc_routes: 'Sequence[BaseRoute] | None'=None, rest_routes: 'Sequence[BaseRoute] | None'=None) -> None
```

Source: [add_a2a_routes_to_fastapi](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py:106).

Source-docstring summary: Mounts A2A routes on a FastAPI app and enriches them for ``/docs``.

<!-- declaration:routes/fastapi_routes.py:187:add_a2a_routes_to_fastapi._openapi -->
### `add_a2a_routes_to_fastapi._openapi` — line 187

```python
def _openapi() -> dict[str, Any]
```

Source: [add_a2a_routes_to_fastapi._openapi](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/fastapi_routes.py:187).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

## `routes/jsonrpc_dispatcher.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/jsonrpc_dispatcher.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py).

<!-- declaration:routes/jsonrpc_dispatcher.py:103:JsonRpcDispatcher -->
### `JsonRpcDispatcher` — line 103

```python
class JsonRpcDispatcher()
```

Source: [JsonRpcDispatcher](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:103).

Source-docstring summary: Base class for A2A JSONRPC applications.

<!-- declaration:routes/jsonrpc_dispatcher.py:128:JsonRpcDispatcher.__init__ -->
### `JsonRpcDispatcher.__init__` — line 128

```python
def __init__(self, request_handler: RequestHandler, context_builder: ServerCallContextBuilder | None=None, enable_v0_3_compat: bool=False) -> None
```

Source: [JsonRpcDispatcher.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:128).

Source-docstring summary: Initializes the JsonRpcDispatcher.

<!-- declaration:routes/jsonrpc_dispatcher.py:164:JsonRpcDispatcher._generate_error_response -->
### `JsonRpcDispatcher._generate_error_response` — line 164

```python
def _generate_error_response(self, request_id: str | int | None, error: Exception | JSONRPCError | A2AError) -> JSONResponse
```

Source: [JsonRpcDispatcher._generate_error_response](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:164).

Source-docstring summary: Creates a Starlette JSONResponse for a JSON-RPC error.

<!-- declaration:routes/jsonrpc_dispatcher.py:206:JsonRpcDispatcher.handle_requests -->
### `JsonRpcDispatcher.handle_requests` — line 206

```python
async def handle_requests(self, request: Request) -> Response
```

Source: [JsonRpcDispatcher.handle_requests](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:206).

Source-docstring summary: Handles incoming POST requests to the main A2A endpoint.

<!-- declaration:routes/jsonrpc_dispatcher.py:346:JsonRpcDispatcher._process_streaming_request -->
### `JsonRpcDispatcher._process_streaming_request` — line 346

```python
async def _process_streaming_request(self, request_id: str | int | None, request_obj: Any, context: ServerCallContext) -> AsyncGenerator[dict[str, Any], None]
```

Source: [JsonRpcDispatcher._process_streaming_request](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:346).

Source-docstring summary: Processes streaming requests (SendStreamingMessage or SubscribeToTask).

<!-- declaration:routes/jsonrpc_dispatcher.py:382:JsonRpcDispatcher._process_streaming_request._wrap_stream -->
### `JsonRpcDispatcher._process_streaming_request._wrap_stream` — line 382

```python
async def _wrap_stream(st: AsyncGenerator, first_evt: Event | None) -> AsyncGenerator[dict[str, Any], None]
```

Source: [JsonRpcDispatcher._process_streaming_request._wrap_stream](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:382).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:385:JsonRpcDispatcher._process_streaming_request._wrap_stream._map_event -->
### `JsonRpcDispatcher._process_streaming_request._wrap_stream._map_event` — line 385

```python
def _map_event(evt: Event) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._process_streaming_request._wrap_stream._map_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:385).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:403:JsonRpcDispatcher._handle_send_message -->
### `JsonRpcDispatcher._handle_send_message` — line 403

```python
async def _handle_send_message(self, request_obj: SendMessageRequest, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_send_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:403).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:413:JsonRpcDispatcher._handle_cancel_task -->
### `JsonRpcDispatcher._handle_cancel_task` — line 413

```python
async def _handle_cancel_task(self, request_obj: CancelTaskRequest, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_cancel_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:413).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:421:JsonRpcDispatcher._handle_get_task -->
### `JsonRpcDispatcher._handle_get_task` — line 421

```python
async def _handle_get_task(self, request_obj: GetTaskRequest, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_get_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:421).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:429:JsonRpcDispatcher._handle_list_tasks -->
### `JsonRpcDispatcher._handle_list_tasks` — line 429

```python
async def _handle_list_tasks(self, request_obj: ListTasksRequest, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_list_tasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:429).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:439:JsonRpcDispatcher._handle_create_task_push_notification_config -->
### `JsonRpcDispatcher._handle_create_task_push_notification_config` — line 439

```python
async def _handle_create_task_push_notification_config(self, request_obj: TaskPushNotificationConfig, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_create_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:439).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:451:JsonRpcDispatcher._handle_get_task_push_notification_config -->
### `JsonRpcDispatcher._handle_get_task_push_notification_config` — line 451

```python
async def _handle_get_task_push_notification_config(self, request_obj: GetTaskPushNotificationConfigRequest, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_get_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:451).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:463:JsonRpcDispatcher._handle_list_task_push_notification_configs -->
### `JsonRpcDispatcher._handle_list_task_push_notification_configs` — line 463

```python
async def _handle_list_task_push_notification_configs(self, request_obj: ListTaskPushNotificationConfigsRequest, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_list_task_push_notification_configs](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:463).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:477:JsonRpcDispatcher._handle_delete_task_push_notification_config -->
### `JsonRpcDispatcher._handle_delete_task_push_notification_config` — line 477

```python
async def _handle_delete_task_push_notification_config(self, request_obj: DeleteTaskPushNotificationConfigRequest, context: ServerCallContext) -> None
```

Source: [JsonRpcDispatcher._handle_delete_task_push_notification_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:477).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:486:JsonRpcDispatcher._handle_get_extended_agent_card -->
### `JsonRpcDispatcher._handle_get_extended_agent_card` — line 486

```python
async def _handle_get_extended_agent_card(self, request_obj: GetExtendedAgentCardRequest, context: ServerCallContext) -> dict[str, Any]
```

Source: [JsonRpcDispatcher._handle_get_extended_agent_card](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:486).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/jsonrpc_dispatcher.py:497:JsonRpcDispatcher._process_non_streaming_request -->
### `JsonRpcDispatcher._process_non_streaming_request` — line 497

```python
async def _process_non_streaming_request(self, request_obj: Any, context: ServerCallContext) -> dict[str, Any] | None
```

Source: [JsonRpcDispatcher._process_non_streaming_request](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:497).

Source-docstring summary: Processes non-streaming requests.

<!-- declaration:routes/jsonrpc_dispatcher.py:548:JsonRpcDispatcher._create_response -->
### `JsonRpcDispatcher._create_response` — line 548

```python
def _create_response(self, context: ServerCallContext, handler_result: AsyncGenerator[dict[str, Any]] | dict[str, Any]) -> Response
```

Source: [JsonRpcDispatcher._create_response](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:548).

Source-docstring summary: Creates a Starlette Response based on the result from the request handler.

<!-- declaration:routes/jsonrpc_dispatcher.py:569:JsonRpcDispatcher._create_response.event_generator -->
### `JsonRpcDispatcher._create_response.event_generator` — line 569

```python
async def event_generator(stream: AsyncGenerator[dict[str, Any]]) -> AsyncGenerator[dict[str, str]]
```

Source: [JsonRpcDispatcher._create_response.event_generator](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_dispatcher.py:569).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

## `routes/jsonrpc_routes.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/jsonrpc_routes.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_routes.py).

<!-- declaration:routes/jsonrpc_routes.py:28:create_jsonrpc_routes -->
### `create_jsonrpc_routes` — line 28

```python
def create_jsonrpc_routes(request_handler: RequestHandler, rpc_url: str, context_builder: ServerCallContextBuilder | None=None, enable_v0_3_compat: bool=False) -> list['Route']
```

Source: [create_jsonrpc_routes](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/jsonrpc_routes.py:28).

Source-docstring summary: Creates the Starlette Route for the A2A protocol JSON-RPC endpoint.

## `routes/rest_dispatcher.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/rest_dispatcher.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py).

<!-- declaration:routes/rest_dispatcher.py:65:RestDispatcher -->
### `RestDispatcher` — line 65

```python
class RestDispatcher()
```

Source: [RestDispatcher](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:65).

Source-docstring summary: Dispatches incoming REST requests to the appropriate handler methods.

<!-- declaration:routes/rest_dispatcher.py:71:RestDispatcher.__init__ -->
### `RestDispatcher.__init__` — line 71

```python
def __init__(self, request_handler: RequestHandler, context_builder: ServerCallContextBuilder | None=None) -> None
```

Source: [RestDispatcher.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:71).

Source-docstring summary: Initializes the RestDispatcher.

<!-- declaration:routes/rest_dispatcher.py:96:RestDispatcher._build_call_context -->
### `RestDispatcher._build_call_context` — line 96

```python
def _build_call_context(self, request: Request) -> ServerCallContext
```

Source: [RestDispatcher._build_call_context](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:96).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/rest_dispatcher.py:102:RestDispatcher._handle_non_streaming -->
### `RestDispatcher._handle_non_streaming` — line 102

```python
async def _handle_non_streaming(self, request: Request, handler_func: Callable[[ServerCallContext], Awaitable[TResponse]]) -> TResponse
```

Source: [RestDispatcher._handle_non_streaming](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:102).

Source-docstring summary: Centralized error handling and context management for unary calls.

<!-- declaration:routes/rest_dispatcher.py:111:RestDispatcher._handle_streaming -->
### `RestDispatcher._handle_streaming` — line 111

```python
async def _handle_streaming(self, request: Request, handler_func: Callable[[ServerCallContext], AsyncIterator[Any]]) -> EventSourceResponse
```

Source: [RestDispatcher._handle_streaming](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:111).

Source-docstring summary: Centralized error handling and context management for streaming calls.

<!-- declaration:routes/rest_dispatcher.py:142:RestDispatcher._handle_streaming.event_generator -->
### `RestDispatcher._handle_streaming.event_generator` — line 142

```python
async def event_generator() -> AsyncIterator[ServerSentEvent]
```

Source: [RestDispatcher._handle_streaming.event_generator](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:142).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:routes/rest_dispatcher.py:157:RestDispatcher.on_message_send -->
### `RestDispatcher.on_message_send` — line 157

```python
async def on_message_send(self, request: Request) -> Response
```

Source: [RestDispatcher.on_message_send](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:157).

Source-docstring summary: Handles the 'message/send' REST method.

<!-- declaration:routes/rest_dispatcher.py:161:RestDispatcher.on_message_send._handler -->
### `RestDispatcher.on_message_send._handler` — line 161

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.SendMessageResponse
```

Source: [RestDispatcher.on_message_send._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:161).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:178:RestDispatcher.on_message_send_stream -->
### `RestDispatcher.on_message_send_stream` — line 178

```python
async def on_message_send_stream(self, request: Request) -> EventSourceResponse
```

Source: [RestDispatcher.on_message_send_stream](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:178).

Source-docstring summary: Handles the 'message/stream' REST method.

<!-- declaration:routes/rest_dispatcher.py:184:RestDispatcher.on_message_send_stream._handler -->
### `RestDispatcher.on_message_send_stream._handler` — line 184

```python
async def _handler(context: ServerCallContext) -> AsyncIterator[dict[str, Any]]
```

Source: [RestDispatcher.on_message_send_stream._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:184).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:199:RestDispatcher.on_cancel_task -->
### `RestDispatcher.on_cancel_task` — line 199

```python
async def on_cancel_task(self, request: Request) -> Response
```

Source: [RestDispatcher.on_cancel_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:199).

Source-docstring summary: Handles the 'tasks/cancel' REST method.

<!-- declaration:routes/rest_dispatcher.py:203:RestDispatcher.on_cancel_task._handler -->
### `RestDispatcher.on_cancel_task._handler` — line 203

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.Task
```

Source: [RestDispatcher.on_cancel_task._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:203).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:216:RestDispatcher.on_subscribe_to_task -->
### `RestDispatcher.on_subscribe_to_task` — line 216

```python
async def on_subscribe_to_task(self, request: Request) -> EventSourceResponse
```

Source: [RestDispatcher.on_subscribe_to_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:216).

Source-docstring summary: Handles the 'SubscribeToTask' REST method.

<!-- declaration:routes/rest_dispatcher.py:223:RestDispatcher.on_subscribe_to_task._handler -->
### `RestDispatcher.on_subscribe_to_task._handler` — line 223

```python
async def _handler(context: ServerCallContext) -> AsyncIterator[dict[str, Any]]
```

Source: [RestDispatcher.on_subscribe_to_task._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:223).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:235:RestDispatcher.on_get_task -->
### `RestDispatcher.on_get_task` — line 235

```python
async def on_get_task(self, request: Request) -> Response
```

Source: [RestDispatcher.on_get_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:235).

Source-docstring summary: Handles the 'tasks/{id}' REST method.

<!-- declaration:routes/rest_dispatcher.py:239:RestDispatcher.on_get_task._handler -->
### `RestDispatcher.on_get_task._handler` — line 239

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.Task
```

Source: [RestDispatcher.on_get_task._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:239).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:252:RestDispatcher.get_push_notification -->
### `RestDispatcher.get_push_notification` — line 252

```python
async def get_push_notification(self, request: Request) -> Response
```

Source: [RestDispatcher.get_push_notification](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:252).

Source-docstring summary: Handles the 'tasks/pushNotificationConfig/get' REST method.

<!-- declaration:routes/rest_dispatcher.py:256:RestDispatcher.get_push_notification._handler -->
### `RestDispatcher.get_push_notification._handler` — line 256

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.TaskPushNotificationConfig
```

Source: [RestDispatcher.get_push_notification._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:256).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:274:RestDispatcher.delete_push_notification -->
### `RestDispatcher.delete_push_notification` — line 274

```python
async def delete_push_notification(self, request: Request) -> Response
```

Source: [RestDispatcher.delete_push_notification](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:274).

Source-docstring summary: Handles the 'tasks/pushNotificationConfig/delete' REST method.

<!-- declaration:routes/rest_dispatcher.py:278:RestDispatcher.delete_push_notification._handler -->
### `RestDispatcher.delete_push_notification._handler` — line 278

```python
async def _handler(context: ServerCallContext) -> None
```

Source: [RestDispatcher.delete_push_notification._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:278).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:292:RestDispatcher.set_push_notification -->
### `RestDispatcher.set_push_notification` — line 292

```python
async def set_push_notification(self, request: Request) -> Response
```

Source: [RestDispatcher.set_push_notification](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:292).

Source-docstring summary: Handles the 'tasks/pushNotificationConfig/set' REST method.

<!-- declaration:routes/rest_dispatcher.py:296:RestDispatcher.set_push_notification._handler -->
### `RestDispatcher.set_push_notification._handler` — line 296

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.TaskPushNotificationConfig
```

Source: [RestDispatcher.set_push_notification._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:296).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:311:RestDispatcher.list_push_notifications -->
### `RestDispatcher.list_push_notifications` — line 311

```python
async def list_push_notifications(self, request: Request) -> Response
```

Source: [RestDispatcher.list_push_notifications](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:311).

Source-docstring summary: Handles the 'tasks/pushNotificationConfig/list' REST method.

<!-- declaration:routes/rest_dispatcher.py:315:RestDispatcher.list_push_notifications._handler -->
### `RestDispatcher.list_push_notifications._handler` — line 315

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.ListTaskPushNotificationConfigsResponse
```

Source: [RestDispatcher.list_push_notifications._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:315).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:329:RestDispatcher.list_tasks -->
### `RestDispatcher.list_tasks` — line 329

```python
async def list_tasks(self, request: Request) -> Response
```

Source: [RestDispatcher.list_tasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:329).

Source-docstring summary: Handles the 'tasks/list' REST method.

<!-- declaration:routes/rest_dispatcher.py:334:RestDispatcher.list_tasks._handler -->
### `RestDispatcher.list_tasks._handler` — line 334

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.ListTasksResponse
```

Source: [RestDispatcher.list_tasks._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:334).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

<!-- declaration:routes/rest_dispatcher.py:348:RestDispatcher.handle_authenticated_agent_card -->
### `RestDispatcher.handle_authenticated_agent_card` — line 348

```python
async def handle_authenticated_agent_card(self, request: Request) -> Response
```

Source: [RestDispatcher.handle_authenticated_agent_card](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:348).

Source-docstring summary: Handles the 'agentCard' REST method.

<!-- declaration:routes/rest_dispatcher.py:354:RestDispatcher.handle_authenticated_agent_card._handler -->
### `RestDispatcher.handle_authenticated_agent_card._handler` — line 354

```python
async def _handler(context: ServerCallContext) -> a2a_pb2.AgentCard
```

Source: [RestDispatcher.handle_authenticated_agent_card._handler](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_dispatcher.py:354).

Source-docstring summary: Captured request adapter: constructs protocol request or converts handler result for this enclosing transport operation; see its enclosing operation in the guide.

## `routes/rest_routes.py`

Behavior: [routes_knowledge.md](routes_knowledge.md). Source: [routes/rest_routes.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_routes.py).

<!-- declaration:routes/rest_routes.py:30:create_rest_routes -->
### `create_rest_routes` — line 30

```python
def create_rest_routes(request_handler: RequestHandler, context_builder: ServerCallContextBuilder | None=None, enable_v0_3_compat: bool=False, path_prefix: str='') -> list['BaseRoute']
```

Source: [create_rest_routes](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/routes/rest_routes.py:30).

Source-docstring summary: Creates the Starlette Routes for the A2A protocol REST endpoint.

## `tasks/__init__.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/__init__.py).

<!-- declaration:tasks/__init__.py:39:DatabaseTaskStore -->
### `DatabaseTaskStore` — line 39

```python
class DatabaseTaskStore()
```

Source: [DatabaseTaskStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/__init__.py:39).

Source-docstring summary: Placeholder for DatabaseTaskStore when dependencies are not installed.

<!-- declaration:tasks/__init__.py:42:DatabaseTaskStore.__init__ -->
### `DatabaseTaskStore.__init__` — line 42

```python
def __init__(self, *args, **kwargs)
```

Source: [DatabaseTaskStore.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/__init__.py:42).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:tasks/__init__.py:61:DatabasePushNotificationConfigStore -->
### `DatabasePushNotificationConfigStore` — line 61

```python
class DatabasePushNotificationConfigStore()
```

Source: [DatabasePushNotificationConfigStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/__init__.py:61).

Source-docstring summary: Placeholder for DatabasePushNotificationConfigStore when dependencies are not installed.

<!-- declaration:tasks/__init__.py:64:DatabasePushNotificationConfigStore.__init__ -->
### `DatabasePushNotificationConfigStore.__init__` — line 64

```python
def __init__(self, *args, **kwargs)
```

Source: [DatabasePushNotificationConfigStore.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/__init__.py:64).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

## `tasks/base_push_notification_sender.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/base_push_notification_sender.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/base_push_notification_sender.py).

<!-- declaration:tasks/base_push_notification_sender.py:25:BasePushNotificationSender -->
### `BasePushNotificationSender` — line 25

```python
class BasePushNotificationSender(PushNotificationSender)
```

Source: [BasePushNotificationSender](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/base_push_notification_sender.py:25).

Source-docstring summary: Base implementation of PushNotificationSender interface.

<!-- declaration:tasks/base_push_notification_sender.py:28:BasePushNotificationSender.__init__ -->
### `BasePushNotificationSender.__init__` — line 28

```python
def __init__(self, httpx_client: httpx.AsyncClient, config_store: PushNotificationConfigStore, context: ServerCallContext | None=None, *, push_url_validator: Callable[[str], Awaitable[bool]] | None=None) -> None
```

Source: [BasePushNotificationSender.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/base_push_notification_sender.py:28).

Source-docstring summary: Initializes the BasePushNotificationSender.

<!-- declaration:tasks/base_push_notification_sender.py:68:BasePushNotificationSender.send_notification -->
### `BasePushNotificationSender.send_notification` — line 68

```python
async def send_notification(self, task_id: str, event: PushNotificationEvent) -> None
```

Source: [BasePushNotificationSender.send_notification](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/base_push_notification_sender.py:68).

Source-docstring summary: Sends a push notification for an event if configuration exists.

<!-- declaration:tasks/base_push_notification_sender.py:87:BasePushNotificationSender._dispatch_notification -->
### `BasePushNotificationSender._dispatch_notification` — line 87

```python
async def _dispatch_notification(self, event: PushNotificationEvent, push_info: TaskPushNotificationConfig, task_id: str) -> bool
```

Source: [BasePushNotificationSender._dispatch_notification](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/base_push_notification_sender.py:87).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

## `tasks/copying_task_store.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/copying_task_store.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/copying_task_store.py).

<!-- declaration:tasks/copying_task_store.py:17:CopyingTaskStoreAdapter -->
### `CopyingTaskStoreAdapter` — line 17

```python
class CopyingTaskStoreAdapter(TaskStore)
```

Source: [CopyingTaskStoreAdapter](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/copying_task_store.py:17).

Source-docstring summary: An adapter that ensures deep copies of tasks are passed to and returned from the underlying TaskStore.

<!-- declaration:tasks/copying_task_store.py:24:CopyingTaskStoreAdapter.__init__ -->
### `CopyingTaskStoreAdapter.__init__` — line 24

```python
def __init__(self, underlying_store: TaskStore)
```

Source: [CopyingTaskStoreAdapter.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/copying_task_store.py:24).

Source-docstring summary: Initializes the enclosing object or optional-dependency placeholder; constructor defaults and effects are covered in the linked guide.

<!-- declaration:tasks/copying_task_store.py:27:CopyingTaskStoreAdapter.save -->
### `CopyingTaskStoreAdapter.save` — line 27

```python
async def save(self, task: Task, context: ServerCallContext) -> None
```

Source: [CopyingTaskStoreAdapter.save](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/copying_task_store.py:27).

Source-docstring summary: Saves a copy of the task to the underlying store.

<!-- declaration:tasks/copying_task_store.py:33:CopyingTaskStoreAdapter.get -->
### `CopyingTaskStoreAdapter.get` — line 33

```python
async def get(self, task_id: str, context: ServerCallContext) -> Task | None
```

Source: [CopyingTaskStoreAdapter.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/copying_task_store.py:33).

Source-docstring summary: Retrieves a task from the underlying store and returns a copy.

<!-- declaration:tasks/copying_task_store.py:44:CopyingTaskStoreAdapter.list -->
### `CopyingTaskStoreAdapter.list` — line 44

```python
async def list(self, params: ListTasksRequest, context: ServerCallContext) -> ListTasksResponse
```

Source: [CopyingTaskStoreAdapter.list](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/copying_task_store.py:44).

Source-docstring summary: Retrieves a list of tasks from the underlying store and returns a copy.

<!-- declaration:tasks/copying_task_store.py:55:CopyingTaskStoreAdapter.delete -->
### `CopyingTaskStoreAdapter.delete` — line 55

```python
async def delete(self, task_id: str, context: ServerCallContext) -> None
```

Source: [CopyingTaskStoreAdapter.delete](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/copying_task_store.py:55).

Source-docstring summary: Deletes a task from the underlying store.

## `tasks/database_push_notification_config_store.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/database_push_notification_config_store.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py).

<!-- declaration:tasks/database_push_notification_config_store.py:51:DatabasePushNotificationConfigStore -->
### `DatabasePushNotificationConfigStore` — line 51

```python
class DatabasePushNotificationConfigStore(PushNotificationConfigStore)
```

Source: [DatabasePushNotificationConfigStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:51).

Source-docstring summary: SQLAlchemy-based implementation of PushNotificationConfigStore.

<!-- declaration:tasks/database_push_notification_config_store.py:76:DatabasePushNotificationConfigStore.__init__ -->
### `DatabasePushNotificationConfigStore.__init__` — line 76

```python
def __init__(self, engine: AsyncEngine, create_table: bool=True, table_name: str='push_notification_configs', encryption_key: str | bytes | None=None, owner_resolver: OwnerResolver=resolve_user_scope, core_to_model_conversion: Callable[[str, TaskPushNotificationConfig, str, 'Fernet | None'], PushNotificationConfigModel] | None=None, model_to_core_conversion: Callable[[PushNotificationConfigModel], TaskPushNotificationConfig] | None=None) -> None
```

Source: [DatabasePushNotificationConfigStore.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:76).

Source-docstring summary: Initializes the DatabasePushNotificationConfigStore.

<!-- declaration:tasks/database_push_notification_config_store.py:145:DatabasePushNotificationConfigStore.initialize -->
### `DatabasePushNotificationConfigStore.initialize` — line 145

```python
async def initialize(self) -> None
```

Source: [DatabasePushNotificationConfigStore.initialize](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:145).

Source-docstring summary: Initialize the database and create the table if needed.

<!-- declaration:tasks/database_push_notification_config_store.py:167:DatabasePushNotificationConfigStore._ensure_initialized -->
### `DatabasePushNotificationConfigStore._ensure_initialized` — line 167

```python
async def _ensure_initialized(self) -> None
```

Source: [DatabasePushNotificationConfigStore._ensure_initialized](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:167).

Source-docstring summary: Ensure the database connection is initialized.

<!-- declaration:tasks/database_push_notification_config_store.py:172:DatabasePushNotificationConfigStore._to_orm -->
### `DatabasePushNotificationConfigStore._to_orm` — line 172

```python
def _to_orm(self, task_id: str, config: TaskPushNotificationConfig, owner: str) -> PushNotificationConfigModel
```

Source: [DatabasePushNotificationConfigStore._to_orm](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:172).

Source-docstring summary: Maps a TaskPushNotificationConfig proto to a SQLAlchemy model instance.

<!-- declaration:tasks/database_push_notification_config_store.py:199:DatabasePushNotificationConfigStore._from_orm -->
### `DatabasePushNotificationConfigStore._from_orm` — line 199

```python
def _from_orm(self, model_instance: PushNotificationConfigModel) -> TaskPushNotificationConfig
```

Source: [DatabasePushNotificationConfigStore._from_orm](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:199).

Source-docstring summary: Maps a SQLAlchemy model instance to a TaskPushNotificationConfig proto.

<!-- declaration:tasks/database_push_notification_config_store.py:281:DatabasePushNotificationConfigStore.set_info -->
### `DatabasePushNotificationConfigStore.set_info` — line 281

```python
async def set_info(self, task_id: str, notification_config: TaskPushNotificationConfig, context: ServerCallContext) -> None
```

Source: [DatabasePushNotificationConfigStore.set_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:281).

Source-docstring summary: Sets or updates the push notification configuration for a task.

<!-- declaration:tasks/database_push_notification_config_store.py:307:DatabasePushNotificationConfigStore._select_configs -->
### `DatabasePushNotificationConfigStore._select_configs` — line 307

```python
async def _select_configs(self, *predicates: 'ColumnElement[bool]') -> list[TaskPushNotificationConfig]
```

Source: [DatabasePushNotificationConfigStore._select_configs](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:307).

Source-docstring summary: Loads configs matching the given predicates and decodes them.

<!-- declaration:tasks/database_push_notification_config_store.py:331:DatabasePushNotificationConfigStore.get_info -->
### `DatabasePushNotificationConfigStore.get_info` — line 331

```python
async def get_info(self, task_id: str, context: ServerCallContext) -> list[TaskPushNotificationConfig]
```

Source: [DatabasePushNotificationConfigStore.get_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:331).

Source-docstring summary: Retrieves all push notification configurations for a task, for the given owner.

<!-- declaration:tasks/database_push_notification_config_store.py:346:DatabasePushNotificationConfigStore.get_info_for_dispatch -->
### `DatabasePushNotificationConfigStore.get_info_for_dispatch` — line 346

```python
async def get_info_for_dispatch(self, task_id: str) -> list[TaskPushNotificationConfig]
```

Source: [DatabasePushNotificationConfigStore.get_info_for_dispatch](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:346).

Source-docstring summary: Retrieves all push notification configurations for a task, across all owners.

<!-- declaration:tasks/database_push_notification_config_store.py:358:DatabasePushNotificationConfigStore.delete_info -->
### `DatabasePushNotificationConfigStore.delete_info` — line 358

```python
async def delete_info(self, task_id: str, context: ServerCallContext, config_id: str | None=None) -> None
```

Source: [DatabasePushNotificationConfigStore.delete_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:358).

Source-docstring summary: Deletes push notification configurations for a task.

<!-- declaration:tasks/database_push_notification_config_store.py:398:DatabasePushNotificationConfigStore._parse_config -->
### `DatabasePushNotificationConfigStore._parse_config` — line 398

```python
def _parse_config(self, json_payload: str, task_id: str | None=None, protocol_version: str | None=None) -> TaskPushNotificationConfig
```

Source: [DatabasePushNotificationConfigStore._parse_config](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_push_notification_config_store.py:398).

Source-docstring summary: Parses a JSON payload into a TaskPushNotificationConfig proto.

## `tasks/database_task_store.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/database_task_store.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py).

<!-- declaration:tasks/database_task_store.py:43:DatabaseTaskStore -->
### `DatabaseTaskStore` — line 43

```python
class DatabaseTaskStore(TaskStore)
```

Source: [DatabaseTaskStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:43).

Source-docstring summary: SQLAlchemy-based implementation of TaskStore.

<!-- declaration:tasks/database_task_store.py:58:DatabaseTaskStore.__init__ -->
### `DatabaseTaskStore.__init__` — line 58

```python
def __init__(self, engine: AsyncEngine, create_table: bool=True, table_name: str='tasks', owner_resolver: OwnerResolver=resolve_user_scope, core_to_model_conversion: Callable[[Task, str], TaskModel] | None=None, model_to_core_conversion: Callable[[TaskModel], Task] | None=None) -> None
```

Source: [DatabaseTaskStore.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:58).

Source-docstring summary: Initializes the DatabaseTaskStore.

<!-- declaration:tasks/database_task_store.py:98:DatabaseTaskStore.initialize -->
### `DatabaseTaskStore.initialize` — line 98

```python
async def initialize(self) -> None
```

Source: [DatabaseTaskStore.initialize](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:98).

Source-docstring summary: Initialize the database and create the table if needed.

<!-- declaration:tasks/database_task_store.py:116:DatabaseTaskStore._ensure_initialized -->
### `DatabaseTaskStore._ensure_initialized` — line 116

```python
async def _ensure_initialized(self) -> None
```

Source: [DatabaseTaskStore._ensure_initialized](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:116).

Source-docstring summary: Ensure the database connection is initialized.

<!-- declaration:tasks/database_task_store.py:121:DatabaseTaskStore._to_orm -->
### `DatabaseTaskStore._to_orm` — line 121

```python
def _to_orm(self, task: Task, owner: str) -> TaskModel
```

Source: [DatabaseTaskStore._to_orm](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:121).

Source-docstring summary: Maps a Proto Task to a SQLAlchemy TaskModel instance.

<!-- declaration:tasks/database_task_store.py:145:DatabaseTaskStore._from_orm -->
### `DatabaseTaskStore._from_orm` — line 145

```python
def _from_orm(self, task_model: TaskModel) -> Task
```

Source: [DatabaseTaskStore._from_orm](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:145).

Source-docstring summary: Maps a SQLAlchemy TaskModel to a Proto Task instance.

<!-- declaration:tasks/database_task_store.py:172:DatabaseTaskStore.save -->
### `DatabaseTaskStore.save` — line 172

```python
async def save(self, task: Task, context: ServerCallContext) -> None
```

Source: [DatabaseTaskStore.save](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:172).

Source-docstring summary: Saves or updates a task in the database for the resolved owner.

<!-- declaration:tasks/database_task_store.py:185:DatabaseTaskStore.get -->
### `DatabaseTaskStore.get` — line 185

```python
async def get(self, task_id: str, context: ServerCallContext) -> Task | None
```

Source: [DatabaseTaskStore.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:185).

Source-docstring summary: Retrieves a task from the database by ID, for the given owner.

<!-- declaration:tasks/database_task_store.py:214:DatabaseTaskStore.list -->
### `DatabaseTaskStore.list` — line 214

```python
async def list(self, params: a2a_pb2.ListTasksRequest, context: ServerCallContext) -> a2a_pb2.ListTasksResponse
```

Source: [DatabaseTaskStore.list](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:214).

Source-docstring summary: Retrieves tasks from the database based on provided parameters, for the given owner.

<!-- declaration:tasks/database_task_store.py:316:DatabaseTaskStore.delete -->
### `DatabaseTaskStore.delete` — line 316

```python
async def delete(self, task_id: str, context: ServerCallContext) -> None
```

Source: [DatabaseTaskStore.delete](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/database_task_store.py:316).

Source-docstring summary: Deletes a task from the database by ID, for the given owner.

## `tasks/inmemory_push_notification_config_store.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/inmemory_push_notification_config_store.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py).

<!-- declaration:tasks/inmemory_push_notification_config_store.py:15:InMemoryPushNotificationConfigStore -->
### `InMemoryPushNotificationConfigStore` — line 15

```python
class InMemoryPushNotificationConfigStore(PushNotificationConfigStore)
```

Source: [InMemoryPushNotificationConfigStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py:15).

Source-docstring summary: In-memory implementation of PushNotificationConfigStore interface.

<!-- declaration:tasks/inmemory_push_notification_config_store.py:22:InMemoryPushNotificationConfigStore.__init__ -->
### `InMemoryPushNotificationConfigStore.__init__` — line 22

```python
def __init__(self, owner_resolver: OwnerResolver=resolve_user_scope) -> None
```

Source: [InMemoryPushNotificationConfigStore.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py:22).

Source-docstring summary: Initializes the InMemoryPushNotificationConfigStore.

<!-- declaration:tasks/inmemory_push_notification_config_store.py:33:InMemoryPushNotificationConfigStore._get_owner_push_notification_infos -->
### `InMemoryPushNotificationConfigStore._get_owner_push_notification_infos` — line 33

```python
def _get_owner_push_notification_infos(self, owner: str) -> dict[str, list[TaskPushNotificationConfig]]
```

Source: [InMemoryPushNotificationConfigStore._get_owner_push_notification_infos](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py:33).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:tasks/inmemory_push_notification_config_store.py:38:InMemoryPushNotificationConfigStore.set_info -->
### `InMemoryPushNotificationConfigStore.set_info` — line 38

```python
async def set_info(self, task_id: str, notification_config: TaskPushNotificationConfig, context: ServerCallContext) -> None
```

Source: [InMemoryPushNotificationConfigStore.set_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py:38).

Source-docstring summary: Sets or updates the push notification configuration for a task in memory.

<!-- declaration:tasks/inmemory_push_notification_config_store.py:68:InMemoryPushNotificationConfigStore.get_info -->
### `InMemoryPushNotificationConfigStore.get_info` — line 68

```python
async def get_info(self, task_id: str, context: ServerCallContext) -> list[TaskPushNotificationConfig]
```

Source: [InMemoryPushNotificationConfigStore.get_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py:68).

Source-docstring summary: Retrieves all push notification configurations for a task from memory, for the given owner.

<!-- declaration:tasks/inmemory_push_notification_config_store.py:82:InMemoryPushNotificationConfigStore.get_info_for_dispatch -->
### `InMemoryPushNotificationConfigStore.get_info_for_dispatch` — line 82

```python
async def get_info_for_dispatch(self, task_id: str) -> list[TaskPushNotificationConfig]
```

Source: [InMemoryPushNotificationConfigStore.get_info_for_dispatch](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py:82).

Source-docstring summary: Retrieves all push notification configurations for a task across all owners.

<!-- declaration:tasks/inmemory_push_notification_config_store.py:96:InMemoryPushNotificationConfigStore.delete_info -->
### `InMemoryPushNotificationConfigStore.delete_info` — line 96

```python
async def delete_info(self, task_id: str, context: ServerCallContext, config_id: str | None=None) -> None
```

Source: [InMemoryPushNotificationConfigStore.delete_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_push_notification_config_store.py:96).

Source-docstring summary: Deletes push notification configurations for a task from memory.

## `tasks/inmemory_task_store.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/inmemory_task_store.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py).

<!-- declaration:tasks/inmemory_task_store.py:18:_InMemoryTaskStoreImpl -->
### `_InMemoryTaskStoreImpl` — line 18

```python
class _InMemoryTaskStoreImpl(TaskStore)
```

Source: [_InMemoryTaskStoreImpl](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:18).

Source-docstring summary: Internal In-memory implementation of TaskStore.

<!-- declaration:tasks/inmemory_task_store.py:25:_InMemoryTaskStoreImpl.__init__ -->
### `_InMemoryTaskStoreImpl.__init__` — line 25

```python
def __init__(self, owner_resolver: OwnerResolver=resolve_user_scope) -> None
```

Source: [_InMemoryTaskStoreImpl.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:25).

Source-docstring summary: Initializes the internal _InMemoryTaskStoreImpl.

<!-- declaration:tasks/inmemory_task_store.py:35:_InMemoryTaskStoreImpl._get_owner_tasks -->
### `_InMemoryTaskStoreImpl._get_owner_tasks` — line 35

```python
def _get_owner_tasks(self, owner: str) -> dict[str, Task]
```

Source: [_InMemoryTaskStoreImpl._get_owner_tasks](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:35).

Source-docstring summary: No callable docstring; inspect the linked behavioral guide and exact implementation for delegation, side effects, and errors.

<!-- declaration:tasks/inmemory_task_store.py:38:_InMemoryTaskStoreImpl.save -->
### `_InMemoryTaskStoreImpl.save` — line 38

```python
async def save(self, task: Task, context: ServerCallContext) -> None
```

Source: [_InMemoryTaskStoreImpl.save](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:38).

Source-docstring summary: Saves or updates a task in the in-memory store for the resolved owner.

<!-- declaration:tasks/inmemory_task_store.py:48:_InMemoryTaskStoreImpl.get -->
### `_InMemoryTaskStoreImpl.get` — line 48

```python
async def get(self, task_id: str, context: ServerCallContext) -> Task | None
```

Source: [_InMemoryTaskStoreImpl.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:48).

Source-docstring summary: Retrieves a task from the in-memory store by ID, for the given owner.

<!-- declaration:tasks/inmemory_task_store.py:73:_InMemoryTaskStoreImpl.list -->
### `_InMemoryTaskStoreImpl.list` — line 73

```python
async def list(self, params: a2a_pb2.ListTasksRequest, context: ServerCallContext) -> a2a_pb2.ListTasksResponse
```

Source: [_InMemoryTaskStoreImpl.list](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:73).

Source-docstring summary: Retrieves a list of tasks from the store, for the given owner.

<!-- declaration:tasks/inmemory_task_store.py:155:_InMemoryTaskStoreImpl.delete -->
### `_InMemoryTaskStoreImpl.delete` — line 155

```python
async def delete(self, task_id: str, context: ServerCallContext) -> None
```

Source: [_InMemoryTaskStoreImpl.delete](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:155).

Source-docstring summary: Deletes a task from the in-memory store by ID, for the given owner.

<!-- declaration:tasks/inmemory_task_store.py:183:InMemoryTaskStore -->
### `InMemoryTaskStore` — line 183

```python
class InMemoryTaskStore(TaskStore)
```

Source: [InMemoryTaskStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:183).

Source-docstring summary: In-memory implementation of TaskStore.

<!-- declaration:tasks/inmemory_task_store.py:191:InMemoryTaskStore.__init__ -->
### `InMemoryTaskStore.__init__` — line 191

```python
def __init__(self, owner_resolver: OwnerResolver=resolve_user_scope, use_copying: bool=True) -> None
```

Source: [InMemoryTaskStore.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:191).

Source-docstring summary: Initializes the InMemoryTaskStore.

<!-- declaration:tasks/inmemory_task_store.py:208:InMemoryTaskStore.save -->
### `InMemoryTaskStore.save` — line 208

```python
async def save(self, task: Task, context: ServerCallContext) -> None
```

Source: [InMemoryTaskStore.save](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:208).

Source-docstring summary: Saves or updates a task in the store.

<!-- declaration:tasks/inmemory_task_store.py:212:InMemoryTaskStore.get -->
### `InMemoryTaskStore.get` — line 212

```python
async def get(self, task_id: str, context: ServerCallContext) -> Task | None
```

Source: [InMemoryTaskStore.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:212).

Source-docstring summary: Retrieves a task from the store by ID.

<!-- declaration:tasks/inmemory_task_store.py:218:InMemoryTaskStore.list -->
### `InMemoryTaskStore.list` — line 218

```python
async def list(self, params: a2a_pb2.ListTasksRequest, context: ServerCallContext) -> a2a_pb2.ListTasksResponse
```

Source: [InMemoryTaskStore.list](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:218).

Source-docstring summary: Retrieves a list of tasks from the store.

<!-- declaration:tasks/inmemory_task_store.py:226:InMemoryTaskStore.delete -->
### `InMemoryTaskStore.delete` — line 226

```python
async def delete(self, task_id: str, context: ServerCallContext) -> None
```

Source: [InMemoryTaskStore.delete](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/inmemory_task_store.py:226).

Source-docstring summary: Deletes a task from the store by ID.

## `tasks/push_notification_config_store.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/push_notification_config_store.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_config_store.py).

<!-- declaration:tasks/push_notification_config_store.py:12:PushNotificationConfigStore -->
### `PushNotificationConfigStore` — line 12

```python
class PushNotificationConfigStore(ABC)
```

Source: [PushNotificationConfigStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_config_store.py:12).

Source-docstring summary: Interface for storing and retrieving push notification configurations for tasks.

<!-- declaration:tasks/push_notification_config_store.py:16:PushNotificationConfigStore.set_info -->
### `PushNotificationConfigStore.set_info` — line 16

```python
async def set_info(self, task_id: str, notification_config: TaskPushNotificationConfig, context: ServerCallContext) -> None
```

Source: [PushNotificationConfigStore.set_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_config_store.py:16).

Source-docstring summary: Sets or updates the push notification configuration for a task.

<!-- declaration:tasks/push_notification_config_store.py:25:PushNotificationConfigStore.get_info -->
### `PushNotificationConfigStore.get_info` — line 25

```python
async def get_info(self, task_id: str, context: ServerCallContext) -> list[TaskPushNotificationConfig]
```

Source: [PushNotificationConfigStore.get_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_config_store.py:25).

Source-docstring summary: Retrieves push notification configurations for a task, scoped to the caller.

<!-- declaration:tasks/push_notification_config_store.py:37:PushNotificationConfigStore.get_info_for_dispatch -->
### `PushNotificationConfigStore.get_info_for_dispatch` — line 37

```python
async def get_info_for_dispatch(self, task_id: str) -> list[TaskPushNotificationConfig]
```

Source: [PushNotificationConfigStore.get_info_for_dispatch](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_config_store.py:37).

Source-docstring summary: Retrieves all push notification configurations for a task, across all owners.

<!-- declaration:tasks/push_notification_config_store.py:72:PushNotificationConfigStore.delete_info -->
### `PushNotificationConfigStore.delete_info` — line 72

```python
async def delete_info(self, task_id: str, context: ServerCallContext, config_id: str | None=None) -> None
```

Source: [PushNotificationConfigStore.delete_info](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_config_store.py:72).

Source-docstring summary: Deletes the push notification configuration for a task.

## `tasks/push_notification_sender.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/push_notification_sender.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_sender.py).

<!-- declaration:tasks/push_notification_sender.py:13:PushNotificationSender -->
### `PushNotificationSender` — line 13

```python
class PushNotificationSender(ABC)
```

Source: [PushNotificationSender](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_sender.py:13).

Source-docstring summary: Interface for sending push notifications for tasks.

<!-- declaration:tasks/push_notification_sender.py:17:PushNotificationSender.send_notification -->
### `PushNotificationSender.send_notification` — line 17

```python
async def send_notification(self, task_id: str, event: PushNotificationEvent) -> None
```

Source: [PushNotificationSender.send_notification](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/push_notification_sender.py:17).

Source-docstring summary: Sends a push notification containing the latest task state.

## `tasks/result_aggregator.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/result_aggregator.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py).

<!-- declaration:tasks/result_aggregator.py:14:ResultAggregator -->
### `ResultAggregator` — line 14

```python
class ResultAggregator()
```

Source: [ResultAggregator](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py:14).

Source-docstring summary: ResultAggregator is used to process the event streams from an AgentExecutor.

<!-- declaration:tasks/result_aggregator.py:27:ResultAggregator.__init__ -->
### `ResultAggregator.__init__` — line 27

```python
def __init__(self, task_manager: TaskManager) -> None
```

Source: [ResultAggregator.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py:27).

Source-docstring summary: Initializes the ResultAggregator.

<!-- declaration:tasks/result_aggregator.py:41:ResultAggregator.current_result -->
### `ResultAggregator.current_result` — line 41

```python
async def current_result(self) -> Task | Message | None
```

Source: [ResultAggregator.current_result](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py:41).

Source-docstring summary: Returns the current aggregated result (Task or Message).

<!-- declaration:tasks/result_aggregator.py:54:ResultAggregator.consume_and_emit -->
### `ResultAggregator.consume_and_emit` — line 54

```python
async def consume_and_emit(self, consumer: EventConsumer) -> AsyncGenerator[Event]
```

Source: [ResultAggregator.consume_and_emit](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py:54).

Source-docstring summary: Processes the event stream from the consumer, updates the task state, and re-emits the same events.

<!-- declaration:tasks/result_aggregator.py:73:ResultAggregator.consume_all -->
### `ResultAggregator.consume_all` — line 73

```python
async def consume_all(self, consumer: EventConsumer) -> Task | Message | None
```

Source: [ResultAggregator.consume_all](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py:73).

Source-docstring summary: Processes the entire event stream from the consumer and returns the final result.

<!-- declaration:tasks/result_aggregator.py:97:ResultAggregator.consume_and_break_on_interrupt -->
### `ResultAggregator.consume_and_break_on_interrupt` — line 97

```python
async def consume_and_break_on_interrupt(self, consumer: EventConsumer, blocking: bool=True, event_callback: Callable[[Event], Awaitable[None]] | None=None) -> tuple[Task | Message | None, bool, asyncio.Task | None]
```

Source: [ResultAggregator.consume_and_break_on_interrupt](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py:97).

Source-docstring summary: Processes the event stream until completion or an interruptible state is encountered.

<!-- declaration:tasks/result_aggregator.py:179:ResultAggregator._continue_consuming -->
### `ResultAggregator._continue_consuming` — line 179

```python
async def _continue_consuming(self, event_stream: AsyncIterator[Event], event_callback: Callable[[Event], Awaitable[None]] | None=None) -> None
```

Source: [ResultAggregator._continue_consuming](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/result_aggregator.py:179).

Source-docstring summary: Continues processing an event stream in a background task.

## `tasks/task_manager.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/task_manager.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py).

<!-- declaration:tasks/task_manager.py:23:append_artifact_to_task -->
### `append_artifact_to_task` — line 23

```python
def append_artifact_to_task(task: Task, event: TaskArtifactUpdateEvent) -> None
```

Source: [append_artifact_to_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:23).

Source-docstring summary: Helper method for updating a Task object with new artifact data from an event.

<!-- declaration:tasks/task_manager.py:90:TaskManager -->
### `TaskManager` — line 90

```python
class TaskManager()
```

Source: [TaskManager](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:90).

Source-docstring summary: Helps manage a task's lifecycle during execution of a request.

<!-- declaration:tasks/task_manager.py:97:TaskManager.__init__ -->
### `TaskManager.__init__` — line 97

```python
def __init__(self, task_store: TaskStore, context: ServerCallContext, task_id: str | None, context_id: str | None, initial_message: Message | None)
```

Source: [TaskManager.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:97).

Source-docstring summary: Initializes the TaskManager.

<!-- declaration:tasks/task_manager.py:130:TaskManager.get_task -->
### `TaskManager.get_task` — line 130

```python
async def get_task(self) -> Task | None
```

Source: [TaskManager.get_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:130).

Source-docstring summary: Retrieves the current task object, either from memory or the store.

<!-- declaration:tasks/task_manager.py:158:TaskManager.save_task_event -->
### `TaskManager.save_task_event` — line 158

```python
async def save_task_event(self, event: Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent) -> Task | None
```

Source: [TaskManager.save_task_event](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:158).

Source-docstring summary: Processes a task-related event (Task, Status, Artifact) and saves the updated task state.

<!-- declaration:tasks/task_manager.py:219:TaskManager.ensure_task_id -->
### `TaskManager.ensure_task_id` — line 219

```python
async def ensure_task_id(self, task_id: str, context_id: str) -> Task
```

Source: [TaskManager.ensure_task_id](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:219).

Source-docstring summary: Ensures a Task object exists in memory, loading from store or creating new if needed.

<!-- declaration:tasks/task_manager.py:249:TaskManager.ensure_task -->
### `TaskManager.ensure_task` — line 249

```python
async def ensure_task(self, event: TaskStatusUpdateEvent | TaskArtifactUpdateEvent) -> Task
```

Source: [TaskManager.ensure_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:249).

Source-docstring summary: Ensures a Task object exists in memory, loading from store or creating new if needed.

<!-- declaration:tasks/task_manager.py:262:TaskManager.process -->
### `TaskManager.process` — line 262

```python
async def process(self, event: Event) -> Event
```

Source: [TaskManager.process](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:262).

Source-docstring summary: Processes an event, updates the task state if applicable, stores it, and returns the event.

<!-- declaration:tasks/task_manager.py:281:TaskManager._init_task_obj -->
### `TaskManager._init_task_obj` — line 281

```python
def _init_task_obj(self, task_id: str, context_id: str) -> Task
```

Source: [TaskManager._init_task_obj](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:281).

Source-docstring summary: Initializes a new task object in memory.

<!-- declaration:tasks/task_manager.py:304:TaskManager._save_task -->
### `TaskManager._save_task` — line 304

```python
async def _save_task(self, task: Task) -> None
```

Source: [TaskManager._save_task](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:304).

Source-docstring summary: Saves the given task to the task store and updates the in-memory `_current_task`.

<!-- declaration:tasks/task_manager.py:318:TaskManager.update_with_message -->
### `TaskManager.update_with_message` — line 318

```python
def update_with_message(self, message: Message, task: Task) -> Task
```

Source: [TaskManager.update_with_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_manager.py:318).

Source-docstring summary: Updates a task object in memory by adding a new message to its history.

## `tasks/task_store.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/task_store.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_store.py).

<!-- declaration:tasks/task_store.py:7:TaskStore -->
### `TaskStore` — line 7

```python
class TaskStore(ABC)
```

Source: [TaskStore](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_store.py:7).

Source-docstring summary: Agent Task Store interface.

<!-- declaration:tasks/task_store.py:14:TaskStore.save -->
### `TaskStore.save` — line 14

```python
async def save(self, task: Task, context: ServerCallContext) -> None
```

Source: [TaskStore.save](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_store.py:14).

Source-docstring summary: Saves or updates a task in the store.

<!-- declaration:tasks/task_store.py:18:TaskStore.get -->
### `TaskStore.get` — line 18

```python
async def get(self, task_id: str, context: ServerCallContext) -> Task | None
```

Source: [TaskStore.get](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_store.py:18).

Source-docstring summary: Retrieves a task from the store by ID.

<!-- declaration:tasks/task_store.py:24:TaskStore.list -->
### `TaskStore.list` — line 24

```python
async def list(self, params: ListTasksRequest, context: ServerCallContext) -> ListTasksResponse
```

Source: [TaskStore.list](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_store.py:24).

Source-docstring summary: Retrieves a list of tasks from the store.

<!-- declaration:tasks/task_store.py:32:TaskStore.delete -->
### `TaskStore.delete` — line 32

```python
async def delete(self, task_id: str, context: ServerCallContext) -> None
```

Source: [TaskStore.delete](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_store.py:32).

Source-docstring summary: Deletes a task from the store by ID.

## `tasks/task_updater.py`

Behavior: [tasks_knowledge.md](tasks_knowledge.md). Source: [tasks/task_updater.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py).

<!-- declaration:tasks/task_updater.py:26:TaskUpdater -->
### `TaskUpdater` — line 26

```python
class TaskUpdater()
```

Source: [TaskUpdater](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:26).

Source-docstring summary: Helper class for agents to publish updates to a task's event queue.

<!-- declaration:tasks/task_updater.py:32:TaskUpdater.__init__ -->
### `TaskUpdater.__init__` — line 32

```python
def __init__(self, event_queue: EventQueue, task_id: str, context_id: str, artifact_id_generator: IDGenerator | None=None, message_id_generator: IDGenerator | None=None)
```

Source: [TaskUpdater.__init__](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:32).

Source-docstring summary: Initializes the TaskUpdater.

<!-- declaration:tasks/task_updater.py:67:TaskUpdater.update_status -->
### `TaskUpdater.update_status` — line 67

```python
async def update_status(self, state: TaskState, message: Message | None=None, timestamp: str | None=None, metadata: dict[str, Any] | None=None) -> None
```

Source: [TaskUpdater.update_status](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:67).

Source-docstring summary: Updates the status of the task and publishes a `TaskStatusUpdateEvent`.

<!-- declaration:tasks/task_updater.py:113:TaskUpdater.add_artifact -->
### `TaskUpdater.add_artifact` — line 113

```python
async def add_artifact(self, parts: list[Part], artifact_id: str | None=None, name: str | None=None, metadata: dict[str, Any] | None=None, append: bool | None=None, last_chunk: bool | None=None, extensions: list[str] | None=None) -> None
```

Source: [TaskUpdater.add_artifact](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:113).

Source-docstring summary: Adds an artifact chunk to the task and publishes a `TaskArtifactUpdateEvent`.

<!-- declaration:tasks/task_updater.py:157:TaskUpdater.complete -->
### `TaskUpdater.complete` — line 157

```python
async def complete(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.complete](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:157).

Source-docstring summary: Marks the task as completed and publishes a final status update.

<!-- declaration:tasks/task_updater.py:164:TaskUpdater.failed -->
### `TaskUpdater.failed` — line 164

```python
async def failed(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.failed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:164).

Source-docstring summary: Marks the task as failed and publishes a final status update.

<!-- declaration:tasks/task_updater.py:171:TaskUpdater.reject -->
### `TaskUpdater.reject` — line 171

```python
async def reject(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.reject](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:171).

Source-docstring summary: Marks the task as rejected and publishes a final status update.

<!-- declaration:tasks/task_updater.py:178:TaskUpdater.submit -->
### `TaskUpdater.submit` — line 178

```python
async def submit(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.submit](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:178).

Source-docstring summary: Marks the task as submitted and publishes a status update.

<!-- declaration:tasks/task_updater.py:185:TaskUpdater.start_work -->
### `TaskUpdater.start_work` — line 185

```python
async def start_work(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.start_work](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:185).

Source-docstring summary: Marks the task as working and publishes a status update.

<!-- declaration:tasks/task_updater.py:192:TaskUpdater.cancel -->
### `TaskUpdater.cancel` — line 192

```python
async def cancel(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.cancel](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:192).

Source-docstring summary: Marks the task as cancelled and publishes a finalstatus update.

<!-- declaration:tasks/task_updater.py:199:TaskUpdater.requires_input -->
### `TaskUpdater.requires_input` — line 199

```python
async def requires_input(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.requires_input](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:199).

Source-docstring summary: Marks the task as input required and publishes a status update.

<!-- declaration:tasks/task_updater.py:206:TaskUpdater.requires_auth -->
### `TaskUpdater.requires_auth` — line 206

```python
async def requires_auth(self, message: Message | None=None) -> None
```

Source: [TaskUpdater.requires_auth](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:206).

Source-docstring summary: Marks the task as auth required and publishes a status update.

<!-- declaration:tasks/task_updater.py:212:TaskUpdater.new_agent_message -->
### `TaskUpdater.new_agent_message` — line 212

```python
def new_agent_message(self, parts: list[Part], metadata: dict[str, Any] | None=None) -> Message
```

Source: [TaskUpdater.new_agent_message](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/server/tasks/task_updater.py:212).

Source-docstring summary: Creates a new message object sent by the agent for this task/context.

