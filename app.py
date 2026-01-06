"""
Aplicación web para predicción de vuelos usando aprendizaje no supervisado
"""
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os
import sys

app = Flask(__name__)

# Cargar el modelo entrenado
MODEL_PATH = 'models/flight_cluster_model.pkl'
SCALER_PATH = 'models/scaler.pkl'

def load_model():
    """Cargar modelo y scaler si existen"""
    model = None
    scaler = None
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print(f"Model loaded successfully from {MODEL_PATH}")
        else:
            print(f"Model file not found: {MODEL_PATH}")
        
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            print(f"Scaler loaded successfully from {SCALER_PATH}")
        else:
            print(f"Scaler file not found: {SCALER_PATH}")
    except Exception as e:
        print(f"Error loading model: {str(e)}", file=sys.stderr)
    return model, scaler

# Cargar modelo al inicio (opcional, para verificar)
print("Starting application...")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
if os.path.exists('models'):
    print(f"Files in models directory: {os.listdir('models')}")
else:
    print("Models directory does not exist")

@app.route('/')
def index():
    """Página principal"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

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
    model, scaler = load_model()
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    }), 200

@app.route('/test')
def test():
    """Test endpoint para verificar que la app funciona"""
    return jsonify({
        'message': 'Application is running!',
        'python_version': sys.version,
        'current_dir': os.getcwd(),
        'files': os.listdir('.')
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

