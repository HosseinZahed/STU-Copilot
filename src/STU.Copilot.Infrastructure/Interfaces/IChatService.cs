using STU.Copilot.Infrastructure.Models.Chat;

namespace STU.Copilot.Infrastructure.Interfaces;

public interface IChatService
{
    IEnumerable<string> GetChatCompletionAsync(string tenantId, string userId,
        string? sessionId, string userPrompt);

    Task<List<ChatSession>> GetChatSessionsAsync(string tenantId, string userId);

    Task<List<ChatMessage>> GetChatSessionMessagesAsync(string tenantId, string userId,
        string sessionId);

    Task<string> GenerateChatSessionTitleAsync(string tenantId, string userId,
        string? sessionId, string prompt);
}
