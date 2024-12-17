from django import forms
from django.contrib.auth.models import Group
from .models import Funcionario

class RegistroForm(forms.ModelForm):
    # Añadir el campo para seleccionar el grupo/rol
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Todos los grupos disponibles
        required=True,
        label="Seleccionar Rol",
        empty_label="Selecciona un grupo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Funcionario
        fields = ['nombre', 'cedula', 'CPS', 'sitio_expedicion', 'objeto', 'obligaciones', 'vr_inicial_contrato', 
                  'valor_mensual_honorarios', 'fecha_suscripcion', 'fecha_inicio', 'fecha_terminacion', 
                  'tiempo_ejecucion_dia', 'año_contrato', 'radicado']  # No incluimos 'grupo' aquí ya que es gestionado por el campo adicional.