import json

from assistant.core.llm import LLMClient
from memory.candidate import MemoryCandidate


class MemoryExtractionError(Exception):
    pass


class MemoryExtractor:
    def __init__(
        self,
        llm: LLMClient,
    ):
        self.llm = llm

    def extract(
        self,
        message: str,
        existing_memories: list[str] | None = None,
    ) -> list[MemoryCandidate]:
        message = message.strip()

        if not message:
            return []

        existing_memories = existing_memories or []

        existing_memory_context = ""

        if existing_memories:
            existing_memory_context = (
                "\n\nHere are the user's existing memories:\n"
                + "\n".join(
                    f"- {memory}"
                    for memory in existing_memories
                )
                + (
                    "\n\nIf the user's message updates one of "
                    "these memories, use the same key as the "
                    "existing memory."
                )
            )

        response = self.llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a memory extraction component for a "
                        "personal AI assistant.\n\n"
                        "Identify information about the user that is "
                        "likely to remain useful in future conversations.\n\n"
                        "Remember things such as the user's identity, "
                        "preferences, pets, relationships, location, "
                        "occupation, hobbies, long-term goals, and "
                        "ongoing projects.\n\n"
                        "Do not remember temporary states, casual "
                        "conversation, questions, requests, or general "
                        "facts that are not about the user.\n\n"
                        "For every memory, provide:\n"
                        "- key: a stable identifier for the specific fact\n"
                        "- content: a complete, concise factual statement "
                        "about the user\n\n"
                        "IMPORTANT: The content must contain the complete "
                        "fact, not only the value of the fact. It must be "
                        "understandable on its own without the original "
                        "user message.\n\n"
                        "For example, if the user says "
                        "\"My favorite programming language is Python.\", "
                        "return content such as "
                        "\"User's favorite programming language is Python.\" "
                        "Do NOT return only \"Python\".\n\n"
                        "If the user says "
                        "\"I have a dog named Max and I live in Denmark.\", "
                        "extract both facts separately, for example:\n"
                        "- \"User's dog's name is Max.\"\n"
                        "- \"User lives in Denmark.\"\n\n"
                        "Use the same key whenever the same fact is "
                        "mentioned again or updated. For example, the "
                        "user's favorite color should use the key "
                        "'favorite_color'.\n\n"
                        "When an existing memory represents the same "
                        "fact as the user's new message, update that "
                        "memory by returning its existing key with the "
                        "new content. Do not create a second key for "
                        "the same fact."
                        f"{existing_memory_context}\n\n"
                        "Return ONLY valid JSON in this exact format:\n"
                        "{\"memories\": ["
                        "{\"key\": \"example_key\", "
                        "\"content\": \"Example memory.\"}"
                        "]}\n\n"
                        "If there is nothing worth remembering, return:\n"
                        "{\"memories\": []}\n\n"
                        "Do not include explanations."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        if not response:
            return []

        try:
            data = json.loads(response)
        except json.JSONDecodeError as error:
            raise MemoryExtractionError(
                "Memory extractor returned invalid JSON."
            ) from error

        if not isinstance(data, dict):
            raise MemoryExtractionError(
                "Memory extractor returned an invalid response."
            )

        memories = data.get("memories")

        if not isinstance(memories, list):
            raise MemoryExtractionError(
                "Memory extractor response is missing a memories list."
            )

        candidates = []

        for memory in memories:
            if not isinstance(memory, dict):
                continue

            key = memory.get("key")
            content = memory.get("content")

            if not isinstance(key, str):
                continue

            if not isinstance(content, str):
                continue

            key = key.strip()
            content = content.strip()

            if not key or not content:
                continue

            candidates.append(
                MemoryCandidate(
                    content=content,
                    key=key,
                )
            )

        return candidates