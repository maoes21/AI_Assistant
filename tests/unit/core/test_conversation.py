from assistant.core.conversation import Conversation


def test_conversation_starts_empty():
    conversation = Conversation()

    assert conversation.get_messages() == []


def test_conversation_adds_user_message():
    conversation = Conversation()

    conversation.add_user_message("Hello.")

    assert conversation.get_messages() == [
        {
            "role": "user",
            "content": "Hello.",
        }
    ]


def test_conversation_adds_assistant_message():
    conversation = Conversation()

    conversation.add_assistant_message("Hi!")

    assert conversation.get_messages() == [
        {
            "role": "assistant",
            "content": "Hi!",
        }
    ]


def test_conversation_preserves_message_order():
    conversation = Conversation()

    conversation.add_user_message("Hello.")
    conversation.add_assistant_message("Hi!")
    conversation.add_user_message("How are you?")

    assert conversation.get_messages() == [
        {
            "role": "user",
            "content": "Hello.",
        },
        {
            "role": "assistant",
            "content": "Hi!",
        },
        {
            "role": "user",
            "content": "How are you?",
        },
    ]


def test_get_messages_returns_copy():
    conversation = Conversation()

    conversation.add_user_message("Hello.")

    messages = conversation.get_messages()
    messages.append(
        {
            "role": "assistant",
            "content": "Injected.",
        }
    )

    assert conversation.get_messages() == [
        {
            "role": "user",
            "content": "Hello.",
        }
    ]


def test_get_user_messages_returns_only_user_messages():
    conversation = Conversation()

    conversation.add_user_message(
        "My dog's name is Max."
    )

    conversation.add_assistant_message(
        "Nice to meet Max!"
    )

    conversation.add_user_message(
        "He is five years old."
    )

    assert conversation.get_user_messages() == [
        "My dog's name is Max.",
        "He is five years old.",
    ]