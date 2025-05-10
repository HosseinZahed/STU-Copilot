namespace STU.Copilot.AI.Services;

internal class CosmosDBService : ICosmosDBService
{
    public Task<bool> DeleteChatSessionAsync(string tenantId, string userId, string sessionId)
    {
        throw new NotImplementedException();
    }

    public Task<ChatSession> GetChatSessionAsync(string tenantId, string userId, string sessionId)
    {
        throw new NotImplementedException();
    }

    public Task<List<ChatMessage>> GetChatSessionMessagesAsync(string tenantId, string userId, string sessionId)
    {
        throw new NotImplementedException();
    }

    public Task<List<ChatSession>> GetChatSessionsAsync(string tenantId, string userId)
    {
        throw new NotImplementedException();
    }

    public Task<ChatMessage> InsertChatMessageAsync(ChatMessage message)
    {
        throw new NotImplementedException();
    }

    public Task<ChatSession> InsertChatSessionAsync(ChatSession session)
    {
        throw new NotImplementedException();
    }

    public Task<ChatMessage> UpdateChatMessageAsync(ChatMessage message)
    {
        throw new NotImplementedException();
    }

    public Task<ChatSession> UpdateChatSessionAsync(ChatSession session)
    {
        throw new NotImplementedException();
    }
}
