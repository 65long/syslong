from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import exceptions
from django.conf import settings
class SyslongAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        print('----------', token)
        salt = settings.SECRET_KEY
        payload = None
        try:
            payload = jwt.decode(token, salt, True)
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed('guoqi')
        except jwt.DecodeError:
            raise AuthenticationFailed('renzheng shibai')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('feifa token')
        return payload, token


