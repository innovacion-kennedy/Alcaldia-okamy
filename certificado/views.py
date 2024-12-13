from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Funcionario
from .forms import RegistroForm
from django.http import HttpResponse, JsonResponse
import pdfkit
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import csv
from datetime import datetime
from django.core.files.storage import default_storage
from django.template.loader import render_to_string

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        cedula = request.POST['cedula']
        password = request.POST['password']
        user = authenticate(request, username=cedula, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def generar_certificado(request, cedula):
    Funcionario = Funcionario.objects.get(cedula=cedula)
    rendered = render_to_string('certificado_template.html', {
        'nombre': Funcionario.nombre,
        'cedula': Funcionario.cedula,
        'CPS': Funcionario.CPS,
        'sitio_expedicion': Funcionario.sitio_expedicion,
        'objeto': Funcionario.objeto,
        'obligaciones': Funcionario.obligaciones,
        'vr_inicial_contrato': Funcionario.vr_inicial_contrato,
        'valor_mensual_honorarios': Funcionario.valor_mensual_honorarios,
        'fecha_suscripcion': Funcionario.fecha_suscripcion,
        'fecha_inicio': Funcionario.fecha_inicio,
        'fecha_terminacion': Funcionario.fecha_terminacion,
        'tiempo_ejecucion_dia': Funcionario.tiempo_ejecucion_dia,
        'radicado': Funcionario.radicado,
        'año_contrato': Funcionario.año_contrato
    })
    pdf = pdfkit.from_string(rendered, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{cedula}.pdf"'
    return response

@login_required
def obtener_certificado(request, cedula):
    Funcionario = Funcionario.objects.get(cedula=cedula)
    if Funcionario:
        archivo_pdf = generar_certificado(request, cedula)
        return archivo_pdf
    else:
        return JsonResponse({'mensaje': 'Funcionario no encontrado'}, status=404)

@login_required
def preview_certificado(request, cedula):
    Funcionario = Funcionario.objects.get(cedula=cedula)
    if Funcionario:
        return render(request, 'certificado_template.html', {
            'nombre': Funcionario.nombre,
            'cedula': Funcionario.cedula,
            'CPS': Funcionario.CPS,
            'sitio_expedicion': Funcionario.sitio_expedicion,
            'objeto': Funcionario.objeto,
            'obligaciones': Funcionario.obligaciones,
            'vr_inicial_contrato': Funcionario.vr_inicial_contrato,
            'valor_mensual_honorarios': Funcionario.valor_mensual_honorarios,
            'fecha_suscripcion': Funcionario.fecha_suscripcion,
            'fecha_inicio': Funcionario.fecha_inicio,
            'fecha_terminacion': Funcionario.fecha_terminacion,
            'tiempo_ejecucion_dia': Funcionario.tiempo_ejecucion_dia,
            'radicado': "123456",  # Ejemplo de radicado
            'año_contrato': Funcionario.año_contrato
        })
    else:
        return JsonResponse({'mensaje': 'Funcionario no encontrado'}, status=404)

@login_required
def crear_datos(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        cedula = request.POST['cedula']
        CPS = request.POST['CPS']
        sitio_expedicion = request.POST['sitio_expedicion']
        objeto = request.POST['objeto']
        obligaciones = request.POST['obligaciones']
        vr_inicial_contrato = request.POST['vr_inicial_contrato']
        valor_mensual_honorarios = request.POST['valor_mensual_honorarios']
        fecha_suscripcion = datetime.strptime(request.POST['fecha_suscripcion'], '%Y-%m-%d').date()
        fecha_inicio = datetime.strptime(request.POST['fecha_inicio'], '%Y-%m-%d').date()
        fecha_terminacion = datetime.strptime(request.POST['fecha_terminacion'], '%Y-%m-%d').date()
        tiempo_ejecucion_dia = request.POST['tiempo_ejecucion_dia']
        año_contrato = fecha_suscripcion.year

        Funcionario_existente = Funcionario.objects.filter(cedula=cedula).first()
        if Funcionario_existente:
            return JsonResponse({'mensaje': 'La cédula ya está en uso. Por favor, usa una cédula diferente.'}, status=400)

        nuevo_Funcionario = Funcionario(
            nombre=nombre,
            cedula=cedula,
            CPS=CPS,
            sitio_expedicion=sitio_expedicion,
            objeto=objeto,
            obligaciones=obligaciones,
            vr_inicial_contrato=vr_inicial_contrato,
            valor_mensual_honorarios=valor_mensual_honorarios,
            fecha_suscripcion=fecha_suscripcion,
            fecha_inicio=fecha_inicio,
            fecha_terminacion=fecha_terminacion,
            tiempo_ejecucion_dia=tiempo_ejecucion_dia,
            año_contrato=año_contrato
        )
        nuevo_Funcionario.save()
        return redirect('buscar_certificado')

    return render(request, 'crear_datos.html')

@login_required
def listar_cedulas(request):
    Funcionarios = Funcionario.objects.all()
    datos_Funcionarios = [{'cedula': Funcionario.cedula, 'nombre': Funcionario.nombre, 'CPS': Funcionario.CPS, 'año_contrato': Funcionario.año_contrato} for Funcionario in Funcionarios]
    return render(request, 'listar_cedulas.html', {'datos_Funcionarios': datos_Funcionarios})

@login_required
def editar_datos(request, cedula):
    Funcionario = Funcionario.objects.get(cedula=cedula)
    if request.method == 'POST':
        Funcionario.nombre = request.POST['nombre']
        Funcionario.CPS = request.POST['CPS']
        Funcionario.sitio_expedicion = request.POST['sitio_expedicion']
        Funcionario.objeto = request.POST['objeto']
        Funcionario.obligaciones = request.POST['obligaciones']
        Funcionario.vr_inicial_contrato = request.POST['vr_inicial_contrato']
        Funcionario.valor_mensual_honorarios = request.POST['valor_mensual_honorarios']
        Funcionario.fecha_suscripcion = datetime.strptime(request.POST['fecha_suscripcion'], '%Y-%m-%d').date()
        Funcionario.fecha_inicio = datetime.strptime(request.POST['fecha_inicio'], '%Y-%m-%d').date()
        Funcionario.fecha_terminacion = datetime.strptime(request.POST['fecha_terminacion'], '%Y-%m-%d').date()
        Funcionario.tiempo_ejecucion_dia = request.POST['tiempo_ejecucion_dia']
        Funcionario.año_contrato = Funcionario.fecha_suscripcion.year
        Funcionario.radicado = request.POST['radicado']
        Funcionario.save()
        return redirect('buscar_certificado')

    return render(request, 'editar_datos.html', {'Funcionario': Funcionario})

@login_required
def eliminar_datos(request, cedula):
    Funcionario = Funcionario.objects.get(cedula=cedula)
    if Funcionario:
        Funcionario.delete()
    return redirect('buscar_certificado')

@login_required
def buscar_certificado(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        año = request.POST.get('año')
        Funcionario = Funcionario.objects.filter(cedula=cedula, año_contrato=año).first()
        if Funcionario:
            return render(request, 'resultado_busqueda.html', {'Funcionario': Funcionario})
        else:
            return render(request, 'resultado_busqueda.html', {'mensaje': 'Funcionario no encontrado. Por favor, crea un nuevo Funcionario.'})
    return render(request, 'buscar_cert.html')

@login_required
def cargar_csv(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'mensaje': 'No se ha subido ningún archivo'}, status=400)
        
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            file_path = default_storage.save(file.name, file)
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    nombre, cedula, CPS, sitio_expedicion, objeto, obligaciones, vr_inicial_contrato, valor_mensual_honorarios, fecha_suscripcion, fecha_inicio, fecha_terminacion, tiempo_ejecucion_dia, año_contrato = row
                    Funcionario.objects.update_or_create(
                        cedula=cedula,
                        defaults={
                            'nombre': nombre,
                            'CPS': CPS,
                            'sitio_expedicion': sitio_expedicion,
                            'objeto': objeto,
                            'obligaciones': obligaciones,
                            'vr_inicial_contrato': vr_inicial_contrato,
                            'valor_mensual_honorarios': valor_mensual_honorarios,
                            'fecha_suscripcion': datetime.strptime(fecha_suscripcion, '%Y-%m-%d').date(),
                            'fecha_inicio': datetime.strptime(fecha_inicio, '%Y-%m-%d').date(),
                            'fecha_terminacion': datetime.strptime(fecha_terminacion, '%Y-%m-%d').date(),
                            'tiempo_ejecucion_dia': tiempo_ejecucion_dia,
                            'año_contrato': año_contrato
                        }
                    )
            return redirect('listar_cedulas')
        else:
            return JsonResponse({'mensaje': 'El archivo debe ser un CSV'}, status=400)
    return render(request, 'cargar_csv.html')

@login_required
def descargar_csv(request):
    Funcionarios = Funcionario.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Funcionarios.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre', 'cedula', 'CPS', 'sitio_expedicion', 'objeto', 'obligaciones', 'vr_inicial_contrato', 'valor_mensual_honorarios', 'fecha_suscripcion', 'fecha_inicio', 'fecha_terminacion', 'tiempo_ejecucion_dia', 'año_contrato'])
    for Funcionario in Funcionarios:
        writer.writerow([Funcionario.nombre, Funcionario.cedula, Funcionario.CPS, Funcionario.sitio_expedicion, Funcionario.objeto, Funcionario.obligaciones, Funcionario.vr_inicial_contrato, Funcionario.valor_mensual_honorarios, Funcionario.fecha_suscripcion, Funcionario.fecha_inicio, Funcionario.fecha_terminacion, Funcionario.tiempo_ejecucion_dia, Funcionario.año_contrato])
    return response