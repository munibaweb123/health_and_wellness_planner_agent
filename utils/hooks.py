from agents import RunHooks, Agent, RunContextWrapper

class HealthAgentHooks(RunHooks):
    def __init__(self):
        self.event_counter = 0
        self.name = "HealthAgentHooks"

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"📌 {self.name} {self.event_counter}: Agent '{agent.name}' started.")
        print(f"📊 Initial usage: {context.usage}")

    async def on_tool_start(self, context: RunContextWrapper, tool, input) -> None:
        print(f"🛠️ Tool '{tool.name}' started.")
        print(f"➡️ Input: {input}")

    async def on_tool_end(self, context: RunContextWrapper, tool, output) -> None:
        print(f"✅ Tool '{tool.name}' completed.")
        print(f"📦 Output: {output}")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output) -> None:
        print(f"🎯 Agent '{agent.name}' finished.")
        print(f"🏁 Final Output: {output}")

    async def on_tool_error(self, context: RunContextWrapper, tool, error: Exception) -> None:
        print(f"❌ Tool '{tool.name}' raised an error: {error}")

    async def on_agent_error(self, context: RunContextWrapper, agent: Agent, error: Exception) -> None:
        print(f"🔥 Agent '{agent.name}' failed with error: {error}")
