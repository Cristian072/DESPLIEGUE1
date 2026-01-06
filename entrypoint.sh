#!/bin/bash
# No usar set -e para permitir que la app inicie incluso si el entrenamiento falla

# Obtener puerto de Railway o usar 5000 por defecto
PORT=${PORT:-5000}

echo "=========================================="
echo "Starting Flight Clustering Application"
echo "=========================================="
echo "Port: $PORT"
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo ""

# Verificar si el dataset existe
if [ ! -f "DATA SET VUELOS - 70 000.csv" ]; then
    echo "⚠️  WARNING: Dataset file not found!"
    echo "The dataset CSV file is not available."
    echo "The application will start, but model training will be skipped."
    echo "You can upload the dataset later and retrain the model via the web interface."
    echo ""
    DATASET_EXISTS=0
else
    echo "✅ Dataset file found: DATA SET VUELOS - 70 000.csv"
    DATASET_EXISTS=1
    echo ""
fi

# Verificar si el modelo existe, si no, intentar entrenarlo
if [ ! -f "models/flight_cluster_model.pkl" ]; then
    if [ "$DATASET_EXISTS" -eq 1 ]; then
        echo "📊 Model not found. Attempting to train model..."
        echo "This may take a few minutes..."
        if python train_model.py; then
            echo "✅ Model trained successfully!"
        else
            echo "❌ Model training failed, but application will start anyway."
            echo "You can retrain the model later via the web interface."
        fi
    else
        echo "⚠️  Cannot train model - dataset file not found!"
        echo "Application will start without a trained model."
        echo "Upload the dataset and use the 'Retrain Model' button in the Maintenance tab."
    fi
    echo ""
else
    echo "✅ Model found. Skipping training."
    echo ""
fi

# Crear directorio models si no existe
mkdir -p models

# Ejecutar health check (si existe) - no crítico si falla
if [ -f "scripts/health_check.py" ]; then
    echo "🔍 Running health check..."
    python scripts/health_check.py || echo "Health check completed with warnings"
    echo ""
fi

# Verificar que gunicorn esté instalado
if ! command -v gunicorn &> /dev/null; then
    echo "❌ ERROR: gunicorn not found!"
    echo "Installing gunicorn..."
    pip install gunicorn
fi

echo "=========================================="
echo "Starting Gunicorn server..."
echo "Listening on 0.0.0.0:$PORT"
echo "=========================================="
echo ""

# Ejecutar gunicorn - esto debe ejecutarse siempre
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload \
    app:app

