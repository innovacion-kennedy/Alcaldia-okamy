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

    Guía de Instalación de Docker
Linux (Ubuntu)

    Actualizar el sistema:

    sudo apt-get update
    sudo apt-get upgrade

    Instalar dependencias:

    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

    Agregar la clave GPG de Docker:

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    Agregar el repositorio de Docker:

    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    Instalar Docker:

    sudo apt-get update
    sudo apt-get install docker-ce

    Verificar la instalación:

    sudo systemctl status docker

Windows y macOS

    Descargar Docker Desktop desde Docker Hub.
    Ejecutar el instalador y seguir las instrucciones en pantalla.
    Reiniciar el sistema si es necesario.
    Verificar la instalación abriendo una terminal y ejecutando:

    docker --version

Guía de Instalación de Docker Compose
Linux (Ubuntu)

    Descargar la última versión de Docker Compose:

    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    Aplicar permisos de ejecución:

    sudo chmod +x /usr/local/bin/docker-compose

    Verificar la instalación:

    docker-compose --version

Windows y macOS

Docker Compose viene incluido con Docker Desktop, por lo que no necesitas instalarlo por separado. Solo asegúrate de que Docker Desktop esté instalado y actualizado.

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

