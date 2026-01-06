# Flight Clustering Prediction System

Aplicación web con modelo de aprendizaje no supervisado (K-Means) para agrupar y predecir características de vuelos.

## 📋 Requisitos del Proyecto

Este proyecto cumple con los requisitos de la segunda unidad:
- ✅ Modelo de aprendizaje no supervisado (K-Means Clustering)
- ✅ Aplicación web desplegable
- ✅ Pipelines de CI/CD automatizados
- ✅ Procesos de mantenimiento continuo

## 🚀 Inicio Rápido

### 1. Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Entrenar el modelo (requiere el archivo DATA SET VUELOS - 70 000.xlsx)
python train_model.py

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

### 2. Despliegue con Docker

```bash
# Construir la imagen
docker build -t flight-clustering-app .

# Ejecutar el contenedor
docker run -p 5000:5000 flight-clustering-app
```

### 3. Despliegue en Producción

#### Opción A: Heroku

```bash
# Instalar Heroku CLI
# Crear archivo Procfile
echo "web: gunicorn app:app" > Procfile

# Desplegar
heroku create tu-app-nombre
git push heroku main
```

#### Opción B: Railway / Render

1. Conectar tu repositorio GitHub
2. La plataforma detectará automáticamente el Dockerfile
3. Desplegar

## 📁 Estructura del Proyecto

```
.
├── app.py                 # Aplicación Flask principal
├── train_model.py         # Script para entrenar el modelo
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Configuración Docker
├── templates/
│   └── index.html        # Interfaz web
├── models/               # Modelos entrenados (se crean al entrenar)
│   ├── flight_cluster_model.pkl
│   └── scaler.pkl
└── .github/workflows/
    └── ci.yml           # Pipeline de CI/CD
```

## 🔧 Funcionalidades

### Modelo de Clustering

- **Algoritmo**: K-Means
- **Características**: Duración, Distancia, Precio
- **Métricas**: Silhouette Score
- **Hiperparámetros**: n_clusters=5, random_state=42

### API Endpoints

- `GET /` - Interfaz web
- `POST /predict` - Predicción de cluster
- `GET /health` - Health check

## 🔄 CI/CD Pipeline

El pipeline automatizado incluye:

1. **Tests**: Verificación de dependencias y sintaxis
2. **Build**: Construcción de imagen Docker
3. **Deploy**: (Configurar según plataforma)

## 📊 Entrenamiento del Modelo

```bash
python train_model.py
```

El script:
1. Carga datos del Excel
2. Preprocesa y limpia datos
3. Entrena modelo K-Means
4. Evalúa con Silhouette Score
5. Guarda modelo y scaler

## 🧪 Pruebas

### Prueba Manual

```bash
# Health check
curl http://localhost:5000/health

# Predicción
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"duration": 2.5, "distance": 1500, "price": 250}'
```

## 📝 Próximos Pasos para Mejorar

1. ✅ Estructura básica creada
2. ⏳ Ajustar preprocesamiento según columnas reales del dataset
3. ⏳ Agregar más métricas de evaluación
4. ⏳ Mejorar interfaz web
5. ⏳ Agregar visualizaciones
6. ⏳ Implementar re-entrenamiento automático
7. ⏳ Agregar logging y monitoreo

## 🛠️ Tecnologías

- **Backend**: Flask (Python)
- **ML**: Scikit-learn (K-Means)
- **Data**: Pandas, NumPy
- **Deploy**: Docker, Gunicorn
- **CI/CD**: GitHub Actions

## 📄 Licencia

Proyecto académico - Universidad

