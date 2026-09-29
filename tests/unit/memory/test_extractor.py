import pytest
from unittest.mock import Mock
from memory.extractor import (
    MemoryExtractionError,
    MemoryExtractor,
)


def test_extractor_returns_memory_candidates():
    llm = Mock()

    llm.chat.return_value = (
        '{"memories": ['
        '{"key": "favorite_color", '
        '"content": "User\'s favorite color is green."}'
        ']}'
    )

    extractor = MemoryExtractor(llm)

    candidates = extractor.extract(
        "Green has always been my favorite color."
    )

    assert len(candidates) == 1
    assert candidates[0].key == "favorite_color"
    assert candidates[0].content == "User's favorite color is green."


def test_extractor_can_return_multiple_memories():
    llm = Mock()

    llm.chat.return_value = (
        '{"memories": ['
        '{"key": "location", '
        '"content": "User lives in Denmark."}, '
        '{"key": "pet_dog", '
        '"content": "User has a dog named Max."}'
        ']}'
    )

    extractor = MemoryExtractor(llm)

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
    llm = Mock()

    llm.chat.return_value = '{"memories": []}'

    extractor = MemoryExtractor(llm)

    candidates = extractor.extract(
        "What is the capital of France?"
    )

    assert candidates == []


def test_extractor_returns_no_memories_for_empty_message():
    llm = Mock()

    extractor = MemoryExtractor(llm)

    assert extractor.extract("") == []

    llm.chat.assert_not_called()


def test_extractor_raises_for_invalid_json():
    llm = Mock()

    llm.chat.return_value = "This is not valid JSON."

    extractor = MemoryExtractor(llm)

    with pytest.raises(MemoryExtractionError):
        extractor.extract(
            "My favorite color is green."
        )


def test_extractor_raises_for_invalid_response_structure():
    llm = Mock()

    llm.chat.return_value = '{"memories": "not a list"}'

    extractor = MemoryExtractor(llm)

    with pytest.raises(MemoryExtractionError):
        extractor.extract(
            "My favorite color is green."
        )