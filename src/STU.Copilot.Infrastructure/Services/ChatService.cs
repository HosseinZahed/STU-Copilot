namespace STU.Copilot.Infrastructure.Services;

internal class ChatService : IChatService
{
    public Task<string> GenerateChatSessionTitleAsync(string tenantId, string userId, string? sessionId, string prompt)
    {
        throw new NotImplementedException();
    }

    public IEnumerable<string> GetChatCompletionAsync(string tenantId, string userId, string? sessionId, string userPrompt)
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
}
