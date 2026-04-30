import json

from src.indexer import Indexer


def test_tokenize_is_case_insensitive_and_removes_punctuation():
    indexer = Indexer()

    tokens = indexer.tokenize("Good, GOOD! Friends.")

    assert tokens == ["good", "good", "friends"]


def test_build_index_stores_frequency_and_positions():
    pages = [
        {
            "url": "https://example.com/page1",
            "content": "good friends good"
        }
    ]

    indexer = Indexer()
    index_data = indexer.build_index(pages)

    assert "good" in index_data["index"]
    assert "friends" in index_data["index"]

    good_posting = index_data["index"]["good"]["1"]

    assert good_posting["frequency"] == 2
    assert good_posting["positions"] == [0, 2]


def test_save_and_load_index(tmp_path):
    pages = [
        {
            "url": "https://example.com/page1",
            "content": "life is good"
        }
    ]

    filepath = tmp_path / "index.json"

    indexer = Indexer()
    index_data = indexer.build_index(pages)
    indexer.save_index(str(filepath), index_data)

    loaded_indexer = Indexer()
    loaded_data = loaded_indexer.load_index(str(filepath))

    assert loaded_data["documents"]["1"]["url"] == "https://example.com/page1"
    assert "life" in loaded_data["index"]