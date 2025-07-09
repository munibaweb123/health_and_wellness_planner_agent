from agents import function_tool
from typing import Optional, List, Dict
from context import UserSessionContext

@function_tool
def goal_analyzer(
    goal: str,
    preferences: Optional[str] = None,
    lifestyle: Optional[str] = None,
    context: Optional[UserSessionContext] = None
) -> Dict:
    """
    Analyze the user's goal and return a structured health plan with sample meal and workout plans.

    Args:
        goal (str): The user's health and wellness goal.
        preferences (str): The user's dietary preferences.
        lifestyle (str): The user's lifestyle habits.
        context (UserSessionContext, optional): Shared user session context.

    Returns:
        dict: A partial HealthPlanOutput structure with meal_plan, workout_plan, and notes.
    """
    print("📌 [Tool Triggered] goal_analyzer")

    # Update context
    if context:
        context.goal = {
            "goal": goal,
            "preferences": preferences,
            "lifestyle": lifestyle
        }

    # Generate basic mock data
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
