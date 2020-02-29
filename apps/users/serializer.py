# encoding: utf-8

from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'password', 'nickname', 'mobile', 'email', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True},
                        'is_superuser': {'read_only': True},
                        }

    def create(self, validated_data):
        obj = super(UserSerializer, self).create(validated_data=validated_data)
        obj.set_password(validated_data.get('password'))
        obj.save()
        return obj

    def update(self, instance, validated_data):
        print(validated_data)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
            validated_data.pop('password')
        obj = super(UserSerializer, self).update(instance=instance, validated_data=validated_data)
        return obj