from agents import function_tool
from typing import Optional
from context import UserSessionContext



@function_tool
def goal_analyzer(
    goal: str,
    preferences: Optional[str] = None,
    lifestyle: Optional[str] = None,
    context: Optional[UserSessionContext] = None
) -> str:
    """
    Analyze the user's goal and provide a personalized health and wellness plan.

    Args:
        goal (str): The user's health and wellness goal.
        preferences (str): The user's dietary preferences.
        lifestyle (str): The user's lifestyle habits.
        context (UserSessionContext, optional): Shared user session context.

    Returns:
        str: A personalized health and wellness plan.
    """
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
        f"Based on your goal of '{goal}', your preferences of '{preferences}', and your lifestyle of '{lifestyle}', "
        f"here is your personalized health and wellness plan."
        f"{context_info}"
    )