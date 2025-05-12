using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace STU.Copilot.Infrastructure.Services;

public static partial class DependencyInjection
{
    public static void AddSemanticKernelService(this IHostApplicationBuilder builder)
    {
        builder.Services.AddOptions<SemanticKernelServiceSettings>()
            .Bind(builder.Configuration.GetSection("SemanticKernelServiceSettings"));

        builder.Services.AddSingleton<ISemanticKernelService, SemanticKernelService>();
    }

    public static void AddCosmosDBService(this IHostApplicationBuilder builder)
    {
        builder.Services.AddOptions<CosmosDBSettings>()
            .Bind(builder.Configuration.GetSection("CosmosDBSettings"));
        builder.Services.AddSingleton<ICosmosDBService, CosmosDBService>();
    }

    public static void AddChatService(this IHostApplicationBuilder builder)
    {
        builder.Services.AddSingleton<IChatService, ChatService>();
    }
}
