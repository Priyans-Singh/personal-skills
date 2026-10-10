"""Small task-based A2A 1.0 server; run with an ASGI server of your choice.

Demo uses anonymous, process-local storage. Add verified authentication and
owner resolution before exposing private task data.
"""
from contextlib import asynccontextmanager

from starlette.applications import Starlette

from a2a.helpers.proto_helpers import new_task_from_user_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
    create_rest_routes,
)
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill


class EchoExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None or not context.task_id or not context.context_id:
            raise ValueError("A message and both IDs are required")
        if context.current_task is None:
            await event_queue.enqueue_event(new_task_from_user_message(context.message))
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.start_work()
        await updater.add_artifact(
            [new_text_part(context.get_user_input())], name="echo", last_chunk=True
        )
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.task_id and context.context_id:
            await TaskUpdater(event_queue, context.task_id, context.context_id).cancel()


def create_app() -> Starlette:
    card = AgentCard(
        name="Echo agent",
        description="Echoes user text as a task artifact",
        version="1.0.0",
        supported_interfaces=[
            AgentInterface(
                url="http://localhost:8000",
                protocol_binding="HTTP+JSON",
                protocol_version="1.0",
            ),
            AgentInterface(
                url="http://localhost:8000/rpc",
                protocol_binding="JSONRPC",
                protocol_version="1.0",
            ),
        ],
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        skills=[AgentSkill(id="echo", name="Echo", description="Echo text", tags=["demo"])],
    )
    handler = DefaultRequestHandler(EchoExecutor(), InMemoryTaskStore(), card)

    @asynccontextmanager
    async def lifespan(app: Starlette):
        try:
            yield
        finally:
            await handler.aclose()

    app = Starlette(
        routes=[
            *create_agent_card_routes(card),
            *create_jsonrpc_routes(handler, rpc_url="/rpc"),
            *create_rest_routes(handler),
        ],
        lifespan=lifespan,
    )
    app.state.a2a_handler = handler
    return app


app = create_app()
