
from django.urls import path
from . import views

urlpatterns = [
  path("history", views.GetUserHistoryView.as_view(), name="history")
]