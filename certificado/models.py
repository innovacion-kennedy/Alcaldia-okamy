from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Cesion(models.Model):
    cedente = models.CharField(max_length=255)
    cesionario = models.CharField(max_length=255)
    fecha_cesion = models.DateField()

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
    correo = models.EmailField(max_length=255, unique=True, default='correo@ejemplo.com')
    fecha_terminacion_prorrogas = models.DateField(null=True, blank=True, default='2024-12-31')
    plazo_total_ejecucion = models.IntegerField(null=True, blank=True, default=0)
    cesion = models.ForeignKey(Cesion, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    suspensiones = models.TextField(null=True, blank=True, default='')
    estado = models.CharField(max_length=255, choices=[('activo', 'Activo'), ('terminado', 'Terminado')], default='terminado')

class Radicado(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=255, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='radicados')