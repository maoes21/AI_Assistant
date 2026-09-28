from openai import OpenAI


class LLMClient:
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

    def chat(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content