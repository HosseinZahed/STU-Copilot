using System.Text.Json.Serialization;

namespace STU.Copilot.Infrastructure.Models.Chat;
public record ChatSession
{
    /// <summary>
    /// Unique identifier
    /// </summary>
    public string Id { get; set; }

    /// <summary>
    /// Partition key
    /// </summary>
    public string SessionId { get; set; }

    public string Type { get; set; }

    public string TenantId { get; set; }

    public string UserId { get; set; }

    public string Name { get; set; }

    [JsonIgnore]
    public List<ChatMessage> Messages { get; set; }

    public ChatSession(string tenantId, string userId)
    {
        Id = Guid.NewGuid().ToString();
        TenantId = tenantId;
        UserId = userId;
        Type = nameof(ChatSession);
        SessionId = Id;
        Name = "New Chat";
        Messages = new List<ChatMessage>();
    }

    public void AddMessage(ChatMessage message)
    {
        Messages.Add(message);
    }

    public void UpdateMessage(ChatMessage message)
    {
        var match = Messages.Single(m => m.Id == message.Id);
        var index = Messages.IndexOf(match);
        Messages[index] = message;
    }
}
