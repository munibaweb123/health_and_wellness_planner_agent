# Assuming this is your tools.py or similar file
from agents import function_tool, RunContextWrapper
from typing import Dict, List
# IMPORT NECESSARY PYDANTIC MODELS FROM user_context.py
from user_context import UserSessionContext, Goal, MealPlan, WorkoutPlan, MealDay

@function_tool
def goal_analyzer(
    ctx: RunContextWrapper[UserSessionContext],
    goal: str, # This parameter is for the 'type' of goal (e.g., "Weight Loss")
    preferences: str = "", # Input for dietary preferences (comma-separated string)
    lifestyle: str = ""
) -> Dict:
    """
    Analyze the user's goal and return a structured health plan with sample meal and workout plans.
    """
    print("📌 [Tool Triggered] goal_analyzer")

    # Update context using wrapper
    if ctx.context:
        # --- CRITICAL CORRECTION HERE ---
        # Assign a Goal Pydantic object, not a raw dictionary
        ctx.context.goal = Goal(
            type=goal,
            target="",  # You might want to parse a target from user input if available
            duration="" # You might want to parse a duration from user input if available
        )
        # --------------------------------

        # Assign preferences as a list of strings, consistent with user_context.py
        ctx.context.diet_preferences = [pref.strip() for pref in preferences.split(',') if pref.strip()] if preferences else []

        # If you were to update other optional models in ctx.context (like meal_plan, workout_plan),
        # you would also need to construct them as their respective Pydantic objects.
        # Example for meal_plan (hypothetical):
        # sample_meal_days = [MealDay(day=f"Day {i+1}", meals=[m]) for i, m in enumerate(meal_plan)]
        # ctx.context.meal_plan = MealPlan(days=sample_meal_days)

        # Assuming injury_notes in ctx.context is now Optional[List[str]]
        # ctx.context.injury_notes = ["No new injuries noted."] # Example assignment


    # Sample data for the RETURN value of this tool (these are simple lists of strings)
    # This part is correct for a tool's output.
    meal_plan = [
        "Day 1: Chickpea salad",
        "Day 2: Quinoa with vegetables",
        "Day 3: Lentil soup with whole grain bread",
        "Day 4: Grilled tofu with brown rice",
        "Day 5: Oats and fruit bowl",
        "Day 6: Stir-fried veggies",
        "Day 7: Vegetable soup and roti"
    ]

    workout_plan = [
        "Day 1: Brisk walk (30 mins)",
        "Day 2: Strength training (bodyweight)",
        "Day 3: Rest or light stretching",
        "Day 4: Cardio workout (HIIT style)",
        "Day 5: Yoga or Pilates",
        "Day 6: Strength training (core focus)",
        "Day 7: Rest day"
    ]

    return {
        "meal_plan": meal_plan,
        "workout_plan": workout_plan,
        "notes": f"Plan based on goal: '{goal}', preferences: '{preferences}', lifestyle: '{lifestyle}'."
    }