from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import os

#C:\Windows\Fonts
LOCAL_FONT_DIR = "C:\Windows\Fonts"

class ListFontsView(APIView):
  def get(self, request):
    fonts = [f for f in os.listdir(LOCAL_FONT_DIR) if f.endswith(".ttf")]
    return Response(fonts)

class GetFontView(APIView):
  def get(self, request, *args, **kwargs):
    filename = kwargs.get("font", "")
    file_path = os.path.join(LOCAL_FONT_DIR, filename)
    if os.path.exists(file_path):
      with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/x-font-ttf")
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response
    else:
      return HttpResponse("Archivo no encontrado", status=404)