FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para modelos
RUN mkdir -p models

# Exponer puerto (Railway usa variable PORT)
EXPOSE $PORT

# Comando para ejecutar la aplicación
# Railway proporciona la variable PORT automáticamente
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app

