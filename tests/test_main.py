import builtins
from unittest.mock import patch
from src import main


def test_exit_command():
    with patch.object(builtins, "input", side_effect=["exit"]):
        main.main()


def test_help_command():
    with patch.object(builtins, "input", side_effect=["help", "exit"]):
        main.main()


def test_invalid_command():
    with patch.object(builtins, "input", side_effect=["unknown", "exit"]):
        main.main()