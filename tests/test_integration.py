from src.indexer import Indexer
from src.search import SearchEngine


def test_full_index_and_search_integration():
    pages = [
        {
            "url": "https://quotes.toscrape.com/",
            "content": "The world is full of good friends"
        },
        {
            "url": "https://quotes.toscrape.com/page/2/",
            "content": "Good friends make life better"
        },
        {
            "url": "https://quotes.toscrape.com/page/3/",
            "content": "Life is beautiful"
        }
    ]

    indexer = Indexer()
    index_data = indexer.build_index(pages)

    search_engine = SearchEngine(index_data)
    results = search_engine.find("good friends")

    assert len(results) == 2
    assert results[0]["score"] >= results[1]["score"]
    assert all("url" in result for result in results)


def test_saved_index_can_be_loaded_and_searched(tmp_path):
    pages = [
        {
            "url": "https://example.com/page1",
            "content": "search engines use inverted index structures"
        }
    ]

    filepath = tmp_path / "index.json"

    indexer = Indexer()
    index_data = indexer.build_index(pages)
    indexer.save_index(str(filepath), index_data)

    loaded_indexer = Indexer()
    loaded_data = loaded_indexer.load_index(str(filepath))

    search_engine = SearchEngine(loaded_data)
    results = search_engine.find("inverted index")

    assert len(results) == 1
    assert results[0]["url"] == "https://example.com/page1"