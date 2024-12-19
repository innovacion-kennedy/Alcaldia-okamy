FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV XDG_RUNTIME_DIR=/tmp/runtime-root

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xvfb \
    libfontconfig \
    iputils-ping \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    && apt-get clean

RUN mkdir -p /tmp/runtime-root && chmod 700 /tmp/runtime-root

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["xvfb-run", "-a", "python", "manage.py", "runserver", "0.0.0.0:8000"]