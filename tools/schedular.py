from agents import function_tool
import datetime
from typing import Optional
from context import UserSessionContext

@function_tool
def schedular(
    start_date: str = "",
    day_of_week: str = "Sunday",
    time_of_day: str = "09:00",
    context: Optional[UserSessionContext] = None
) -> str:
    """
    Schedules recurring weekly progress checks.

    Args:
        start_date (str): The date to start scheduling from (YYYY-MM-DD). Defaults to today if not provided.
        day_of_week (str): The day of the week for the check (e.g., 'Sunday').
        time_of_day (str): The time of day for the check (HH:MM, 24-hour format).
        context (UserSessionContext, optional): Shared user session context.

    Returns:
        str: Confirmation of the scheduled recurring progress checks.
    """
    if not start_date:
        start_date = datetime.date.today().isoformat()

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
        f"Weekly progress checks are scheduled every {day_of_week} at {time_of_day}, "
        f"starting from {start_date}."
        f"{context_info}"
    )