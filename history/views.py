from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from commons.utils import user_from_request
from .models import History
from .serializers import HistorySerializer

class GetUserHistoryView(APIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request):
    user = user_from_request(request)
    if not user:
      return Response({"message": "user not found"}, status=404)
    history = History.objects.filter(user=user)
    history = HistorySerializer(history, many=True).data
    return Response(history)