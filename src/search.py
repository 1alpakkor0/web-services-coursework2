import math
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

    def calculate_tfidf_score(self, term, doc_id):
        """
        Calculate TF-IDF score for a term in a document.

        TF = frequency of the term in the document
        IDF = log((N + 1) / (df + 1)) + 1

        Smoothing is used to avoid division by zero.
        """
        total_documents = len(self.documents)
        document_frequency = len(self.index.get(term, {}))

        term_frequency = self.index[term][doc_id]["frequency"]

        idf = math.log((total_documents + 1) / (document_frequency + 1)) + 1

        return term_frequency * idf

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
                self.calculate_tfidf_score(term, doc_id)
                for term in query_terms
            )

            results.append({
                "doc_id": doc_id,
                "url": self.documents[doc_id]["url"],
                "score": round(score, 4),
                "matched_terms": query_terms
            })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results