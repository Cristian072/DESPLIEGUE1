FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py train_model.py ./
COPY templates/ templates/
COPY scripts/ scripts/
RUN mkdir -p models

# Copiar script de inicio
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Copiar dataset (el archivo debe existir en el contexto de build)
# Si el archivo no existe localmente, puedes:
# 1. Comentar esta línea y proporcionarlo como volumen en Railway
# 2. O asegurarte de que el archivo esté en el mismo directorio que el Dockerfile
COPY ["DATA SET VUELOS - 70 000.csv", "DATA SET VUELOS - 70 000.csv"]

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Usar script de inicio
ENTRYPOINT ["./entrypoint.sh"]

