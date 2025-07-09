from agents import function_tool
from typing import Optional, Dict
from context import UserSessionContext

# In-memory store
user_progress = {}

def tracker_logic(
    user_id: str,
    update: str = "",
    context: Optional[UserSessionContext] = None
) -> Dict:
    """Standalone logic that can be called directly or via tool."""
    print("📈 [tracker_logic called]")

    if user_id not in user_progress:
        user_progress[user_id] = {"updates": [], "context": {}}

    if update:
        user_progress[user_id]["updates"].append(update)

    if context:
        context.progress_logs.append({
            "update": update,
            "count": len(user_progress[user_id]["updates"])
        })

    updates = user_progress[user_id]["updates"]
    latest_update = updates[-1] if updates else "No updates yet."

    return {
        "tracking_summary": (
            f"Progress update recorded for user {user_id}. "
            f"Total updates: {len(updates)}. "
            f"Latest: {latest_update}"
        )
    }

# ✅ Register as tool for agent use
@function_tool
def tracker(
    user_id: str,
    update: str = "",
    context: Optional[UserSessionContext] = None
) -> Dict:
    return tracker_logic(user_id, update, context)
