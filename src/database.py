import sqlite3
from datetime import datetime

DB_NAME = "water_tracker.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT,
            intake_ml INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()



def log_water_intake(userid, intake_ml):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO water_intake (userid, intake_ml, timestamp)
        VALUES (?, ?, ?)
    ''', (userid, intake_ml, datetime.now()))
    conn.commit()
    conn.close()


def get_intake_history(userid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT intake_ml, timestamp FROM water_intake
        WHERE userid = ?
        ORDER BY timestamp DESC
    ''', (userid,))
    results = cursor.fetchall()
    conn.close()
    return results

create_table()  # Ensure the table is created when the module is imported