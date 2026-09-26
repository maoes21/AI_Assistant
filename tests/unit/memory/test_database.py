from memory.database import MemoryDatabase


def test_database_starts_empty(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    assert database.get_memories() == []

    database.close()


def test_database_can_store_memory(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory("My dog is named Max.")

    assert database.get_memories() == [
        "My dog is named Max."
    ]

    database.close()


def test_database_can_store_multiple_memories(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory("My dog is named Max.")
    database.add_memory("My favorite color is green.")

    assert database.get_memories() == [
        "My dog is named Max.",
        "My favorite color is green.",
    ]

    database.close()


def test_database_can_search_memories(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory("My dog is named Max.")
    database.add_memory("My favorite color is green.")

    assert database.search_memories("dog") == [
        "My dog is named Max."
    ]

    assert database.search_memories("green") == [
        "My favorite color is green."
    ]

    database.close()


def test_database_search_is_case_insensitive(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory("My dog is named Max.")

    assert database.search_memories("DOG") == [
        "My dog is named Max."
    ]

    database.close()