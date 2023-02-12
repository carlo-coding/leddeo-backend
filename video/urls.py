from django.urls import path, include
from . import views


urlpatterns = [
  path("subtitles", views.SubtitlesRecordView.as_view(), name="subtitle"),
  path("downloads", views.DownloadsRecordView.as_view(), name="download")
]

urlpatterns = [
  path("upload", views.VideoUploadView.as_view(), name="upload"),
  path("caption", views.VideoCaptionView.as_view(), name="caption"),
  path("records/", include(urlpatterns))
]