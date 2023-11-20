# modulos de rest_framework
from rest_framework import serializers
# modelos
from api.models import (
    AntecedentesMedicos,
    Usuario,
)

# Serializers


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class AntecedentesMedicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntecedentesMedicos
        fields = '__all__'
