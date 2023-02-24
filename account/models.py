from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserInfo(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  email_verified =models.BooleanField(default=False)
  balance = models.FloatField(default=0, null=True)
  verify_string = models.TextField(default="",null=True)
  customer_id = models.CharField(max_length=40)