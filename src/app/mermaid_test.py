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


logging.basicConfig(level=logging.INFO)
logging.getLogger("openai").setLevel(logging.INFO)
logging.getLogger("semantic_kernel").setLevel(logging.INFO)

mermaid_ink_endpoint = os.getenv("MERMAID_INK_ENDPOINT")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AI_FOUNDRY_KEY")


def create_kernel(agent_name: str,
                  model_name: str,
                  api_version: str = "2024-12-01-preview") -> Kernel:
    """Create a kernel with the desired model."""
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=model_name,
            endpoint=endpoint,
            api_key=api_key,
            service_id=agent_name,
            api_version=api_version)
    )
    return kernel


class MermaidPlugins:

    def __init__(self):
        pass

    @kernel_function(name="mermaid_diagram_to_image",
                     description="Convert a Mermaid diagram definition to an image.")
    async def mermaid_diagram_to_image(self, graph_definition: str) -> str:
        """Convert a Mermaid diagram definition to an image."""
        print("Tool called")
        try:
            # Encode the graph definition
            graph_bytes = graph_definition.encode('utf-8')
            base64_bytes = base64.urlsafe_b64encode(graph_bytes)
            base64_string = base64_bytes.decode('ascii')

            # Make request to mermaid-ink service with proper URL construction
            url = f'{mermaid_ink_endpoint.rstrip("/")}/img/{base64_string}?&width=300&scale=1.5'
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Validate that we received image data
            if not response.content or len(response.content) == 0:
                raise ValueError(
                    "Received empty response from mermaid service")

            # Check if the response is likely an image (basic validation)
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                raise ValueError(
                    f"Expected image content, got: {content_type}")

            # Generate blob name and upload directly from response content
            blob_name = f"{uuid.uuid4()}.jpg"
            storage_account_service.upload_blob(
                container_name="chat-files",
                blob_name=blob_name,
                data=response.content,
                overwrite=True
            )
            return blob_name

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to generate mermaid image: {e}")
        except Exception as e:
            raise RuntimeError(f"Error processing mermaid diagram: {e}")


def create_agent(agent_name: str,
                 model_name: str,
                 instructions: str) -> ChatCompletionAgent:
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
        description="Mermaid diagram generation agent",
        instructions=instructions,
        plugins=[MermaidPlugins()]

    )
    return agent


# image_name = mermaid_diagram_to_image("graph TD; A-->B; A-->C; B-->D; C-->D;")
# print(image_name)
# user_input = ("An architecture for an application with a "
#               "backend service and a frontend user interface and"
#               "a database on Azure.")


async def main():
    mermaid_agent: ChatCompletionAgent = create_agent(
        agent_name="mermaid_agent",
        model_name="gpt-5-mini",
        instructions="""        
            First create a standard and simple Mermaid diagram definition based on the user input.
            Then you MUST call the tool with the created Mermaid diagram definition.
            Finally, return the output of the tool.
        """
    )

    # user_input = "graph TD; A-->B; A-->C; B-->D; C-->D;"
    user_input = ("An architecture for an application with a "
                  "backend service and a frontend user interface and"
                  "a database on Azure.")

    response: ChatMessageContent = await mermaid_agent.get_response(
        messages=user_input
    )
    # Try to parse the response as JSON, else print raw content
    try:
        print(response)
        # result = json.loads(response.content)
        # print(json.dumps(result, indent=2))
    except Exception:
        print(response.content)


if __name__ == "__main__":
    asyncio.run(main())
