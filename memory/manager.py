from memory.database import MemoryDatabase


class MemoryManager:
    def __init__(self, database: MemoryDatabase | None = None):
        self.database = database or MemoryDatabase()

    def remember(self, content: str) -> None:
        content = content.strip()

        if not content:
            raise ValueError("Memory content cannot be empty.")

        self.database.add_memory(content)

    def get_all(self) -> list[str]:
        return self.database.get_memories()

    def search(self, query: str) -> list[str]:
        return self.database.search_memories(query)

    def close(self) -> None:
        self.database.close()