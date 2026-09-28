from types import SimpleNamespace
from unittest.mock import Mock

from memory.extractor import MemoryExtractor


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


def test_extractor_returns_memory_candidates():
    client = Mock()

    client.chat.completions.create.return_value = create_response(
        '{"memories": ['
        '{"key": "favorite_color", '
        '"content": "User\'s favorite color is green."}'
        ']}'
    )

    extractor = MemoryExtractor(client)

    candidates = extractor.extract(
        "Green has always been my favorite color."
    )

    assert len(candidates) == 1
    assert candidates[0].key == "favorite_color"
    assert candidates[0].content == "User's favorite color is green."


def test_extractor_can_return_multiple_memories():
    client = Mock()

    client.chat.completions.create.return_value = create_response(
        '{"memories": ['
        '{"key": "location", '
        '"content": "User lives in Denmark."}, '
        '{"key": "pet_dog", '
        '"content": "User has a dog named Max."}'
        ']}'
    )

    extractor = MemoryExtractor(client)

    candidates = extractor.extract(
        "I live in Denmark and my dog is named Max."
    )

    assert [
        (candidate.key, candidate.content)
        for candidate in candidates
    ] == [
        ("location", "User lives in Denmark."),
        ("pet_dog", "User has a dog named Max."),
    ]


def test_extractor_returns_no_memories_when_model_finds_none():
    client = Mock()

    client.chat.completions.create.return_value = create_response(
        '{"memories": []}'
    )

    extractor = MemoryExtractor(client)

    candidates = extractor.extract(
        "What is the capital of France?"
    )

    assert candidates == []


def test_extractor_returns_no_memories_for_empty_message():
    client = Mock()

    extractor = MemoryExtractor(client)

    assert extractor.extract("") == []

    client.chat.completions.create.assert_not_called()


def test_extractor_handles_invalid_json():
    client = Mock()

    client.chat.completions.create.return_value = create_response(
        "This is not valid JSON."
    )

    extractor = MemoryExtractor(client)

    candidates = extractor.extract(
        "My favorite color is green."
    )

    assert candidates == []