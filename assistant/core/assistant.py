from openai import OpenAI


class Assistant:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8080/v1",
        model: str = "Qwen3-8B",
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key="local",
        )
        self.model = model
        self.conversation = []

    def chat(self, message: str) -> str:
        self.conversation.append(
            {
                "role": "user",
                "content": message,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation,
        )

        assistant_message = response.choices[0].message.content

        self.conversation.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        return assistant_message