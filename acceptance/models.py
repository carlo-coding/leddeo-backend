from django.db import models
from django.contrib.auth.models import User

class Acceptance(models.Model):
  version = models.CharField(max_length=30)
  title = models.TextField()
  template = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

class UserAcceptance(models.Model):
  acceptance = models.ForeignKey(Acceptance, on_delete=models.SET_NULL, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  accepted = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)