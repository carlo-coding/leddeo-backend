from rest_framework import serializers
from .models import SubtitlesRecord, DownloadsRecord

class SubtitlesRecordSerializer(serializers.ModelSerializer): 
  class Meta:
    model = SubtitlesRecord
    fields = "__all__"

class DownloadsRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = DownloadsRecord
    fields = "__all__"