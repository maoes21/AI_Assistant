from assistant.core.message_builder import MessageBuilder


def test_message_builder_returns_conversation_without_memories():
    builder = MessageBuilder()

    conversation = [
        {
            "role": "user",
            "content": "Hello.",
        }
    ]

    assert builder.build(conversation, []) == conversation


def test_message_builder_adds_memory_system_message():
    builder = MessageBuilder()

    conversation = [
        {
            "role": "user",
            "content": "Tell me about my dog.",
        }
    ]

    result = builder.build(
        conversation,
        ["User has a dog named Max."],
    )

    assert result == [
        {
            "role": "system",
            "content": (
                "You have access to the following long-term "
                "memories about the user. Use them when they "
                "are relevant to the current conversation.\n\n"
                "- User has a dog named Max."
            ),
        },
        {
            "role": "user",
            "content": "Tell me about my dog.",
        },
    ]


def test_message_builder_includes_multiple_memories():
    builder = MessageBuilder()

    result = builder.build(
        [],
        [
            "User has a dog named Max.",
            "User lives in Denmark.",
        ],
    )

    assert result[0]["content"] == (
        "You have access to the following long-term "
        "memories about the user. Use them when they "
        "are relevant to the current conversation.\n\n"
        "- User has a dog named Max.\n"
        "- User lives in Denmark."
    )


def test_message_builder_does_not_modify_conversation():
    builder = MessageBuilder()

    conversation = [
        {
            "role": "user",
            "content": "Hello.",
        }
    ]

    builder.build(
        conversation,
        ["User lives in Denmark."],
    )

    assert conversation == [
        {
            "role": "user",
            "content": "Hello.",
        }
    ]