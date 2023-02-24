from rest_framework import serializers
from .models import Plan

class PlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Plan
    fields = (
      "stripe_subscription_id", 
      "status", 
      "billing_cycle_anchor",
      "start_date",
      "trial_start",
      "trial_end",
      "current_period_end",
      "current_period_start",
      "cancel_at",
      "canceled_at",
      "ended_at",
      "name",
      "lookup_key",
      "interval",
      "unit_amount",
      "currency"
    )