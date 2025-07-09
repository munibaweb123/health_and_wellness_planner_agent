from agents import function_tool
import datetime
from typing import Optional, List
from context import UserSessionContext

@function_tool
def schedular(
    start_date: str = "",
    day_of_week: str = "Sunday",
    time_of_day: str = "09:00",
    context: Optional[UserSessionContext] = None
) -> List[str]:
    """
    Schedules recurring weekly progress checks.

    Returns:
        List[str]: List of scheduled check-in descriptions.
    """
    print("📆 [Tool Triggered] schedular")

    if not start_date:
        start_date = datetime.date.today().isoformat()

    # Compose schedule string
    schedule_note = (
        f"Weekly progress checks scheduled every {day_of_week} at {time_of_day}, "
        f"starting from {start_date}."
    )

    # Store or log in context if needed
    if context:
        context.progress_logs.append({
            "type": "schedule",
            "value": schedule_note
        })

    return [schedule_note]
