from memory.candidate import MemoryCandidate


def _clean_value(value: str) -> str:
    return value.rstrip(".!?").strip()


class MemoryDetector:
    def detect(self, message: str) -> MemoryCandidate | None:
        message = message.strip()

        if not message:
            return None

        normalized_message = message.lower()

        if normalized_message.startswith("my name is "):
            name = _clean_value(message[len("my name is "):])

            return MemoryCandidate(
                content=f"User's name is {name}."
            )

        if normalized_message.startswith("my favorite color is "):
            color = _clean_value(
                message[len("my favorite color is "):]
            )

            return MemoryCandidate(
                content=f"User's favorite color is {color}."
            )

        if normalized_message.startswith("my dog is "):
            dog = _clean_value(
                message[len("my dog is "):]
            )

            return MemoryCandidate(
                content=f"User's dog is {dog}."
            )

        if normalized_message.startswith("my cat is "):
            cat = _clean_value(
                message[len("my cat is "):]
            )

            return MemoryCandidate(
                content=f"User's cat is {cat}."
            )

        if normalized_message.startswith("i live in "):
            location = _clean_value(
                message[len("i live in "):]
            )

            return MemoryCandidate(
                content=f"User lives in {location}."
            )

        if normalized_message.startswith("i work at "):
            workplace = _clean_value(
                message[len("i work at "):]
            )

            return MemoryCandidate(
                content=f"User works at {workplace}."
            )

        if normalized_message.startswith("i work as "):
            job = _clean_value(
                message[len("i work as "):]
            )

            return MemoryCandidate(
                content=f"User works as {job}."
            )

        if normalized_message.startswith("my job is "):
            job = _clean_value(
                message[len("my job is "):]
            )

            return MemoryCandidate(
                content=f"User's job is {job}."
            )

        if normalized_message.startswith("i have a dog"):
            return MemoryCandidate(
                content="User has a dog."
            )

        if normalized_message.startswith("i have a cat"):
            return MemoryCandidate(
                content="User has a cat."
            )

        return None