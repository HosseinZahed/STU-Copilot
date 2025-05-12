namespace STU.Copilot.Infrastructure.Models;
public record AzureOpenAISettings
{
    public required string ChatDeploymentName { get; set; }

    public required string EmbeddingDeploymentName { get; set; }

    public required string Endpoint { get; set; }

    public required string Key { get; set; }
}
