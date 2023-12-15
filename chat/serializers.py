# modulos de rest_framework
from rest_framework import serializers
# modelos
from chat.models import Chat, Mensaje

# Serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'
