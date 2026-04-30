import time

from src.indexer import Indexer
from src.search import SearchEngine


def test_indexing_performance_on_larger_synthetic_dataset():
    pages = []

    for i in range(200):
        pages.append({
            "url": f"https://example.com/page{i}",
            "content": "good friends life search engine index " * 50
        })

    indexer = Indexer()

    start = time.perf_counter()
    index_data = indexer.build_index(pages)
    end = time.perf_counter()

    assert len(index_data["documents"]) == 200
    assert "search" in index_data["index"]
    assert end - start < 2.0


def test_search_performance_on_larger_synthetic_dataset():
    pages = []

    for i in range(200):
        pages.append({
            "url": f"https://example.com/page{i}",
            "content": "good friends life search engine index " * 50
        })

    indexer = Indexer()
    index_data = indexer.build_index(pages)
    search_engine = SearchEngine(index_data)

    start = time.perf_counter()
    results = search_engine.find("good friends")
    end = time.perf_counter()

    assert len(results) == 200
    assert end - start < 1.0