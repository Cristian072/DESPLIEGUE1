#!/bin/bash
set -e

# Obtener puerto de Railway o usar 5000 por defecto
PORT=${PORT:-5000}

echo "Starting application on port $PORT"
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# Verificar si el modelo existe, si no, entrenarlo
if [ ! -f "models/flight_cluster_model.pkl" ]; then
    echo "Model not found. Training model..."
    python train_model.py
else
    echo "Model found. Skipping training."
fi

# Ejecutar health check (si existe)
if [ -f "scripts/health_check.py" ]; then
    echo "Running health check..."
    python scripts/health_check.py || echo "Health check completed with warnings"
else
    echo "Health check script not found, skipping..."
fi

# Ejecutar gunicorn
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app

