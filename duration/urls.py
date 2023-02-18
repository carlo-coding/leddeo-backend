from django.urls import path
from . import views

urlpatterns = [
    path("translation", views.get_translation_duration),
    path("transcription", views.get_transcription_duration),
    path("download", views.get_download_duration)
]