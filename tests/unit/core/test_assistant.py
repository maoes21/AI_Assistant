from types import SimpleNamespace
from unittest.mock import Mock
from memory.candidate import MemoryCandidate
from memory.database import MemoryDatabase
from memory.manager import MemoryManager
from assistant.core.assistant import Assistant
from memory.extractor import MemoryExtractionError


def create_response(content: str):
    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=content
                )
            )
        ]
    )


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

    assert assistant.conversation.get_messages() == []

    assistant.close()


def test_assistant_can_remember(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    assistant = Assistant(memory_manager=manager)

    assistant.remember(
        MemoryCandidate(
            key="pet_dog",
            content="My dog is named Max.",
        )
    )

    assert assistant.get_memories() == [
        "My dog is named Max."
    ]

    assistant.close()


def test_memory_persists_between_assistants(tmp_path):
    database_path = tmp_path / "memory.db"

    first_database = MemoryDatabase(str(database_path))
    first_manager = MemoryManager(first_database)
    first_assistant = Assistant(memory_manager=first_manager)

    first_assistant.remember(
        MemoryCandidate(
            key="favorite_color",
            content="My favorite color is green.",
        )
    )

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

    assistant.remember(
        MemoryCandidate(
            key="pet_dog",
            content="My dog is named Max.",
        )
    )

    assert assistant.get_memories() == [
        "My dog is named Max."
    ]

    assert assistant.memory.search("dog") == [
        "My dog is named Max."
    ]

    assistant.close()


def test_assistant_stores_extracted_memory_candidates(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    extractor = Mock()
    extractor.extract.return_value = [
        MemoryCandidate(
            key="favorite_color",
            content="User's favorite color is green.",
        ),
        MemoryCandidate(
            key="location",
            content="User lives in Denmark.",
        ),
    ]

    assistant = Assistant(
        memory_manager=manager,
        memory_extractor=extractor,
    )

    assistant.client.chat.completions.create = Mock(
        return_value=create_response("Okay.")
    )

    assistant.chat("I'm Alex and I live in Denmark.")

    assert assistant.get_memories() == [
        "User's favorite color is green.",
        "User lives in Denmark.",
    ]

    extractor.extract.assert_called_once_with(
        "I'm Alex and I live in Denmark."
    )

    assistant.close()


def test_assistant_does_not_store_when_extractor_finds_nothing(
    tmp_path,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    extractor = Mock()
    extractor.extract.return_value = []

    assistant = Assistant(
        memory_manager=manager,
        memory_extractor=extractor,
    )

    assistant.client.chat.completions.create = Mock(
        return_value=create_response("Paris.")
    )

    assistant.chat("What is the capital of France?")

    assert assistant.get_memories() == []

    extractor.extract.assert_called_once_with(
        "What is the capital of France?"
    )

    assistant.close()


def test_assistant_updates_existing_memory(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    extractor = Mock()
    extractor.extract.side_effect = [
        [
            MemoryCandidate(
                key="favorite_color",
                content="User's favorite color is green.",
            )
        ],
        [
            MemoryCandidate(
                key="favorite_color",
                content="User's favorite color is blue.",
            )
        ],
    ]

    assistant = Assistant(
        memory_manager=manager,
        memory_extractor=extractor,
    )

    assistant.client.chat.completions.create = Mock(
        side_effect=[
            create_response("I'll remember that."),
            create_response("Got it."),
        ]
    )

    assistant.chat("My favorite color is green.")

    assistant.chat("My favorite color is blue now.")

    assert assistant.get_memories() == [
        "User's favorite color is blue.",
    ]

    assistant.close()


def test_assistant_includes_relevant_memories_in_model_request(
    tmp_path,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    manager.remember(
        MemoryCandidate(
            key="favorite_color",
            content="User's favorite color is green.",
        )
    )

    extractor = Mock()
    extractor.extract.return_value = []

    assistant = Assistant(
        memory_manager=manager,
        memory_extractor=extractor,
    )

    assistant.client.chat.completions.create = Mock(
        return_value=create_response("Max is your dog.")
    )

    assistant.chat("Tell me about my dog.")

    request = (
        assistant.client
        .chat.completions
        .create
        .call_args
    )

    messages = request.kwargs["messages"]

    assert messages[0]["role"] == "system"

    assert (
        "User has a dog named Max."
        in messages[0]["content"]
    )

    assert (
        "User's favorite color is green."
        not in messages[0]["content"]
    )

    assistant.close()


def test_assistant_preserves_conversation_messages(
    tmp_path,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    extractor = Mock()
    extractor.extract.return_value = []

    assistant = Assistant(
        memory_manager=manager,
        memory_extractor=extractor,
    )

    assistant.client.chat.completions.create = Mock(
        side_effect=[
            create_response("First response."),
            create_response("Second response."),
        ]
    )

    assistant.chat("Hello.")

    assistant.chat("How are you?")

    assert assistant.conversation.get_messages() == [
        {
            "role": "user",
            "content": "Hello.",
        },
        {
            "role": "assistant",
            "content": "First response.",
        },
        {
            "role": "user",
            "content": "How are you?",
        },
        {
            "role": "assistant",
            "content": "Second response.",
        },
    ]

    assistant.close()


def test_assistant_can_forget_memory(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    assistant = Assistant(memory_manager=manager)

    assistant.remember(
        MemoryCandidate(
            key="favorite_color",
            content="My favorite color is green.",
        )
    )

    assistant.forget("favorite_color")

    assert assistant.get_memories() == []

    assistant.close()


def test_assistant_can_forget_all_memories(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    assistant = Assistant(memory_manager=manager)

    assistant.remember(
        MemoryCandidate(
            key="favorite_color",
            content="My favorite color is green.",
        )
    )

    assistant.remember(
        MemoryCandidate(
            key="pet_dog",
            content="My dog is named Max.",
        )
    )

    assistant.forget_all()

    assert assistant.get_memories() == []

    assistant.close()


def test_assistant_searches_memories_using_conversation_context(
    tmp_path,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    extractor = Mock()
    extractor.extract.return_value = []

    assistant = Assistant(
        memory_manager=manager,
        memory_extractor=extractor,
    )

    assistant.client.chat.completions.create = Mock(
        side_effect=[
            create_response("Max sounds great."),
            create_response("A birthday present could be a new toy."),
        ]
    )

    assistant.chat("My dog's name is Max.")
    assistant.chat("What should I get him for his birthday?")

    request = (
        assistant.client
        .chat.completions
        .create
        .call_args
    )

    messages = request.kwargs["messages"]

    assert messages[0]["role"] == "system"

    assert (
        "User has a dog named Max."
        in messages[0]["content"]
    )

    assistant.close()


def test_assistant_continues_when_memory_extraction_fails(
    tmp_path,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    extractor = Mock()
    extractor.extract.side_effect = MemoryExtractionError(
        "Invalid JSON."
    )

    assistant = Assistant(
        memory_manager=manager,
        memory_extractor=extractor,
    )

    assistant.client.chat.completions.create = Mock(
        return_value=create_response("I can still help.")
    )

    response = assistant.chat(
        "What is the capital of France?"
    )

    assert response == "I can still help."

    assert assistant.conversation.get_messages() == [
        {
            "role": "user",
            "content": "What is the capital of France?",
        },
        {
            "role": "assistant",
            "content": "I can still help.",
        },
    ]

    assert assistant.get_memories() == []

    extractor.extract.assert_called_once_with(
        "What is the capital of France?"
    )

    assistant.close()