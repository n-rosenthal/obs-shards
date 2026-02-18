"""
    `backend/apps/registers/services/embeddings/__init__.py`
    
    Embedding services
"""

from .factory import get_embedding_provider


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding for the given text.

    :param text: str, the text to generate an embedding for
    :return: list[float], the generated embedding
    """
    provider = get_embedding_provider()
    return provider.generate_embedding(text)