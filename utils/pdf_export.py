# utils/pdf_export.py
from fpdf import FPDF
import sqlite3
import os

def generate_user_progress_pdf(user_id: str, file_path=None) -> str:
    # Ensure static/reports directory exists
    os.makedirs("static/reports", exist_ok=True)

    # Default relative path inside /static
    if not file_path:
        file_path = f"reports/report_{user_id}.pdf"

    # Fetch logs from database
    conn = sqlite3.connect("user_progress.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_name, progress_update, timestamp FROM progress_logs WHERE user_id = ? ORDER BY timestamp",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if rows:
        user_name = rows[0][0] or "User"
        pdf.cell(200, 10, txt=f"Progress Report for {user_name} (ID: {user_id})", ln=True, align='C')
        pdf.ln(10)

        for i, (name, update, timestamp) in enumerate(rows, start=1):
            pdf.multi_cell(0, 10, txt=f"{i}. [{timestamp}]\n{update}\n")
    else:
        pdf.cell(200, 10, txt=f"No progress logs found for user ID {user_id}", ln=True, align='C')

    # Save it under static directory
    full_path = os.path.join("static", file_path)
    pdf.output(full_path)

    return file_path  # returns relative path like 'reports/report_123.pdf'
