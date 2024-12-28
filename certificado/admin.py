from django.contrib import admin
from .models import Usuario, Funcionario, Radicado, Cesion

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'role', 'CPS', 'sitio_expedicion')
    search_fields = ('nombre', 'cedula', 'CPS')
    list_filter = ('role', 'sitio_expedicion')

@admin.register(Radicado)
class RadicadoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'usuario')
    search_fields = ('numero', 'usuario__username')

@admin.register(Cesion)
class CesionAdmin(admin.ModelAdmin):
    list_display = ('cedente', 'cesionario', 'fecha_cesion')
    search_fields = ('cedente', 'cesionario')
