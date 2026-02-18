"""
    `shards/apps/registers/services/embeddings/factory.py`
    
    Factory for embedding providers
"""


from django.conf import settings
from .openai_provider import OpenAIEmbeddingProvider
from .local_provider import LocalEmbeddingProvider


def get_embedding_provider():
    provider = settings.EMBEDDING_PROVIDER

    if provider == "openai":
        return OpenAIEmbeddingProvider()

    if provider == "local":
        return LocalEmbeddingProvider()

    raise ValueError("Invalid embedding provider")
