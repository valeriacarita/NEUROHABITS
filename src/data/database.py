# src/data/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "neurohabits.db"


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
def get_connection():
    """Retorna una conexión a la base de datos."""
    db = Database()
    return db.connect()


def create_tables():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
    """)

    # habits
    cur.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        timestamp TEXT,
        duration INTEGER,
        difficulty INTEGER,
        mood TEXT,
        notes TEXT,
        completed INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # progress
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date TEXT,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )
    """)

    # aseguramos usuario por defecto
    cur.execute("SELECT id FROM users WHERE name = ?", ("default",))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("default", None))
    
   
    conn.commit()
    conn.close()



