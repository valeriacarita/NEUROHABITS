# src/console/models.py
from dataclasses import dataclass

@dataclass
class Habit:
    id: int | None
    user_id: int
    name: str
    timestamp: str
    duration: int
    difficulty: int
    mood: str
    notes: str
    completed: int = 0

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            timestamp=row["timestamp"],
            duration=row["duration"],
            difficulty=row["difficulty"],
            mood=row["mood"],
            notes=row["notes"],
            completed=row["completed"]
        )
