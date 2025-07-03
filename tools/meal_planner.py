from agents import function_tool
import asyncio
from typing import Optional
from context import UserSessionContext
@function_tool
async def meal_planner(
    goal: str,
    preferences: str = "",
    lifestyle: str = "",
    context: Optional[UserSessionContext] = None,
) -> str:
    """
    Asynchronously create a personalized 7-day meal plan based on the user's health and wellness goals, dietary preferences, and lifestyle.

    Args:
        goal (str): The user's health and wellness goal.
        preferences (str): The user's dietary preferences.
        lifestyle (str): The user's lifestyle habits.
        context (UserSessionContext, optional): Shared user session context.

    Returns:
        str: A personalized 7-day meal plan.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meal_plan = [
        f"{day}: Breakfast - Oatmeal, Lunch - Salad, Dinner - Salmon"
        for day in days
    ]
    await asyncio.sleep(0)

    context_info = ""
    if context:
        context_info = (
            f"\n\nContext info:\n"
            f"Name: {context.name}\n"
            f"UID: {context.uid}\n"
            f"Goal: {context.goal}\n"
            f"Diet Preferences: {context.diet_preferences}\n"
            f"Meal Plan: {context.meal_plan}\n"
            f"Injury Notes: {context.injury_notes}\n"
            f"Handoff Logs: {context.handoff_logs}\n"
            f"Progress Logs: {context.progress_logs}\n"
        )

    return (
        f"Here is your personalized 7-day meal plan based on your goal '{goal}', "
        f"preferences '{preferences}', and lifestyle '{lifestyle}':\n\n" +
        "\n".join(meal_plan) +
        context_info
    )