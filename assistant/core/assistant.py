from openai import OpenAI

from memory.database import MemoryDatabase


class Assistant:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8080/v1",
        model: str = "Qwen3-8B",
        memory_database: MemoryDatabase | None = None,
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key="local",
        )
        self.model = model
        self.conversation = []
        self.memory = memory_database or MemoryDatabase()

    def chat(self, message: str) -> str:
        self.conversation.append(
            {
                "role": "user",
                "content": message,
            }
        )

        relevant_memories = self.memory.search_memories(message)

        messages = []

        if relevant_memories:
            memory_context = "\n".join(
                f"- {memory}"
                for memory in relevant_memories
            )

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "You have access to the following long-term "
                        "memories about the user. Use them when they "
                        "are relevant to the current conversation.\n\n"
                        f"{memory_context}"
                    ),
                }
            )

        messages.extend(self.conversation)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        assistant_message = response.choices[0].message.content

        self.conversation.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        return assistant_message

    def remember(self, content: str) -> None:
        self.memory.add_memory(content)

    def get_memories(self) -> list[str]:
        return self.memory.get_memories()

    def close(self) -> None:
        self.memory.close()