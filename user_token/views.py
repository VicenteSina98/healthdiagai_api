# modulos de django
from django.shortcuts import render
# modulos de rest_framework
from rest_framework_simplejwt.views import TokenObtainPairView
# serializers
from user_token.serializers import MyTokenObtainPairSerializer

# Vistas


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
