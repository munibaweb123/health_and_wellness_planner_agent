import asyncio
from agents import Runner
from tools.orchestrator_health_agent import orchestrate_health_plan  # adjust if needed
from context import UserSessionContext
from config import config

async def test_orchestrator():
    user_input = "I want to lose 5kg in 2 months. I am a busy office worker. Give me a 7-day meal plan and fitness schedule."
    user_id = "123"

    context = UserSessionContext(
        name="John Doe",
        uid=123,
        goal={"type": "weight loss", "target": "5kg", "duration": "2 months"},
        diet_preferences="balanced",
        workout_plan={"days": [], "details": ""},
        meal_plan=[],
        injury_notes="None",
        handoff_logs=[],
        progress_logs=[],
    )

    try:
        result = await Runner.run(
            orchestrate_health_plan,
            user_input,
            
            run_config=config
        )
        print("✅ Final Output:\n", result.final_output)

    except Exception as e:
        print("❌ Test Failed:", str(e))


if __name__ == "__main__":
    asyncio.run(test_orchestrator())
