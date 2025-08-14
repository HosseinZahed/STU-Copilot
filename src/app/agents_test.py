import base64
import uuid
import requests
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatPromptExecutionSettings
)
from services.storage_account_service import storage_account_service
import os
import asyncio
import json
import logging
from dotenv import load_dotenv

load_dotenv(override=True)


logging.basicConfig(level=logging.INFO)
logging.getLogger("openai").setLevel(logging.INFO)
logging.getLogger("semantic_kernel").setLevel(logging.INFO)


mermaid_ink_endpoint = os.getenv("MERMAID_INK_ENDPOINT")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AI_FOUNDRY_KEY")


class SamplePlugin:    
    
    def __init__(self):
        pass

    @kernel_function(name="sample_text", description="A sample tool that returns a text.")
    async def sample_text(self, input: str) -> str:
        return f"This is a sample text with input: {input}"


def create_agent(agent_name: str, model_name: str) -> ChatCompletionAgent:
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=model_name,
            endpoint=endpoint,
            api_key=api_key,
            service_id=agent_name,
            api_version="2024-12-01-preview")
    )
    agent = ChatCompletionAgent(
        kernel=kernel,
        name=agent_name,
        description="agent with a tool",
        instructions="""
                You MUST call the tool and return the output of the tool.
            """,
        plugins=[SamplePlugin()]

    )
    return agent


async def main():    
    agent: ChatCompletionAgent = create_agent(
        agent_name="sample_agent", model_name="gpt-5-mini")
    print(f"Agent created: {agent.name}")
    response = await agent.get_response(messages="Hello, world!")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
