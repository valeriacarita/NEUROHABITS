# src/console/user_controllers.py
from src.data.database import get_connection

class UserController:
    def create_user(self, name: str, email: str | None = None) -> int | None:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            new_id = cur.lastrowid
            print(f"✅ Usuario '{name}' creado. ID: {new_id}")
            return new_id
        except Exception as e:
            print("❌ Error al crear usuario:", e)
            return None
        finally:
            conn.close()

    def list_users(self) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users ORDER BY id ASC")
        rows = cur.fetchall()
        conn.close()
        if not rows:
            print("⚠️  No hay usuarios registrados.")
            return []
        print("\n👤 Usuarios registrados:")
        for r in rows:
            print(f"{r['id']}: {r['name']} | {r['email'] or '-'}")
        return rows

    def delete_user(self, user_id: int) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        if deleted:
            print(f"🗑️ Usuario con ID {user_id} eliminado.")
        else:
            print("⚠️ Usuario no encontrado.")
        return deleted

    def select_user(self, user_id: int) -> int | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            print(f"✅ Usuario activo cambiado a: {row['name']} (ID {row['id']})")
            return row["id"]
        else:
            print("⚠️ Usuario no encontrado.")
            return None
    
    def get_user_name_by_id(self, user_id: int) -> str | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return row["name"] if row else None




