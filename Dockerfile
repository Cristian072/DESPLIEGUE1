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

# Copiar dataset (opcional - el archivo está en .gitignore)
# Como el archivo CSV está en .gitignore, no estará disponible durante el build
# El archivo se puede proporcionar de las siguientes formas:
# 1. Como volumen en Railway (recomendado para archivos grandes)
# 2. Descargándolo en runtime desde un almacenamiento externo
# 3. O quitando *.csv del .gitignore y agregando solo este archivo específico
# Por ahora, comentamos esta línea para que el build no falle
# COPY ["DATA SET VUELOS - 10 000.csv", "./"]

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Usar script de inicio
ENTRYPOINT ["./entrypoint.sh"]

