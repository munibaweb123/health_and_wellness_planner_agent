from agents import function_tool
import asyncio
from typing import Optional, List
from context import UserSessionContext

@function_tool
async def meal_planner(
    goal: str,
    preferences: str = "",
    lifestyle: str = "",
    context: Optional[UserSessionContext] = None,
) -> List[str]:
    """
    Asynchronously create a personalized 7-day meal plan based on the user's health and wellness goals, dietary preferences, and lifestyle.

    Returns:
        List[str]: A list of 7 meal plan entries.
    """
    print("🥗 [Tool Triggered] meal_planner")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meal_plan = [
        f"{day}: Breakfast - Oatmeal with fruit, Lunch - Chickpea salad, Dinner - Grilled vegetables"
        for day in days
    ]

    # Simulate async behavior
    await asyncio.sleep(0)

    # Optionally store in context
    if context:
        context.meal_plan = meal_plan

    return meal_plan
