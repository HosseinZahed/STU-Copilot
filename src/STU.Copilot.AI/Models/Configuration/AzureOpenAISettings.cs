namespace STU.Copilot.AI.Models.Configuration;
public record AzureOpenAISettings
{
    public const string SectionName = "AzureOpenAI";

    public required string ChatDeploymentName { get; set; }

    public required string EmbeddingDeploymentName { get; set; }

    public required string Endpoint { get; set; }

    public required string Key { get; set; }
}
