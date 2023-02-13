from .models import Acceptance
from .serializers import AcceptanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class AcceptanceView(APIView):
  def get(self, request):
    acceptance = Acceptance.objects.latest("created_at")
    data = AcceptanceSerializer(acceptance).data
    return Response(data)