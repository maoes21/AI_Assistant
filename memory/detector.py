class MemoryDetector:
    def should_remember(self, message: str) -> bool:
        message = message.strip().lower()

        if not message:
            return False

        memory_phrases = [
            "my name is",
            "my favorite",
            "i live in",
            "i work at",
            "i work as",
            "my job is",
            "my dog is",
            "my cat is",
            "i have a dog",
            "i have a cat",
        ]

        return any(
            phrase in message
            for phrase in memory_phrases
        )