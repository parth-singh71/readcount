from rest_framework import serializers
from .models import StoryView


class StoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryView
        fields = '__all__'
