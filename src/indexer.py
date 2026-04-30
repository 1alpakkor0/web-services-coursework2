import json
import os
import re
from collections import defaultdict


class Indexer:
    def __init__(self):
        self.index = defaultdict(dict)
        self.documents = {}

    def tokenize(self, text):
        text = text.lower()
        return re.findall(r"\b[a-z0-9]+\b", text)

    def build_index(self, pages):
        self.index = defaultdict(dict)
        self.documents = {}

        for doc_id, page in enumerate(pages, start=1):
            url = page["url"]
            content = page["content"]

            self.documents[str(doc_id)] = {
                "url": url,
                "content": content
            }

            tokens = self.tokenize(content)

            word_positions = defaultdict(list)

            for position, word in enumerate(tokens):
                word_positions[word].append(position)

            for word, positions in word_positions.items():
                self.index[word][str(doc_id)] = {
                    "frequency": len(positions),
                    "positions": positions
                }

        return {
            "documents": self.documents,
            "index": dict(self.index)
        }

def save_index(self, filepath, index_data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(index_data, file, indent=4)

def load_index(self, filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            "Index file not found. Please run the build command first."
        )

    with open(filepath, "r", encoding="utf-8") as file:
        index_data = json.load(file)

    self.documents = index_data["documents"]
    self.index = index_data["index"]

    return index_data