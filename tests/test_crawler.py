from src.crawler import Crawler
from unittest.mock import patch


SAMPLE_HTML = """
<html>
<body>
    <div class="quote">
        <span class="text">“The world as we have created it is a process of our thinking.”</span>
        <small class="author">Albert Einstein</small>
    </div>
    <li class="next">
        <a href="/page/2/">Next</a>
    </li>
</body>
</html>
"""


def test_parse_quotes_extracts_quote_and_author():
    crawler = Crawler(politeness_delay=0)

    quotes = crawler.parse_quotes(SAMPLE_HTML, "https://quotes.toscrape.com/")

    assert len(quotes) == 1
    assert quotes[0]["author"] == "Albert Einstein"
    assert "world" in quotes[0]["text"]
    assert quotes[0]["url"] == "https://quotes.toscrape.com/"


def test_get_next_page_url_returns_absolute_url():
    crawler = Crawler(politeness_delay=0)

    next_url = crawler.get_next_page_url(
        SAMPLE_HTML,
        "https://quotes.toscrape.com/"
    )

    assert next_url == "https://quotes.toscrape.com/page/2/"



def test_fetch_page_success():
    crawler = Crawler(politeness_delay=0)

    html = crawler.fetch_page("https://quotes.toscrape.com/")
    assert html is not None


def test_fetch_page_failure():
    crawler= Crawler(politeness_delay=0)
    html=crawler.fetch_page("https://invalid-url-12345.com")
    assert html is None


def test_crawl_stops_without_next_page():
    crawler= Crawler(politeness_delay=0)

    with patch.object(crawler, "fetch_page", return_value="<html></html>"):
        pages = crawler.crawl()
        assert isinstance(pages, list)