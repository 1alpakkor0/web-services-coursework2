from src.indexer import Indexer
from src.search import SearchEngine


def create_test_search_engine():
    pages = [
        {
            "url": "https://example.com/page1",
            "content": "good friends good life"
        },
        {
            "url": "https://example.com/page2",
            "content": "good people"
        },
        {
            "url": "https://example.com/page3",
            "content": "friends forever"
        }
    ]

    indexer = Indexer()
    index_data = indexer.build_index(pages)

    return SearchEngine(index_data)


def test_print_word_index_returns_postings():
    search_engine = create_test_search_engine()

    result = search_engine.print_word_index("good")

    assert "1" in result
    assert "2" in result
    assert result["1"]["frequency"] == 2


def test_find_single_word_returns_matching_pages():
    search_engine = create_test_search_engine()

    results = search_engine.find("life")

    assert len(results) == 1
    assert results[0]["url"] == "https://example.com/page1"


def test_find_multiple_words_returns_intersection_only():
    search_engine = create_test_search_engine()

    results = search_engine.find("good friends")

    assert len(results) == 1
    assert results[0]["url"] == "https://example.com/page1"


def test_find_is_case_insensitive():
    search_engine = create_test_search_engine()

    results = search_engine.find("GOOD FRIENDS")

    assert len(results) == 1
    assert results[0]["url"] == "https://example.com/page1"


def test_find_unknown_word_returns_empty_list():
    search_engine = create_test_search_engine()

    results = search_engine.find("unknownword")

    assert results == []


def test_find_empty_query_returns_empty_list():
    search_engine = create_test_search_engine()

    results = search_engine.find("")

    assert results == []