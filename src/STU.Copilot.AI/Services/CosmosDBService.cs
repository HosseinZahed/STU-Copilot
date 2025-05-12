using System.Diagnostics;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Cosmos.Fluent;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using STU.Copilot.AI.Helpers;

namespace STU.Copilot.AI.Services;

public class CosmosDBService : ICosmosDBService
{
    public readonly CosmosDBSettings _settings;
    public readonly ILogger<CosmosDBService> _logger;
    public readonly Database _database;
    public readonly Container _chatData;
    public readonly Container _userData;

    public CosmosDBService(IOptions<CosmosDBSettings> settings,
        ILogger<CosmosDBService> logger)
    {
        _settings = settings?.Value ?? throw new ArgumentNullException(nameof(settings));
        _logger = logger;

        // Initializing Cosmos DB service
        _logger.LogInformation("Initializing Cosmos DB service.");

        if (!_settings.EnableTracing)
        {
            var defaultTrace = Type.GetType("Microsoft.Azure.Cosmos.Core.Trace.DefaultTrace,Microsoft.Azure.Cosmos.Direct");
            var traceSource = defaultTrace?.GetProperty("TraceSource")?.GetValue(null) as TraceSource;
            traceSource.Switch.Level = SourceLevels.All;
            traceSource.Listeners.Clear();
        }

        CosmosSerializationOptions options = new()
        {
            PropertyNamingPolicy = CosmosPropertyNamingPolicy.CamelCase
        };

        var cosmosClient = new CosmosClientBuilder(_settings.CosmosUri, _settings.CosmosKey)
            .WithSerializerOptions(options)
            .WithConnectionModeGateway()
            .Build();

        _database = cosmosClient.GetDatabase(_settings.Database) ??
            throw new ArgumentException($"Database {_settings.Database} not found in Cosmos DB.", nameof(_settings.Database));

        _chatData = _database.GetContainer(_settings.ChatDataContainer.Trim()) ??
            throw new ArgumentException($"Container {_settings.ChatDataContainer} not found in Cosmos DB.", nameof(_settings.ChatDataContainer));

        _userData = _database.GetContainer(_settings.UserDataContainer.Trim()) ??
            throw new ArgumentException($"Container {_settings.UserDataContainer} not found in Cosmos DB.", nameof(_settings.UserDataContainer));

        _logger.LogInformation("Cosmos DB service initialized.");
    }

    public async Task<List<ChatSession>> GetChatSessionsAsync(string tenantId, string userId)
    {
        var query = new QueryDefinition("SELECT DISTINCT * FROM c WHERE c.type = @type")
            .WithParameter("@type", nameof(ChatSession));

        var partitionKey = PartitionManager.GetChatDataPartialPK(tenantId, userId);
        var response = _chatData.GetItemQueryIterator<ChatSession>(query, null,
            new QueryRequestOptions() { PartitionKey = partitionKey });

        var output = new List<ChatSession>();
        while (response.HasMoreResults)
        {
            var results = await response.ReadNextAsync();
            output.AddRange(results);
        }

        return output;
    }

    public async Task<ChatSession> GetChatSessionAsync(string tenantId, string userId,
        string sessionId)
    {
        var partitionKey = PartitionManager.GetChatDataFullPK(tenantId, userId, sessionId);

        return await _chatData.ReadItemAsync<ChatSession>(
            id: sessionId,
            partitionKey: partitionKey);
    }

    public Task<ChatSession> InsertChatSessionAsync(ChatSession session)
    {
        throw new NotImplementedException();
    }

    public Task<ChatSession> UpdateChatSessionAsync(ChatSession session)
    {
        throw new NotImplementedException();
    }

    public Task<bool> DeleteChatSessionAsync(string tenantId, string userId, string sessionId)
    {
        throw new NotImplementedException();
    }

    public Task<ChatMessage> InsertChatMessageAsync(ChatMessage message)
    {
        throw new NotImplementedException();
    }

    public Task<ChatMessage> UpdateChatMessageAsync(ChatMessage message)
    {
        throw new NotImplementedException();
    }

    public Task<List<ChatMessage>> GetChatSessionMessagesAsync(string tenantId, string userId,
        string sessionId)
    {
        throw new NotImplementedException();
    }
}
