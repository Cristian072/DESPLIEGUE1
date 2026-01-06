#!/bin/bash
# Script para Railway - Entrena el modelo si no existe
if [ ! -f "models/flight_cluster_model.pkl" ]; then
    echo "Model not found. Training model..."
    python train_model.py
else
    echo "Model already exists. Skipping training."
fi

