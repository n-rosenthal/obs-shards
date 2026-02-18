from rest_framework.viewsets import ModelViewSet

from ..models import Activity
from ..serializers import ActivitySerializer

class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
