from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate as auth
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework import status
import jwt
from .models import WebRes
import logging

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.



class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            data = dict(token=jwt_encode_handler(payload), username=user.username, status=200)
            return Response(data, 200)
        data = dict(message='auth failed', status=401)
        return Response(data, 401)


class MenuView(APIView):
    # authentication_classes = []

    def get(self, request, *args, **kwargs):
        webres = request.user.role.resource.filter(is_menu=True).all()
        logging.info('webres-------{}'.format(webres))
        res = []
        temp_dic = {}
        for web in webres:
                logging.info('web pid----%s' %web.pid)
                if web.pid is None:
                    if web.id not in temp_dic:
                        temp_dic[web.id] = {'name': web.name, 'path': web.path, 'children': []}
                    else:
                        temp_dic[web.id]['name'] = web.name
                        temp_dic[web.id]['path'] = web.path
                else:
                    child = {'name': web.name, 'path': web.path}
                    if web.pid.id not in temp_dic:
                        temp_dic[web.pid.id] = {'children': [child]}
                    else:
                        temp_dic[web.pid.id]['children'].append(child)

        return Response({'menu': temp_dic.values()})
