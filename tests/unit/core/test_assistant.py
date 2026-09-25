from assistant.core.assistant import Assistant


def test_assistant_uses_configured_model():
    assistant = Assistant(model="test-model")

    assert assistant.model == "test-model"


def test_assistant_has_client():
    assistant = Assistant()

    assert assistant.client is not None