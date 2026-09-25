from assistant.core.assistant import Assistant


def main() -> None:
    assistant = Assistant()

    print("AI Assistant v0.2")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = assistant.chat(user_input)

        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()