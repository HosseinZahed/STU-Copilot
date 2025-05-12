using Microsoft.Azure.Cosmos;

namespace STU.Copilot.AI.Helpers;

public static class PartitionManager
{
    public static PartitionKey GetChatDataFullPK(string tenantId, string userId, string sessionId)
    {
        var partitionKey = new PartitionKeyBuilder()
            .Add(tenantId)
            .Add(userId)
            .Add(sessionId)
            .Build();
        return partitionKey;
    }

    public static PartitionKey GetChatDataPartialPK(string tenantId, string userId)
    {
        var partitionKey = new PartitionKeyBuilder()
            .Add(tenantId)
            .Add(userId)
            .Build();
        return partitionKey;
    }

    public static PartitionKey GetTenantPartialPK(string tenantId)
    {
        var partitionKey = new PartitionKeyBuilder()
            .Add(tenantId)
            .Build();
        return partitionKey;
    }

    public static PartitionKey GetUserDataFullPK(string tenantId)
    {
        var partitionKey = new PartitionKeyBuilder()
            .Add(tenantId)
            .Build();
        return partitionKey;
    }
}
