"""
The retrieval layer, this is the 'R' in RAG.

Approach: TF-IDF vectorization + cosine similarity over the knowledge base.
This is deliberately NOT a heavyweight embedding model — it needs no GPU,
no model download, and no API key, so the demo always works, but it's a
genuine, inspectable, non-black-box similarity search (a talking point for
your 'design tradeoff' segment of the video: you could swap this for
sentence-transformer embeddings for better semantic matching, at the cost
of a slower cold start and a model download).

Classification reuses the same TF-IDF space: each category's centroid is
the average vector of its own articles, and a query is classified by
whichever centroid it's closest to.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import list_kb_articles

CATEGORIES = ["Billing", "Technical", "Account Access", "General"]


class RetrievalEngine:
    def __init__(self):
        self.vectorizer = None
        self.article_vectors = None
        self.articles = []
        self.category_centroids = {}
        self.fit()

    def fit(self):
        """(Re)build the TF-IDF index from whatever is currently in the KB."""
        self.articles = list_kb_articles()
        corpus = [f"{a['title']} {a['content']} {a.get('keywords', '')}" for a in self.articles]

        if not corpus:
            self.vectorizer = None
            self.article_vectors = None
            return

        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.article_vectors = self.vectorizer.fit_transform(corpus)

        # category centroid = mean vector of that category's articles
        for cat in CATEGORIES:
            idxs = [i for i, a in enumerate(self.articles) if a["category"] == cat]
            if idxs:
                self.category_centroids[cat] = np.asarray(
                    self.article_vectors[idxs].mean(axis=0)
                )

    def classify(self, query):
        """Return (category, confidence 0-1) for a query string."""
        if not self.vectorizer or not self.category_centroids:
            return "General", 0.0

        q_vec = self.vectorizer.transform([query])
        best_cat, best_score = "General", -1.0
        for cat, centroid in self.category_centroids.items():
            score = cosine_similarity(q_vec, centroid)[0][0]
            if score > best_score:
                best_cat, best_score = cat, float(score)
        return best_cat, max(best_score, 0.0)

    def retrieve(self, query, top_k=3):
        """Return top_k (article, similarity_score) pairs for a query."""
        if not self.vectorizer or self.article_vectors is None:
            return []

        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.article_vectors)[0]
        ranked_idx = np.argsort(sims)[::-1][:top_k]
        return [(self.articles[i], float(sims[i])) for i in ranked_idx]
