from assistant.core.llm import LLMClient
from memory.extractor import MemoryExtractor
from memory.manager import MemoryManager


class Assistant:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8080/v1",
        model: str = "Qwen3-8B",
        memory_manager: MemoryManager | None = None,
        memory_extractor: MemoryExtractor | None = None,
        llm_client: LLMClient | None = None,
    ):
        self.llm = llm_client or LLMClient(
            base_url=base_url,
            model=model,
        )

        self.client = self.llm.client
        self.model = self.llm.model
        self.conversation = []

        self.memory = memory_manager or MemoryManager()

        self.memory_extractor = memory_extractor or MemoryExtractor(
            llm=self.llm,
        )

    def chat(self, message: str) -> str:
        memory_candidates = self.memory_extractor.extract(message)

        for candidate in memory_candidates:
            self.memory.remember(candidate)

        self.conversation.append(
            {"role": "user", "content": message}
        )

        relevant_memories = self.memory.search(message)

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

        assistant_message = self.llm.chat(messages)

        self.conversation.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        return assistant_message

    def remember(self, candidate) -> None:
        self.memory.remember(candidate)

    def get_memories(self) -> list[str]:
        return self.memory.get_all()

    def close(self) -> None:
        self.memory.close()