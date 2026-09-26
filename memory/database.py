import sqlite3
from pathlib import Path


class MemoryDatabase:
    def __init__(self, database_path: str = "data/memory.db"):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(self.database_path)

        self._create_tables()

    def _create_tables(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def add_memory(self, content: str) -> None:
        self.connection.execute(
            "INSERT INTO memories (content) VALUES (?)",
            (content,),
        )

        self.connection.commit()

    def get_memories(self) -> list[str]:
        cursor = self.connection.execute(
            """
            SELECT content
            FROM memories
            ORDER BY created_at ASC
            """
        )

        return [row[0] for row in cursor.fetchall()]

    def search_memories(self, query: str) -> list[str]:
        words = [
            word.strip(".,!?;:()[]{}\"'")
            for word in query.lower().split()
        ]

        words = [word for word in words if word]

        if not words:
            return []

        conditions = " OR ".join(
            "LOWER(content) LIKE ?"
            for _ in words
        )

        parameters = [
            f"%{word}%"
            for word in words
        ]

        cursor = self.connection.execute(
            f"""
            SELECT content
            FROM memories
            WHERE {conditions}
            ORDER BY created_at ASC
            """,
            parameters,
        )

        return [row[0] for row in cursor.fetchall()]

    def close(self) -> None:
        self.connection.close()