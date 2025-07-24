from agents import function_tool, RunContextWrapper
import datetime
from typing import List
from user_context import UserSessionContext

@function_tool
def schedular(
    ctx: RunContextWrapper[UserSessionContext],
    start_date: str = "",
    day_of_week: str = "Sunday",
    time_of_day: str = "09:00",
) -> List[str]:
    """
    Schedules recurring weekly progress checks.

    Returns:
        List[str]: List of scheduled check-in descriptions.
    """

    def _schedular(context: UserSessionContext) -> List[str]:
        print("📆 [Tool Triggered] schedular")

        if not start_date:
            current_date = datetime.date.today()
            start_date_str = current_date.isoformat()
        else:
            start_date_str = start_date

        # Compose schedule string
        schedule_note = (
            f"Weekly progress checks scheduled every {day_of_week} at {time_of_day}, "
            f"starting from {start_date_str}."
        )

        # Store in context
        context.progress_logs.append({
            "type": "schedule",
            "value": schedule_note
        })

        return [schedule_note]

    return ctx.run(_schedular)
