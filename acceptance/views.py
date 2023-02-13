from .models import Acceptance
from .serializers import AcceptanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class AcceptanceView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      lang = kwargs.get("lang", "es")
      acceptance = Acceptance.objects.filter(language=lang).latest("created_at")
      data = AcceptanceSerializer(acceptance).data
      return Response(data)
    except Acceptance.DoesNotExist:
      return Response(None, status=404)