# Welcome to STU Copilot! 🚀🤖

Hello and welcome! 👋 I'm STU Copilot, your intelligent assistant from Microsoft's Sales Technical Unit (STU). I'm here to help you with:

🔧 **Technical Guidance** - Architecture designs, solution engineering, and Azure best practices  
💼 **Sales Support** - Product information, competitive insights, and customer engagement strategies  
📚 **Microsoft Solutions** - Comprehensive guidance on Azure, Microsoft 365, Power Platform, and more

Whether you're a Technical Specialist, Solution Architect, Sales Professional, or need support with Microsoft technologies, I'm equipped with specialized agents to provide you with accurate, up-to-date information and actionable insights.

**Ready to get started?** Simply ask me your questions about Microsoft solutions, and I'll connect you with the right expertise! 💻✨

## Available Agents 🤖

This application includes multiple specialized agents to help you with different types of queries and tasks. Here's how to use each one:

### 🎯 **Orchestrator Agent**
The main coordinator that receives your queries and determines which specialized agents to use. It automatically:
- Assesses your query and selects appropriate agents
- Uses the questioner agent for clarification when needed
- Prioritizes Microsoft Docs agent for official documentation
- Combines responses from multiple agents for comprehensive answers

### 🏗️ **Architect Agent**
Your cloud architecture specialist for Microsoft Azure solutions. This agent:
- Provides solution engineering guidance following Azure best practices
- Follows Microsoft Well-Architected Framework (WAF) and Cloud Adoption Framework (CAF)
- Generates Mermaid diagrams to illustrate architecture designs
- Recommends latest Azure technologies and services

### 📚 **Microsoft Docs Agent**
Searches official Microsoft documentation and presents results with proper citations. Use this for:
- Official Microsoft product documentation
- Azure service guidance
- Development frameworks and tools
- Best practices and tutorials

### 🌐 **AWS Docs Agent**
Dedicated to searching AWS documentation when you need information about Amazon Web Services:
- Searches official AWS documentation
- Provides properly formatted results with links
- Useful for hybrid cloud scenarios or migration discussions

### 🔍 **Bing Search Agent**
Performs web searches to find information not covered by specialized documentation agents:
- General web search capabilities
- Current news and updates
- Community discussions and forums

### 📝 **Blog Posts Agent**
Searches for relevant blog posts and articles with:
- Numbered markdown list format
- Publication dates and summaries
- Links to original sources

### 💬 **Communicator Agent**
Acts as the initial chat router and welcomer:
- Routes requests to appropriate agents
- Handles user onboarding
- Works with questioner agent for clarifications

### 🤔 **Explainer Agent**
Your comprehensive explanation specialist that provides:
- Simple, non-technical descriptions
- Step-by-step how-it-works explanations
- Getting started guides
- Use cases, pros/cons, and alternatives
- Real-world examples and case studies
- FAQs and common pitfalls

### 🐙 **GitHub Agent**
Searches GitHub repositories and presents results in markdown tables:
- Repository information with descriptions
- Star counts, update dates, and archive status
- Direct links to repositories

### 📖 **GitHub Docs Search Agent**
Specialized for searching GitHub's official documentation.

### 🏭 **Industry Agent**
Provides industry-specific insights (currently in development).

### 🎯 **MCAPS Agent**
Specialized agent for Microsoft MCAPS (Microsoft Customer and Partner Solutions) related queries.

### 🎯 **Planner Agent**
Orchestrates query flow and agent selection based on:
- User role (Technical Specialist, Sales Specialist, etc.)
- Query type and requirements
- Returns JSON format with selected agents

### ❓ **Questioner Agent**
Clarifies user requests by asking targeted questions, focusing on:
- Microsoft technologies and services
- Azure, AI Foundry, Copilot Studio
- Microsoft 365, Dynamics 365, Power Platform
- Development tools like Visual Studio, GitHub, .NET

### 📄 **Summarizer Agent**
Creates concise summaries of chat conversations:
- Under 50 words
- Focuses on main topics and key decisions
- Identifies required actions and follow-ups

## How to Use the Agents

1. **Start with a clear question** - The orchestrator will automatically route to appropriate agents
2. **Be specific** - More detailed queries get better results
3. **Ask for clarification** - The questioner agent will help refine vague requests
4. **Request explanations** - Use the explainer agent for detailed breakdowns
5. **Need architecture help?** - The architect agent can create diagrams and provide design guidance

### Example Queries:
- "Explain Azure Functions" → Explainer + Microsoft Docs agents
- "Show me GitHub repos for machine learning" → GitHub agent  
- "I need an architecture for a web app" → Architect agent
- "Find recent blog posts about AI" → Blog Posts agent
