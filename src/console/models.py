# src/console/models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Habit:
    id: Optional[int]
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
            user_id=row.get("user_id", 1),
            name=row["name"],
            timestamp=row.get("timestamp", ""),
            duration=row.get("duration", 0),
            difficulty=row.get("difficulty", 3),
            mood=row.get("mood", ""),
            notes=row.get("notes", ""),
            completed=row.get("completed", 0)
        )

