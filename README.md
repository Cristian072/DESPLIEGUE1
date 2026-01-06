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
├── app.py                      # Aplicación Flask
├── train_model.py              # Entrenamiento del modelo
├── entrypoint.sh               # Script de inicio
├── Dockerfile                  # Configuración Docker
├── requirements.txt            # Dependencias
├── templates/
│   └── index.html             # Interfaz web moderna
├── scripts/
│   ├── process_new_data.py   # Procesar nueva data
│   └── health_check.py        # Health check del sistema
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # Pipeline CI/CD
└── models/                    # Modelos entrenados
```

## 🔧 Endpoints API

- `GET /` - Interfaz web principal
- `POST /predict` - Predicción de cluster para un vuelo
- `GET /api/clusters` - Información sobre clusters
- `GET /api/cluster-visualization` - Datos para visualización 2D
- `GET /api/stats` - Estadísticas del dataset
- `POST /api/query` - Consultar vuelos con filtros
- `POST /api/upload-data` - Subir nueva data y retrenar modelo
- `POST /api/retrain` - Retrenar modelo manualmente
- `GET /health` - Health check del sistema
- `GET /test` - Test endpoint

## 🔄 Pipelines de Mantenimiento e Integración Continua

### Pipeline CI/CD (GitHub Actions)

El proyecto incluye un pipeline automatizado en `.github/workflows/ci-cd.yml` que:

1. **Test**: Ejecuta health checks y validaciones
2. **Train Model**: Entrena el modelo automáticamente en cada push
3. **Deploy**: Despliega automáticamente a Railway

### Procesamiento de Nueva Data

Cuando tengas nueva data de vuelos:

1. **Opción 1: Interfaz Web**
   - Ve a la pestaña "Maintenance"
   - Sube el archivo CSV con nueva data
   - El sistema automáticamente:
     - Valida la estructura del CSV
     - Combina con el dataset existente
     - Crea un backup del dataset anterior
     - Retrena el modelo automáticamente

2. **Opción 2: Script Manual**
   ```bash
   python scripts/process_new_data.py --new-data nuevo_archivo.csv
   python train_model.py  # Retrenar modelo
   ```

### Características del Pipeline

- ✅ Validación automática de datos
- ✅ Backup automático antes de cambios
- ✅ Retrenamiento automático del modelo
- ✅ Health checks en cada despliegue
- ✅ Integración continua con GitHub Actions
- ✅ Despliegue automático a Railway

## 🎨 Características de la Interfaz

- **Predicción**: Formulario interactivo para predecir clusters
- **Visualización de Clusters**: 
  - Gráficos de barras con distribución
  - Visualización 2D con PCA
  - Detalles de cada cluster
- **Consultas**: Búsqueda avanzada de vuelos con filtros
- **Estadísticas**: Dashboard con métricas del dataset
- **Mantenimiento**: Upload de nueva data y retrenamiento

## 🛠️ Tecnologías

- **Backend**: Flask, Scikit-learn, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js, Plotly
- **ML**: K-Means Clustering, PCA
- **DevOps**: Docker, Railway, GitHub Actions
- **CI/CD**: GitHub Actions workflows

## 📊 Modelo de Aprendizaje

- **Tipo**: Aprendizaje No Supervisado (K-Means)
- **Características**: 
  - Retrasos de salida y llegada
  - Retrasos por clima
  - Duración del vuelo
  - Hora de salida
  - Día de la semana
  - Origen y destino codificados
- **Métricas**: Silhouette Score para evaluación
- **Clusters**: Número óptimo determinado automáticamente

