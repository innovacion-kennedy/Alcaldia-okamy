# Alcaldia-
# Alcaldía Okamy

## Descripción
Este proyecto es una aplicación web desarrollada con Django que incluye módulos de prueba "accounts" y certificado. La aplicación está configurada para ejecutarse en un entorno Docker, lo que facilita su instalación en cualquier sistema operativo (Linux, Windows, macOS).

## Requisitos del Sistema
- Python 3.9
- Django >=3.2,<4.0
- Docker y Docker Compose
- PostgreSQL
- wkhtmltopdf
- Jazzmin

## Instalación

### Clonar el repositorio
```bash
git clone https://github.com/innovacion-kennedy/Alcaldia-okamy.git
cd Alcaldia-okamy

Configurar el entorno
Docker

    Instalar Docker:
        Guía de instalación de Docker
        Guía de instalación de Docker Compose

    Configurar y levantar los servicios:

    docker-compose up --build

Configuración de Django

    Instalar dependencias:

    pip install -r requirements.txt

    Migrar la base de datos:

    docker-compose run web python manage.py migrate


   

Construir y levantar los servicios con Docker:

docker-compose up --build

Acceder a la aplicación:

    Abrir un navegador web y navegar a http://localhost:8000.


Estructura del Proyecto

    accounts: Aplicación de prueba.
    certificado: Aplicación de certificados.
    Dockerfile: Configuración de Docker para el entorno de desarrollo.
    docker-compose.yml: Configuración de Docker Compose.
    requirements.txt: Dependencias del proyecto.

Crear nuevas aplicaciones en Django

    Crear una nueva aplicación:

    docker-compose run web python manage.py startapp <nombre_de_la_app>

    Agregar la nueva aplicación a INSTALLED_APPS en settings.py:

    INSTALLED_APPS = [
        ...
        '<nombre_de_la_app>',
    ]

Comandos Básicos de Git

    Hacer commit:

    git add .
    git commit -m "Mensaje del commit"
    git push origin <nombre_de_la_rama>

    Crear y cambiar de ramas:

    git checkout -b <nombre_de_la_rama>
    git checkout <nombre_de_la_rama>

Contribución

    Clonar el repositorio y crear una nueva rama:

    git clone https://github.com/innovacion-kennedy/Alcaldia-okamy.git
    cd Alcaldia-okamy
    git checkout -b <nombre_de_tu_rama>

    Hacer cambios y enviar un pull request:

    git add .
    git commit -m "Descripción de los cambios"
    git push origin <nombre_de_tu_rama>

