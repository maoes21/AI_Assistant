from unittest.mock import Mock, patch

from assistant.core.llm import LLMClient


def test_llm_client_stores_model():
    client = LLMClient(model="test-model")

    assert client.model == "test-model"


@patch("assistant.core.llm.OpenAI")
def test_llm_client_creates_openai_client(mock_openai):
    LLMClient(
        base_url="http://test-server/v1",
        model="test-model",
    )

    mock_openai.assert_called_once_with(
        base_url="http://test-server/v1",
        api_key="local",
    )


@patch("assistant.core.llm.OpenAI")
def test_llm_client_chat_sends_messages(mock_openai):
    response = Mock()
    response.choices = [
        Mock(
            message=Mock(
                content="Hello!",
            )
        )
    ]

    mock_openai.return_value.chat.completions.create.return_value = response

    client = LLMClient(
        base_url="http://test-server/v1",
        model="test-model",
    )

    messages = [
        {"role": "user", "content": "Hello"},
    ]

    client.chat(messages)

    mock_openai.return_value.chat.completions.create.assert_called_once_with(
        model="test-model",
        messages=messages,
    )


@patch("assistant.core.llm.OpenAI")
def test_llm_client_chat_returns_response_content(mock_openai):
    response = Mock()
    response.choices = [
        Mock(
            message=Mock(
                content="Hello!",
            )
        )
    ]

    mock_openai.return_value.chat.completions.create.return_value = response

    client = LLMClient(
        base_url="http://test-server/v1",
        model="test-model",
    )

    result = client.chat(
        [{"role": "user", "content": "Hello"}]
    )

    assert result == "Hello!"