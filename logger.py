import sqlite3
from datetime import datetime

DB_PATH = 'data/database.db'

def init_db():
    """Initialize the database if it doesn't exist."""
    try:
        # Create the database file and tables if they don't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            action TEXT,
                            ip TEXT,
                            mac TEXT,
                            hostname TEXT,
                            timestamp DATETIME)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

def log_event(action, ip, mac, hostname):
    """Log an event (cut/restore) in the database."""
    timestamp = datetime.now()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO logs (action, ip, mac, hostname, timestamp)
                          VALUES (?, ?, ?, ?, ?)''', (action, ip, mac, hostname, timestamp))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging event: {e}")
