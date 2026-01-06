"""
Aplicación web para predicción de vuelos usando aprendizaje no supervisado
"""
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os
import sys
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import json

app = Flask(__name__)

# Cargar el modelo entrenado
MODEL_PATH = 'models/flight_cluster_model.pkl'
SCALER_PATH = 'models/scaler.pkl'
FEATURES_PATH = 'models/feature_names.pkl'
ORIGIN_ENCODER_PATH = 'models/origin_encoder.pkl'
DEST_ENCODER_PATH = 'models/dest_encoder.pkl'
DATA_PATH = 'DATA SET VUELOS - 70 000.csv'

def load_model():
    """Cargar modelo, scaler y encoders si existen"""
    model = None
    scaler = None
    feature_names = None
    origin_encoder = None
    dest_encoder = None
    
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
        
        if os.path.exists(FEATURES_PATH):
            feature_names = joblib.load(FEATURES_PATH)
            print(f"Feature names loaded successfully")
        
        if os.path.exists(ORIGIN_ENCODER_PATH):
            origin_encoder = joblib.load(ORIGIN_ENCODER_PATH)
            print(f"Origin encoder loaded successfully")
        
        if os.path.exists(DEST_ENCODER_PATH):
            dest_encoder = joblib.load(DEST_ENCODER_PATH)
            print(f"Dest encoder loaded successfully")
            
    except Exception as e:
        print(f"Error loading model: {str(e)}", file=sys.stderr)
        import traceback
        print(traceback.format_exc(), file=sys.stderr)
    return model, scaler, feature_names, origin_encoder, dest_encoder

# Inicialización al importar (solo para logging)
if __name__ != '__main__':
    print("Flask app module loaded")
    print(f"Current directory: {os.getcwd()}")

@app.route('/')
def index():
    """Página principal"""
    try:
        return render_template('index.html')
    except Exception as e:
        # Si falla el template, mostrar página simple
        return f"""
        <html>
        <head><title>Flight Clustering System</title></head>
        <body>
            <h1>Flight Clustering System</h1>
            <p>Application is running!</p>
            <p>Template error: {str(e)}</p>
            <p><a href="/test">Test endpoint</a></p>
            <p><a href="/health">Health check</a></p>
        </body>
        </html>
        """, 200

def preprocess_flight_data(data, origin_encoder, dest_encoder):
    """Preprocesar datos de vuelo para predicción"""
    # Convertir fecha
    fecha = pd.to_datetime(data.get('fecha', datetime.now().strftime('%d/%m/%Y')), format='%d/%m/%Y', errors='coerce')
    
    # Extraer características temporales
    dia_semana = fecha.dayofweek if pd.notna(fecha) else 0
    mes = fecha.month if pd.notna(fecha) else 1
    
    # Hora de salida
    hora_salida = int(data.get('hora_salida', 1200))
    hora_salida_num = int(str(hora_salida).zfill(4)[:2]) if hora_salida else 12
    
    # Calcular duración aproximada
    hora_llegada = int(data.get('hora_llegada', hora_salida + 200))
    duracion = (
        (int(str(hora_llegada).zfill(4)[:2])*60 + int(str(hora_llegada).zfill(4)[2:])) -
        (int(str(hora_salida).zfill(4)[:2])*60 + int(str(hora_salida).zfill(4)[2:]))
    )
    if duracion < 0:
        duracion += 1440
    
    # Codificar origen y destino
    origen = data.get('origen', 'JFK')
    destino = data.get('destino', 'LAX')
    
    try:
        origen_encoded = origin_encoder.transform([origen])[0] if origin_encoder else 0
    except:
        origen_encoded = 0
    
    try:
        destino_encoded = dest_encoder.transform([destino])[0] if dest_encoder else 0
    except:
        destino_encoded = 0
    
    # Retrasos
    retraso_salida = float(data.get('retraso_salida', 0))
    retraso_llegada = float(data.get('retraso_llegada', 0))
    retraso_clima = float(data.get('retraso_clima', 0))
    
    # Construir vector de características
    features = np.array([[
        retraso_salida,
        retraso_llegada,
        retraso_clima,
        duracion,
        hora_salida_num,
        dia_semana,
        origen_encoded,
        destino_encoded
    ]])
    
    return features

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para hacer predicciones"""
    try:
        data = request.json
        
        # Cargar modelo, scaler y encoders
        model, scaler, feature_names, origin_encoder, dest_encoder = load_model()
        
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model not trained yet. Please train the model first.'
            }), 400
        
        # Preprocesar datos
        features = preprocess_flight_data(data, origin_encoder, dest_encoder)
        
        # Normalizar
        features_scaled = scaler.transform(features)
        
        # Predecir cluster
        cluster = model.predict(features_scaled)[0]
        
        # Calcular distancia al centroide
        centroid = model.cluster_centers_[cluster]
        distance = np.linalg.norm(features_scaled[0] - centroid)
        
        return jsonify({
            'cluster': int(cluster),
            'distance_to_centroid': float(distance),
            'message': f'Flight belongs to cluster {cluster}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clusters', methods=['GET'])
def get_clusters():
    """Obtener información sobre los clusters"""
    try:
        model, scaler, feature_names, origin_encoder, dest_encoder = load_model()
        
        if model is None:
            return jsonify({
                'error': 'Modelo no entrenado aún. Por favor, entrene el modelo primero.',
                'model_exists': False,
                'scaler_exists': scaler is not None
            }), 400
        
        if scaler is None:
            return jsonify({
                'error': 'Scaler no encontrado. Por favor, entrene el modelo primero.',
                'model_exists': True,
                'scaler_exists': False
            }), 400
        
        # Verificar que el modelo tenga cluster_centers
        if not hasattr(model, 'cluster_centers_') or model.cluster_centers_ is None:
            return jsonify({
                'error': 'El modelo no tiene centros de clusters definidos. Por favor, entrene el modelo nuevamente.',
                'model_exists': True,
                'scaler_exists': True
            }), 400
        
        # Cargar datos para calcular tamaños de clusters
        n_clusters = model.n_clusters if hasattr(model, 'n_clusters') else 0
        cluster_sizes = np.zeros(n_clusters)
        
        if os.path.exists(DATA_PATH):
            try:
                df = pd.read_csv(DATA_PATH, nrows=10000)
                df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
                df['Dia_semana'] = df['Fecha'].dt.dayofweek
                df['Hora_salida_num'] = df['Hora_salida'].apply(lambda x: int(str(x).zfill(4)[:2]) if pd.notna(x) else 0)
                df['Duracion_vuelo'] = (
                    df['Hora_llegada'].apply(lambda x: int(str(int(x)).zfill(4)[:2])*60 + int(str(int(x)).zfill(4)[2:]) if pd.notna(x) else 0) -
                    df['Hora_salida'].apply(lambda x: int(str(int(x)).zfill(4)[:2])*60 + int(str(int(x)).zfill(4)[2:]) if pd.notna(x) else 0)
                )
                df['Duracion_vuelo'] = df['Duracion_vuelo'].apply(lambda x: x + 1440 if x < 0 else x)
                
                if origin_encoder is not None:
                    df['Origen_encoded'] = origin_encoder.transform(df['Origen'].astype(str))
                else:
                    df['Origen_encoded'] = 0
                
                if dest_encoder is not None:
                    df['Destino_encoded'] = dest_encoder.transform(df['Destino'].astype(str))
                else:
                    df['Destino_encoded'] = 0
                
                feature_cols = ['Retraso_Salida', 'Retraso_llegada', 'Retraso_Clima', 
                              'Duracion_vuelo', 'Hora_salida_num', 'Dia_semana',
                              'Origen_encoded', 'Destino_encoded']
                
                X = df[feature_cols].dropna()
                if len(X) > 0:
                    X_scaled = scaler.transform(X)
                    labels = model.predict(X_scaled)
                    cluster_sizes = np.bincount(labels, minlength=n_clusters)
            except Exception as e:
                print(f"Error procesando datos para clusters: {str(e)}")
                import traceback
                print(traceback.format_exc())
                # Usar tamaños por defecto si hay error
                pass
        
        clusters_info = []
        for i, center in enumerate(model.cluster_centers_):
            # Calcular estadísticas del cluster
            cluster_data = {
                'cluster': int(i),
                'center': center.tolist(),
                'size': int(cluster_sizes[i]) if i < len(cluster_sizes) else 0
            }
            
            # Agregar interpretación del cluster basada en centroides
            if len(center) >= 3:
                cluster_data['characteristics'] = {
                    'avg_departure_delay': float(center[0]),
                    'avg_arrival_delay': float(center[1]),
                    'avg_weather_delay': float(center[2]),
                    'cluster_type': 'High Delay' if center[0] > 20 or center[1] > 20 else 
                                   'Weather Affected' if center[2] > 5 else 
                                   'On Time' if center[0] < 5 and center[1] < 5 else 'Moderate Delay'
                }
            
            clusters_info.append(cluster_data)
        
        return jsonify({
            'n_clusters': n_clusters,
            'clusters': clusters_info,
            'feature_names': feature_names.tolist() if feature_names is not None else []
        })
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error en /api/clusters: {str(e)}")
        print(error_trace)
        return jsonify({
            'error': f'Error al obtener clusters: {str(e)}',
            'traceback': error_trace if app.debug else None
        }), 500

@app.route('/api/airports', methods=['GET'])
def get_airports():
    """Obtener lista de aeropuertos disponibles"""
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({'error': 'Dataset no encontrado'}), 404
        
        df = pd.read_csv(DATA_PATH, usecols=['Origen', 'Destino'])
        origins = sorted(df['Origen'].unique().tolist())
        destinations = sorted(df['Destino'].unique().tolist())
        all_airports = sorted(list(set(origins + destinations)))
        
        return jsonify({
            'airports': all_airports,
            'origins': origins,
            'destinations': destinations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas del dataset"""
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({'error': 'Dataset no encontrado'}), 404
        
        df = pd.read_csv(DATA_PATH, nrows=10000)  # Limitar para performance
        
        # Convertir fechas
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
        
        stats = {
            'total_flights': len(df),
            'date_range': {
                'start': df['Fecha'].min().strftime('%Y-%m-%d') if pd.notna(df['Fecha'].min()) else None,
                'end': df['Fecha'].max().strftime('%Y-%m-%d') if pd.notna(df['Fecha'].max()) else None
            },
            'delays': {
                'departure': {
                    'mean': float(df['Retraso_Salida'].mean()),
                    'std': float(df['Retraso_Salida'].std()),
                    'max': float(df['Retraso_Salida'].max())
                },
                'arrival': {
                    'mean': float(df['Retraso_llegada'].mean()),
                    'std': float(df['Retraso_llegada'].std()),
                    'max': float(df['Retraso_llegada'].max())
                },
                'weather': {
                    'mean': float(df['Retraso_Clima'].mean()),
                    'max': float(df['Retraso_Clima'].max())
                }
            },
            'top_routes': df.groupby(['Origen', 'Destino']).size().nlargest(10).to_dict(),
            'top_origins': df['Origen'].value_counts().head(10).to_dict(),
            'top_destinations': df['Destino'].value_counts().head(10).to_dict()
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query_flights():
    """Consultar vuelos con filtros"""
    try:
        filters = request.json
        if not os.path.exists(DATA_PATH):
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = pd.read_csv(DATA_PATH, nrows=50000)  # Limitar para performance
        
        # Aplicar filtros
        if 'origen' in filters:
            df = df[df['Origen'] == filters['origen']]
        if 'destino' in filters:
            df = df[df['Destino'] == filters['destino']]
        if 'min_delay' in filters:
            df = df[df['Retraso_Salida'] >= filters['min_delay']]
        if 'max_delay' in filters:
            df = df[df['Retraso_Salida'] <= filters['max_delay']]
        
        # Limitar resultados
        limit = filters.get('limit', 100)
        df = df.head(limit)
        
        # Predecir clusters para estos vuelos
        model, scaler, _, origin_encoder, dest_encoder = load_model()
        if model is not None and scaler is not None:
            predictions = []
            for _, row in df.iterrows():
                flight_data = {
                    'fecha': row['Fecha'],
                    'origen': row['Origen'],
                    'destino': row['Destino'],
                    'hora_salida': row['Hora_salida'],
                    'hora_llegada': row['Hora_llegada'],
                    'retraso_salida': row['Retraso_Salida'],
                    'retraso_llegada': row['Retraso_llegada'],
                    'retraso_clima': row['Retraso_Clima']
                }
                features = preprocess_flight_data(flight_data, origin_encoder, dest_encoder)
                features_scaled = scaler.transform(features)
                cluster = model.predict(features_scaled)[0]
                predictions.append(int(cluster))
            df['Cluster'] = predictions
        
        return jsonify({
            'count': len(df),
            'flights': df.to_dict('records')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """Retrenar modelo con nueva data"""
    try:
        # Ejecutar script de entrenamiento
        import subprocess
        result = subprocess.run(
            ['python', 'train_model.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Model retrained successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Training failed',
                'output': result.stderr
            }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-data', methods=['POST'])
def upload_data():
    """Subir nueva data y retrenar modelo"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validar extensión
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are supported'}), 400
        
        # Guardar archivo temporalmente
        import tempfile
        import uuid
        
        filename = f"new_data_{uuid.uuid4().hex[:8]}.csv"
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(temp_path)
        
        # Procesar nueva data
        import subprocess
        result = subprocess.run(
            ['python', 'scripts/process_new_data.py', '--new-data', temp_path],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        # Limpiar archivo temporal
        try:
            os.remove(temp_path)
        except:
            pass
        
        if result.returncode == 0:
            # Retrenar modelo automáticamente
            retrain_result = subprocess.run(
                ['python', 'train_model.py'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return jsonify({
                'success': True,
                'message': 'Data uploaded successfully',
                'output': result.stdout,
                'retrain_success': retrain_result.returncode == 0,
                'retrain_output': retrain_result.stdout if retrain_result.returncode == 0 else retrain_result.stderr
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Processing failed',
                'output': result.stderr
            }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cluster-visualization', methods=['GET'])
def get_cluster_visualization():
    """Obtener datos para visualización 2D/3D de clusters"""
    try:
        model, scaler, feature_names, origin_encoder, dest_encoder = load_model()
        
        if model is None:
            return jsonify({'error': 'Model not trained yet'}), 400
        
        if not os.path.exists(DATA_PATH):
            return jsonify({'error': 'Dataset not found'}), 404
        
        # Cargar muestra de datos
        df = pd.read_csv(DATA_PATH, nrows=5000)
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
        df['Dia_semana'] = df['Fecha'].dt.dayofweek
        df['Hora_salida_num'] = df['Hora_salida'].apply(lambda x: int(str(x).zfill(4)[:2]) if pd.notna(x) else 0)
        df['Duracion_vuelo'] = (
            df['Hora_llegada'].apply(lambda x: int(str(int(x)).zfill(4)[:2])*60 + int(str(int(x)).zfill(4)[2:]) if pd.notna(x) else 0) -
            df['Hora_salida'].apply(lambda x: int(str(int(x)).zfill(4)[:2])*60 + int(str(int(x)).zfill(4)[2:]) if pd.notna(x) else 0)
        )
        df['Duracion_vuelo'] = df['Duracion_vuelo'].apply(lambda x: x + 1440 if x < 0 else x)
        
        if origin_encoder is not None:
            df['Origen_encoded'] = origin_encoder.transform(df['Origen'].astype(str))
        else:
            df['Origen_encoded'] = 0
        
        if dest_encoder is not None:
            df['Destino_encoded'] = dest_encoder.transform(df['Destino'].astype(str))
        else:
            df['Destino_encoded'] = 0
        
        feature_cols = ['Retraso_Salida', 'Retraso_llegada', 'Retraso_Clima', 
                      'Duracion_vuelo', 'Hora_salida_num', 'Dia_semana',
                      'Origen_encoded', 'Destino_encoded']
        
        X = df[feature_cols].dropna()
        if len(X) == 0:
            return jsonify({'error': 'No valid data after preprocessing'}), 400
        
        X_scaled = scaler.transform(X)
        labels = model.predict(X_scaled)
        
        # Reducir dimensionalidad para visualización (usar PCA o seleccionar features principales)
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X_scaled)
        
        # Preparar datos para visualización
        visualization_data = {
            'points': [
                {
                    'x': float(X_2d[i][0]),
                    'y': float(X_2d[i][1]),
                    'cluster': int(labels[i]),
                    'departure_delay': float(X.iloc[i]['Retraso_Salida']),
                    'arrival_delay': float(X.iloc[i]['Retraso_llegada']),
                    'origin': str(df.iloc[X.index[i]]['Origen']),
                    'destination': str(df.iloc[X.index[i]]['Destino'])
                }
                for i in range(len(X_2d))
            ],
            'centroids_2d': [
                {
                    'x': float(pca.transform([center])[0][0]),
                    'y': float(pca.transform([center])[0][1]),
                    'cluster': int(i)
                }
                for i, center in enumerate(model.cluster_centers_)
            ],
            'n_clusters': model.n_clusters,
            'explained_variance': pca.explained_variance_ratio_.tolist()
        }
        
        return jsonify(visualization_data)
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    model, scaler, feature_names, origin_encoder, dest_encoder = load_model()
    
    # Verificar si el dataset existe y es legible
    data_readable = False
    data_rows = 0
    if os.path.exists(DATA_PATH):
        try:
            df_test = pd.read_csv(DATA_PATH, nrows=10)
            data_readable = True
            data_rows = len(pd.read_csv(DATA_PATH, usecols=[0]))
        except:
            data_readable = False
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'n_clusters': model.n_clusters if model is not None else 0,
        'data_available': os.path.exists(DATA_PATH),
        'data_readable': data_readable,
        'data_rows': data_rows,
        'model_path_exists': os.path.exists(MODEL_PATH),
        'scaler_path_exists': os.path.exists(SCALER_PATH)
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

