import pytest

from memory.database import MemoryDatabase
from memory.manager import MemoryManager


def test_manager_can_remember(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember("My dog is named Max.")

    assert manager.get_all() == [
        "My dog is named Max."
    ]

    manager.close()


def test_manager_can_search(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember("My dog is named Max.")
    manager.remember("My favorite color is green.")

    assert manager.search("dog") == [
        "My dog is named Max."
    ]

    manager.close()


def test_manager_rejects_empty_memory(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    with pytest.raises(ValueError):
        manager.remember("")

    manager.close()


def test_manager_strips_whitespace(tmp_path):
    database = MemoryDatabase(str(tmp_path / "memory.db"))
    manager = MemoryManager(database)

    manager.remember("   My dog is named Max.   ")

    assert manager.get_all() == [
        "My dog is named Max."
    ]

    manager.close()