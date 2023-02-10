from rest_framework import viewsets
from rest_framework.response import Response
from .models import Faq
from .serializer import FaqSerializer
from commons.permissions import ReadonlyIfNotAdmin

class ProductViewSet(viewsets.ModelViewSet):
  queryset = Faq.objects.all()
  serializer_class = FaqSerializer
  lookup_field = "pk"
  permission_classes = (ReadonlyIfNotAdmin,)

