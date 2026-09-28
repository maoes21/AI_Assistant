import sqlite3

from memory.database import MemoryDatabase


def test_database_starts_empty(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    assert database.get_memories() == []

    database.close()


def test_database_can_store_memory(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    assert database.get_memories() == [
        "User has a dog named Max.",
    ]

    database.close()


def test_database_can_store_multiple_memories(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )
    database.add_memory(
        "favorite_color",
        "User's favorite color is green.",
    )

    assert database.get_memories() == [
        "User has a dog named Max.",
        "User's favorite color is green.",
    ]

    database.close()


def test_database_replaces_memory_with_same_key(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "favorite_color",
        "User's favorite color is green.",
    )

    database.add_memory(
        "favorite_color",
        "User's favorite color is blue.",
    )

    assert database.get_memories() == [
        "User's favorite color is blue.",
    ]

    database.close()


def test_database_preserves_memories_with_different_keys(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "favorite_color",
        "User's favorite color is green.",
    )

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    database.add_memory(
        "favorite_color",
        "User's favorite color is blue.",
    )

    assert database.get_memories() == [
        "User's favorite color is blue.",
        "User has a dog named Max.",
    ]

    database.close()


def test_database_can_search_memories(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    database.add_memory(
        "favorite_color",
        "User's favorite color is green.",
    )

    assert database.search_memories("dog") == [
        "User has a dog named Max.",
    ]

    assert database.search_memories("green") == [
        "User's favorite color is green.",
    ]

    database.close()


def test_database_search_is_case_insensitive(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    assert database.search_memories("DOG") == [
        "User has a dog named Max.",
    ]

    database.close()


def test_database_search_ranks_memories_by_relevance(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "location",
        "User lives in Denmark.",
    )

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    database.add_memory(
        "dog_hobby",
        "User enjoys taking the dog on long walks.",
    )

    results = database.search_memories(
        "dog walks"
    )

    assert results == [
        "User enjoys taking the dog on long walks.",
        "User has a dog named Max.",
    ]

    database.close()


def test_database_search_returns_empty_for_no_matches(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    assert database.search_memories(
        "favorite color"
    ) == []

    database.close()


def test_database_search_handles_empty_query(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    assert database.search_memories("") == []

    database.close()


def test_database_search_respects_limit(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    for index in range(10):
        database.add_memory(
            f"memory_{index}",
            f"User likes apples number {index}.",
        )

    results = database.search_memories(
        "apples",
        limit=3,
    )

    assert len(results) == 3

    database.close()


def test_database_search_preserves_insertion_order_for_equal_scores(
    tmp_path,
):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "first",
        "User likes apples.",
    )

    database.add_memory(
        "second",
        "User likes bananas.",
    )

    database.add_memory(
        "third",
        "User likes oranges.",
    )

    assert database.search_memories("likes") == [
        "User likes apples.",
        "User likes bananas.",
        "User likes oranges.",
    ]

    database.close()


def test_database_can_delete_memory(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    database.delete_memory("pet_dog")

    assert database.get_memories() == []

    database.close()


def test_database_delete_does_not_affect_other_memories(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    database.add_memory(
        "favorite_color",
        "User's favorite color is green.",
    )

    database.delete_memory("pet_dog")

    assert database.get_memories() == [
        "User's favorite color is green.",
    ]

    database.close()


def test_database_can_delete_all_memories(tmp_path):
    database_path = tmp_path / "memory.db"

    database = MemoryDatabase(str(database_path))

    database.add_memory(
        "pet_dog",
        "User has a dog named Max.",
    )

    database.add_memory(
        "favorite_color",
        "User's favorite color is green.",
    )

    database.delete_all_memories()

    assert database.get_memories() == []

    database.close()


def test_database_migrates_legacy_schema(tmp_path):
    database_path = tmp_path / "memory.db"

    connection = sqlite3.connect(database_path)

    connection.execute(
        """
        CREATE TABLE memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.execute(
        """
        INSERT INTO memories (content)
        VALUES (?)
        """,
        ("User has a dog named Max.",),
    )

    connection.execute(
        """
        INSERT INTO memories (content)
        VALUES (?)
        """,
        ("User's favorite color is green.",),
    )

    connection.commit()
    connection.close()

    database = MemoryDatabase(str(database_path))

    assert database.get_memories() == [
        "User has a dog named Max.",
        "User's favorite color is green.",
    ]

    columns = database._get_columns()

    assert columns == {
        "id",
        "key",
        "content",
        "created_at",
        "updated_at",
    }

    cursor = database.connection.execute(
        """
        SELECT key
        FROM memories
        ORDER BY id ASC
        """
    )

    assert [row[0] for row in cursor.fetchall()] == [
        "legacy_1",
        "legacy_2",
    ]

    database.close()


def test_search_ignores_stop_words(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))

    database.add_memory(
        "pet_dog",
        "My dog is named Max.",
    )

    database.add_memory(
        "favorite_color",
        "My favorite color is green.",
    )

    assert database.search_memories(
        "What do you know about my dog?"
    ) == [
        "My dog is named Max.",
    ]

    database.close()


def test_search_returns_empty_when_query_contains_only_stop_words(
    tmp_path,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))

    database.add_memory(
        "pet_dog",
        "My dog is named Max.",
    )

    assert database.search_memories(
        "what do you know about my"
    ) == []

    database.close()


def test_search_stop_words_do_not_affect_relevance_ranking(
    tmp_path,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))

    database.add_memory(
        "pet_dog",
        "My dog is named Max.",
    )

    database.add_memory(
        "dog_hobby",
        "My dog enjoys long walks.",
    )

    assert database.search_memories(
        "What do you know about my dog walks?"
    ) == [
        "My dog enjoys long walks.",
        "My dog is named Max.",
    ]

    database.close()