from dataclasses import dataclass


@dataclass
class MemoryRecord:
    key: str
    content: str