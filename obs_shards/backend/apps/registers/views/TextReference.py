from rest_framework.viewsets import ModelViewSet

from ..models import TextReference
from ..serializers import TextReferenceSerializer


class TextReferenceViewSet(ModelViewSet):
    queryset = TextReference.objects.all()
    serializer_class = TextReferenceSerializer