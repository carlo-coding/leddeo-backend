from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .functions.translate_json import translate_json
from rest_framework.permissions import IsAuthenticated
from commons.permissions import CustomerHasPlan
from history.models import History
from .models import TranslationRecord
from commons.utils import user_from_request
from .functions.detect_language import detect_language
from .serializers import TranslationRecordSerializer
import string
from time import time

class TranslateView(APIView):
  parser_class = (JSONParser,)
  permission_classes=[IsAuthenticated, CustomerHasPlan]

  def post(self, request, *args, **kwargs):
    st = time()
    user = user_from_request(request)

    data = request.data
    code = kwargs.get("code")

    text_content = "".join([i["text"] for i in data])
    number_of_words = sum([i.strip(string.punctuation).isalpha() for i in text_content.split()])
    from_code = detect_language(text_content)
    translation = translate_json(data, from_code, code)

    history = History.objects.create(
      user=user,
      action="ST",
      description=f"made a subtitles translation from {from_code} to {code}"
    )
    history.save()

    et = time()
    TranslationRecord.objects.create(
      user=user,
      number_of_words=number_of_words,
      source_language=from_code,
      target_language=code,
      process_duration=et - st,
    ).save()

    return Response(translation, content_type="application/json")


class TranslationRecordView(APIView):
  permission_classes=[IsAuthenticated]
  def get(self, request):
    objects = TranslationRecord.objects.all()
    data = TranslationRecordSerializer(objects, many=True).data
    return Response(data)