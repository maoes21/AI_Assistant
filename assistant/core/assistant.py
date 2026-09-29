from assistant.core.conversation import Conversation
from assistant.core.llm import LLMClient
from assistant.core.message_builder import MessageBuilder
from memory.extractor import (
    MemoryExtractionError,
    MemoryExtractor,
)
from memory.manager import MemoryManager


class Assistant:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8080/v1",
        model: str = "Qwen3-8B",
        memory_manager: MemoryManager | None = None,
        memory_extractor: MemoryExtractor | None = None,
        llm_client: LLMClient | None = None,
        message_builder: MessageBuilder | None = None,
    ):
        self.llm = llm_client or LLMClient(
            base_url=base_url,
            model=model,
        )

        self.client = self.llm.client
        self.model = self.llm.model

        self.conversation = Conversation()

        self.memory = memory_manager or MemoryManager()

        self.memory_extractor = memory_extractor or MemoryExtractor(
            llm=self.llm,
        )

        self.message_builder = (
            message_builder or MessageBuilder()
        )

    def chat(self, message: str) -> str:
        existing_memories = self.memory.get_all()

        try:
            memory_candidates = self.memory_extractor.extract(
                message,
                existing_memories=existing_memories,
            )
        except MemoryExtractionError:
            memory_candidates = []

        for candidate in memory_candidates:
            self.memory.remember(candidate)

        self.conversation.add_user_message(message)

        memory_query = "\n".join(
            self.conversation.get_user_messages()
        )

        relevant_memories = self.memory.search(memory_query)

        messages = self.message_builder.build(
            conversation_messages=(
                self.conversation.get_messages()
            ),
            relevant_memories=relevant_memories,
        )

        assistant_message = self.llm.chat(messages)

        self.conversation.add_assistant_message(
            assistant_message
        )

        return assistant_message

    def remember(self, candidate) -> None:
        self.memory.remember(candidate)

    def get_memories(self) -> list[str]:
        return self.memory.get_all()

    def close(self) -> None:
        self.memory.close()

    def forget(self, key: str) -> None:
        self.memory.forget(key)

    def forget_all(self) -> None:
        self.memory.forget_all()