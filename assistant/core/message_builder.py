class MessageBuilder:
    _MEMORY_SYSTEM_PROMPT = (
        "You have access to the following long-term "
        "memories about the user. Use them when they "
        "are relevant to the current conversation."
    )

    def build(
        self,
        conversation_messages: list[dict[str, str]],
        relevant_memories: list[str],
    ) -> list[dict[str, str]]:
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
                        f"{self._MEMORY_SYSTEM_PROMPT}\n\n"
                        f"{memory_context}"
                    ),
                }
            )

        messages.extend(conversation_messages)

        return messages