from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from ledeo import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.permissions import IsAuthenticated
from ledeo.settings import SECRET_KEY as secretkey
from commons.utils import user_from_request
import jwt
class RegisterView(APIView):
  def post(self, request, *args, **kwargs):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
      "message": "User created successfully"
    })

class GetUserInfoView(APIView):
  permission_classes=[IsAuthenticated]
  def get(self, request):
    token = request.headers.get('Authorization').split(" ")[1]
    payload = jwt.decode(jwt=token, key=secretkey, algorithms=['HS256']) 
    user_id = payload.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if not user:
      return Response({ "message": "no user info available" }, status=400)
    user_data = UserSerializer(user).data
    return Response(user_data)

class GoogleView(APIView):
    def post(self, token_request):
        request = requests.Request()
        id_info = id_token.verify_oauth2_token(
            id_token=token_request.data.get("token"), 
            request=request, 
            audience=settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=15
          )
        if 'error' in id_info:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content, status=401)
        try:
            user = User.objects.get(email=id_info['email'])
        except User.DoesNotExist:
          serializer = RegisterSerializer(data={
            "username": id_info['email'],
            "email": id_info['email'],
            "password": BaseUserManager().make_random_password()+"ABCabc123@#$&"
          })
          serializer.is_valid(raise_exception=True)
          serializer.save()
        
        user = User.objects.get(email=id_info['email'])
        token = RefreshToken.for_user(user)
        response = {}
        response['username'] = user.username
        response['access'] = str(token.access_token)
        response['refresh'] = str(token)
        return Response(response)

class EditUserInfoView(APIView):
  permission_classes=[IsAuthenticated]
  def put(self, request):
    username = request.data.get("username", "")
    if not username:
      return Response({ "message": "no username provided" }, status=400)
      
    user = user_from_request(request)
    if not user:
      return Response({ "message": "user does not exists" }, status=404)

    user.username = username
    user.save()

    user_data = UserSerializer(user).data

    return Response(user_data, status=200)