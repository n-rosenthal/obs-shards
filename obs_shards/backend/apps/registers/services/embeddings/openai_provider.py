"""
    `shards/apps/registers/services/embeddings/openai_provider.py`
    
    OpenAI embedding provider
"""

from openai import OpenAI
from django.conf import settings
from .base import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding
