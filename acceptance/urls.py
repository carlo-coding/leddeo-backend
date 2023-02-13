from django.urls import path
from . import views

urlpatterns = [
  path("latest/<lang>", views.AcceptanceView.as_view(), name="latest acceptance")
]