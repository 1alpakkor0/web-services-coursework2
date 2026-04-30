import builtins
from unittest.mock import patch

from src import main


def test_print_before_loading_index(capsys):
    with patch.object(builtins, "input", side_effect=["print love", "exit"]):
        main.main()

    output = capsys.readouterr().out
    assert "No index loaded" in output


def test_find_before_loading_index(capsys):
    with patch.object(builtins, "input", side_effect=["find good friends", "exit"]):
        main.main()

    output = capsys.readouterr().out
    assert "No index loaded" in output


def test_print_command_wrong_usage(capsys, tmp_path):
    main.INDEX_FILE = str(tmp_path / "index.json")

    pages = [{"url": "https://example.com", "content": "love life"}]

    with patch.object(main.Crawler, "crawl", return_value=pages):
        with patch.object(builtins, "input", side_effect=["build", "print", "exit"]):
            main.main()

    output = capsys.readouterr().out
    assert "Usage: print <word>" in output


def test_find_command_wrong_usage(capsys, tmp_path):
    main.INDEX_FILE = str(tmp_path / "index.json")

    pages = [{"url": "https://example.com", "content": "love life"}]

    with patch.object(main.Crawler, "crawl", return_value=pages):
        with patch.object(builtins, "input", side_effect=["build", "find", "exit"]):
            main.main()

    output = capsys.readouterr().out
    assert "Usage: find <query terms>" in output


def test_load_missing_index_file(capsys, tmp_path):
    main.INDEX_FILE = str(tmp_path / "missing_index.json")

    with patch.object(builtins, "input", side_effect=["load", "exit"]):
        main.main()

    output = capsys.readouterr().out
    assert "Index file not found" in output


def test_build_load_print_and_find_through_cli(capsys, tmp_path):
    main.INDEX_FILE = str(tmp_path / "index.json")

    pages = [
        {
            "url": "https://example.com/page1",
            "content": "good friends good"
        },
        {
            "url": "https://example.com/page2",
            "content": "good life"
        }
    ]

    commands = [
        "build",
        "load",
        "print good",
        "find good friends",
        "find unknownword",
        "exit"
    ]

    with patch.object(main.Crawler, "crawl", return_value=pages):
        with patch.object(builtins, "input", side_effect=commands):
            main.main()

    output = capsys.readouterr().out

    assert "Index built successfully" in output
    assert "Index loaded successfully" in output
    assert "Found 1 matching page" in output
    assert "No matching pages found" in output