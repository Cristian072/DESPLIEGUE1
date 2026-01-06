#!/bin/bash
# Script opcional para descargar el dataset si no está disponible localmente
# Puedes usar este script en Railway para descargar el dataset desde un almacenamiento externo

echo "Checking for dataset..."

if [ ! -f "DATA SET VUELOS - 70 000.csv" ]; then
    echo "Dataset not found locally."
    
    # Opción 1: Descargar desde una URL (si tienes el archivo en algún lugar)
    # wget -O "DATA SET VUELOS - 70 000.csv" "https://tu-url.com/dataset.csv"
    
    # Opción 2: Copiar desde un volumen montado en Railway
    # cp /mnt/dataset/"DATA SET VUELOS - 70 000.csv" .
    
    # Opción 3: Usar Railway Variables/Secrets para la URL
    if [ ! -z "$DATASET_URL" ]; then
        echo "Downloading dataset from $DATASET_URL..."
        wget -O "DATA SET VUELOS - 70 000.csv" "$DATASET_URL"
    else
        echo "DATASET_URL not set. Please provide the dataset manually."
        echo "You can:"
        echo "1. Mount it as a volume in Railway"
        echo "2. Set DATASET_URL environment variable"
        echo "3. Upload it manually after deployment"
    fi
else
    echo "Dataset found locally."
fi

