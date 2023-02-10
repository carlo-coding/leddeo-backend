from rest_framework.serializers import ModelSerializer
from .models import History

class HistorySerializer(ModelSerializer):
  class Meta:
    model = History
    fields = ("id", "action", "description", "created_at")