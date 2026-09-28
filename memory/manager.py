import re

from memory.candidate import MemoryCandidate
from memory.database import MemoryDatabase


class MemoryManager:
    _KEY_PATTERN = re.compile(r"^[a-z0-9_]+$")

    def __init__(self, database: MemoryDatabase | None = None):
        self.database = database or MemoryDatabase()

    def remember(self, candidate: MemoryCandidate) -> None:
        key = self._normalize_key(candidate.key)
        content = candidate.content.strip()

        if not content:
            raise ValueError("Memory content cannot be empty.")

        self.database.add_memory(
            key=key,
            content=content,
        )

    def get_all(self) -> list[str]:
        return self.database.get_memories()

    def search(self, query: str) -> list[str]:
        return self.database.search_memories(query)

    def forget(self, key: str) -> None:
        key = self._normalize_key(key)

        self.database.delete_memory(key)

    def forget_all(self) -> None:
        self.database.delete_all_memories()

    @classmethod
    def _normalize_key(cls, key: str) -> str:
        key = key.strip().lower()

        if not key:
            raise ValueError("Memory key cannot be empty.")

        if len(key) > 100:
            raise ValueError(
                "Memory key cannot be longer than 100 characters."
            )

        if not cls._KEY_PATTERN.fullmatch(key):
            raise ValueError(
                "Memory key may only contain lowercase letters, "
                "numbers, and underscores."
            )

        return key

    def close(self) -> None:
        self.database.close()