from django.urls import path
from . import views

urlpatterns = [
    path('generar_certificado/<str:cedula>/', views.generar_certificado, name='generar_certificado'),
    path('obtener_certificado/<str:cedula>/', views.obtener_certificado, name='obtener_certificado'),
    path('preview_certificado/<str:cedula>/', views.preview_certificado, name='preview_certificado'),
    path('crear_datos/', views.crear_datos, name='crear_datos'),
    path('listar_cedulas/', views.listar_cedulas, name='listar_cedulas'),
    path('editar_datos/<str:cedula>/', views.editar_datos, name='editar_datos'),
    path('eliminar_datos/<str:cedula>/', views.eliminar_datos, name='eliminar_datos'),
    path('buscar_certificado/', views.buscar_certificado, name='buscar_certificado'),
    path('cargar_csv/', views.cargar_csv, name='cargar_csv'),
    path('descargar_csv/', views.descargar_csv, name='descargar_csv'),
]