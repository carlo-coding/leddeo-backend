from rest_framework.decorators import api_view
from rest_framework.response import Response
from .functions import preditions

@api_view(["POST"])
def get_download_duration(request):
  duration = request.data.get("duration", None)
  size = request.data.get("size", None)
  if not duration or not size:
    return Response({ "message": "body fields not valid" }, status=400)
  duration = float(duration)
  size = float(size)
  return Response({ "prediction": preditions.predict_download(duration, size) })

@api_view(["POST"])
def get_transcription_duration(request):
  duration = request.data.get("duration", None)
  size = request.data.get("size", None)
  if not duration or not size:
    return Response({ "message": "body fields not valid" }, status=400)
  duration = float(duration)
  size = float(size)
  return Response({ "prediction": preditions.predict_transcription(duration, size) })

@api_view(["POST"])
def get_translation_duration(request):
  words = request.data.get("words", None)
  if not words:
    return Response({ "message": "body fields not valid" }, status=400)
  words = int(words)
  return Response({ "prediction": preditions.predict_translation(words) })
