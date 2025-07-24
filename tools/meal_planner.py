from agents import function_tool, RunContextWrapper
from user_context import UserSessionContext, MealPlan
from typing import List

@function_tool
async def meal_planner(
    ctx: RunContextWrapper[UserSessionContext],
    goal: str,
    preferences: str = "",
    lifestyle: str = "",
) -> List[str]:
    """
    Generates a personalized 7-day meal plan based on goal, preferences, and lifestyle.
    """

    async def _meal_planner(context: UserSessionContext) -> List[str]:
        print("🥗 [Tool Triggered] meal_planner")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        plan = [
            f"{day}: Breakfast - Oatmeal with fruit, Lunch - Chickpea salad, Dinner - Grilled vegetables"
            for day in days
        ]

        # Store meal plan in context
        if context.meal_plan is None:
            context.meal_plan = MealPlan()
        context.meal_plan.days = plan

        return plan

    return await ctx.run(_meal_planner)
