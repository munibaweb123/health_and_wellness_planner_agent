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
        "INSERT INTO progress_logs (user_id, user_name, progress_update, timestamp) VALUES (?, ?, ?, datetime('now'))",
        (user_id, user_name, progress_update)
    )
    conn.commit()
    conn.close()

def get_user_logs(user_id: str):
    conn = sqlite3.connect("user_progress.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_name, progress_update, timestamp FROM progress_logs WHERE user_id = ? ORDER BY timestamp",
        (user_id,)
    )
    logs = cursor.fetchall()
    conn.close()

    return [
        {"name": name, "update": update, "timestamp": timestamp}
        for name, update, timestamp in logs
    ]
