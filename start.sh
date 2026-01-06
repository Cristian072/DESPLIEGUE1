#!/bin/bash
# Script de inicio para Railway
set -e

echo "Starting application..."
echo "PORT: ${PORT:-5000}"
echo "Current directory: $(pwd)"
echo "Files: $(ls -la)"

# Ejecutar gunicorn
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 app:app

