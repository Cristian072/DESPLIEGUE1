"""
Aplicación web para predicción de vuelos usando aprendizaje no supervisado
"""
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os
import sys
import subprocess
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
# El dataset puede estar en diferentes ubicaciones según el entorno
DATA_PATH = os.environ.get('DATA_PATH', 'DATA SET VUELOS - 10 000.csv')

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
    print("=" * 50)
    print("GET /api/clusters - Iniciando...")
    print(f"Current directory: {os.getcwd()}")
    print(f"DATA_PATH: {DATA_PATH}")
    print(f"DATA_PATH exists: {os.path.exists(DATA_PATH)}")
    print(f"MODEL_PATH exists: {os.path.exists(MODEL_PATH)}")
    print(f"SCALER_PATH exists: {os.path.exists(SCALER_PATH)}")
    print("=" * 50)
    
    try:
        model, scaler, feature_names, origin_encoder, dest_encoder = load_model()
        
        print(f"Model loaded: {model is not None}")
        print(f"Scaler loaded: {scaler is not None}")
        print(f"Feature names loaded: {feature_names is not None}")
        print(f"Origin encoder loaded: {origin_encoder is not None}")
        print(f"Dest encoder loaded: {dest_encoder is not None}")
        
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
        
        # Obtener número de clusters
        try:
            n_clusters = model.n_clusters if hasattr(model, 'n_clusters') else len(model.cluster_centers_)
        except:
            n_clusters = len(model.cluster_centers_) if model.cluster_centers_ is not None else 0
        
        if n_clusters == 0:
            return jsonify({
                'error': 'No se pudo determinar el número de clusters del modelo.',
                'model_exists': True,
                'scaler_exists': True
            }), 400
        
        # Inicializar tamaños de clusters
        cluster_sizes = np.zeros(n_clusters, dtype=int)
        
        # Intentar cargar datos para calcular tamaños de clusters (opcional)
        if os.path.exists(DATA_PATH):
            try:
                df = pd.read_csv(DATA_PATH, nrows=10000)
                
                # Verificar que las columnas necesarias existan
                required_cols = ['Fecha', 'Hora_salida', 'Hora_llegada', 'Origen', 'Destino', 
                               'Retraso_Salida', 'Retraso_llegada', 'Retraso_Clima']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    print(f"Advertencia: Columnas faltantes en el dataset: {missing_cols}")
                else:
                    # Procesar datos
                    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
                    df['Dia_semana'] = df['Fecha'].dt.dayofweek
                    df['Hora_salida_num'] = df['Hora_salida'].apply(
                        lambda x: int(str(int(x)).zfill(4)[:2]) if pd.notna(x) else 0
                    )
                    
                    # Calcular duración del vuelo
                    def calc_duration(hora_salida, hora_llegada):
                        try:
                            h_sal = int(str(int(hora_salida)).zfill(4)[:2]) * 60 + int(str(int(hora_salida)).zfill(4)[2:]) if pd.notna(hora_salida) else 0
                            h_lleg = int(str(int(hora_llegada)).zfill(4)[:2]) * 60 + int(str(int(hora_llegada)).zfill(4)[2:]) if pd.notna(hora_llegada) else 0
                            duration = h_lleg - h_sal
                            return duration + 1440 if duration < 0 else duration
                        except:
                            return 0
                    
                    df['Duracion_vuelo'] = df.apply(
                        lambda row: calc_duration(row['Hora_salida'], row['Hora_llegada']), axis=1
                    )
                    
                    # Codificar origen y destino
                    try:
                        if origin_encoder is not None:
                            df['Origen_encoded'] = origin_encoder.transform(df['Origen'].astype(str))
                        else:
                            df['Origen_encoded'] = 0
                    except Exception as enc_error:
                        print(f"Error codificando origen: {str(enc_error)}")
                        df['Origen_encoded'] = 0
                    
                    try:
                        if dest_encoder is not None:
                            df['Destino_encoded'] = dest_encoder.transform(df['Destino'].astype(str))
                        else:
                            df['Destino_encoded'] = 0
                    except Exception as enc_error:
                        print(f"Error codificando destino: {str(enc_error)}")
                        df['Destino_encoded'] = 0
                    
                    # Preparar características
                    feature_cols = ['Retraso_Salida', 'Retraso_llegada', 'Retraso_Clima', 
                                  'Duracion_vuelo', 'Hora_salida_num', 'Dia_semana',
                                  'Origen_encoded', 'Destino_encoded']
                    
                    # Verificar que todas las columnas existan
                    available_cols = [col for col in feature_cols if col in df.columns]
                    if len(available_cols) == len(feature_cols):
                        X = df[feature_cols].dropna()
                        if len(X) > 0:
                            try:
                                X_scaled = scaler.transform(X)
                                labels = model.predict(X_scaled)
                                cluster_sizes = np.bincount(labels, minlength=n_clusters)
                            except Exception as pred_error:
                                print(f"Error prediciendo clusters: {str(pred_error)}")
                                import traceback
                                print(traceback.format_exc())
            except Exception as e:
                print(f"Error procesando datos para clusters: {str(e)}")
                import traceback
                print(traceback.format_exc())
                # Continuar con tamaños por defecto (ceros)
        
        # Construir información de clusters
        clusters_info = []
        try:
            for i in range(n_clusters):
                if i < len(model.cluster_centers_):
                    center = model.cluster_centers_[i]
                    
                    # Calcular estadísticas del cluster
                    cluster_data = {
                        'cluster': int(i),
                        'center': center.tolist() if hasattr(center, 'tolist') else list(center),
                        'size': int(cluster_sizes[i]) if i < len(cluster_sizes) else 0
                    }
                    
                    # Agregar interpretación del cluster basada en centroides
                    if len(center) >= 3:
                        try:
                            dep_delay = float(center[0])
                            arr_delay = float(center[1])
                            weather_delay = float(center[2])
                            
                            # Determinar tipo de cluster
                            if dep_delay > 20 or arr_delay > 20:
                                cluster_type = 'High Delay'
                                recommendations = [
                                    'Revisar operaciones en este aeropuerto/ruta específica',
                                    'Considerar aumentar tiempo de conexión para vuelos afectados',
                                    'Analizar causas operacionales (equipos, personal, mantenimiento)',
                                    'Implementar protocolos de recuperación más rápidos',
                                    'Monitorear estas rutas con mayor frecuencia'
                                ]
                                impact = 'Alto impacto en satisfacción del cliente y costos operativos'
                            elif weather_delay > 5:
                                cluster_type = 'Weather Affected'
                                recommendations = [
                                    'Mejorar pronósticos meteorológicos y planificación anticipada',
                                    'Tener planes de contingencia para condiciones climáticas adversas',
                                    'Comunicar proactivamente a pasajeros sobre posibles retrasos',
                                    'Considerar rutas alternativas durante temporadas de mal tiempo',
                                    'Invertir en sistemas de detección temprana de condiciones climáticas'
                                ]
                                impact = 'Impacto moderado, principalmente por factores externos'
                            elif dep_delay < 5 and arr_delay < 5:
                                cluster_type = 'On Time'
                                recommendations = [
                                    'Mantener los estándares operativos actuales',
                                    'Documentar mejores prácticas de estas rutas',
                                    'Replicar estrategias exitosas en otras rutas',
                                    'Usar como referencia para benchmarking interno',
                                    'Comunicar éxitos al equipo para motivación'
                                ]
                                impact = 'Excelente desempeño, mantener y replicar'
                            else:
                                cluster_type = 'Moderate Delay'
                                recommendations = [
                                    'Identificar causas específicas de retrasos moderados',
                                    'Optimizar tiempos de embarque y desembarque',
                                    'Revisar asignación de puertas y recursos',
                                    'Mejorar coordinación entre departamentos',
                                    'Implementar mejoras incrementales en procesos'
                                ]
                                impact = 'Impacto moderado, oportunidades de mejora identificadas'
                            
                            cluster_data['characteristics'] = {
                                'avg_departure_delay': dep_delay,
                                'avg_arrival_delay': arr_delay,
                                'avg_weather_delay': weather_delay,
                                'cluster_type': cluster_type,
                                'recommendations': recommendations,
                                'impact': impact
                            }
                        except Exception as char_error:
                            print(f"Error calculando características del cluster {i}: {str(char_error)}")
                            cluster_data['characteristics'] = {
                                'avg_departure_delay': 0.0,
                                'avg_arrival_delay': 0.0,
                                'avg_weather_delay': 0.0,
                                'cluster_type': 'Unknown'
                            }
                    else:
                        cluster_data['characteristics'] = {
                            'avg_departure_delay': 0.0,
                            'avg_arrival_delay': 0.0,
                            'avg_weather_delay': 0.0,
                            'cluster_type': 'Unknown'
                        }
                    
                    clusters_info.append(cluster_data)
        except Exception as cluster_error:
            print(f"Error construyendo información de clusters: {str(cluster_error)}")
            import traceback
            print(traceback.format_exc())
            return jsonify({
                'error': f'Error construyendo información de clusters: {str(cluster_error)}',
                'n_clusters': n_clusters
            }), 500
        
        # Preparar respuesta
        response_data = {
            'n_clusters': n_clusters,
            'clusters': clusters_info,
            'dataset_available': os.path.exists(DATA_PATH),
            'note': 'Los tamaños de clusters pueden ser 0 si el dataset no está disponible. Los clusters se muestran basados en los centroides del modelo.'
        }
        
        # Agregar feature_names si está disponible
        try:
            if feature_names is not None:
                if hasattr(feature_names, 'tolist'):
                    response_data['feature_names'] = feature_names.tolist()
                elif isinstance(feature_names, (list, np.ndarray)):
                    response_data['feature_names'] = list(feature_names)
                else:
                    response_data['feature_names'] = []
            else:
                response_data['feature_names'] = []
        except Exception as fn_error:
            print(f"Error procesando feature_names: {str(fn_error)}")
            response_data['feature_names'] = []
        
        print(f"Returning clusters data: {len(clusters_info)} clusters")
        return jsonify(response_data), 200
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error crítico en /api/clusters: {str(e)}")
        print(error_trace)
        return jsonify({
            'error': f'Error al obtener clusters: {str(e)}',
            'error_type': type(e).__name__,
            'traceback': error_trace if app.debug else None
        }), 500

@app.route('/api/airports', methods=['GET'])
def get_airports():
    """Obtener lista de aeropuertos disponibles"""
    # Lista completa de aeropuertos por defecto (siempre disponible)
    default_airports = [
        'JFK', 'LAX', 'ORD', 'DFW', 'DEN', 'ATL', 'PHX', 'IAH', 'LAS', 'MIA',
        'SEA', 'MSP', 'DTW', 'PHL', 'LGA', 'BOS', 'SFO', 'CLT', 'EWR', 'MCO',
        'SLC', 'BWI', 'DCA', 'MDW', 'HNL', 'AUS', 'PDX', 'STL', 'BNA', 'SAN',
        'IAH', 'FLL', 'IAD', 'TPA', 'OAK', 'SMF', 'SJC', 'RDU', 'MSY', 'MCI',
        'CLE', 'IND', 'CMH', 'PIT', 'CVG', 'MEM', 'JAX', 'RSW', 'BUF', 'OGG'
    ]
    
    try:
        # Intentar leer del dataset si existe
        if os.path.exists(DATA_PATH):
            try:
                # Leer solo las columnas necesarias para ahorrar memoria
                df = pd.read_csv(DATA_PATH, usecols=['Origen', 'Destino'], nrows=50000)
                origins = sorted(df['Origen'].dropna().unique().tolist())
                destinations = sorted(df['Destino'].dropna().unique().tolist())
                all_airports = sorted(list(set(origins + destinations)))
                
                # Si se encontraron aeropuertos válidos, usarlos
                if len(all_airports) > 0:
                    return jsonify({
                        'airports': all_airports,
                        'origins': origins,
                        'destinations': destinations,
                        'source': 'dataset'
                    }), 200
            except Exception as csv_error:
                print(f"Error leyendo CSV en /api/airports: {str(csv_error)}")
                # Continuar para usar lista por defecto
        
        # Si no hay dataset o falló la lectura, usar lista por defecto
        return jsonify({
            'airports': default_airports,
            'origins': default_airports,
            'destinations': default_airports,
            'source': 'default',
            'note': 'Dataset no disponible, usando lista de aeropuertos por defecto'
        }), 200
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error crítico en /api/airports: {str(e)}")
        print(error_trace)
        # SIEMPRE devolver lista por defecto, incluso en caso de error crítico
        return jsonify({
            'airports': default_airports,
            'origins': default_airports,
            'destinations': default_airports,
            'source': 'default',
            'error': f'Error al cargar aeropuertos: {str(e)}',
            'note': 'Usando lista de aeropuertos por defecto'
        }), 200  # Siempre devolver 200 para que el frontend pueda procesar la respuesta

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas del dataset"""
    try:
        if not os.path.exists(DATA_PATH):
            # Si no hay dataset, devolver información del modelo en su lugar
            model, scaler, feature_names, origin_encoder, dest_encoder = load_model()
            return jsonify({
                'error': 'Dataset no encontrado',
                'dataset_available': False,
                'model_info': {
                    'model_loaded': model is not None,
                    'scaler_loaded': scaler is not None,
                    'n_clusters': model.n_clusters if model is not None else 0,
                    'note': 'Suba el dataset CSV desde la sección Mantenimiento para ver estadísticas detalladas'
                }
            }), 200  # Devolver 200 en lugar de 404 para que el frontend pueda mostrar el mensaje
        
        df = pd.read_csv(DATA_PATH, nrows=10000)  # Limitar para performance
        
        # Convertir fechas
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
        
        stats = {
            'dataset_available': True,
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
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

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

@app.route('/api/train', methods=['POST'])
def train_model():
    """Entrenar modelo inicial o retrenar modelo existente"""
    try:
        # Verificar que el dataset existe
        if not os.path.exists(DATA_PATH):
            return jsonify({
                'success': False,
                'error': 'Dataset no encontrado. Por favor, suba el archivo CSV primero desde la sección "Subir Nueva Data".',
                'requires_dataset': True
            }), 400
        
        # Verificar si el modelo ya existe
        model_exists = os.path.exists(MODEL_PATH)
        action = 'retrenar' if model_exists else 'entrenar'
        
        print(f"Iniciando {action} del modelo...")
        print(f"Dataset: {DATA_PATH} (existe: {os.path.exists(DATA_PATH)})")
        print(f"Modelo existente: {MODEL_PATH} (existe: {model_exists})")
        
        # Ejecutar script de entrenamiento con límite de memoria
        import subprocess
        result = subprocess.run(
            ['python', 'train_model.py'],
            capture_output=True,
            text=True,
            timeout=600,
            env={**os.environ, 'TRAINING_MAX_ROWS': '15000'}
        )
        
        # Verificar que el modelo se creó correctamente
        model_created = os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH)
        
        if result.returncode == 0 and model_created:
            return jsonify({
                'success': True,
                'message': f'Modelo {action}do exitosamente',
                'output': result.stdout,
                'action': action,
                'model_created': True
            })
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return jsonify({
                'success': False,
                'error': f'Error en el {action} del modelo',
                'output': error_msg,
                'exit_code': result.returncode,
                'model_created': model_created
            }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'El entrenamiento excedió el tiempo límite (10 minutos). Intente con un dataset más pequeño.'
        }), 500
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error en train_model: {str(e)}")
        print(error_trace)
        return jsonify({
            'success': False,
            'error': f'Error inesperado: {str(e)}',
            'traceback': error_trace if app.debug else None
        }), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """Alias para /api/train - mantener compatibilidad"""
    return train_model()

@app.route('/api/upload-data', methods=['POST'])
def upload_data():
    """Subir nueva data y retrenar modelo"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó ningún archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        # Validar extensión
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Solo se admiten archivos CSV'}), 400
        
        # Guardar archivo en el directorio actual (más confiable en Railway)
        import uuid
        import shutil
        
        filename = f"new_data_{uuid.uuid4().hex[:8]}.csv"
        file_path = os.path.join('.', filename)
        
        try:
            file.save(file_path)
            print(f"Archivo guardado: {file_path}")
            
            if not os.path.exists(file_path):
                return jsonify({'error': 'Error al guardar el archivo'}), 500
            
            file_size = os.path.getsize(file_path)
            print(f"Tamaño del archivo: {file_size} bytes")
            
            # Verificar que el archivo no esté vacío
            if file_size == 0:
                os.remove(file_path)
                return jsonify({'error': 'El archivo está vacío'}), 400
            
            # Si existe el dataset principal, combinarlo; si no, usar el nuevo como principal
            if os.path.exists(DATA_PATH):
                print("Combinando con dataset existente...")
                # Leer muestras para verificar formato con manejo de encoding
                try:
                    df_existing_sample = pd.read_csv(DATA_PATH, nrows=10, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df_existing_sample = pd.read_csv(DATA_PATH, nrows=10, encoding='latin-1')
                    except:
                        df_existing_sample = pd.read_csv(DATA_PATH, nrows=10, encoding='utf-8', errors='ignore')
                
                try:
                    df_new_sample = pd.read_csv(file_path, nrows=10, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df_new_sample = pd.read_csv(file_path, nrows=10, encoding='latin-1')
                    except:
                        df_new_sample = pd.read_csv(file_path, nrows=10, encoding='utf-8', errors='ignore')
                
                # Normalizar nombres de columnas (strip y convertir a string)
                df_existing_sample.columns = df_existing_sample.columns.str.strip().astype(str)
                df_new_sample.columns = df_new_sample.columns.str.strip().astype(str)
                
                # Comparar columnas de manera flexible (ignorar orden)
                existing_cols_set = set(df_existing_sample.columns)
                new_cols_set = set(df_new_sample.columns)
                
                if existing_cols_set != new_cols_set:
                    missing_cols = existing_cols_set - new_cols_set
                    extra_cols = new_cols_set - existing_cols_set
                    error_msg = 'Las columnas no coinciden.\n'
                    if missing_cols:
                        error_msg += f'Columnas faltantes en el nuevo archivo: {list(missing_cols)}\n'
                    if extra_cols:
                        error_msg += f'Columnas adicionales en el nuevo archivo: {list(extra_cols)}\n'
                    error_msg += f'\nColumnas esperadas: {sorted(list(existing_cols_set))}\n'
                    error_msg += f'Columnas recibidas: {sorted(list(new_cols_set))}'
                    
                    os.remove(file_path)
                    return jsonify({
                        'error': error_msg,
                        'expected_columns': sorted(list(existing_cols_set)),
                        'received_columns': sorted(list(new_cols_set)),
                        'missing_columns': list(missing_cols) if missing_cols else [],
                        'extra_columns': list(extra_cols) if extra_cols else []
                    }), 400
                
                # Reordenar columnas del nuevo archivo para que coincidan con el existente
                column_order = list(df_existing_sample.columns)
                
                # Combinar archivos completos con manejo de encoding
                print("Leyendo archivos completos...")
                try:
                    df_existing = pd.read_csv(DATA_PATH, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df_existing = pd.read_csv(DATA_PATH, encoding='latin-1')
                    except:
                        df_existing = pd.read_csv(DATA_PATH, encoding='utf-8', errors='ignore')
                
                try:
                    df_new = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df_new = pd.read_csv(file_path, encoding='latin-1')
                    except:
                        df_new = pd.read_csv(file_path, encoding='utf-8', errors='ignore')
                
                # Normalizar columnas
                df_existing.columns = df_existing.columns.str.strip().astype(str)
                df_new.columns = df_new.columns.str.strip().astype(str)
                
                # Reordenar columnas del nuevo dataset para que coincidan
                if set(df_new.columns) == set(column_order):
                    df_new = df_new[column_order]
                
                # Crear backup
                backup_path = f"{DATA_PATH}.backup_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
                df_existing.to_csv(backup_path, index=False)
                print(f"Backup creado: {backup_path}")
                
                # Combinar y eliminar duplicados
                print("Combinando datasets...")
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                before_dedup = len(df_combined)
                
                # Determinar columnas para identificar duplicados (solo las que existen)
                dedup_cols = ['Fecha', 'Origen', 'Destino', 'Hora_salida']
                if 'Num_vuelo' in df_combined.columns:
                    dedup_cols.append('Num_vuelo')
                
                # Verificar que todas las columnas existan
                available_dedup_cols = [col for col in dedup_cols if col in df_combined.columns]
                
                if len(available_dedup_cols) > 0:
                    df_combined = df_combined.drop_duplicates(
                        subset=available_dedup_cols,
                        keep='last'
                    )
                else:
                    print("Advertencia: No se pudieron eliminar duplicados - columnas requeridas no encontradas")
                
                after_dedup = len(df_combined)
                duplicates_removed = before_dedup - after_dedup
                
                df_combined.to_csv(DATA_PATH, index=False)
                message = f'Data combinada exitosamente. Total: {len(df_combined)} filas'
                if duplicates_removed > 0:
                    message += f'. Se eliminaron {duplicates_removed} duplicados'
            else:
                # Usar el nuevo archivo como principal
                # Primero validar que el archivo tenga las columnas necesarias
                try:
                    df_new_check = pd.read_csv(file_path, nrows=10, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df_new_check = pd.read_csv(file_path, nrows=10, encoding='latin-1')
                    except:
                        df_new_check = pd.read_csv(file_path, nrows=10, encoding='utf-8', errors='ignore')
                
                df_new_check.columns = df_new_check.columns.str.strip().astype(str)
                
                # Verificar columnas mínimas requeridas
                required_cols = ['Fecha', 'Origen', 'Destino', 'Hora_salida', 'Hora_llegada', 
                               'Retraso_Salida', 'Retraso_llegada', 'Retraso_Clima']
                missing_required = [col for col in required_cols if col not in df_new_check.columns]
                
                if missing_required:
                    os.remove(file_path)
                    return jsonify({
                        'error': f'El archivo no tiene las columnas mínimas requeridas. Faltan: {missing_required}',
                        'required_columns': required_cols,
                        'received_columns': list(df_new_check.columns)
                    }), 400
                
                shutil.move(file_path, DATA_PATH)
                print(f"Dataset principal creado: {DATA_PATH}")
                
                try:
                    df_new = pd.read_csv(DATA_PATH, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df_new = pd.read_csv(DATA_PATH, encoding='latin-1')
                    except:
                        df_new = pd.read_csv(DATA_PATH, encoding='utf-8', errors='ignore')
                
                message = f'Dataset principal creado desde archivo subido. Total: {len(df_new)} filas'
            
            # Limpiar archivo temporal si aún existe
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Retrenar modelo automáticamente
            print("Iniciando retrenamiento del modelo...")
            retrain_result = subprocess.run(
                ['python', 'train_model.py'],
                capture_output=True,
                text=True,
                timeout=600,
                env={**os.environ, 'TRAINING_MAX_ROWS': '15000'}
            )
            
            retrain_success = retrain_result.returncode == 0 and os.path.exists('models/flight_cluster_model.pkl')
            
            return jsonify({
                'success': True,
                'message': message,
                'retrain_success': retrain_success,
                'retrain_output': retrain_result.stdout if retrain_success else retrain_result.stderr,
                'retrain_exit_code': retrain_result.returncode
            })
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error procesando archivo: {error_trace}")
            
            # Limpiar archivo temporal si existe
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
            
            # Extraer mensaje de error más claro
            error_msg = str(e)
            error_type = type(e).__name__
            
            # Mensajes de error más descriptivos
            if 'UnicodeDecodeError' in error_type or 'UnicodeEncodeError' in error_type or 'charmap' in error_msg:
                error_msg = 'Error de codificación de caracteres. El archivo debe usar codificación UTF-8 o Latin-1. Intente guardar el archivo como UTF-8.'
            elif 'MemoryError' in error_type or 'MemoryError' in error_msg:
                error_msg = 'Error de memoria. El archivo es demasiado grande. Intente con un archivo más pequeño o divida los datos en lotes.'
            elif 'KeyError' in error_type:
                error_msg = f'Error: Columna faltante en el archivo. {error_msg}'
            elif 'ValueError' in error_type:
                error_msg = f'Error de formato en los datos: {error_msg}'
            elif 'EmptyDataError' in error_type:
                error_msg = 'El archivo CSV está vacío o no tiene datos válidos.'
            elif 'ParserError' in error_type:
                error_msg = f'Error al leer el archivo CSV. Verifique que el formato sea correcto: {error_msg}'
            
            print(f"Error detallado: {error_type}: {error_msg}")
            print(f"Traceback completo: {error_trace}")
            
            return jsonify({
                'success': False,
                'error': f'Error procesando archivo: {error_msg}',
                'error_type': error_type,
                'traceback': error_trace if app.debug else None
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

