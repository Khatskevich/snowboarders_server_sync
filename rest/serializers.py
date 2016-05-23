from rest_framework import serializers
from rest_framework.decorators import api_view

from rest.rest_helper import get_validated_serializer
from suser.models import User


class UserHashSerializer(serializers.Serializer):
    hash = serializers.CharField(help_text='Unic hash of the session', required=True)

class UsersGetSerializer(UserHashSerializer):
    pass

class IdSerializer(UserHashSerializer):
    id = serializers.IntegerField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("is_superuser", "is_staff", "is_active", "user_permissions", "groups", 'password',)

