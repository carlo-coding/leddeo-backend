from django.urls import path
from . import views

urlpatterns = [
  path("check", views.HealthCheckView.as_view(), name="health/check")
]