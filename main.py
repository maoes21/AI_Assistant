from assistant.core.assistant import Assistant
from memory.candidate import MemoryCandidate


def main():
    assistant = Assistant()

    print("AI Assistant v0.4")
    print("Type 'exit' to quit.")
    print()

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                break

            if user_input == "/memories":
                memories = assistant.get_memories()

                if not memories:
                    print("Assistant: No memories stored.")
                else:
                    print("Assistant: Memories:")

                    for memory in memories:
                        print(f"- {memory}")

                continue

            if user_input.startswith("/remember "):
                parts = user_input.split(maxsplit=2)

                if len(parts) < 3:
                    print(
                        "Assistant: Usage: "
                        "/remember <key> <content>"
                    )
                    continue

                key = parts[1]
                content = parts[2]

                try:
                    assistant.remember(
                        MemoryCandidate(
                            key=key,
                            content=content,
                        )
                    )
                except ValueError as error:
                    print(f"Assistant: {error}")
                    continue

                print("Assistant: Memory saved.")
                continue

            if user_input.startswith("/forget"):
                parts = user_input.split(maxsplit=1)

                if len(parts) == 1:
                    print(
                        "Assistant: Usage: "
                        "/forget <key> or /forget all"
                    )
                    continue

                target = parts[1].strip()

                if target.lower() == "all":
                    assistant.memory.forget_all()
                    print("Assistant: All memories forgotten.")
                    continue

                try:
                    assistant.memory.forget(target)
                except ValueError as error:
                    print(f"Assistant: {error}")
                    continue

                print("Assistant: Memory forgotten.")
                continue

            response = assistant.chat(user_input)

            print(f"Assistant: {response}")

    finally:
        assistant.close()


if __name__ == "__main__":
    main()