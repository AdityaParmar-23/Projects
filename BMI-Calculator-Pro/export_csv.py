import sqlite3
import csv
import os

from database import DB_NAME


def export_user(username):
    """
    Export all BMI records for a user to CSV.
    """

    try:
        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                username,
                weight,
                height,
                bmi,
                category,
                created_at
            FROM bmi_records
            WHERE username = ?
            ORDER BY created_at ASC
        """, (username,))

        rows = cursor.fetchall()

        conn.close()

        if not rows:
            return False, "No BMI records found."

        safe_username = "".join(
            character
            for character in username
            if character.isalnum() or character in (" ", "_", "-")
        ).strip()

        if not safe_username:
            safe_username = "user"

        filename = f"{safe_username}_bmi_history.csv"

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Username",
                "Weight (kg)",
                "Height (cm)",
                "BMI",
                "Category",
                "Date"
            ])

            writer.writerows(rows)

        return True, os.path.abspath(filename)

    except (sqlite3.Error, OSError) as error:
        return False, str(error)