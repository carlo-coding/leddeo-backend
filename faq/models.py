from django.db import models

class Faq(models.Model):
  question = models.CharField(max_length=255)
  answer = models.TextField(blank=False)
  lang = models.CharField(max_length=5)
  category = models.CharField(max_length=255, default="")
  keywords = models.TextField(default="")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)