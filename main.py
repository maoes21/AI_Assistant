from assistant.core.assistant import Assistant


def main() -> None:
    assistant = Assistant()

    print("AI Assistant v0.4")
    print("Type 'exit' to quit.")
    print("Type '/remember <text>' to save a memory.")
    print("Type '/memories' to view saved memories.\n")

    try:
        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                break

            if user_input.startswith("/remember "):
                memory = user_input[len("/remember "):].strip()

                if memory:
                    assistant.remember(memory)
                    print("Assistant: I'll remember that.\n")
                else:
                    print("Assistant: Please provide something to remember.\n")

                continue

            if user_input == "/memories":
                memories = assistant.get_memories()

                if memories:
                    print("\nAssistant: I remember:")
                    for memory in memories:
                        print(f"- {memory}")
                    print()
                else:
                    print("\nAssistant: I don't have any memories yet.\n")

                continue

            response = assistant.chat(user_input)

            print(f"\nAssistant: {response}\n")

    finally:
        assistant.close()


if __name__ == "__main__":
    main()