from django.db import models
from django.contrib.auth.models import User

class TranslationRecord(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  number_of_words = models.IntegerField()
  source_language = models.CharField(max_length=5)
  target_language = models.CharField(max_length=5)
  process_duration = models.FloatField()
  created_at = models.DateTimeField(auto_now_add=True)