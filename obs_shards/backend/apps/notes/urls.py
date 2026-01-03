"""
    `backend/apps/notes/urls.py`
    
    URLs for the `obs-shards/notes` application
"""
#   REST framework router
from rest_framework.routers import DefaultRouter

#   Entities viewsets
from .views import NoteViewSet


#   Router definition and registering of URLs
router = DefaultRouter()
router.register(r"notes", NoteViewSet, basename="note")

urlpatterns = router.urls
