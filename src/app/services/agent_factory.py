import os
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatPromptExecutionSettings
)
from .cache_service import cache_service
from .plugin_factory import (
    github_plugin, microsoft_docs_plugin, blog_posts_plugin,
    seismic_plugin, bing_plugin, aws_docs_plugin
)
import logging


# Configure logging
logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)


class AgentFactory:
    """Factory for creating chat completion agents."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AI_FOUNDRY_KEY")
        if not self.endpoint or not self.api_key:
            raise EnvironmentError(
                "Missing Azure Open AI endpoint or API key.")

        self.agents = {
            "questioner_agent": self.get_questioner_agent(),
            "planner_agent": self.get_planner_agent(),
            # "github_agent": self.get_github_agent(),
            "github_docs_search_agent": self.get_github_docs_search_agent(),
            "microsoft_docs_agent": self.get_microsoft_docs_agent(),
            "blog_posts_agent": self.get_blog_posts_agent(),
            # "seismic_agent": self.get_seismic_agent(),
            "bing_search_agent": self.get_bing_search_agent(),
            "architect_agent": self.get_architect_agent(),
            "summarizer_agent": self.get_summarizer_agent(),
            "aws_docs_agent": self.get_aws_docs_agent(),
            "explainer_agent": self.get_explainer_agent(),
        }
        self.agents["orchestrator_agent"] = self.get_orchestrator_agent()

    def create_kernel(self,
                      agent_name: str,
                      model_name: str,
                      api_version: str = "2024-12-01-preview") -> Kernel:
        """Create a kernel with the desired model."""
        kernel = Kernel()
        kernel.add_service(
            AzureChatCompletion(
                deployment_name=model_name,
                endpoint=self.endpoint,
                api_key=self.api_key,
                service_id=agent_name,
                api_version=api_version)
        )

        return kernel

    def get_agents(self) -> dict[str, ChatCompletionAgent]:
        """Get all agents."""
        return self.agents

    def get_orchestrator_agent(self) -> ChatCompletionAgent:
        """Create an orchestrator agent with the necessary plugins."""
        agent_name = "orchestrator_agent"
        model_name = "gpt-5-mini"

        # Create a new kernel instance with the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name,

        )

        # Create the agent
        orchestrator_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="Orchestrator agent that manages the workflow of other agents.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[
                self.agents.get("questioner_agent"),
                self.agents.get("microsoft_docs_agent"),
                # self.agents.get("github_agent"),
                self.agents.get("github_docs_search_agent"),
                self.agents.get("blog_posts_agent"),
                # self.agents.get("seismic_agent"),
                self.agents.get("bing_search_agent"),
                self.agents.get("aws_docs_agent"),
                self.agents.get("explainer_agent"),
            ],
            arguments=KernelArguments(
                reasoning={
                    "effort": "minimal"
                }
            )
        )

        return orchestrator_agent

    def get_questioner_agent(self) -> ChatCompletionAgent:
        """Create a questioner agent with the necessary plugins."""
        agent_name = "questioner_agent"
        model_name = "gpt-5-nano"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        questioner_agent = ChatCompletionAgent(
            kernel=kernel,
            description="Questioner agent that asks clarifying questions to gather more information.",
            name=agent_name,
            instructions=cache_service.load_prompt(agent_name)
        )

        return questioner_agent

    def get_planner_agent(self) -> ChatCompletionAgent:
        """Create a planner agent with the necessary plugins."""
        agent_name = "planner_agent"
        model_name = "o3-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        planner_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            instructions=cache_service.load_prompt(agent_name)
        )

        return planner_agent

    def get_github_agent(self) -> ChatCompletionAgent:
        """Create a GitHub agent with the necessary plugins."""
        agent_name = "github_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name,
        )

        # Create the agent
        github_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="GitHub agent that fetches relevant information from GitHub repositories.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[github_plugin.github_repository_search]
        )

        return github_agent

    def get_microsoft_docs_agent(self) -> ChatCompletionAgent:
        """Create a Microsoft Docs agent with the necessary plugins."""
        agent_name = "microsoft_docs_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        microsoft_docs_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="Microsoft Docs agent that fetches relevant documentation from Microsoft Docs.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[microsoft_docs_plugin.microsoft_docs_search]
        )

        return microsoft_docs_agent

    def get_blog_posts_agent(self) -> ChatCompletionAgent:
        """Create a Blog Posts agent with the necessary plugins."""
        agent_name = "blog_posts_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        blog_posts_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="Blog Posts agent that searches for relevant blog posts.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[blog_posts_plugin.blog_posts_search]
        )

        return blog_posts_agent

    def get_seismic_agent(self) -> ChatCompletionAgent:
        """Create a Seismic agent with the necessary plugins."""
        agent_name = "seismic_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        seismic_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="Seismic agent that searches for relevant presentations and PowerPoints.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[seismic_plugin.seismic_search]
        )

        return seismic_agent

    def get_bing_search_agent(self) -> ChatCompletionAgent:
        """Create a Bing Search agent with the necessary plugins."""
        agent_name = "bing_search_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        bing_search_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="Bing Search agent that performs web searches to find relevant information.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[bing_plugin.bing_search]
        )

        return bing_search_agent

    def get_github_docs_search_agent(self) -> ChatCompletionAgent:
        """Create a GitHub Docs Search agent with the necessary plugins."""
        agent_name = "github_docs_search_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        github_docs_search_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="GitHub Docs Search agent that performs searches to find relevant documentation.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[github_plugin.github_docs_search]
        )

        return github_docs_search_agent

    def get_aws_docs_agent(self) -> ChatCompletionAgent:
        """Create an AWS Docs agent with the necessary plugins."""
        agent_name = "aws_docs_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        aws_docs_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="AWS Docs agent that fetches relevant documentation from AWS Docs.",
            instructions=cache_service.load_prompt(agent_name),
            plugins=[aws_docs_plugin.aws_docs_search]
        )

        return aws_docs_agent

    def get_architect_agent(self) -> ChatCompletionAgent:
        """Create an architect agent with the necessary plugins."""
        agent_name = "architect_agent"
        model_name = "o3-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        architect_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            instructions=cache_service.load_prompt(agent_name),
            plugins=[
                microsoft_docs_plugin.microsoft_docs_search,
                bing_plugin.bing_search
            ]
        )

        return architect_agent

    def get_summarizer_agent(self) -> ChatCompletionAgent:
        """Create a summarizer agent with the necessary plugins."""
        agent_name = "summarizer_agent"
        model_name = "gpt-5-mini"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        summarizer_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="Summarizer agent that condenses information into concise summaries.",
            instructions=cache_service.load_prompt(agent_name)
        )

        return summarizer_agent

    def get_explainer_agent(self) -> ChatCompletionAgent:
        """Create an explainer agent with the necessary plugins."""
        agent_name = "explainer_agent"
        model_name = "gpt-5-chat"

        # Clone the base kernel and add the OpenAI service
        kernel = self.create_kernel(
            agent_name=agent_name,
            model_name=model_name
        )

        # Create the agent
        explainer_agent = ChatCompletionAgent(
            kernel=kernel,
            name=agent_name,
            description="Explainer agent that provides detailed explanations of concepts.",
            instructions=cache_service.load_prompt(agent_name)
        )

        return explainer_agent

    @staticmethod
    def execution_settings() -> OpenAIChatPromptExecutionSettings:
        """Create request settings for the OpenAI service."""
        return OpenAIChatPromptExecutionSettings(
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )


# Global instance
agent_factory = AgentFactory()
