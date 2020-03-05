# encoding: utf-8
__auther__ = 'liufulong'
__date__ = '2020/1/8 22:07'


import traceback
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (AuthenticationFailed, MethodNotAllowed, NotAuthenticated,
                                       PermissionDenied as RestPermissionDenied,
                                       ValidationError,
                                       Throttled)
from django.http import Http404
# from component.constants import ResponseCodeStatus
# from common.log import logger


def exception_handler(exc, content):
    if not hasattr(exc, "detail"):
        exc.detail = getattr(exc, "message", "")
    data = dict(data=None)
    if isinstance(exc, Throttled):
        temp_data = {
            'message': exc.detail,
            'code': status.HTTP_429_TOO_MANY_REQUESTS,
        }
        data.update(temp_data)
        return Response(data, status=status.HTTP_429_TOO_MANY_REQUESTS)
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        temp_data = {
            'message': exc.detail,
            'code': status.HTTP_401_UNAUTHORIZED,
            # 'login_url': LOGIN_URL
        }
        data.update(temp_data)
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, PermissionDenied) or isinstance(exc, RestPermissionDenied):
        temp_data = {
            'code': status.HTTP_403_FORBIDDEN,
            'message': exc.detail
        }
        data.update(temp_data)
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, Http404):
        # 更改返回的状态为为自定义错误类型的状态码
        print(type(exc))
        data.update({
                'code': status.HTTP_404_NOT_FOUND,
                'message': exc.detail or u'不能找到您请求的资源',
            })
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, ValidationError):
        data.update({
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': exc.detail
        })

    elif isinstance(exc, MethodNotAllowed):
        data.update({
                'code': status.HTTP_405_METHOD_NOT_ALLOWED,
                'message': exc.detail,
            })

    else:
            # 调试模式
            # logger.error(traceback.format_exc())
            # print traceback.format_exc()
            # if settings.RUN_MODE != 'PRODUCT':
            #     raise exc
            # 正式环境，屏蔽500
        data.update({
                'code': status.HTTP_200_OK,
                'message': exc.detail,
            })

        # set_rollback()
    return Response(data, status=status.HTTP_200_OK)