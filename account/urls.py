from django.urls import path
from . import views
urlpatterns = [
  path("register", views.RegisterView.as_view(), name="register"),
  path("google", views.GoogleView.as_view(), name="google"),
  path("info", views.GetUserInfoView.as_view(), name="info"),
  path("edit", views.EditUserInfoView.as_view(), name="edit")
]