# modulos de django
from django.db import models
# modelos de otras apps
from api.models import Usuario

# Modelos


class Chat(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, default=None)
    nombre = models.CharField(max_length=100, null=False, blank=True)
    creado_el = models.DateTimeField(auto_now_add=True)


class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    enviado_por_bot = models.BooleanField(null=False)
    texto = models.TextField(null=False, blank=True)
