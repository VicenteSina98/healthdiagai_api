# modulos de django
from django.db import models
from django.contrib.auth.models import User

# Modelos


class Usuario(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=None)
    email = models.EmailField(unique=True, default=None)
    nombres = models.CharField(max_length=100, null=False)
    primer_apellido = models.CharField(max_length=60, null=False)
    segundo_apellido = models.CharField(max_length=60, null=False)
    fecha_nacimiento = models.DateField(null=False)
    altura = models.FloatField(null=False)
    peso = models.FloatField(null=False)
    sexo = models.CharField(max_length=1, null=False)


class AntecedentesMedicos(models.Model):
    enfermedades_cronicas = models.CharField(
        max_length=250, null=True, blank=True, default="")
    historial_alergias = models.CharField(
        max_length=250, null=True, blank=True, default="")
    historial_cirugias = models.CharField(
        max_length=250, null=True, blank=True, default="")
    historial_medicamentos = models.CharField(
        max_length=250, null=True, blank=True, default="")
    historial_enfermedades_familia = models.CharField(
        max_length=250, null=True, blank=True, default="")
    historial_enfermedades_infecciosas = models.CharField(
        max_length=250, null=True, blank=True, default="")
    historial_habitos_salud = models.CharField(
        max_length=250, null=True, blank=True, default="")
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, primary_key=True)
