"""
Script para entrenar el modelo de clustering con datos de vuelos
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import joblib
import os

def load_data(file_path):
    """Cargar datos del Excel"""
    print(f"Loading data from {file_path}...")
    df = pd.read_excel(file_path)
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {df.columns.tolist()}")
    return df

def preprocess_data(df):
    """Preprocesar datos para el modelo"""
    print("Preprocessing data...")
    
    # Seleccionar columnas numéricas relevantes
    # Ajustar según las columnas reales del dataset
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Intentar identificar columnas relevantes para vuelos
    feature_cols = []
    for col in ['duration', 'duracion', 'tiempo', 'time', 'distance', 'distancia', 
                'price', 'precio', 'costo', 'cost']:
        if col in df.columns:
            feature_cols.append(col)
    
    # Si no encontramos columnas específicas, usar las primeras numéricas
    if len(feature_cols) < 2:
        feature_cols = numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
    
    print(f"Using features: {feature_cols}")
    
    # Seleccionar y limpiar datos
    X = df[feature_cols].copy()
    X = X.dropna()
    
    print(f"Data after cleaning: {X.shape[0]} rows")
    
    return X, feature_cols

def train_model(X, n_clusters=5):
    """Entrenar modelo de clustering"""
    print(f"Training K-Means model with {n_clusters} clusters...")
    
    # Normalizar datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Entrenar K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    # Evaluar modelo
    silhouette = silhouette_score(X_scaled, kmeans.labels_)
    print(f"Silhouette Score: {silhouette:.4f}")
    
    return kmeans, scaler, silhouette

def save_model(model, scaler, output_dir='models'):
    """Guardar modelo y scaler"""
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, 'flight_cluster_model.pkl')
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

def main():
    """Función principal"""
    data_file = 'DATA SET VUELOS - 70 000.xlsx'
    
    if not os.path.exists(data_file):
        print(f"Error: File {data_file} not found!")
        return
    
    # Cargar datos
    df = load_data(data_file)
    
    # Preprocesar
    X, feature_cols = preprocess_data(df)
    
    if X.shape[0] < 10:
        print("Error: Not enough data after preprocessing!")
        return
    
    # Entrenar modelo
    model, scaler, score = train_model(X, n_clusters=5)
    
    # Guardar modelo
    save_model(model, scaler)
    
    print("\nModel training completed successfully!")
    print(f"Silhouette Score: {score:.4f}")

if __name__ == '__main__':
    main()

