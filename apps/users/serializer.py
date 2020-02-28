# encoding: utf-8

from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'password', 'nickname', 'mobile']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        obj = super(UserSerializer, self).create(validated_data=validated_data)
        obj.set_password(validated_data.get('password'))
        obj.save()
        return obj