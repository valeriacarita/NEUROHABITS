# src/data/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "neurohabits.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Asegura que la carpeta exista
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    c = conn.cursor()

    # Tabla de usuarios (simple, para relacionar registros)
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    # Tabla de hábitos
    c.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        timestamp TEXT,
        duration INTEGER,
        difficulty INTEGER,
        mood TEXT,
        notes TEXT,
        completed INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    # Asegurar que exista un usuario por defecto (id único)
    c.execute("SELECT id FROM users WHERE name = ?", ("default",))
    if c.fetchone() is None:
        c.execute("INSERT INTO users (name) VALUES (?)", ("default",))

    conn.commit()
    conn.close()
