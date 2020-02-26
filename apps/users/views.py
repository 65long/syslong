from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate as auth
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework import status
import jwt

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.


class LoginView(APIView):
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            data = dict(token=jwt.encode(payload, settings.SECRET_KEY), username=user.username, status=200)
            return Response(data, 200)
        data = dict(message='auth failed', status=401)
        return Response(data, 401)

class MenuView(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response({'name': 'hahaha'})
