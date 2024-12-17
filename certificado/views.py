from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario, Funcionario
from .forms import RegistroForm
from django.http import HttpResponse, JsonResponse
import pdfkit
import csv
from datetime import datetime
from django.core.files.storage import default_storage
from django.template.loader import render_to_string

@login_required
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')

@login_required
def gestionar_funcionario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    # Intentamos obtener el Funcionario asociado al usuario, si no existe, lo creamos.
    try:
        funcionario = usuario.funcionario  # Si ya existe el Funcionario
    except Funcionario.DoesNotExist:
        funcionario = None

    # Si el método es POST, intentamos guardar el funcionario.
    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=funcionario)
        if form.is_valid():
            nuevo_funcionario = form.save(commit=False)
            nuevo_funcionario.usuario = usuario  # Asociamos el Funcionario al Usuario
            nuevo_funcionario.save()  # Guardamos el Funcionario

            # Redirigimos a la vista de generar certificado si es necesario
            return redirect('certificado:generar_certificado', cedula=nuevo_funcionario.cedula)
    else:
        form = RegistroForm(instance=funcionario)

    return render(request, 'gestionar_funcionario.html', {'form': form, 'usuario': usuario, 'funcionario': funcionario})


@login_required
def eliminar_datos(request, cedula):
    funcionario = get_object_or_404(Funcionario, cedula=cedula)
    funcionario.delete()  
    return redirect('certificado:listar_cedulas')  

@login_required
def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea el usuario
            login(request, user)  # Autentica al usuario
            return redirect('certificado:buscar_certificado')  # Redirige a la vista de búsqueda
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})

@login_required
def login_view(request):
    if request.method == 'POST':
        cedula = request.POST['cedula']
        password = request.POST['password']
        user = authenticate(request, username=cedula, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def generar_certificado(request, cedula):
    funcionario = get_object_or_404(Funcionario, cedula=cedula)

    rendered = render_to_string('certificado_template.html', {'funcionario': funcionario})
    pdf = pdfkit.from_string(rendered, False)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{cedula}.pdf"'
    return response

@login_required
def preview_certificado(request, cedula):
    funcionario = get_object_or_404(Funcionario, cedula=cedula)
    
    return render(request, 'certificado_template.html', {'funcionario': funcionario})

@login_required
def listar_cedulas(request):
    funcionarios = Funcionario.objects.all()
    datos_funcionarios = [
        {'cedula': funcionario.cedula, 'nombre': funcionario.nombre, 'CPS': funcionario.CPS, 'año_contrato': funcionario.año_contrato} 
        for funcionario in funcionarios
    ]
    return render(request, 'listar_cedulas.html', {'datos_funcionarios': datos_funcionarios})

@login_required
def eliminar_datos(request, cedula):
    funcionario = get_object_or_404(Funcionario, cedula=cedula)
    funcionario.delete()
    return redirect('listar_cedulas')

@login_required
def buscar_certificado(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()  # Asegúrate de manejar entradas vacías
        año = request.POST.get('año', '').strip()

        # Valida que los campos no estén vacíos
        if not cedula or not año:
            return render(request, 'resultado_busqueda.html', {'mensaje': 'Por favor, completa todos los campos.'})

        # Buscar el funcionario por cédula y año del contrato
        Funcionario_obj = Funcionario.objects.filter(cedula=cedula, año_contrato=año).first()

        if Funcionario_obj:
            return render(request, 'resultado_busqueda.html', {'Funcionario': Funcionario_obj})
        else:
            return render(request, 'resultado_busqueda.html', {'mensaje': 'Funcionario no encontrado. Por favor, crea un nuevo Funcionario.'})

    return render(request, 'buscar_cert.html')

@login_required
def cargar_csv(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'mensaje': 'No se ha subido ningún archivo'}, status=400)
        
        file = request.FILES['file']
        
        if not file.name.endswith('.csv'):
            return JsonResponse({'mensaje': 'El archivo debe ser un CSV'}, status=400)

        file_path = default_storage.save(file.name, file)

        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)  # Omitir encabezado
                
                registros_creados = 0
                registros_actualizados = 0

                for row in reader:
                    if len(row) != 13:
                        continue  # O manejar el caso de columnas faltantes

                    # Desestructuración de la fila
                    nombre, cedula, CPS, sitio_expedicion, objeto, obligaciones, vr_inicial_contrato, valor_mensual_honorarios, fecha_suscripcion, fecha_inicio, fecha_terminacion, tiempo_ejecucion_dia, año_contrato = row

                    try:
                        fecha_suscripcion = datetime.strptime(fecha_suscripcion, '%Y-%m-%d').date()
                        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                        fecha_terminacion = datetime.strptime(fecha_terminacion, '%Y-%m-%d').date()
                    except ValueError:
                        continue  # Ignorar filas con fechas mal formateadas

                    funcionario, creado = Funcionario.objects.update_or_create(
                        cedula=cedula,
                        defaults={
                            'nombre': nombre,
                            'CPS': CPS,
                            'sitio_expedicion': sitio_expedicion,
                            'objeto': objeto,
                            'obligaciones': obligaciones,
                            'vr_inicial_contrato': vr_inicial_contrato,
                            'valor_mensual_honorarios': valor_mensual_honorarios,
                            'fecha_suscripcion': fecha_suscripcion,
                            'fecha_inicio': fecha_inicio,
                            'fecha_terminacion': fecha_terminacion,
                            'tiempo_ejecucion_dia': tiempo_ejecucion_dia,
                            'año_contrato': año_contrato
                        }
                    )

                    if creado:
                        registros_creados += 1
                    else:
                        registros_actualizados += 1

            return JsonResponse({
                'mensaje': f'{registros_creados} registros creados, {registros_actualizados} actualizados.'
            })

        except Exception as e:
            return JsonResponse({'mensaje': f'Error al procesar el archivo: {str(e)}'}, status=500)

    return render(request, 'cargar_csv.html')

@login_required
def descargar_csv(request):
    funcionarios = Funcionario.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Funcionarios.csv"'
    response['Content-Encoding'] = 'utf-8'

    writer = csv.DictWriter(response, fieldnames=[
        'nombre', 'cedula', 'CPS', 'sitio_expedicion', 'objeto', 'obligaciones',
        'vr_inicial_contrato', 'valor_mensual_honorarios', 'fecha_suscripcion',
        'fecha_inicio', 'fecha_terminacion', 'tiempo_ejecucion_dia', 'año_contrato'
    ])
    writer.writeheader()

    for funcionario in funcionarios:
        writer.writerow({
            'nombre': funcionario.nombre,
            'cedula': funcionario.cedula,
            'CPS': funcionario.CPS,
            'sitio_expedicion': funcionario.sitio_expedicion,
            'objeto': funcionario.objeto,
            'obligaciones': funcionario.obligaciones,
            'vr_inicial_contrato': funcionario.vr_inicial_contrato,
            'valor_mensual_honorarios': funcionario.valor_mensual_honorarios,
            'fecha_suscripcion': funcionario.fecha_suscripcion.strftime('%Y-%m-%d'),
            'fecha_inicio': funcionario.fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_terminacion': funcionario.fecha_terminacion.strftime('%Y-%m-%d'),
            'tiempo_ejecucion_dia': funcionario.tiempo_ejecucion_dia,
            'año_contrato': funcionario.año_contrato
        })

    return response