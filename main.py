from config import config
from agents import Runner
from health_agent import health_agent
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

async def main():
    user_context = None  # Or your UserSessionContext instance

    try:
        result = Runner.run_streamed(
            health_agent,
            input="I want to lose 5kg in 2 months. Give me a 7-day meal plan and fitness schedule for a busy office worker.",
            context=user_context,
            run_config=config
        )
        async for event in result.stream_events():
            # Just print the event data or event itself
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
    except Exception as e:
        print(f"\n[Error] {e}")

if __name__ == "__main__":
    asyncio.run(main())