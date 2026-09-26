from memory.database import MemoryDatabase

from assistant.core.assistant import Assistant


def test_assistant_uses_configured_model():
    assistant = Assistant(model="test-model")

    assert assistant.model == "test-model"

    assistant.close()


def test_assistant_has_client():
    assistant = Assistant()

    assert assistant.client is not None

    assistant.close()


def test_assistant_starts_with_empty_conversation():
    assistant = Assistant()

    assert assistant.conversation == []

    assistant.close()


def test_assistant_can_remember(tmp_path):
    database_path = tmp_path / "memory.db"
    database = MemoryDatabase(str(database_path))

    assistant = Assistant(memory_database=database)

    assistant.remember("My dog is named Max.")

    assert assistant.get_memories() == [
        "My dog is named Max."
    ]

    assistant.close()


def test_memory_persists_between_assistants(tmp_path):
    database_path = tmp_path / "memory.db"

    first_database = MemoryDatabase(str(database_path))
    first_assistant = Assistant(memory_database=first_database)

    first_assistant.remember("My favorite color is green.")
    first_assistant.close()

    second_database = MemoryDatabase(str(database_path))
    second_assistant = Assistant(memory_database=second_database)

    assert second_assistant.get_memories() == [
        "My favorite color is green."
    ]

    second_assistant.close()