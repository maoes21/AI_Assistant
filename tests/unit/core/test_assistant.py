from memory.database import MemoryDatabase
from memory.manager import MemoryManager

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
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    assistant = Assistant(memory_manager=manager)

    assistant.remember("My dog is named Max.")

    assert assistant.get_memories() == [
        "My dog is named Max."
    ]

    assistant.close()


def test_memory_persists_between_assistants(tmp_path):
    database_path = tmp_path / "memory.db"

    first_database = MemoryDatabase(str(database_path))
    first_manager = MemoryManager(first_database)
    first_assistant = Assistant(memory_manager=first_manager)

    first_assistant.remember("My favorite color is green.")
    first_assistant.close()

    second_database = MemoryDatabase(str(database_path))
    second_manager = MemoryManager(second_database)
    second_assistant = Assistant(memory_manager=second_manager)

    assert second_assistant.get_memories() == [
        "My favorite color is green."
    ]

    second_assistant.close()


def test_assistant_can_retrieve_memories(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    assistant = Assistant(memory_manager=manager)

    assistant.remember("My dog is named Max.")

    assert assistant.get_memories() == [
        "My dog is named Max."
    ]

    assert assistant.memory.search("dog") == [
        "My dog is named Max."
    ]

    assistant.close()


def test_assistant_automatically_remembers(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)
    assistant = Assistant(memory_manager=manager)

    assistant.chat("My favorite color is green.")

    assert assistant.get_memories() == [
        "My favorite color is green."
    ]

    assistant.close()