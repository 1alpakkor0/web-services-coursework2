import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"


class Crawler:
    def __init__(self, base_url=BASE_URL, politeness_delay=6):
        self.base_url = base_url
        self.politeness_delay = politeness_delay
        self.visited_urls = set()

    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as error:
            print(f"Failed to fetch {url}: {error}")
            return None

    def parse_quotes(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        quotes = []

        for quote_block in soup.select(".quote"):
            quote_text = quote_block.select_one(".text")
            author = quote_block.select_one(".author")

            if quote_text and author:
                quotes.append({
                    "url": url,
                    "text": quote_text.get_text(strip=True),
                    "author": author.get_text(strip=True)
                })

        return quotes

    def get_next_page_url(self, html, current_url):
        soup = BeautifulSoup(html, "html.parser")
        next_link = soup.select_one("li.next a")

        if next_link and next_link.get("href"):
            return urljoin(current_url, next_link["href"])

        return None

    def crawl(self):
        current_url = self.base_url
        all_pages = []

        while current_url and current_url not in self.visited_urls:
            print(f"Crawling: {current_url}")
            self.visited_urls.add(current_url)

            html = self.fetch_page(current_url)
            if html is None:
                break

            quotes = self.parse_quotes(html, current_url)

            page_text = " ".join(
                f"{quote['text']} {quote['author']}" for quote in quotes
            )

            all_pages.append({
                "url": current_url,
                "content": page_text,
                "quotes": quotes
            })

            next_url = self.get_next_page_url(html, current_url)

            if next_url:
                print(f"Waiting {self.politeness_delay} seconds before next request...")
                time.sleep(self.politeness_delay)

            current_url = next_url

        return all_pages