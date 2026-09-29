class Conversation:
    def __init__(self):
        self.messages: list[dict[str, str]] = []

    def add_user_message(self, message: str) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str) -> None:
        self.messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def get_messages(self) -> list[dict[str, str]]:
        return list(self.messages)

    def get_user_messages(self) -> list[str]:
        return [
            message["content"]
            for message in self.messages
            if message["role"] == "user"
        ]