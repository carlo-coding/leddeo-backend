from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .functions.translate_json import translate_json
from rest_framework.permissions import IsAuthenticated
from commons.permissions import CustomerHasPlan
from history.models import History
from commons.utils import user_from_request
from .functions.detect_language import detect_language
class TranslateView(APIView):
  parser_class = (JSONParser,)
  permission_classes=[IsAuthenticated, CustomerHasPlan]

  def post(self, request, *args, **kwargs):
    user = user_from_request(request)

    data = request.data
    code = kwargs.get("code")

    from_code = detect_language("".join([i["text"] for i in data]))
    translation = translate_json(data, from_code, code)

    history = History.objects.create(
      user=user,
      action="ST",
      description=f"made a subtitles translation from {from_code} to {code}"
    )
    history.save()

    return Response(translation, content_type="application/json")
