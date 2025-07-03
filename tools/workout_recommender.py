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
) -> str:
    """
    Asynchronously suggest a 7-day workout plan based on the user's goals and experience.

    Args:
        goal (str): The user's fitness goal.
        experience (str): The user's fitness experience level (e.g., beginner, intermediate, advanced).
        preferences (str): Any workout preferences or restrictions.
        context (UserSessionContext, optional): Shared user session context.

    Returns:
        str: A personalized 7-day workout plan.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workout_plan = [
        f"{day}: 30 min brisk walk" for day in days
    ]
    await asyncio.sleep(0)  # Simulate async operation

    context_info = ""
    if context:
        context_info = (
            f"\n\nContext info:\n"
            f"Name: {context.name}\n"
            f"UID: {context.uid}\n"
            f"Goal: {context.goal}\n"
            f"Diet Preferences: {context.diet_preferences}\n"
            f"Workout Plan: {context.workout_plan}\n"
            f"Meal Plan: {context.meal_plan}\n"
            f"Injury Notes: {context.injury_notes}\n"
            f"Handoff Logs: {context.handoff_logs}\n"
            f"Progress Logs: {context.progress_logs}\n"
        )

    return (
        f"Here is your personalized 7-day workout plan based on your goal '{goal}', "
        f"experience '{experience}', and preferences '{preferences}':\n\n" +
        "\n".join(workout_plan) +
        context_info
    )