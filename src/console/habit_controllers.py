# src/console/habit_controllers.py
from src.data.database import get_connection
from datetime import datetime

class HabitController:
    def create_habit(self, user_id: int, name: str, description: str | None = None,
                     frequency: str | None = None, duration: int = 0,
                     difficulty: int = 3, mood: str | None = None, notes: str | None = None):
        conn = get_connection()
        cur = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            "INSERT INTO habits (user_id, name, description, frequency, timestamp, duration, difficulty, mood, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, name, description, frequency, now, duration, difficulty, mood, notes)
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        print(f"✅ Hábito '{name}' creado (ID {new_id}).")
        return new_id

    def get_habits(self, user_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, description, frequency, status, timestamp FROM habits WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return [(r["id"], r["name"], r["description"], r["frequency"], r["status"], r["timestamp"]) for r in rows]

    def add_progress(self, habit_id: int):
        conn = get_connection()
        cur = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO progress (habit_id, date) VALUES (?, ?)", (habit_id, date))
        conn.commit()
        conn.close()
        print("✅ Progreso registrado para hábito ID", habit_id)

    def delete_habit(self, habit_id: int, user_id: int) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM habits WHERE id = ? AND user_id = ?", (habit_id, user_id))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        if deleted:
            print(f"🗑️ Hábito {habit_id} eliminado.")
        else:
            print("⚠️ No se encontró hábito con ese ID para el usuario actual.")
        return deleted
    def update_habit(self, habit_id: int, user_id: int, name: str | None = None,
                    description: str | None = None, frequency: str | None = None,
                    duration: int | None = None, difficulty: int | None = None,
                    mood: str | None = None, notes: str | None = None) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        
        # Construimos el SET dinámico
        updates = []
        values = []
        if name: 
            updates.append("name = ?")
            values.append(name)
        if description: 
            updates.append("description = ?")
            values.append(description)
        if frequency: 
            updates.append("frequency = ?")
            values.append(frequency)
        if duration is not None: 
            updates.append("duration = ?")
            values.append(duration)
        if difficulty is not None: 
            updates.append("difficulty = ?")
            values.append(difficulty)
        if mood: 
            updates.append("mood = ?")
            values.append(mood)
        if notes: 
            updates.append("notes = ?")
            values.append(notes)

        if not updates:
            print("⚠️ No se proporcionaron campos para actualizar.")
            return False

        query = f"UPDATE habits SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
        values.extend([habit_id, user_id])
        cur.execute(query, values)
        conn.commit()
        updated = cur.rowcount > 0
        conn.close()
        if updated:
            print(f"✏️ Hábito {habit_id} modificado correctamente.")
        else:
            print("⚠️ No se encontró el hábito para este usuario.")
        return updated

