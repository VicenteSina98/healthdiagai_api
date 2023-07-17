from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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
        max_length=250, null=True, blank=True)
    historial_alergias = models.CharField(
        max_length=250, null=True, blank=True)
    historial_cirugias = models.CharField(
        max_length=250, null=True, blank=True)
    historial_medicamentos = models.CharField(
        max_length=250, null=True, blank=True)
    historial_enfermedades_familia = models.CharField(
        max_length=250, null=True, blank=True)
    historial_enfermedades_infecciosas = models.CharField(
        max_length=250, null=True, blank=True)
    historial_habitos_salud = models.CharField(
        max_length=250, null=True, blank=True)
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, primary_key=True)


class Prediccion(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, default=None)
    enfermedad1 = models.CharField(max_length=250, null=False, blank=True)
    enfermedad2 = models.CharField(max_length=250, null=False, blank=True)
    enfermedad3 = models.CharField(max_length=250, null=False, blank=True)
    enfermedad4 = models.CharField(max_length=250, null=False, blank=True)
    enfermedad5 = models.CharField(max_length=250, null=False, blank=True)
    profesional1 = models.CharField(max_length=250, null=False, blank=True)
    profesional2 = models.CharField(max_length=250, null=False, blank=True)
    profesional3 = models.CharField(max_length=250, null=False, blank=True)
    profesional4 = models.CharField(max_length=250, null=False, blank=True)
    profesional5 = models.CharField(max_length=250, null=False, blank=True)


class Mensaje(models.Model):
    prediccion = models.ForeignKey(Prediccion, on_delete=models.CASCADE)
    enviado_por_bot = models.BooleanField(null=False)
    texto = models.CharField(max_length=250, null=False, blank=True)
