#!/bin/bash
set -e

# Obtener puerto de Railway o usar 5000 por defecto
PORT=${PORT:-5000}

echo "Starting application on port $PORT"
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# Ejecutar gunicorn
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app

