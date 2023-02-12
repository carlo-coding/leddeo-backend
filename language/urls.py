from django.urls import path, include
from . import views

urlpatterns = [
  path("translations", views.TranslationRecordView.as_view(), name="translate record")
]

urlpatterns = [
  path("translate/<code>", views.TranslateView.as_view(), name="translate"),
  path("records/", include(urlpatterns))
]