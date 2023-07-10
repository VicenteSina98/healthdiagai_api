from django.db import models

# Create your models here.
class Usuario(models.Model):
    email = models.EmailField(max_length=250, null=False, unique=True, default='correo@correo.com')
    password = models.CharField(max_length=16, null=False, default='1234')
    nombres = models.CharField(max_length=100, null=False)
    primer_apellido = models.CharField(max_length=60, null=False)
    segundo_apellido = models.CharField(max_length=60, null=False)
    fecha_nacimiento = models.DateField(null=False)
    altura = models.FloatField(null=False)
    peso =  models.FloatField(null=False)
    sexo = models.CharField(max_length=1, null=False)

class AntecedentesMedicos(models.Model):
	enfermedades_cronicas = models.CharField(max_length=250, null=True)
	historial_alergias = models.CharField(max_length=250, null=True)
	historial_cirugias = models.CharField(max_length=250, null=True)
	historial_medicamentos = models.CharField(max_length=250, null=True)
	historial_enfermedades_familia = models.CharField(max_length=250, null=True)
	historial_enfermedades_infecciosas = models.CharField(max_length=250, null=True)
	historial_habitos_salud = models.CharField(max_length=250, null=True)
	usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)

class Prediccion(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Mensaje(models.Model):
	prediccion = models.ForeignKey(Prediccion, on_delete=models.CASCADE)
	enviado_por_bot = models.BooleanField(null=False)