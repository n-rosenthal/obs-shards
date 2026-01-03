"""
    `backend/apps/notes/views.py`
    
    Views for the `obs-shards/notes` application.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Note
from .serializers import NoteSerializer, NoteCreateUpdateSerializer


class NoteViewSet(ModelViewSet):
    """
    Viewset for the `Note` model
    """
    #   Queryset for all the notes
    queryset = Note.objects.all()

    #   filters for the backend
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    #   fields for filtering
    filterset_fields = ["doctype", "date"]
    
    #   fields for searching
    search_fields = ["title", "content"]

    #   order-by fields
    ordering_fields = ["created_at", "updated_at", "date"]
    
    #   default order-by created_at field
    ordering = ["-created_at"]

    def get_serializer_class(self) -> NoteSerializer | NoteCreateUpdateSerializer:
        """
        Return the serializer class for the current action.

        If the action is "create", "update", or "partial_update", return
        `NoteCreateUpdateSerializer`. Otherwise, return `NoteSerializer`
        """
        if self.action in ["create", "update", "partial_update"]:
            return NoteCreateUpdateSerializer
        return NoteSerializer
