from rest_framework import serializers

from .models import Author, TextReference
from .serializers import AuthorSerializer

class TextReferenceSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = TextReference
        fields = "__all__"

