from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  stripe_subscription_id = models.CharField(max_length=40, primary_key=True)
  stripe_plan_id = models.CharField(max_length=40)
  active = models.BooleanField()
  billing_cycle_anchor = models.DateTimeField()
  name = models.CharField(max_length=40)
  start_date = models.DateTimeField(blank=True, null=True)
  trial_start = models.DateTimeField(blank=True, null=True)
  trial_end = models.DateTimeField(blank=True, null=True)
  current_period_end = models.DateTimeField(blank=True, null=True)
  current_period_start = models.DateTimeField(blank=True, null=True)
  cancel_at = models.DateTimeField(blank=True, null=True)
  canceled_at =  models.DateTimeField(blank=True, null=True)
  ended_at =  models.DateTimeField(blank=True, null=True)
