
from rest_framework import serializers
from .models import Acceptance

class AcceptanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Acceptance
    fields = "__all__"