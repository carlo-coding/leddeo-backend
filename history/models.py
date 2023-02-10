from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  action = models.CharField(
    max_length=30,
    choices=[
      ("VC", "Video Caption"),
      ("ST", "Subtitles Translation"),
      ("?", "Unknown")
    ],
    default="?"
  )
  description = models.TextField(blank=True, default="")
  created_at = models.DateTimeField(auto_now_add=True)