"""
Aplicación web para predicción de vuelos usando aprendizaje no supervisado
"""
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__)

# Cargar el modelo entrenado
MODEL_PATH = 'models/flight_cluster_model.pkl'
SCALER_PATH = 'models/scaler.pkl'

def load_model():
    """Cargar modelo y scaler si existen"""
    model = None
    scaler = None
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
    return model, scaler

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para hacer predicciones"""
    try:
        data = request.json
        
        # Cargar modelo y scaler
        model, scaler = load_model()
        
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model not trained yet. Please train the model first.'
            }), 400
        
        # Preparar datos de entrada
        features = np.array([[
            float(data.get('duration', 0)),
            float(data.get('distance', 0)),
            float(data.get('price', 0))
        ]])
        
        # Normalizar
        features_scaled = scaler.transform(features)
        
        # Predecir cluster
        cluster = model.predict(features_scaled)[0]
        
        return jsonify({
            'cluster': int(cluster),
            'message': f'Flight belongs to cluster {cluster}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

