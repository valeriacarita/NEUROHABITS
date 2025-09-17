# src/console/controllers.py
from src.data.database import init_db, get_connection
from src.console.models import Habit

class HabitController:
    def __init__(self):
        # Inicializa DB y tablas si no existen
        init_db()
        self.conn = get_connection()
        self.user_id = self._get_default_user_id()

    def _get_default_user_id(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM users WHERE name = ?", ("default",))
        row = cur.fetchone()
        return row["id"] if row else 1

    def add_habit(self, name, timestamp, duration, difficulty, mood, notes):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO habits (user_id, name, timestamp, duration, difficulty, mood, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.user_id, name, timestamp, duration, difficulty, mood, notes))
        self.conn.commit()
        print("✅ Hábito guardado.")

    def list_habits(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM habits WHERE user_id = ? ORDER BY id DESC", (self.user_id,))
        rows = cur.fetchall()
        if not rows:
            print("⚠️  No hay hábitos registrados.")
            return
        print("\n📋 Hábitos registrados:")
        for row in rows:
            h = Habit.from_row(row)
            print(f"{h.id}. {h.name} | {h.timestamp} | {h.duration} min | dif:{h.difficulty} | ánimo:{h.mood}")
