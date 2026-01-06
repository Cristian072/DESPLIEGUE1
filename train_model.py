"""
Script para entrenar el modelo de clustering con datos de vuelos
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score
import joblib
import os
from datetime import datetime

def load_data(file_path, max_rows=None):
    """Cargar datos del CSV"""
    print(f"Loading data from {file_path}...")
    # Limitar número de filas para evitar problemas de memoria en Railway
    # Railway tiene límites de memoria (típicamente 512MB-1GB), así que usamos una muestra
    if max_rows is None:
        # Usar un límite conservador para Railway (memoria limitada)
        max_rows = 8000  # Límite seguro para Railway (512MB-1GB de RAM)
    
    if max_rows:
        print(f"Limiting to {max_rows} rows for memory efficiency...")
        # Leer solo el límite de filas directamente para ahorrar memoria
        # Esto evita cargar todo el archivo en memoria
        df = pd.read_csv(file_path, nrows=max_rows)
        print(f"Loaded {len(df)} rows (limited to {max_rows} for memory efficiency)")
    else:
        df = pd.read_csv(file_path)
    
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {df.columns.tolist()}")
    return df

def preprocess_data(df):
    """Preprocesar datos para el modelo"""
    print("Preprocessing data...")
    
    # Crear copia para trabajar
    df_processed = df.copy()
    
    # Convertir fecha a datetime
    df_processed['Fecha'] = pd.to_datetime(df_processed['Fecha'], format='%d/%m/%Y', errors='coerce')
    
    # Extraer características temporales
    df_processed['Dia_semana'] = df_processed['Fecha'].dt.dayofweek
    df_processed['Mes'] = df_processed['Fecha'].dt.month
    df_processed['Hora_salida_num'] = df_processed['Hora_salida'].apply(lambda x: int(str(x).zfill(4)[:2]) if pd.notna(x) else 0)
    
    # Calcular duración del vuelo (aproximada)
    df_processed['Duracion_vuelo'] = (
        df_processed['Hora_llegada'].apply(lambda x: int(str(int(x)).zfill(4)[:2])*60 + int(str(int(x)).zfill(4)[2:]) if pd.notna(x) else 0) -
        df_processed['Hora_salida'].apply(lambda x: int(str(int(x)).zfill(4)[:2])*60 + int(str(int(x)).zfill(4)[2:]) if pd.notna(x) else 0)
    )
    # Manejar vuelos que cruzan medianoche
    df_processed['Duracion_vuelo'] = df_processed['Duracion_vuelo'].apply(lambda x: x + 1440 if x < 0 else x)
    
    # Codificar origen y destino
    le_origin = LabelEncoder()
    le_dest = LabelEncoder()
    df_processed['Origen_encoded'] = le_origin.fit_transform(df_processed['Origen'].astype(str))
    df_processed['Destino_encoded'] = le_dest.fit_transform(df_processed['Destino'].astype(str))
    
    # Seleccionar características para clustering
    feature_cols = [
        'Retraso_Salida',
        'Retraso_llegada', 
        'Retraso_Clima',
        'Duracion_vuelo',
        'Hora_salida_num',
        'Dia_semana',
        'Origen_encoded',
        'Destino_encoded'
    ]
    
    print(f"Using features: {feature_cols}")
    
    # Seleccionar y limpiar datos
    X = df_processed[feature_cols].copy()
    X = X.dropna()
    
    print(f"Data after cleaning: {X.shape[0]} rows")
    print(f"Missing values: {X.isnull().sum().sum()}")
    
    # Guardar encoders para uso futuro
    os.makedirs('models', exist_ok=True)
    joblib.dump(le_origin, 'models/origin_encoder.pkl')
    joblib.dump(le_dest, 'models/dest_encoder.pkl')
    
    return X, feature_cols, df_processed.loc[X.index]

def find_optimal_clusters(X_scaled, max_k=10):
    """Encontrar número óptimo de clusters usando método del codo y silhouette"""
    print("Finding optimal number of clusters...")
    inertias = []
    silhouette_scores = []
    # Reducir rango y usar menos inicializaciones para ahorrar memoria
    k_range = range(2, min(max_k + 1, min(8, X_scaled.shape[0] // 10)))
    
    for k in k_range:
        # Usar menos inicializaciones para ahorrar memoria
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=5, max_iter=100)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        # Usar muestra para silhouette si hay muchos datos
        if X_scaled.shape[0] > 10000:
            sample_size = 10000
            sample_indices = np.random.choice(X_scaled.shape[0], sample_size, replace=False)
            silhouette_scores.append(silhouette_score(X_scaled[sample_indices], kmeans.labels_[sample_indices]))
        else:
            silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
        print(f"  k={k}: Silhouette={silhouette_scores[-1]:.4f}")
    
    # Elegir k con mejor silhouette score
    optimal_k = k_range[np.argmax(silhouette_scores)]
    print(f"Optimal k: {optimal_k} (Silhouette: {max(silhouette_scores):.4f})")
    
    return optimal_k

def train_model(X, n_clusters=None):
    """Entrenar modelo de clustering"""
    # Normalizar datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Encontrar número óptimo de clusters si no se especifica
    if n_clusters is None:
        n_clusters = find_optimal_clusters(X_scaled)
    
    print(f"Training K-Means model with {n_clusters} clusters...")
    
    # Entrenar K-Means con parámetros optimizados para memoria
    # Reducir n_init y max_iter para ahorrar memoria en Railway
    # Usar algoritmo 'elkan' que es más eficiente en memoria para datasets pequeños
    kmeans = KMeans(
        n_clusters=n_clusters, 
        random_state=42, 
        n_init=3,  # Reducido de 5 a 3 para ahorrar memoria
        max_iter=100,
        algorithm='lloyd'  # Usar algoritmo estándar que es más estable
    )
    print("Fitting K-Means model (this may take a moment)...")
    kmeans.fit(X_scaled)
    
    # Evaluar modelo (usar muestra si hay muchos datos para ahorrar memoria)
    if X_scaled.shape[0] > 5000:
        sample_size = min(5000, X_scaled.shape[0])
        sample_indices = np.random.choice(X_scaled.shape[0], sample_size, replace=False)
        silhouette = silhouette_score(X_scaled[sample_indices], kmeans.labels_[sample_indices])
        print(f"Silhouette Score (estimated from {sample_size} samples): {silhouette:.4f}")
    else:
        silhouette = silhouette_score(X_scaled, kmeans.labels_)
        print(f"Silhouette Score: {silhouette:.4f}")
    
    return kmeans, scaler, silhouette

def save_model(model, scaler, feature_cols, output_dir='models'):
    """Guardar modelo, scaler y metadata"""
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, 'flight_cluster_model.pkl')
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    features_path = os.path.join(output_dir, 'feature_names.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(feature_cols, features_path)
    
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")
    print(f"Feature names saved to {features_path}")

def main():
    """Función principal"""
    data_file = 'DATA SET VUELOS - 10 000.csv'
    
    if not os.path.exists(data_file):
        print(f"Error: File {data_file} not found!")
        return
    
    # Cargar datos con límite de memoria para Railway
    # Usar máximo 20,000 filas para evitar problemas de memoria
    max_rows = int(os.environ.get('TRAINING_MAX_ROWS', 20000))
    print(f"Using max_rows={max_rows} for training (set TRAINING_MAX_ROWS env var to change)")
    df = load_data(data_file, max_rows=max_rows)
    
    # Preprocesar
    X, feature_cols, df_processed = preprocess_data(df)
    
    if X.shape[0] < 10:
        print("Error: Not enough data after preprocessing!")
        return
    
    # Entrenar modelo (usar None para encontrar k óptimo automáticamente)
    model, scaler, score = train_model(X, n_clusters=100)
    
    # Guardar modelo
    save_model(model, scaler, feature_cols)
    
    # Guardar estadísticas de clusters
    labels = model.predict(scaler.transform(X))
    df_processed['Cluster'] = labels
    cluster_stats = df_processed.groupby('Cluster').agg({
        'Retraso_Salida': ['mean', 'std', 'count'],
        'Retraso_llegada': ['mean', 'std'],
        'Retraso_Clima': 'mean',
        'Duracion_vuelo': 'mean'
    }).round(2)
    
    print("\n" + "="*50)
    print("CLUSTER STATISTICS")
    print("="*50)
    print(cluster_stats)
    
    print("\nModel training completed successfully!")
    print(f"Silhouette Score: {score:.4f}")
    print(f"Number of clusters: {model.n_clusters}")
    print(f"Total samples: {X.shape[0]}")

if __name__ == '__main__':
    main()

