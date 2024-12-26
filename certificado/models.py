from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Funcionario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='funcionario')
    nombre = models.CharField(max_length=255)
    cedula = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255)
    CPS = models.CharField(max_length=255)
    sitio_expedicion = models.CharField(max_length=255)
    objeto = models.TextField()
    obligaciones = models.TextField()
    vr_inicial_contrato = models.IntegerField()
    valor_mensual_honorarios = models.IntegerField()
    fecha_suscripcion = models.DateField()
    fecha_inicio = models.DateField()
    fecha_terminacion = models.DateField()
    tiempo_ejecucion_dia = models.IntegerField()
    año_contrato = models.IntegerField()
    radicado = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255, unique=True)

class Radicado(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=255, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='radicados')