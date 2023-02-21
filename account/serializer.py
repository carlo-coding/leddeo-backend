from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo
import re
import stripe
from plans.serializers import PlanSerializer
from plans.models import Plan
from django.contrib.auth.base_user import BaseUserManager
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields=("id", "email", "username", "password")
    extra_kwargs={
      "password": {
        "write_only": True
      }
    }
  
  def validate_email(self, email):
    found_user = User.objects.filter(email=email).first()
    if found_user:
      raise serializers.ValidationError("Email is already in use")
    return email
  
  def validate_password(self, password):
    pattern = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&.])[A-Za-z\d@$!%*#?&.]{8,}"
    validated = re.search(pattern, password)
    if not validated:
      raise serializers.ValidationError("Password not valid")
    return password

  def create(self, validated_data):

    user = User.objects.create_user(
      username=validated_data["username"],
      password=validated_data["password"],
      email=validated_data["email"],
    )
    verify_string = BaseUserManager().make_random_password()
    customer = stripe.Customer.create(email=validated_data["email"])
    userInfo = UserInfo.objects.create(
      user=user, 
      customer_id=customer.id, 
      verify_string=verify_string,
    )
    userInfo.save()
    return user
  

class UserInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserInfo
    fields = ("user_id", "customer_id", "email_verified")

class UserSerializer(serializers.ModelSerializer):
  plans = serializers.SerializerMethodField(read_only=True)
  info = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = User
    fields = ("id", "username", "email", "plans", "info")
  
  def get_plans(self, obj):
    plans = Plan.objects.filter(user=obj)
    return PlanSerializer(plans, many=True, read_only=True).data

  def get_info(self, obj):
    user_info = UserInfo.objects.filter(user=obj).first()
    return UserInfoSerializer(user_info, read_only=True).data
