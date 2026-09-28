import json

from openai import OpenAI

from memory.candidate import MemoryCandidate


class MemoryExtractor:
    def __init__(
        self,
        client: OpenAI,
        model: str = "Qwen3-8B",
    ):
        self.client = client
        self.model = model

    def extract(self, message: str) -> list[MemoryCandidate]:
        message = message.strip()

        if not message:
            return []

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
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
                        "- content: a concise factual statement about the user\n\n"
                        "Use the same key whenever the same fact is "
                        "mentioned again. For example, the user's favorite "
                        "color should use the key 'favorite_color'.\n\n"
                        "Return ONLY valid JSON in this exact format:\n"
                        '{"memories": ['
                        '{"key": "example_key", '
                        '"content": "Example memory."}'
                        "]}\n\n"
                        "If there is nothing worth remembering, return:\n"
                        '{"memories": []}\n\n'
                        "Do not include explanations."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            return []

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return []

        memories = data.get("memories", [])

        if not isinstance(memories, list):
            return []

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