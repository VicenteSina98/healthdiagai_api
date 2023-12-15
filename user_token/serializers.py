# modulos de django
from django.contrib.auth.models import User
# modulos de rest_framework
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token
