"""
    `backend/apps/notes/serializers.py`
    
    Serializers for the `obs-shards/notes` application.
"""
#   REST framework model serializers
from rest_framework import serializers

#   type `Note`
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
        Serializer for the `Note` model
    """
    class Meta:
        """
            Meta class for the `NoteSerializer`
        """
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "metadata",
            
            "doctype",
            
            "date",
            "interval",
            
            "created_at",
            "updated_at",
        ]


class NoteCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "title",
            "content",
            "doctype",
            "date",
            "metadata",
        ]
