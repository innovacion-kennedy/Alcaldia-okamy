from django.contrib import admin
from django.urls import path, include
from okamy import views as okamy_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', okamy_views.home, name='home'), 
    path('accounts/', include('accounts.urls')),
    path('certificado/', include('certificado.urls', namespace='certificado')),
]