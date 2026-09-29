import sqlite3
from pathlib import Path

from memory.record import MemoryRecord


class MemoryDatabase:
    _STOP_WORDS = {
        "a",
        "about",
        "an",
        "and",
        "are",
        "do",
        "does",
        "for",
        "how",
        "i",
        "in",
        "is",
        "me",
        "my",
        "of",
        "on",
        "the",
        "to",
        "what",
        "when",
        "where",
        "which",
        "who",
        "why",
        "with",
        "you",
        "your",
    }

    def __init__(self, database_path: str = "data/memory.db"):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.database_path)
        self._create_tables()

    def _create_tables(self) -> None:
        if not self._table_exists():
            self._create_memory_table()
            return

        columns = self._get_columns()

        required_columns = {
            "id",
            "key",
            "content",
            "created_at",
            "updated_at",
        }

        if required_columns.issubset(columns):
            return

        self._migrate_memory_table()

    def _table_exists(self) -> bool:
        cursor = self.connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'memories'
            """
        )
        return cursor.fetchone() is not None

    def _get_columns(self) -> set[str]:
        cursor = self.connection.execute(
            """
            PRAGMA table_info(memories)
            """
        )
        return {row[1] for row in cursor.fetchall()}

    def _create_memory_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.commit()

    def _migrate_memory_table(self) -> None:
        columns = self._get_columns()

        if "content" not in columns:
            raise RuntimeError(
                "Cannot migrate memories table because it does "
                "not contain a content column."
            )

        self.connection.execute(
            """
            ALTER TABLE memories
            RENAME TO memories_old
            """
        )

        self._create_memory_table()

        if "created_at" in columns:
            self.connection.execute(
                """
                INSERT INTO memories (
                    id,
                    key,
                    content,
                    created_at,
                    updated_at
                )
                SELECT
                    id,
                    'legacy_' || id,
                    content,
                    created_at,
                    created_at
                FROM memories_old
                """
            )
        else:
            self.connection.execute(
                """
                INSERT INTO memories (
                    id,
                    key,
                    content
                )
                SELECT
                    id,
                    'legacy_' || id,
                    content
                FROM memories_old
                """
            )

        self.connection.execute("DROP TABLE memories_old")
        self.connection.commit()

    def add_memory(self, key: str, content: str) -> None:
        self.connection.execute(
            """
            INSERT INTO memories (
                key,
                content
            )
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                content = excluded.content,
                updated_at = CURRENT_TIMESTAMP
            """,
            (key, content),
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

    def get_memory_records(self) -> list[MemoryRecord]:
        cursor = self.connection.execute(
            """
            SELECT key, content
            FROM memories
            ORDER BY created_at ASC
            """
        )

        return [
            MemoryRecord(
                key=row[0],
                content=row[1],
            )
            for row in cursor.fetchall()
        ]

    @classmethod
    def _tokenize(cls, text: str) -> list[str]:
        words = [
            word.strip(".,!?;:()[]{}\"'")
            for word in text.lower().split()
        ]

        return [
            word
            for word in words
            if word and word not in cls._STOP_WORDS
        ]

    def search_memories(
        self,
        query: str,
        limit: int = 5,
    ) -> list[str]:
        words = self._tokenize(query)

        if not words:
            return []

        cursor = self.connection.execute(
            """
            SELECT content
            FROM memories
            """
        )

        memories = [row[0] for row in cursor.fetchall()]

        scored_memories = []

        for index, memory in enumerate(memories):
            memory_words = set(self._tokenize(memory))

            score = sum(
                word in memory_words
                for word in words
            )

            if score > 0:
                scored_memories.append((score, index, memory))

        scored_memories.sort(
            key=lambda item: (-item[0], item[1])
        )

        return [
            memory
            for _, _, memory in scored_memories[:limit]
        ]

    def delete_memory(self, key: str) -> None:
        self.connection.execute(
            """
            DELETE FROM memories
            WHERE key = ?
            """,
            (key,),
        )
        self.connection.commit()

    def delete_all_memories(self) -> None:
        self.connection.execute("DELETE FROM memories")
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()