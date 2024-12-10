# Base de la imagen
FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    hostapd \
    dnsmasq \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos de la aplicación
COPY . /app

# Dar permisos de ejecución al script de configuración
RUN chmod +x /app/configurar_punto_acceso.sh

# Instalar dependencias de Python
RUN pip install --no-cache-dir psycopg2-binary

# Exponer los puertos
EXPOSE 5000 5001

# Ejecutar el script de configuración del punto de acceso y el servidor
CMD ["/bin/bash", "-c", "/app/configurar_punto_acceso.sh && python /app/server.py"]
