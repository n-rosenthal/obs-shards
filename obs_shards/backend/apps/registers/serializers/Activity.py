from rest_framework import serializers

from .models import Activity, ReadingActivity
from .serializers import TextReferenceSerializer

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

class ReadingActivitySerializer(serializers.ModelSerializer):
    text = TextReferenceSerializer()

    class Meta:
        model = ReadingActivity
        fields = "__all__"
