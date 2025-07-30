import os
from typing import List, Dict, Optional
import chainlit as cl
from services.chat_service import ChatService
from services.agent_factory import AgentFactory
from semantic_kernel.contents import ChatHistory
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
import logging
import socketio
from engineio.payload import Payload


# Set the buffer size to 10MB or use a configurable value from the environment
MAX_HTTP_BUFFER_SIZE = int(os.getenv("MAX_HTTP_BUFFER_SIZE", 100_000_000))
# Configurable buffer size
sio = socketio.AsyncServer(
    async_mode='aiohttp',
    transport='websocket',
    max_http_buffer_size=MAX_HTTP_BUFFER_SIZE)
Payload.max_decode_packets = 500


# Basic logging configuration
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("azure").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("azure.cosmos").setLevel(logging.CRITICAL)
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("semantic_kernel").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("httpcore").setLevel(logging.CRITICAL)
logging.getLogger("anyio").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp.access").setLevel(logging.CRITICAL)
logging.getLogger("engineio").setLevel(logging.CRITICAL)
logging.getLogger("socketio").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

# Initialize services and agents
chat_service: ChatService = ChatService()
agent_factory: AgentFactory = AgentFactory()
agents: dict[str, ChatCompletionAgent] = agent_factory.get_agents()


@cl.oauth_callback
async def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    print(f"OAuth callback for provider {provider_id}")
    default_user.identifier = raw_user_data["mail"]
    default_user.display_name = raw_user_data["displayName"]
    default_user.metadata["user_id"] = raw_user_data["id"]
    default_user.metadata["first_name"] = raw_user_data["givenName"]
    default_user.metadata["job_title"] = raw_user_data["jobTitle"]
    default_user.metadata["office_location"] = raw_user_data["officeLocation"]
    return default_user


@cl.on_chat_start
async def on_chat_start():
    # Populate commands in the user session
    await cl.context.emitter.set_commands(
        chat_service.get_commands()
    )

    # Initialize the chat service and chat history
    chat_history: ChatHistory = ChatHistory()

    # Get the user ID and job title from the user session
    user = cl.user_session.get("user")

    # Construct the welcome message
    welcome_message = chat_service.get_welcome_message(
        user_first_name=user.metadata.get("first_name", "Guest"),
        user_job_title=user.metadata.get("job_title", None),
    )

    # Clear the latest agent name
    latest_agent_name = None

    # Show the welcome message to the user
    await cl.Message(content=welcome_message).send()

    # icon_element = cl.CustomElement(name="Icon")
    # await cl.Message(content="", elements=[icon_element]).send()

    chat_history.add_assistant_message(welcome_message)

    cl.user_session.set("chat_service", chat_service)
    cl.user_session.set("chat_history", chat_history)
    cl.user_session.set("chat_thread", None)
    cl.user_session.set("latest_agent_name", latest_agent_name)


@cl.on_message
async def on_message(user_message: cl.Message):
    chat_service: ChatService = cl.user_session.get("chat_service")
    chat_history: ChatHistory = cl.user_session.get("chat_history")
    chat_thread: ChatHistoryAgentThread = cl.user_session.get("chat_thread")

    responder_agent: ChatCompletionAgent = agent_factory.select_responder_agent(
        current_message=user_message,
        chat_history=chat_history,
        latest_agent_name=cl.user_session.get("latest_agent_name")
    )
    print(f"Selected responder agent: {responder_agent.name}")

    agent_actions = chat_service.get_actions(agent_name=responder_agent.name)

    # Set the latest agent in the user session
    cl.user_session.set("latest_agent_name", responder_agent.name)

    chat_history.add_user_message(user_message.content)
    answer = cl.Message(content="", actions=agent_actions)

    # Select which messages to send to the agent
    messages = chat_history if responder_agent in [
        agents["orchestrator"],
        agents["questioner"],
        agents["planner"]
    ] else user_message.content

    # Set the latest agent in the user session
    cl.user_session.set("latest_agent", responder_agent.name)

    # Stream the agent's response token by token
    async for token in responder_agent.invoke_stream(
            messages=messages,
            thread=chat_thread
    ):
        if token.content:
            await answer.stream_token(token.content.content)

    cl.user_session.set("chat_thread", token.thread)
    chat_history.add_assistant_message(answer.content)

    # Send the final message
    await answer.send()


@cl.set_starters  # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="AI Assistant",
            message="Design an AI assistant with frontend, backend, and database integration.",
        ),
        cl.Starter(
            label="Data Analysis Bot",
            message="Create a bot to analyze and visualize data trends.",
        ),
        cl.Starter(
            label="Weather Bot",
            message="How is the weather today?",
        ),
    ]


@cl.action_callback("action_button")
async def on_action_button(action: cl.Action):
    """Handle action button clicks."""
    chat_history: ChatHistory = cl.user_session.get("chat_history")
    user_prompts = "\n".join(
        [msg.content for msg in chat_history if msg.role == "user"]
    )

    await on_message(cl.Message(
        content=user_prompts,
        command=action.payload["command"]
    ))
