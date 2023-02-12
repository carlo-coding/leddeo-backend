from rest_framework import serializers
from .models import TranslationRecord

class TranslationRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = TranslationRecord
    fields = "__all__"