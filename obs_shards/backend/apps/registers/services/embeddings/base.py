"""
    `backend/apps/registers/services/embeddings/base.py`
"""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding for the given text.
        """
        raise NotImplementedError
