import asyncio
from agents import function_tool, RunContextWrapper
from typing import Dict
from user_context import UserSessionContext

@function_tool
async def workout_recommender(
    ctx: RunContextWrapper[UserSessionContext],
    goal: str,
    experience: str = "",
    preferences: str = ""
) -> Dict:
    """
    Suggest a 7-day workout plan based on the user's goals and experience.
    """
    print("📌 [Tool Triggered] workout_recommender")

    # Example use of context (optional)
    if ctx.context:
        ctx.context.workout_plan = {
            "days": [
                "Monday: 30 min brisk walk",
                "Tuesday: 30 min brisk walk",
                "Wednesday: 30 min brisk walk",
                "Thursday: 30 min brisk walk",
                "Friday: 30 min brisk walk",
                "Saturday: 30 min brisk walk",
                "Sunday: 30 min brisk walk"
            ],
            "details": f"Recommended for goal '{goal}' and experience '{experience}'"
        }

    await asyncio.sleep(0)  # Simulate async call if needed

    return {
        "workout_plan": ctx.context.workout_plan["days"] if ctx.context else [],
        "notes": f"Generated for goal '{goal}', experience '{experience}', and preferences '{preferences}'"
    }
