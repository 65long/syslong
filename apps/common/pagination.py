# encoding: utf-8

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


# 自定义分页类
class CommonPagination(PageNumberPagination):
    # 默认每页显示多少个
    page_size = 10
    page_size_query_param = "size"
    # 最大页数不超过100
    max_page_size = 100
    # 获取页码数的
    page_query_param = "page"

    def get_paginated_response(self, data):
        "自定义分页后返回的内容"
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            ('data', data),
        ]))
