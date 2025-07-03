from agents import function_tool
from typing import Optional
from context import UserSessionContext

# Simple in-memory tracker (for demonstration; replace with persistent storage as needed)
user_progress = {}

@function_tool
def tracker(
    user_id: str,
    update: str = "",
    context: Optional[UserSessionContext] = None
) -> str:
    """
    Accepts updates, tracks user progress, and modifies session context.

    Args:
        user_id (str): Unique identifier for the user/session.
        update (str): Progress update or note from the user.
        context (UserSessionContext): Optional session context to modify.

    Returns:
        str: Confirmation and current progress summary.
    """
    if user_id not in user_progress:
        user_progress[user_id] = {"updates": [], "context": {}}
    if update:
        user_progress[user_id]["updates"].append(update)
    if context:
        # Store the context as a dict for serialization and display
        user_progress[user_id]["context"] = context.dict(exclude_unset=True)
    updates = user_progress[user_id]["updates"]

    ctx = user_progress[user_id]["context"]
    context_info = ""
    if ctx:
        context_info = (
            f"\n\nContext info:"
            f"\nName: {ctx.get('name')}"
            f"\nUID: {ctx.get('uid')}"
            f"\nGoal: {ctx.get('goal')}"
            f"\nDiet Preferences: {ctx.get('diet_preferences')}"
            f"\nWorkout Plan: {ctx.get('workout_plan')}"
            f"\nMeal Plan: {ctx.get('meal_plan')}"
            f"\nInjury Notes: {ctx.get('injury_notes')}"
            f"\nHandoff Logs: {ctx.get('handoff_logs')}"
            f"\nProgress Logs: {ctx.get('progress_logs')}"
        )

    return (
        f"Progress updated for user {user_id}.\n"
        f"Total updates: {len(updates)}.\n"
        f"Latest update: {updates[-1] if updates else 'No updates yet.'}\n"
        f"{context_info}"
    )