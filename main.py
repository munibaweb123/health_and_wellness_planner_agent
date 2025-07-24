from config import config
from agents import Runner
from health_agent import health_agent
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
import traceback  # <- Add this

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
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
            else:
                print(f"\n[Debug Event] {event}")  # Optional: see non-delta events
    except Exception as e:
        print(f"\n[Error] {e}")
        traceback.print_exc()  # <- Full traceback here

if __name__ == "__main__":
    asyncio.run(main())
