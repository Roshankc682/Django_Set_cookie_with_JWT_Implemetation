from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField(max_length=200, write_only=True)
    first_name = serializers.CharField(max_length=200, write_only=True)
    last_name = serializers.CharField(max_length=200, write_only=True)
    id = serializers.CharField(max_length=1000, write_only=True)
    username = serializers.CharField(max_length=1000, write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'id']

    def create(self, data):
        return Users.objects.create_user(**data)


# =====================Login token genreated===================================
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['user'] = user.username
        return token
# =============================================================================
