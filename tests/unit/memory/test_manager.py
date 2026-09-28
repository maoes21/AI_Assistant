import pytest

from memory.candidate import MemoryCandidate
from memory.database import MemoryDatabase
from memory.manager import MemoryManager


def test_manager_can_remember(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    assert manager.get_all() == [
        "User has a dog named Max.",
    ]

    manager.close()


def test_manager_can_search(tmp_path):
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

    assert manager.search("dog") == [
        "User has a dog named Max.",
    ]

    manager.close()


def test_manager_search_returns_most_relevant_memory_first(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="location",
            content="User lives in Denmark.",
        )
    )

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    manager.remember(
        MemoryCandidate(
            key="dog_hobby",
            content="User enjoys taking the dog on long walks.",
        )
    )

    assert manager.search("dog walks") == [
        "User enjoys taking the dog on long walks.",
        "User has a dog named Max.",
    ]

    manager.close()


def test_manager_search_returns_empty_for_no_matches(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    assert manager.search("favorite color") == []

    manager.close()


def test_manager_search_handles_empty_query(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    assert manager.search("") == []

    manager.close()


def test_manager_rejects_empty_key(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    with pytest.raises(ValueError):
        manager.remember(
            MemoryCandidate(
                key="",
                content="User has a dog named Max.",
            )
        )

    manager.close()


def test_manager_rejects_empty_content(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    with pytest.raises(ValueError):
        manager.remember(
            MemoryCandidate(
                key="pet_dog",
                content="",
            )
        )

    manager.close()


def test_manager_strips_content_whitespace(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="   User has a dog named Max.   ",
        )
    )

    assert manager.get_all() == [
        "User has a dog named Max.",
    ]

    manager.close()


def test_manager_normalizes_key_case_and_whitespace(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="  PET_DOG  ",
            content="User has a dog named Max.",
        )
    )

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Buddy.",
        )
    )

    assert manager.get_all() == [
        "User has a dog named Buddy.",
    ]

    manager.close()


@pytest.mark.parametrize(
    "key",
    [
        "favorite color",
        "favorite-color",
        "favorite/color",
        "favorite.color",
        "favorite@color",
    ],
)
def test_manager_rejects_invalid_key_characters(
    tmp_path,
    key,
):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    with pytest.raises(ValueError):
        manager.remember(
            MemoryCandidate(
                key=key,
                content="Some memory.",
            )
        )

    manager.close()


def test_manager_rejects_key_longer_than_100_characters(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    key = "a" * 101

    with pytest.raises(ValueError):
        manager.remember(
            MemoryCandidate(
                key=key,
                content="Some memory.",
            )
        )

    manager.close()


def test_manager_updates_existing_memory(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="favorite_color",
            content="User's favorite color is green.",
        )
    )

    manager.remember(
        MemoryCandidate(
            key="favorite_color",
            content="User's favorite color is blue.",
        )
    )

    assert manager.get_all() == [
        "User's favorite color is blue.",
    ]

    manager.close()


def test_manager_can_forget_memory(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    manager.forget("pet_dog")

    assert manager.get_all() == []

    manager.close()


def test_manager_forget_normalizes_key(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember(
        MemoryCandidate(
            key="pet_dog",
            content="User has a dog named Max.",
        )
    )

    manager.forget("  PET_DOG  ")

    assert manager.get_all() == []

    manager.close()


def test_manager_forget_preserves_other_memories(tmp_path):
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

    manager.forget("pet_dog")

    assert manager.get_all() == [
        "User's favorite color is green.",
    ]

    manager.close()


def test_manager_can_forget_all_memories(tmp_path):
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

    manager.forget_all()

    assert manager.get_all() == []

    manager.close()


def test_manager_rejects_empty_forget_key(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    with pytest.raises(ValueError):
        manager.forget("")

    manager.close()


def test_manager_rejects_invalid_forget_key(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    with pytest.raises(ValueError):
        manager.forget("favorite color")

    manager.close()