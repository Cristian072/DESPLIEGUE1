FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py train_model.py ./
COPY templates/ templates/
RUN mkdir -p models

# Copiar script de inicio
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Usar script de inicio
ENTRYPOINT ["./entrypoint.sh"]

