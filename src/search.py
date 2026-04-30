import re


class SearchEngine:
    def __init__(self, index_data):
        self.documents = index_data.get("documents", {})
        self.index = index_data.get("index", {})

    def tokenize_query(self, query):
        query = query.lower()
        return re.findall(r"\b[a-z0-9]+\b", query)

    def print_word_index(self, word):
        word = word.lower()

        if word not in self.index:
            return f"No index entry found for '{word}'."

        return self.index[word]

    def find(self, query):
        query_terms = self.tokenize_query(query)

        if not query_terms:
            return []

        for term in query_terms:
            if term not in self.index:
                return []

        matching_doc_ids = set(self.index[query_terms[0]].keys())

        for term in query_terms[1:]:
            matching_doc_ids &= set(self.index[term].keys())

        results = []

        for doc_id in matching_doc_ids:
            score = sum(
                self.index[term][doc_id]["frequency"]
                for term in query_terms
            )

            results.append({
                "doc_id": doc_id,
                "url": self.documents[doc_id]["url"],
                "score": score,
                "matched_terms": query_terms
            })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results