import streamlit as st
import asyncio
import sqlite3
from datetime import datetime
from fpdf import FPDF
from tools.tracker import tracker_logic
from utils.hooks import HealthAgentHooks

from agents import Runner
from health_agent import health_agent
from tools.tracker import tracker
from context import UserSessionContext
from config import config

# ----------------------------
# 🌱 SESSION INIT
# ----------------------------
if "user_context" not in st.session_state:
    st.session_state.user_context = UserSessionContext(name="Muniba", uid=123)

user_context = st.session_state.user_context
user_id = str(user_context.uid)
user_name = user_context.name

# ----------------------------
# 📋 Sample Prompts
# ----------------------------
st.title("💪 Health & Wellness Planner Agent")

st.markdown("""
**Tip:** Include a clear goal and preferences in your prompt:
- `"I want to lose 5kg in 2 months. I prefer a vegetarian diet and low-impact workouts."`
- `"Help me gain muscle in 3 months. I have a nut allergy."`
""")

sample_prompts = [
    "I want to lose 5kg in 2 months. Give me a 7-day meal plan and fitness schedule for a busy office worker.",
    "I want to gain 3kg in 3 months. I prefer a high-protein vegetarian diet.",
    "I want to lose 4kg in 1 month. I have a knee injury. Suggest safe exercises and a healthy meal plan for weight loss.",
    "I want to maintain my weight in 6 months. Create a balanced diet and workout plan for managing diabetes.",
    "I want to lose 3kg in 1 month. I want a gluten-free meal plan and low-impact workouts."
]

selected_prompt = st.selectbox("Or select a sample prompt:", options=sample_prompts)
user_input = st.text_area("🧠 Enter your health goal and preferences:", selected_prompt)

# ----------------------------
# ✅ SQLite Save Function
# ----------------------------
def save_progress_to_db(user_id: str, user_name: str, progress_update: str):
    conn = sqlite3.connect("user_progress.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            user_name TEXT,
            progress_update TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute(
        "INSERT INTO progress_logs (user_id, user_name, progress_update, timestamp) VALUES (?, ?, ?, ?)",
        (
            user_id,
            user_name,
            progress_update,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    conn.commit()
    conn.close()

# ----------------------------
# 📤 PDF Export Function
# ----------------------------
def generate_user_progress_pdf(user_id: str, file_path="user_progress_report.pdf"):
    conn = sqlite3.connect("user_progress.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, progress_update, timestamp FROM progress_logs WHERE user_id = ? ORDER BY timestamp", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if rows:
        name = rows[0][0] or "User"
        pdf.cell(200, 10, txt=f"Progress Report for {name} (ID: {user_id})", ln=True, align='C')
        pdf.ln(10)
        for i, (name, update, timestamp) in enumerate(rows, start=1):
            pdf.multi_cell(0, 10, txt=f"{i}. [{timestamp}]\n{update}\n")
    else:
        pdf.cell(200, 10, txt=f"No progress logs found for user ID {user_id}", ln=True, align='C')

    pdf.output(file_path)
    return file_path

# ----------------------------
# 🧠 Run Agent & Get Plan
# ----------------------------
if st.button("🧠 Get My Plan"):
    async def get_response():
        try:
            result = Runner.run_streamed(
                health_agent,
                input=user_input,
                context=user_context,
                run_config=config,
                hooks=HealthAgentHooks() # Use custom hooks for logging
            )

            # Optional: Collect streamed text (for future chat UI)
            async for _ in result.stream_events():
                pass  # Ignore streaming output for now

            # ✅ Return final structured output (Pydantic model)
            return result.final_output, None
        except Exception as e:
            return None, str(e)

    response, error = asyncio.run(get_response())

    if error:
        if "Guardrail InputGuardrail triggered tripwire" in error:
            st.error("⚠️ Input rejected by guardrail. Please include a clear health-related goal.")
        else:
            st.error(f"⚠️ {error}")
    elif response:
        if response.notes:
            st.info(response.notes)
        if response.meal_plan:
            st.subheader("🥗 Meal Plan")
            for item in response.meal_plan:
                st.markdown(f"- {item}")
        if response.workout_plan:
            st.subheader("🏋️ Workout Plan")
            for item in response.workout_plan:
                st.markdown(f"- {item}")
        if response.tracking_summary:
            st.subheader("📈 Tracking Summary")
            st.markdown(response.tracking_summary)

# ----------------------------
# ✏️ Track Progress Section
# ----------------------------
st.divider()
st.subheader("📈 Track Your Daily Progress")

progress_update = st.text_area("Log today's progress:")

if st.button("✅ Submit Progress"):
    try:
        save_progress_to_db(user_id, user_name, progress_update)

        # ✅ Correct direct logic call
        tracking_result = tracker_logic(
            user_id=user_id,
            update=progress_update,
            context=user_context
        )

        st.success(tracking_result["tracking_summary"])
    except Exception as e:
        st.error(f"⚠️ Could not record progress: {e}")


# ----------------------------
# 📄 Export PDF Report
# ----------------------------
st.subheader("📄 Export My Progress Report")

if st.button("📥 Download My Report"):
    try:
        file_path = generate_user_progress_pdf(user_id)
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="progress_report.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"⚠️ Failed to generate report: {e}")
