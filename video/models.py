from django.db import models
from django.contrib.auth.models import User

class SubtitlesRecord(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  audio_duration = models.FloatField() #Seconds
  audio_size = models.FloatField() # Bytes
  process_duration = models.FloatField() #Seconds
  whisper_model = models.CharField(max_length=15)
  number_of_words = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)

class DownloadsRecord(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  video_duration = models.FloatField() #Seconds
  video_size = models.FloatField() # Bytes
  video_size_compressed = models.FloatField() # Bytes
  process_duration = models.FloatField() #Seconds
  created_at = models.DateTimeField(auto_now_add=True)