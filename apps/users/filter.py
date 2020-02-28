# encoding: utf-8

from django_filters.rest_framework import FilterSet
import django_filters

from .models import UserProfile


class UserFilter(FilterSet):
    keyword = django_filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = UserProfile
        fields = '__all__'