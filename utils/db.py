import datetime
import sqlite3


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
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ FIXED
        )
    )
    conn.commit()
    conn.close()
