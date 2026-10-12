import sqlite3


DB_NAME = "bmi_records.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error:
        return False


def save_record(username, weight, height, bmi, category):
    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bmi_records
            (username, weight, height, bmi, category)
            VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            weight,
            height,
            bmi,
            category
        ))

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error:
        return False


def get_users():
    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT username
            FROM bmi_records
            ORDER BY username COLLATE NOCASE
        """)

        users = [row[0] for row in cursor.fetchall()]

        conn.close()

        return users

    except sqlite3.Error:
        return []


def get_history(username):
    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT bmi, created_at
            FROM bmi_records
            WHERE username = ?
            ORDER BY created_at ASC
        """, (username,))

        data = cursor.fetchall()

        conn.close()

        return data

    except sqlite3.Error:
        return []


def get_latest_record(username):
    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT weight, height, bmi, category, created_at
            FROM bmi_records
            WHERE username = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (username,))

        record = cursor.fetchone()

        conn.close()

        return record

    except sqlite3.Error:
        return None


def get_record_count(username):
    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM bmi_records
            WHERE username = ?
        """, (username,))

        count = cursor.fetchone()[0]

        conn.close()

        return count

    except sqlite3.Error:
        return 0