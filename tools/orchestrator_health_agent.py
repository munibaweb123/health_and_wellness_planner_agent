from agents import Runner, function_tool
from typing import Optional
from user_context import UserSessionContext, HealthPlanOutput
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.schedular import schedular
from tools.tracker import tracker
from tools.workout_recommender import workout_recommender

@function_tool
async def orchestrate_health_plan(
    input_text: str,
    user_id: str = "default",
    context: Optional[UserSessionContext] = None
) -> dict:
    from config import config  # if not already imported

    # ✅ Convert dict to context object if needed
    if context and isinstance(context, dict):
        try:
            context = UserSessionContext(**context)
        except Exception as e:
            return {"notes": f"❌ Error parsing context: {str(e)}"}

    try:
        goal_output = (await Runner.run(goal_analyzer, goal=input_text, context=context, run_config=config)).final_output
        meal_output = (await Runner.run(meal_planner, goal=input_text, context=context, run_config=config)).final_output
        workout_output = (await Runner.run(workout_recommender, goal=input_text, context=context, run_config=config)).final_output
        schedule_output = (await Runner.run(schedular, context=context, run_config=config)).final_output
        progress_output = (await Runner.run(tracker, user_id=user_id, update=input_text, context=context, run_config=config)).final_output
    except Exception as e:
        return {"notes": f"❌ Orchestration failed: {str(e)}"}

    try:
        plan = HealthPlanOutput(
            meal_plan=meal_output.get("meal_plan", []),
            workout_plan=workout_output.get("workout_plan", []),
            schedule=schedule_output.get("schedule", []),
            progress_logs=progress_output.get("progress_logs", []),
            notes=goal_output if isinstance(goal_output, str) else str(goal_output)
        )
        return plan.dict()
    except Exception as e:
        return {"notes": f"❌ Failed to build HealthPlanOutput: {str(e)}"}
