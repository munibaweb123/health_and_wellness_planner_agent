from agents import function_tool
from typing import Optional, Dict, Any
from user_context import UserSessionContext, ProgressLog

# In-memory store
user_progress: Dict[str, Dict[str, Any]] = {}

def tracker_logic(
    user_id: str,
    update: str = "",
    context: Optional[UserSessionContext] = None
) -> Dict[str, Any]:
    """Standalone logic that can be called directly or via tool."""
    print("📈 [tracker_logic called]")

    if user_id not in user_progress:
        user_progress[user_id] = {"updates": []}

    if update:
        user_progress[user_id]["updates"].append(update)

    # Avoid mutation in original context passed by Gemini
    new_logs = list(context.progress_logs) if context and context.progress_logs else []

    if context:
        new_logs.append(ProgressLog(update=update, count=len(user_progress[user_id]["updates"])))

    updates = user_progress[user_id]["updates"]
    latest_update = updates[-1] if updates else "No updates yet."

    return {
        "tracking_summary": (
            f"Progress update recorded for user {user_id}. "
            f"Total updates: {len(updates)}. "
            f"Latest: {latest_update}"
        ),
        "new_progress_logs": [log.dict() for log in new_logs]
    }

# ✅ Register as tool for Gemini
@function_tool
def tracker(
    user_id: str,
    update: str = "",
    context: Optional[UserSessionContext] = None
) -> Dict[str, Any]:
    return tracker_logic(user_id, update, context)
