from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario
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
    usuario = Usuario.objects.get(cedula=cedula)
    rendered = render_to_string('certificado_template.html', {
        'nombre': usuario.nombre,
        'cedula': usuario.cedula,
        'CPS': usuario.CPS,
        'sitio_expedicion': usuario.sitio_expedicion,
        'objeto': usuario.objeto,
        'obligaciones': usuario.obligaciones,
        'vr_inicial_contrato': usuario.vr_inicial_contrato,
        'valor_mensual_honorarios': usuario.valor_mensual_honorarios,
        'fecha_suscripcion': usuario.fecha_suscripcion,
        'fecha_inicio': usuario.fecha_inicio,
        'fecha_terminacion': usuario.fecha_terminacion,
        'tiempo_ejecucion_dia': usuario.tiempo_ejecucion_dia,
        'radicado': usuario.radicado,
        'año_contrato': usuario.año_contrato
    })
    pdf = pdfkit.from_string(rendered, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{cedula}.pdf"'
    return response

@login_required
def obtener_certificado(request, cedula):
    usuario = Usuario.objects.get(cedula=cedula)
    if usuario:
        archivo_pdf = generar_certificado(request, cedula)
        return archivo_pdf
    else:
        return JsonResponse({'mensaje': 'Usuario no encontrado'}, status=404)

@login_required
def preview_certificado(request, cedula):
    usuario = Usuario.objects.get(cedula=cedula)
    if usuario:
        return render(request, 'certificado_template.html', {
            'nombre': usuario.nombre,
            'cedula': usuario.cedula,
            'CPS': usuario.CPS,
            'sitio_expedicion': usuario.sitio_expedicion,
            'objeto': usuario.objeto,
            'obligaciones': usuario.obligaciones,
            'vr_inicial_contrato': usuario.vr_inicial_contrato,
            'valor_mensual_honorarios': usuario.valor_mensual_honorarios,
            'fecha_suscripcion': usuario.fecha_suscripcion,
            'fecha_inicio': usuario.fecha_inicio,
            'fecha_terminacion': usuario.fecha_terminacion,
            'tiempo_ejecucion_dia': usuario.tiempo_ejecucion_dia,
            'radicado': "123456",  # Ejemplo de radicado
            'año_contrato': usuario.año_contrato
        })
    else:
        return JsonResponse({'mensaje': 'Usuario no encontrado'}, status=404)

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

        usuario_existente = Usuario.objects.filter(cedula=cedula).first()
        if usuario_existente:
            return JsonResponse({'mensaje': 'La cédula ya está en uso. Por favor, usa una cédula diferente.'}, status=400)

        nuevo_usuario = Usuario(
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
        nuevo_usuario.save()
        return redirect('buscar_certificado')

    return render(request, 'crear_datos.html')

@login_required
def listar_cedulas(request):
    usuarios = Usuario.objects.all()
    datos_usuarios = [{'cedula': usuario.cedula, 'nombre': usuario.nombre, 'CPS': usuario.CPS, 'año_contrato': usuario.año_contrato} for usuario in usuarios]
    return render(request, 'listar_cedulas.html', {'datos_usuarios': datos_usuarios})

@login_required
def editar_datos(request, cedula):
    usuario = Usuario.objects.get(cedula=cedula)
    if request.method == 'POST':
        usuario.nombre = request.POST['nombre']
        usuario.CPS = request.POST['CPS']
        usuario.sitio_expedicion = request.POST['sitio_expedicion']
        usuario.objeto = request.POST['objeto']
        usuario.obligaciones = request.POST['obligaciones']
        usuario.vr_inicial_contrato = request.POST['vr_inicial_contrato']
        usuario.valor_mensual_honorarios = request.POST['valor_mensual_honorarios']
        usuario.fecha_suscripcion = datetime.strptime(request.POST['fecha_suscripcion'], '%Y-%m-%d').date()
        usuario.fecha_inicio = datetime.strptime(request.POST['fecha_inicio'], '%Y-%m-%d').date()
        usuario.fecha_terminacion = datetime.strptime(request.POST['fecha_terminacion'], '%Y-%m-%d').date()
        usuario.tiempo_ejecucion_dia = request.POST['tiempo_ejecucion_dia']
        usuario.año_contrato = usuario.fecha_suscripcion.year
        usuario.radicado = request.POST['radicado']
        usuario.save()
        return redirect('buscar_certificado')

    return render(request, 'editar_datos.html', {'usuario': usuario})

@login_required
def eliminar_datos(request, cedula):
    usuario = Usuario.objects.get(cedula=cedula)
    if usuario:
        usuario.delete()
    return redirect('buscar_certificado')

@login_required
def buscar_certificado(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        año = request.POST.get('año')
        usuario = Usuario.objects.filter(cedula=cedula, año_contrato=año).first()
        if usuario:
            return render(request, 'resultado_busqueda.html', {'usuario': usuario})
        else:
            return render(request, 'resultado_busqueda.html', {'mensaje': 'Usuario no encontrado. Por favor, crea un nuevo usuario.'})
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
                    Usuario.objects.update_or_create(
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
    usuarios = Usuario.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre', 'cedula', 'CPS', 'sitio_expedicion', 'objeto', 'obligaciones', 'vr_inicial_contrato', 'valor_mensual_honorarios', 'fecha_suscripcion', 'fecha_inicio', 'fecha_terminacion', 'tiempo_ejecucion_dia', 'año_contrato'])
    for usuario in usuarios:
        writer.writerow([usuario.nombre, usuario.cedula, usuario.CPS, usuario.sitio_expedicion, usuario.objeto, usuario.obligaciones, usuario.vr_inicial_contrato, usuario.valor_mensual_honorarios, usuario.fecha_suscripcion, usuario.fecha_inicio, usuario.fecha_terminacion, usuario.tiempo_ejecucion_dia, usuario.año_contrato])
    return response