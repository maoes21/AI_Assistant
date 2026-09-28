from unittest.mock import Mock, patch

from main import main


def test_main_can_show_memories(capsys):
    assistant = Mock()

    assistant.get_memories.return_value = [
        "User has a dog named Max.",
        "User's favorite color is green.",
    ]

    with patch("main.Assistant", return_value=assistant):
        with patch(
            "builtins.input",
            side_effect=[
                "/memories",
                "exit",
            ],
        ):
            main()

    output = capsys.readouterr().out

    assert "User has a dog named Max." in output
    assert "User's favorite color is green." in output

    assistant.close.assert_called_once()


def test_main_reports_empty_memories(capsys):
    assistant = Mock()

    assistant.get_memories.return_value = []

    with patch("main.Assistant", return_value=assistant):
        with patch(
            "builtins.input",
            side_effect=[
                "/memories",
                "exit",
            ],
        ):
            main()

    output = capsys.readouterr().out

    assert "No memories stored." in output

    assistant.close.assert_called_once()


def test_main_can_remember(capsys):
    assistant = Mock()

    with patch("main.Assistant", return_value=assistant):
        with patch(
            "builtins.input",
            side_effect=[
                "/remember favorite_color My favorite color is green.",
                "exit",
            ],
        ):
            main()

    output = capsys.readouterr().out

    assert "Memory saved." in output

    assistant.remember.assert_called_once()

    candidate = assistant.remember.call_args.args[0]

    assert candidate.key == "favorite_color"
    assert candidate.content == "My favorite color is green."

    assistant.close.assert_called_once()


def test_main_requires_key_and_content_for_remember(capsys):
    assistant = Mock()

    with patch("main.Assistant", return_value=assistant):
        with patch(
            "builtins.input",
            side_effect=[
                "/remember favorite_color",
                "exit",
            ],
        ):
            main()

    output = capsys.readouterr().out

    assert (
        "Usage: /remember <key> <content>"
        in output
    )

    assistant.remember.assert_not_called()

    assistant.close.assert_called_once()


def test_main_can_forget_memory(capsys):
    assistant = Mock()

    with patch("main.Assistant", return_value=assistant):
        with patch(
            "builtins.input",
            side_effect=[
                "/forget favorite_color",
                "exit",
            ],
        ):
            main()

    output = capsys.readouterr().out

    assert "Memory forgotten." in output

    assistant.memory.forget.assert_called_once_with(
        "favorite_color"
    )

    assistant.close.assert_called_once()


def test_main_can_forget_all_memories(capsys):
    assistant = Mock()

    with patch("main.Assistant", return_value=assistant):
        with patch(
            "builtins.input",
            side_effect=[
                "/forget all",
                "exit",
            ],
        ):
            main()

    output = capsys.readouterr().out

    assert "All memories forgotten." in output

    assistant.memory.forget_all.assert_called_once()

    assistant.close.assert_called_once()


def test_main_requires_target_for_forget(capsys):
    assistant = Mock()

    with patch("main.Assistant", return_value=assistant):
        with patch(
            "builtins.input",
            side_effect=[
                "/forget",
                "exit",
            ],
        ):
            main()

    output = capsys.readouterr().out

    assert (
        "Usage: /forget <key> or /forget all"
        in output
    )

    assistant.memory.forget.assert_not_called()
    assistant.memory.forget_all.assert_not_called()

    assistant.close.assert_called_once()