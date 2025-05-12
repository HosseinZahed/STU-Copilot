using STU.Copilot.Infrastructure.Models.Chat;

namespace STU.Copilot.Infrastructure.Interfaces;

public interface ICosmosDBService
{
    Task<ChatSession> GetChatSessionAsync(string tenantId, string userId, string sessionId);

    Task<ChatSession> InsertChatSessionAsync(ChatSession session);

    Task<ChatSession> UpdateChatSessionAsync(ChatSession session);

    Task<bool> DeleteChatSessionAsync(string tenantId, string userId, string sessionId);

    Task<ChatMessage> InsertChatMessageAsync(ChatMessage message);

    Task<ChatMessage> UpdateChatMessageAsync(ChatMessage message);

    Task<List<ChatSession>> GetChatSessionsAsync(string tenantId, string userId);

    Task<List<ChatMessage>> GetChatSessionMessagesAsync(string tenantId, string userId,
        string sessionId);
}
