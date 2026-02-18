"""
    `shards/apps/registers/services/embeddings/local_provider.py`
    
    Local embedding provider
"""

from sentence_transformers import SentenceTransformer
from .base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()
