FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para modelos si no existe
RUN mkdir -p models

# Hacer el script ejecutable
RUN chmod +x start.sh || true

# Exponer puerto (Railway usa variable PORT, por defecto 5000)
EXPOSE 5000

# Comando para ejecutar la aplicación
# Railway proporciona la variable PORT automáticamente
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 app:app"]

