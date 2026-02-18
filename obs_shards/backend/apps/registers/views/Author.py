from rest_framework.viewsets import ModelViewSet

from ..models import Author
from ..serializers import AuthorSerializer

class ActivityViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
