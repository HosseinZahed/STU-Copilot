using Microsoft.SemanticKernel.ChatCompletion;

namespace STU.Copilot.Infrastructure.Helpers;

internal static class AuthorRoleHelper
{
    private static readonly Dictionary<string, AuthorRole> s_roleMap =
    new(StringComparer.OrdinalIgnoreCase)
    {
            { "system", AuthorRole.System },
            { "assistant", AuthorRole.Assistant },
            { "user", AuthorRole.User },
            { "tool", AuthorRole.Tool }
    };

    public static AuthorRole? FromString(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            return null;
        }

        return s_roleMap.TryGetValue(name, out var role) ? role : null;
    }
}
