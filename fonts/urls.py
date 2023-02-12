from django.urls import path, include
from . import views

urlpatterns = [
  path("list", views.ListFontsView.as_view(), name="list fonts"),
  path("<font>", views.GetFontView.as_view(), name="get font file")
]