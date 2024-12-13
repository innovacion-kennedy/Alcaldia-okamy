from django import forms
from .models import Funcionario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nombre', 'cedula', 'role', 'CPS', 'sitio_expedicion', 'objeto', 'obligaciones', 'vr_inicial_contrato', 'valor_mensual_honorarios', 'fecha_suscripcion', 'fecha_inicio', 'fecha_terminacion', 'tiempo_ejecucion_dia', 'año_contrato', 'radicado']
