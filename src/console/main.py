# src/console/main.py
from datetime import datetime
from src.data.database import create_tables, Database, get_connection
from src.console.user_controllers import UserController
from src.console.habit_controllers import HabitController
from tabulate import tabulate

def input_int(prompt, default=0):
    try:
        v = input(prompt).strip()
        return int(v) if v else default
    except:
        return default

def register_flow(controller: HabitController, current_user_id: int):
    name = input("Nombre del hábito/meta: ").strip()
    if not name:
        print("Nombre obligatorio.")
        return
    description = input("Descripción (opcional): ").strip()
    frequency = input("Frecuencia (ej. diaria/semanal): ").strip()
    duration = input_int("Duración en minutos (opcional): ", 0)
    difficulty = input_int("Dificultad (1-5, opcional): ", 3)
    mood = input("Estado de ánimo (opcional): ").strip()
    notes = input("Notas (opcional): ").strip()
    controller.create_habit(current_user_id, name, description, frequency, duration, difficulty, mood, notes)

def user_menu(user_controller: UserController):
    while True:
        print("\n=== GESTIÓN DE USUARIOS ===")
        print("1) Crear usuario")
        print("2) Ver usuarios")
        print("3) Eliminar usuario")
        print("4) Seleccionar usuario")
        print("5) Volver al menú principal")
        choice = input("Elige opción: ").strip()
        if choice == '1':
            name = input("Nombre del usuario: ").strip()
            email = input("Email (opcional): ").strip() or None
            user_controller.create_user(name, email)
        elif choice == '2':
            user_controller.list_users()
        elif choice == '3':
            uid = input_int("ID del usuario a eliminar: ", 0)
            if uid:
                user_controller.delete_user(uid)
        elif choice == '4':
            uid = input_int("ID del usuario a seleccionar: ", 0)
            if uid:
                sel = user_controller.select_user(uid)
                if sel:
                    return sel
        elif choice == '5':
            return None
        else:
            print("Opción inválida.")

def habit_menu(controller: HabitController, user_id: int):

    hc = HabitController()

    while True:
        print("\n--- Gestión de Hábitos ---")
        print("1) Registrar hábito")
        print("2) Ver hábitos")
        print("3) Registrar progreso")
        print("4) Eliminar hábito")
        print("5) Modificar Habito")
        print("6) Volver al menú principal")
        opcion = input("Elige opción: ").strip()
        if opcion == '1':
            register_flow(controller, user_id)
        elif opcion == '2':
            habits = controller.get_habits(user_id) # O hc.get_habits(user_id) si usas 'hc'
            if not habits:
                print("⚠️ No tienes hábitos registrados.")
            else:
                # --- AQUÍ EMPIEZA LA IMPLEMENTACIÓN DE TABULATE ---
                
                # 1. Definir los encabezados de la tabla
                headers = ["ID", "Nombre", "Descripción", "Frecuencia", "Estado", "Creado en"]

                # 2. Imprimir la tabla
                # 'habits' es la lista de datos, 'headers' son los títulos, 'tablefmt' es el estilo.
                print("\n📋 Hábitos:")
                print(tabulate(habits, headers=headers, tablefmt="fancy_grid"))
                
                # --- AQUÍ TERMINA LA IMPLEMENTACIÓN DE TABULATE ---        elif opcion == '3':
            hid = input_int("ID del hábito: ", 0)
            if hid:
                controller.add_progress(hid)
        elif opcion == '4':
            habits = controller.get_habits(user_id)
            if not habits:
                print("⚠️ No hay hábitos para eliminar.")
            else:
                for h in habits:
                    print(f"{h[0]}) {h[1]}")
                hid = input_int("ID del hábito a eliminar: ", 0)
                if hid:
                    controller.delete_habit(hid, user_id)
        elif opcion == "5":
                print("\n--- Modificar hábito ---")
                hid = int(input("ID del hábito a modificar: "))
                name = input("Nuevo nombre (o enter para no cambiar): ")
                desc = input("Nueva descripción (o enter para no cambiar): ")
                freq = input("Nueva frecuencia (o enter para no cambiar): ")
                dur = input("Nueva duración (o enter para no cambiar): ")
                dif = input("Nueva dificultad (1-5, o enter para no cambiar): ")
                mood = input("Nuevo estado de ánimo (o enter para no cambiar): ")
                notes = input("Nuevas notas (o enter para no cambiar): ")

                dur = int(dur) if dur else None
                dif = int(dif) if dif else None

                hc.update_habit(hid, user_id, name or None, desc or None, freq or None, dur, dif, mood or None, notes or None)

        elif opcion == '6':
            
            break
        else:
            print("Opción inválida.")

def get_default_user_id():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name = ?", ("default",))
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else None

def main():
    # Crear tablas al inicio
    create_tables()

    # Instanciar controladores
    habit_controller = HabitController()
    user_controller = UserController()

    

    current_user_id = None

    # Aquí ya puedes mostrar tu menú
    while True:
        print("\n=== NEUROHABITS - Consola ===")
        print("1) Gestionar hábitos")
        print("2) Gestionar usuarios")
        print("3) Salir")
        
        # Muestra el usuario activo
        if current_user_id:
            user_name = user_controller.get_user_name_by_id(current_user_id)
            print(f"👉 Usuario activo: {user_name} (ID: {current_user_id})")
        else:
            print("⚠️  No hay usuario activo.")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            if not current_user_id:
                print("⚠️  Primero debes seleccionar un usuario.")
            else:
                habit_menu(habit_controller, current_user_id)
        elif opcion == "2":
            new_user_id = user_menu(user_controller)
            if new_user_id:
                current_user_id = new_user_id
        elif opcion == "3":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    main()

