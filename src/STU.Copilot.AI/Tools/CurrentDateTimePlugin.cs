using System.ComponentModel;
using Microsoft.SemanticKernel;

namespace STU.Copilot.AI.Tools;

internal class CurrentDateTimePlugin
{
    [KernelFunction, Description("Get the current time")]
    public string GetCurrentTime() => DateTime.Now.ToString("HH:mm:ss");

    [KernelFunction, Description("Get the current date")]
    public string GetCurrentDate() => DateTime.Now.ToString("yyyy-MM-dd");
}
