from openai import OpenAI


client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="local",
)


def chat(message: str) -> str:
    response = client.chat.completions.create(
        model="Qwen3-8B",
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )

    return response.choices[0].message.content


def main() -> None:
    print("AI Assistant v0.1")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = chat(user_input)

        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()