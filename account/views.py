from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponseRedirect
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from ledeo import settings
from ledeo.settings import (
  EMAIL_VERIFY_URL as verify_url, 
  EMAIL_VERIFY_REDIRECT_URL as redirect_url
)
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.permissions import IsAuthenticated
from commons.utils import user_from_request, send_mail
from acceptance.functions import save_acceptance
from .models import UserInfo
class RegisterView(APIView):
  def post(self, request, *args, **kwargs):
    acceptance_id = request.data.get("acceptance_id", "")
    serializer = RegisterSerializer(data={
      "username": request.data.get("username", ""),
      "password": request.data.get("password", ""),
      "email": request.data.get("email", ""),
    })
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    verify_string = UserInfo.objects.filter(user=user).first().verify_string
    save_acceptance(
      user=user,
      acceptance_id=acceptance_id
    )

    send_mail(
      subject="Verificación de cuenta", 
      to=user.email, 
      template="verify_email.html",
      template_context={
        "username": user.username, 
        "url": f"{verify_url}/{verify_string}"},
    )

    return Response({
      "message": "User created successfully"
    })
  
class VerifyEmailView(APIView):
  def get(self, request, *args, **kwargs):
    code = kwargs.get("code")
    if not code:
      return Response({ "err": "Invalid code" }, status=400)
    userInfo = UserInfo.objects.filter(verify_string=code).first()
    if not userInfo:
      return Response({ "err": "User not found" }, status=404)
    userInfo.email_verified = True
    userInfo.verify_string = ""
    userInfo.save()
    return HttpResponseRedirect(redirect_to=redirect_url)

class GetUserInfoView(APIView):
  permission_classes=[IsAuthenticated]
  def get(self, request):
    user = user_from_request(request)
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
          user = serializer.save()
          acceptance_id = token_request.data.get("acceptance_id", "")
          save_acceptance(
            user=user,
            acceptance_id=acceptance_id
          )
          userInfo = UserInfo.objects.filter(user=user).first()
          userInfo.email_verified = True
          userInfo.save()
        
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