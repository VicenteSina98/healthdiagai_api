from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_api.models import AntecedentesMedicos, Usuario, Prediccion, Mensaje


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class AntecedentesMedicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntecedentesMedicos
        fields = '__all__'


class PrediccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediccion
        fields = '__all__'


class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'