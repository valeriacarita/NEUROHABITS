# src/console/main.py
from datetime import datetime
from src.console.controllers import HabitController

def input_int(prompt, default=0):
    try:
        v = input(prompt).strip()
        return int(v) if v else default
    except:
        return default

def register_flow(controller: HabitController):
    name = input("Nombre del hábito/meta: ").strip()
    if not name:
        print("Nombre obligatorio.")
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    duration = input_int("Duración (minutos): ", 0)
    difficulty = input_int("Dificultad (1-5): ", 3)
    mood = input("Estado de ánimo (ej: motivado/triste): ").strip()
    notes = input("Notas adicionales: ").strip()
    controller.add_habit(name, now, duration, difficulty, mood, notes)

def main():
    controller = HabitController()
    while True:
        print("\n=== NEUROHABITS - Consola ===")
        print("1) Registrar hábito")
        print("2) Ver hábitos")
        print("3) Salir")
        choice = input("Elige opción: ").strip()
        if choice == '1':
            register_flow(controller)
        elif choice == '2':
            controller.list_habits()
        elif choice == '3':
            print("Saliendo.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
