from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
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
            user = UserProfile.objects.filter(username=username).first()
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('guoqi')
        except jwt.DecodeError:
            raise AuthenticationFailed('renzheng shibai')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('feifa token')
        return user, token


