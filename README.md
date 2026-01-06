# Flight Clustering Prediction System

Aplicación web con modelo de aprendizaje no supervisado (K-Means) para agrupar y predecir características de vuelos.

## 🚀 Inicio Rápido

### Instalación Local

```bash
pip install -r requirements.txt
python train_model.py  # Entrenar modelo
python app.py          # Ejecutar app (http://localhost:5000)
```

### Despliegue con Docker

```bash
docker build -t flight-clustering-app .
docker run -p 5000:5000 flight-clustering-app
```

### Despliegue en Railway

1. Conectar repositorio GitHub a Railway
2. Railway detectará automáticamente el Dockerfile
3. Desplegar

## 📁 Estructura

```
.
├── app.py              # Aplicación Flask
├── train_model.py      # Entrenamiento del modelo
├── entrypoint.sh       # Script de inicio
├── Dockerfile          # Configuración Docker
├── requirements.txt    # Dependencias
├── templates/
│   └── index.html     # Interfaz web
└── models/            # Modelos entrenados
```

## 🔧 Endpoints

- `GET /` - Interfaz web
- `POST /predict` - Predicción de cluster
- `GET /health` - Health check
- `GET /test` - Test endpoint

## 🛠️ Tecnologías

Flask • Scikit-learn • Docker • Railway

