import asyncio
from agents import function_tool
from typing import Optional
from context import UserSessionContext

@function_tool
async def workout_recommender(
    goal: str,
    experience: str = "",
    preferences: str = "",
    context: Optional[UserSessionContext] = None
) -> dict:
    """
    Asynchronously suggest a 7-day workout plan based on the user's goals and experience.

    Args:
        goal (str): The user's fitness goal.
        experience (str): The user's fitness experience level (e.g., beginner, intermediate, advanced).
        preferences (str): Any workout preferences or restrictions.
        context (UserSessionContext, optional): Shared user session context.

    Returns:
        dict: A dictionary with a personalized 7-day workout plan.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workout_plan = [
        f"{day}: 30 min brisk walk" for day in days
    ]
    await asyncio.sleep(0)  # Simulate async operation

    # Optionally, you can still include context_info for debugging/logging
    # but the main return should be a dict for agent output parsing
    return {
        "workout_plan": workout_plan
    }