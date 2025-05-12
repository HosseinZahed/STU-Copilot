namespace STU.Copilot.Infrastructure.Models;
public record SemanticKernelServiceSettings
{
    public required AzureOpenAISettings AzureOpenAISettings { get; init; }
    public required CosmosDBSettings CosmosDBVectorStoreSettings { get; init; }
}
