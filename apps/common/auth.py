# encoding: utf-8

from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
import logging
from users.models import UserProfile


class SyslongAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        payload = None
        user = None
        try:
            # payload = jwt.decode(token, salt, True)
            user_dict = jwt_decode_handler(token)
            username = user_dict.get('username', '')
            user = cache.get(token)
            if not user:
                raise AuthenticationFailed('认证过期')
        except AuthenticationFailed:
            raise AuthenticationFailed('认证失败:无效用户')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('认证过期')
        except jwt.DecodeError:
            raise AuthenticationFailed('认证失败:无效token')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('非法认证')
        return user, token


