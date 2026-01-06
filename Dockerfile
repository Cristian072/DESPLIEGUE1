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
# Copiar modelos entrenados (deben estar en el repositorio Git)
COPY models/ models/

# Copiar script de inicio
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Copiar dataset (el archivo está en el repositorio Git)
COPY ["DATA SET VUELOS - 10 000.csv", "./"]

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Usar script de inicio
ENTRYPOINT ["./entrypoint.sh"]

