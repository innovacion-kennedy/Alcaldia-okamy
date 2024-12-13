FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && apt-get clean

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/