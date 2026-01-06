# 📘 Manual de Usuario - Sistema de Clustering de Vuelos

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Funcionalidades Principales](#funcionalidades-principales)
4. [Mantenimiento del Sistema](#mantenimiento-del-sistema)
5. [Verificación de Datos](#verificación-de-datos)
6. [Lista de Aeropuertos](#lista-de-aeropuertos)
7. [Guía de Uso Paso a Paso](#guía-de-uso-paso-a-paso)
8. [Solución de Problemas](#solución-de-problemas)
9. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🎯 Introducción

El **Sistema de Clustering de Vuelos** es una herramienta web que utiliza **Aprendizaje No Supervisado (K-Means)** para agrupar vuelos según patrones similares de retrasos. Este sistema ayuda a las aerolíneas a:

- Identificar patrones de retrasos en vuelos
- Optimizar la asignación de recursos
- Reducir costos operativos
- Mejorar la satisfacción del cliente
- Tomar decisiones basadas en datos

---

## 🌐 Acceso al Sistema

1. Abra su navegador web (Chrome, Firefox, Edge, Safari)
2. Ingrese la URL proporcionada por Railway (ej: `https://tu-proyecto.railway.app`)
3. La aplicación se cargará automáticamente

**Nota:** No se requiere inicio de sesión. El sistema está disponible para todos los usuarios autorizados.

---

## 🎨 Funcionalidades Principales

### 1. **Predicción de Cluster**
Permite predecir a qué cluster pertenece un vuelo basándose en sus características.

### 2. **Visualización de Clusters**
Muestra los clusters identificados con sus características, recomendaciones e impacto.

### 3. **Consulta de Vuelos**
Permite buscar y filtrar vuelos específicos del dataset.

### 4. **Estadísticas del Dataset**
Muestra estadísticas detalladas sobre los vuelos en el dataset.

### 5. **Mantenimiento**
Permite entrenar modelos, subir nuevos datos y verificar el estado del sistema.

### 6. **Información**
Contiene documentación sobre cómo funciona el sistema y su valor para aerolíneas.

---

## 🔧 Mantenimiento del Sistema

### Entrenar Modelo Inicial

**Cuándo usar:** La primera vez que usa el sistema o cuando necesita reentrenar desde cero.

**Pasos:**
1. Vaya a la pestaña **"Mantenimiento"**
2. Verifique que el dataset esté disponible (debe aparecer "Dataset disponible")
3. Haga clic en el botón **"Entrenar Modelo"**
4. Espere 2-10 minutos mientras se entrena el modelo
5. Verá un mensaje de éxito cuando termine

**Nota:** El entrenamiento usa un máximo de 8,000 filas para optimizar el uso de memoria.

### Subir Nueva Data

**Cuándo usar:** Cuando tiene nuevos datos de vuelos que desea agregar al sistema.

**Requisitos:**
- El archivo debe ser formato CSV
- Debe tener las mismas columnas que el dataset original
- Columnas requeridas:
  - `Fecha`
  - `Origen`
  - `Destino`
  - `Hora_salida`
  - `Hora_llegada`
  - `Retraso_Salida`
  - `Retraso_llegada`
  - `Retraso_Clima`
  - `Num_vuelo` (opcional pero recomendado)

**Pasos:**
1. Vaya a la pestaña **"Mantenimiento"**
2. En la sección **"Subir Nueva Data"**, haga clic en **"Seleccionar archivo"**
3. Seleccione su archivo CSV
4. Haga clic en **"Subir y Reentrenar"**
5. El sistema:
   - Validará que las columnas coincidan
   - Combinará los nuevos datos con el dataset existente
   - Eliminará duplicados automáticamente
   - **Reentrenará el modelo automáticamente**
6. Espere a que termine el proceso (puede tomar 5-15 minutos)
7. Verá un mensaje de éxito cuando termine

**⚠️ Importante:**
- El sistema crea un backup automático antes de combinar datos
- Los duplicados se eliminan basándose en: Fecha, Num_vuelo, Origen, Destino, Hora_salida
- El reentrenamiento es automático, no necesita hacer nada adicional

### Verificar Estado del Sistema

**Pasos:**
1. Vaya a la pestaña **"Mantenimiento"**
2. En la sección **"Estado del Sistema"**, verá:
   - Estado del modelo (entrenado o no)
   - Estado del scaler
   - Disponibilidad del dataset
   - Número de clusters
3. También puede hacer clic en **"Verificar Estado"** para actualizar la información

---

## ✅ Verificación de Datos

### Verificar que el Dataset Esté Disponible

1. Vaya a la pestaña **"Mantenimiento"**
2. Busque la sección **"Estado del Modelo"**
3. Verifique que aparezca:
   - ✅ **"Dataset disponible"** (verde)
   - ✅ **"Dataset legible"** (verde)
   - Número de filas en el dataset

### Verificar el Contenido del Dataset

1. Vaya a la pestaña **"Estadísticas"**
2. Si el dataset está disponible, verá:
   - Total de vuelos
   - Rango de fechas
   - Promedios de retrasos
   - Top rutas, orígenes y destinos
3. Si no está disponible, verá un mensaje informativo

### Verificar que el Modelo Esté Entrenado

1. Vaya a la pestaña **"Clusters"**
2. Si el modelo está entrenado, verá:
   - Gráfico de clusters
   - Tarjetas con información de cada cluster
   - Recomendaciones por cluster
3. Si no está entrenado, verá un mensaje pidiendo entrenar el modelo

### Verificar Predicciones

1. Vaya a la pestaña **"Predicción"**
2. Complete el formulario con datos de un vuelo
3. Haga clic en **"Predecir Cluster"**
4. Si el modelo está entrenado, verá:
   - El cluster asignado
   - La distancia al centroide
5. Si no está entrenado, verá un error

---

## 🛫 Lista de Aeropuertos

El sistema incluye una lista completa de aeropuertos para realizar pruebas. A continuación se muestra la lista con sus abreviaturas y nombres completos:

### Aeropuertos Principales (Top 30)

| Abreviatura | Nombre del Aeropuerto | Ciudad, Estado/País |
|-------------|----------------------|---------------------|
| **JFK** | John F. Kennedy International Airport | Nueva York, NY, USA |
| **LAX** | Los Angeles International Airport | Los Angeles, CA, USA |
| **ORD** | O'Hare International Airport | Chicago, IL, USA |
| **DFW** | Dallas/Fort Worth International Airport | Dallas, TX, USA |
| **DEN** | Denver International Airport | Denver, CO, USA |
| **ATL** | Hartsfield-Jackson Atlanta International Airport | Atlanta, GA, USA |
| **PHX** | Phoenix Sky Harbor International Airport | Phoenix, AZ, USA |
| **IAH** | George Bush Intercontinental Airport | Houston, TX, USA |
| **LAS** | McCarran International Airport | Las Vegas, NV, USA |
| **MIA** | Miami International Airport | Miami, FL, USA |
| **SEA** | Seattle-Tacoma International Airport | Seattle, WA, USA |
| **MSP** | Minneapolis-Saint Paul International Airport | Minneapolis, MN, USA |
| **DTW** | Detroit Metropolitan Airport | Detroit, MI, USA |
| **PHL** | Philadelphia International Airport | Philadelphia, PA, USA |
| **LGA** | LaGuardia Airport | Nueva York, NY, USA |
| **BOS** | Logan International Airport | Boston, MA, USA |
| **SFO** | San Francisco International Airport | San Francisco, CA, USA |
| **CLT** | Charlotte Douglas International Airport | Charlotte, NC, USA |
| **EWR** | Newark Liberty International Airport | Newark, NJ, USA |
| **MCO** | Orlando International Airport | Orlando, FL, USA |
| **SLC** | Salt Lake City International Airport | Salt Lake City, UT, USA |
| **BWI** | Baltimore/Washington International Airport | Baltimore, MD, USA |
| **DCA** | Ronald Reagan Washington National Airport | Washington, DC, USA |
| **MDW** | Chicago Midway International Airport | Chicago, IL, USA |
| **HNL** | Daniel K. Inouye International Airport | Honolulu, HI, USA |
| **AUS** | Austin-Bergstrom International Airport | Austin, TX, USA |
| **PDX** | Portland International Airport | Portland, OR, USA |
| **STL** | St. Louis Lambert International Airport | St. Louis, MO, USA |
| **BNA** | Nashville International Airport | Nashville, TN, USA |
| **SAN** | San Diego International Airport | San Diego, CA, USA |

### Aeropuertos Adicionales (31-50)

| Abreviatura | Nombre del Aeropuerto | Ciudad, Estado/País |
|-------------|----------------------|---------------------|
| **FLL** | Fort Lauderdale-Hollywood International Airport | Fort Lauderdale, FL, USA |
| **IAD** | Washington Dulles International Airport | Washington, DC, USA |
| **TPA** | Tampa International Airport | Tampa, FL, USA |
| **OAK** | Oakland International Airport | Oakland, CA, USA |
| **SMF** | Sacramento International Airport | Sacramento, CA, USA |
| **SJC** | San Jose International Airport | San Jose, CA, USA |
| **RDU** | Raleigh-Durham International Airport | Raleigh, NC, USA |
| **MSY** | Louis Armstrong New Orleans International Airport | Nueva Orleans, LA, USA |
| **MCI** | Kansas City International Airport | Kansas City, MO, USA |
| **CLE** | Cleveland Hopkins International Airport | Cleveland, OH, USA |
| **IND** | Indianapolis International Airport | Indianapolis, IN, USA |
| **CMH** | John Glenn Columbus International Airport | Columbus, OH, USA |
| **PIT** | Pittsburgh International Airport | Pittsburgh, PA, USA |
| **CVG** | Cincinnati/Northern Kentucky International Airport | Cincinnati, OH, USA |
| **MEM** | Memphis International Airport | Memphis, TN, USA |
| **JAX** | Jacksonville International Airport | Jacksonville, FL, USA |
| **RSW** | Southwest Florida International Airport | Fort Myers, FL, USA |
| **BUF** | Buffalo Niagara International Airport | Buffalo, NY, USA |
| **OGG** | Kahului Airport | Kahului, HI, USA |

### Ejemplos de Rutas para Pruebas

**Rutas Populares:**
- **JFK → LAX**: Nueva York a Los Angeles (coast-to-coast)
- **ATL → MIA**: Atlanta a Miami (sureste)
- **ORD → DEN**: Chicago a Denver (centro-oeste)
- **DFW → SFO**: Dallas a San Francisco (suroeste a oeste)
- **BOS → LAX**: Boston a Los Angeles (este a oeste)

**Rutas Cortas:**
- **JFK → LGA**: Nueva York (diferentes aeropuertos)
- **ORD → MDW**: Chicago (diferentes aeropuertos)
- **DCA → BWI**: Washington DC (diferentes aeropuertos)

**Rutas Internacionales (si están en su dataset):**
- **JFK → LHR**: Nueva York a Londres
- **LAX → NRT**: Los Angeles a Tokio
- **MIA → GRU**: Miami a São Paulo

---

## 📖 Guía de Uso Paso a Paso

### Cómo Hacer una Predicción

1. **Acceda a la pestaña "Predicción"**
2. **Complete el formulario:**
   - **Aeropuerto de Origen:** Seleccione de la lista desplegable (ej: JFK)
   - **Aeropuerto de Destino:** Seleccione de la lista desplegable (ej: LAX)
   - **Fecha:** Ingrese en formato DD/MM/YYYY (ej: 08/01/2018)
   - **Hora de Salida:** Ingrese en formato 24h sin puntos (ej: 1200 para 12:00 PM)
   - **Hora de Llegada:** Ingrese en formato 24h sin puntos (ej: 1500 para 3:00 PM)
   - **Retraso Salida:** Ingrese minutos (ej: 10)
   - **Retraso Llegada:** Ingrese minutos (ej: 15)
   - **Retraso Clima:** Ingrese minutos (ej: 0)
3. **Haga clic en "Predecir Cluster"**
4. **Revise el resultado:**
   - Cluster asignado (número)
   - Distancia al centroide
   - Mensaje descriptivo

### Cómo Ver los Clusters

1. **Acceda a la pestaña "Clusters"**
2. **Espere a que carguen los datos** (puede tomar unos segundos)
3. **Explore las visualizaciones:**
   - **Resumen:** Gráfico de barras con tamaños de clusters
   - **Visualización 2D:** Gráfico interactivo con distribución de clusters
   - **Detalles:** Tarjetas con información detallada de cada cluster
4. **En la vista "Detalles", cada cluster muestra:**
   - Tamaño (número de vuelos)
   - Retrasos promedio (salida, llegada, clima)
   - Tipo de cluster (Puntual, Retraso Moderado, etc.)
   - Impacto esperado
   - Recomendaciones específicas

### Cómo Consultar Vuelos

1. **Acceda a la pestaña "Consulta de Vuelos"**
2. **Aplique filtros (opcionales):**
   - **Aeropuerto de Origen:** Seleccione o deje "Todos"
   - **Aeropuerto de Destino:** Seleccione o deje "Todos"
   - **Retraso Mínimo:** Ingrese minutos mínimos (ej: 0)
   - **Retraso Máximo:** Ingrese minutos máximos (ej: 100)
   - **Límite de Resultados:** Número de vuelos a mostrar (1-500)
3. **Haga clic en "Buscar Vuelos"**
4. **Revise los resultados:**
   - Lista de vuelos que coinciden con los filtros
   - Información de cada vuelo
   - Cluster asignado a cada vuelo

### Cómo Ver Estadísticas

1. **Acceda a la pestaña "Estadísticas"**
2. **Espere a que carguen los datos**
3. **Revise las tarjetas de resumen:**
   - Total de vuelos
   - Retrasos promedio (salida, llegada, clima)
4. **Revise el gráfico:**
   - Top 10 rutas más frecuentes
   - Visualización interactiva

---

## 🔍 Solución de Problemas

### Problema: "Modelo no entrenado aún"

**Solución:**
1. Vaya a la pestaña "Mantenimiento"
2. Verifique que el dataset esté disponible
3. Haga clic en "Entrenar Modelo"
4. Espere a que termine el entrenamiento

### Problema: "Dataset no encontrado"

**Solución:**
1. Verifique que el archivo CSV esté en el servidor
2. Si no está, súbalo desde la pestaña "Mantenimiento"
3. Use el botón "Subir Nueva Data"

### Problema: "Las columnas no coinciden" al subir datos

**Solución:**
1. Verifique que su archivo CSV tenga exactamente las mismas columnas que el dataset original
2. Columnas requeridas:
   - Fecha
   - Origen
   - Destino
   - Hora_salida
   - Hora_llegada
   - Retraso_Salida
   - Retraso_llegada
   - Retraso_Clima
3. Asegúrese de que los nombres de las columnas coincidan exactamente (incluyendo mayúsculas y espacios)

### Problema: "Error de codificación de caracteres"

**Solución:**
1. Guarde su archivo CSV con codificación UTF-8
2. En Excel: "Guardar como" → "CSV UTF-8"
3. En otros programas: Asegúrese de seleccionar UTF-8 al exportar

### Problema: "El entrenamiento excedió el tiempo límite"

**Solución:**
1. El dataset puede ser demasiado grande
2. El sistema automáticamente limita a 8,000 filas
3. Si persiste, contacte al administrador del sistema

### Problema: "No puedo ver los clusters"

**Solución:**
1. Verifique que el modelo esté entrenado (pestaña "Mantenimiento")
2. Verifique su conexión a internet
3. Recargue la página (F5)
4. Revise la consola del navegador para errores (F12)

### Problema: "No puedo ver las estadísticas"

**Solución:**
1. Verifique que el dataset esté disponible
2. Vaya a la pestaña "Mantenimiento" y verifique el estado
3. Si el dataset no está disponible, súbalo
4. Recargue la página después de subir el dataset

---

## ❓ Preguntas Frecuentes

### ¿Con qué frecuencia debo agregar nuevos datos?

**Respuesta:** Se recomienda agregar nuevos datos periódicamente (semanal o mensualmente) para mantener el modelo actualizado y reflejar cambios en las operaciones.

### ¿Qué pasa si las columnas de mi nuevo archivo no coinciden exactamente?

**Respuesta:** El sistema valida automáticamente las columnas y le indicará exactamente qué columnas faltan o sobran. Asegúrese de que su archivo tenga las mismas columnas que el dataset original.

### ¿Cuánto tiempo toma reentrenar el modelo?

**Respuesta:** El tiempo depende del tamaño de los datos, pero típicamente toma entre 2-10 minutos. El sistema le notificará cuando el reentrenamiento esté completo.

### ¿Puedo usar el sistema sin tener conocimientos técnicos?

**Respuesta:** Sí, la interfaz está diseñada para ser intuitiva. Solo necesita subir sus archivos CSV y el sistema se encarga del resto automáticamente.

### ¿Qué significa cada tipo de cluster?

**Respuesta:**
- **Puntual:** Vuelos con retrasos mínimos - mantener estándares
- **Retraso Moderado:** Oportunidades de mejora identificadas
- **Afectado por Clima:** Retrasos principalmente por factores externos
- **Alto Retraso:** Requiere atención inmediata y análisis profundo

### ¿Cómo interpreto la distancia al centroide?

**Respuesta:** La distancia al centroide indica qué tan "típico" es el vuelo para su cluster. Una distancia menor significa que el vuelo es más representativo del cluster.

### ¿Puedo exportar los resultados?

**Respuesta:** Actualmente el sistema muestra los resultados en la interfaz web. Para exportar, puede usar las funciones de impresión o captura de pantalla de su navegador.

### ¿Qué hago si el sistema está lento?

**Respuesta:**
1. Verifique su conexión a internet
2. Cierre otras pestañas del navegador
3. Espere unos minutos si acaba de subir datos (el reentrenamiento puede estar en proceso)
4. Recargue la página

### ¿Los datos se guardan permanentemente?

**Respuesta:** Sí, los datos se guardan en el servidor. Sin embargo, se recomienda mantener backups de sus archivos CSV originales.

### ¿Puedo eliminar datos del sistema?

**Respuesta:** Actualmente no hay una función para eliminar datos individuales. Si necesita eliminar datos, debe subir un nuevo dataset completo sin esos datos.

---

## 📞 Soporte

Si tiene problemas que no se resuelven con esta guía:

1. Revise la sección "Solución de Problemas" arriba
2. Revise la pestaña "Información" en el sistema para más detalles
3. Contacte al administrador del sistema
4. Revise los logs del servidor si tiene acceso

---

## 📝 Notas Finales

- **Backups:** El sistema crea backups automáticos antes de combinar datos nuevos
- **Seguridad:** Asegúrese de que solo usuarios autorizados tengan acceso al sistema
- **Actualizaciones:** El sistema se actualiza automáticamente cuando se despliega desde Git
- **Rendimiento:** El sistema está optimizado para trabajar con hasta 13,000+ filas eficientemente

---

## 📎 Anexos Técnicos

### A. Arquitectura del Sistema

#### A.1. Stack Tecnológico

**Backend:**
- **Python 3.11**: Lenguaje de programación principal
- **Flask 3.0.0**: Framework web para la API REST
- **Gunicorn 21.2.0**: Servidor WSGI para producción
- **Pandas 2.1.3**: Manipulación y análisis de datos
- **NumPy 1.26.2**: Computación numérica y arrays multidimensionales
- **Scikit-learn ≥1.3.2**: Biblioteca de machine learning
- **Joblib ≥1.3.2**: Serialización de modelos entrenados

**Frontend:**
- **HTML5**: Estructura de la interfaz
- **CSS3**: Estilos y diseño responsive
- **JavaScript (Vanilla)**: Interactividad y llamadas a API
- **Chart.js 4.4.0**: Visualización de gráficos
- **Plotly 2.26.0**: Visualizaciones interactivas 2D/3D
- **Font Awesome 6.4.0**: Iconografía

**Infraestructura:**
- **Docker**: Containerización de la aplicación
- **Railway**: Plataforma de despliegue y hosting
- **Git**: Control de versiones

**Almacenamiento:**
- **Archivos CSV**: Dataset de vuelos
- **Pickle (.pkl)**: Modelos entrenados y preprocesadores

#### A.2. Arquitectura de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │Predicción│  │ Clusters │  │Consulta  │  │Estadíst.││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘│
└───────┼──────────────┼──────────────┼─────────────┼─────┘
        │              │              │             │
        └──────────────┴──────────────┴─────────────┘
                        │
        ┌───────────────▼───────────────┐
        │      Flask API (Backend)      │
        │  ┌─────────────────────────┐  │
        │  │   Endpoints REST API    │  │
        │  │  /predict               │  │
        │  │  /api/clusters          │  │
        │  │  /api/stats             │  │
        │  │  /api/query             │  │
        │  │  /api/train             │  │
        │  │  /api/upload-data       │  │
        │  └───────────┬─────────────┘  │
        └──────────────┼────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │  Modelo │   │ Dataset │   │Encoders │
   │  KMeans │   │   CSV   │   │ Label   │
   │  (.pkl) │   │         │   │ (.pkl)  │
   └─────────┘   └─────────┘   └─────────┘
```

---

### B. Aprendizaje Automático (Machine Learning)

#### B.1. Tipo de Aprendizaje

**Aprendizaje No Supervisado (Unsupervised Learning)**

El sistema utiliza **clustering**, una técnica de aprendizaje no supervisado que agrupa datos similares sin necesidad de etiquetas predefinidas. Esto permite descubrir patrones ocultos en los datos de vuelos.

**Ventajas del Aprendizaje No Supervisado:**
- No requiere datos etiquetados (más fácil de obtener)
- Descubre patrones inesperados
- Adaptable a nuevos datos
- Útil para exploración de datos

#### B.2. Algoritmo: K-Means Clustering

**Descripción:**
K-Means es un algoritmo de clustering particional que divide los datos en K grupos (clusters) basándose en la similitud de características.

**Funcionamiento:**
1. **Inicialización**: Selecciona K puntos aleatorios como centroides iniciales
2. **Asignación**: Asigna cada punto de datos al centroide más cercano
3. **Actualización**: Recalcula los centroides como el promedio de los puntos asignados
4. **Iteración**: Repite pasos 2 y 3 hasta convergencia

**Parámetros del Modelo:**
- **n_clusters**: 5 (determinado automáticamente por método del codo y silhouette)
- **n_init**: 3 (número de inicializaciones para evitar mínimos locales)
- **max_iter**: 100 (máximo de iteraciones)
- **algorithm**: 'lloyd' (algoritmo estándar de K-Means)
- **random_state**: 42 (para reproducibilidad)

**Fórmula Matemática:**

El objetivo de K-Means es minimizar la **inercia** (suma de distancias al cuadrado):

```
Inercia = Σ(i=1 to n) min(||xi - μj||²)
```

Donde:
- `xi` = punto de datos i
- `μj` = centroide del cluster j
- `n` = número de puntos de datos

#### B.3. Características (Features) Utilizadas

El modelo utiliza **8 características** para agrupar los vuelos:

1. **Retraso_Salida** (minutos): Retraso en la salida del vuelo
2. **Retraso_llegada** (minutos): Retraso en la llegada del vuelo
3. **Retraso_Clima** (minutos): Retraso causado por condiciones climáticas
4. **Duracion_vuelo** (minutos): Duración total del vuelo
5. **Hora_salida_num** (0-23): Hora de salida en formato numérico
6. **Dia_semana** (0-6): Día de la semana (0=Lunes, 6=Domingo)
7. **Origen_encoded** (numérico): Aeropuerto de origen codificado
8. **Destino_encoded** (numérico): Aeropuerto de destino codificado

**Preprocesamiento:**
- **Label Encoding**: Convierte aeropuertos (texto) a números
- **StandardScaler**: Normaliza todas las características a media 0 y desviación estándar 1
- **Cálculo de duración**: Calcula duración basándose en hora de salida y llegada

#### B.4. Selección del Número Óptimo de Clusters

**Método del Codo (Elbow Method):**
Evalúa la inercia (suma de distancias al cuadrado) para diferentes valores de K. El "codo" indica el número óptimo.

**Silhouette Score:**
Mide qué tan bien separados están los clusters. Valores cercanos a 1 indican clusters bien definidos.

```
Silhouette Score = (b - a) / max(a, b)
```

Donde:
- `a` = distancia promedio a puntos en el mismo cluster
- `b` = distancia promedio a puntos en el cluster más cercano

**Proceso de Selección:**
1. Prueba valores de K desde 2 hasta 8
2. Calcula silhouette score para cada K
3. Selecciona K con el mayor silhouette score
4. Resultado típico: **K = 5 clusters**

#### B.5. Evaluación del Modelo

**Métricas Utilizadas:**

1. **Silhouette Score**: 
   - Rango: -1 a 1
   - Valores típicos: 0.3 - 0.6
   - Indica calidad de la separación de clusters

2. **Inercia (Within-Cluster Sum of Squares)**:
   - Mide la compacidad de los clusters
   - Valores menores indican clusters más compactos

3. **Tamaño de Clusters**:
   - Distribución de vuelos entre clusters
   - Clusters balanceados son preferibles

**Interpretación de Resultados:**
- **Cluster 0-4**: Cada uno representa un patrón diferente de retrasos
- **Centroides**: Valores promedio de características para cada cluster
- **Tamaños**: Número de vuelos en cada cluster

---

### C. Modelos y Preprocesadores

#### C.1. Modelo Principal: KMeans

**Archivo**: `models/flight_cluster_model.pkl`

**Atributos del Modelo:**
- `cluster_centers_`: Coordenadas de los centroides (array 5x8)
- `labels_`: Etiquetas de cluster asignadas a cada punto
- `n_clusters`: Número de clusters (5)
- `inertia_`: Suma de distancias al cuadrado
- `n_iter_`: Número de iteraciones realizadas

**Uso:**
```python
# Cargar modelo
model = joblib.load('models/flight_cluster_model.pkl')

# Predecir cluster
cluster = model.predict(datos_normalizados)
```

#### C.2. Preprocesador: StandardScaler

**Archivo**: `models/scaler.pkl`

**Función**: Normaliza las características para que todas tengan la misma escala.

**Transformación:**
```
x_normalizado = (x - media) / desviación_estándar
```

**Por qué es necesario:**
- Retrasos están en minutos (0-200+)
- Hora está en formato 24h (0-23)
- Sin normalización, características con valores mayores dominarían

#### C.3. Encoders: LabelEncoder

**Archivos**: 
- `models/origin_encoder.pkl`
- `models/dest_encoder.pkl`

**Función**: Convierte nombres de aeropuertos (texto) a números.

**Ejemplo:**
```
JFK → 0
LAX → 1
ORD → 2
...
```

**Ventajas:**
- Permite usar algoritmos que requieren datos numéricos
- Mantiene la relación entre aeropuertos

#### C.4. Feature Names

**Archivo**: `models/feature_names.pkl`

**Contenido**: Lista de nombres de las características utilizadas.

**Uso**: Para referencia y debugging del modelo.

---

### D. Tipos de Clusters Identificados

#### D.1. Cluster Tipo: "On Time" (Puntual)

**Características:**
- Retraso de salida promedio: < 5 minutos
- Retraso de llegada promedio: < 5 minutos
- Retraso por clima: Mínimo

**Interpretación:**
Vuelos que operan con puntualidad excelente. Representan las mejores prácticas operacionales.

**Recomendaciones:**
- Mantener los estándares operativos actuales
- Documentar mejores prácticas
- Replicar estrategias exitosas

#### D.2. Cluster Tipo: "Moderate Delay" (Retraso Moderado)

**Características:**
- Retraso de salida promedio: 5-20 minutos
- Retraso de llegada promedio: 5-20 minutos
- Retraso por clima: Bajo

**Interpretación:**
Vuelos con retrasos moderados que pueden mejorarse con optimizaciones operacionales.

**Recomendaciones:**
- Identificar causas específicas de retrasos
- Optimizar tiempos de embarque/desembarque
- Mejorar coordinación entre departamentos

#### D.3. Cluster Tipo: "Weather Affected" (Afectado por Clima)

**Características:**
- Retraso por clima: > 5 minutos
- Retrasos de salida/llegada: Variables

**Interpretación:**
Vuelos principalmente afectados por condiciones climáticas adversas (factores externos).

**Recomendaciones:**
- Mejorar pronósticos meteorológicos
- Tener planes de contingencia
- Comunicar proactivamente a pasajeros
- Considerar rutas alternativas

#### D.4. Cluster Tipo: "High Delay" (Alto Retraso)

**Características:**
- Retraso de salida promedio: > 20 minutos
- Retraso de llegada promedio: > 20 minutos
- Impacto: Alto en satisfacción y costos

**Interpretación:**
Vuelos con retrasos significativos que requieren atención inmediata.

**Recomendaciones:**
- Revisar operaciones en aeropuerto/ruta específica
- Aumentar tiempo de conexión
- Analizar causas operacionales
- Implementar protocolos de recuperación

---

### E. Pipeline de Procesamiento de Datos

#### E.1. Pipeline de Entrenamiento

```
1. Carga de Datos
   └─> Leer CSV (máximo 8,000 filas para optimización)
   
2. Preprocesamiento
   ├─> Convertir fechas a datetime
   ├─> Extraer día de semana
   ├─> Calcular hora de salida numérica
   ├─> Calcular duración del vuelo
   ├─> Codificar origen y destino (LabelEncoder)
   └─> Seleccionar características relevantes
   
3. Normalización
   └─> Aplicar StandardScaler
   
4. Selección de K
   ├─> Probar K de 2 a 8
   ├─> Calcular silhouette score
   └─> Seleccionar K óptimo
   
5. Entrenamiento
   ├─> Inicializar K-Means con K óptimo
   ├─> Ajustar modelo a datos normalizados
   └─> Evaluar con silhouette score
   
6. Guardado
   ├─> Guardar modelo KMeans
   ├─> Guardar StandardScaler
   ├─> Guardar LabelEncoders
   └─> Guardar nombres de características
```

#### E.2. Pipeline de Predicción

```
1. Entrada de Usuario
   └─> Datos del vuelo (origen, destino, fechas, retrasos)
   
2. Preprocesamiento
   ├─> Convertir fecha a datetime
   ├─> Extraer día de semana
   ├─> Calcular hora de salida numérica
   ├─> Calcular duración
   ├─> Codificar origen (usando encoder guardado)
   └─> Codificar destino (usando encoder guardado)
   
3. Normalización
   └─> Aplicar StandardScaler guardado
   
4. Predicción
   └─> Modelo KMeans predice cluster
   
5. Resultado
   ├─> Número de cluster
   ├─> Distancia al centroide
   └─> Interpretación del cluster
```

#### E.3. Pipeline de Actualización de Datos

```
1. Validación
   ├─> Verificar formato CSV
   ├─> Verificar columnas requeridas
   └─> Verificar codificación (UTF-8)
   
2. Combinación
   ├─> Leer dataset existente
   ├─> Leer nuevos datos
   ├─> Combinar DataFrames
   └─> Eliminar duplicados
   
3. Backup
   └─> Crear backup del dataset anterior
   
4. Guardado
   └─> Guardar dataset combinado
   
5. Reentrenamiento
   └─> Ejecutar pipeline de entrenamiento completo
```

---

### F. Optimizaciones Implementadas

#### F.1. Optimización de Memoria

**Problema**: Railway tiene límites de memoria (512MB-1GB)

**Soluciones Implementadas:**
1. **Límite de filas**: Máximo 8,000 filas para entrenamiento
2. **Carga eficiente**: Usar `nrows` en lugar de cargar todo
3. **Reducción de inicializaciones**: `n_init=3` en lugar de 10
4. **Muestreo para evaluación**: Silhouette score con muestra de 5,000 puntos
5. **Limpieza de memoria**: Eliminar DataFrames grandes después de uso

#### F.2. Optimización de Rendimiento

**Técnicas Aplicadas:**
1. **Caché de modelos**: Cargar modelos una vez al inicio
2. **Límite de consultas**: Máximo 50,000 filas en consultas
3. **Paginación**: Límite de resultados en consultas
4. **Procesamiento asíncrono**: Reentrenamiento en background
5. **Compresión**: Modelos guardados en formato pickle optimizado

#### F.3. Optimización de Código

**Mejoras:**
1. **Validación temprana**: Verificar datos antes de procesar
2. **Manejo de errores robusto**: Try-catch en operaciones críticas
3. **Logging**: Información detallada para debugging
4. **Código modular**: Funciones reutilizables

---

### G. Métricas y Evaluación

#### G.1. Métricas de Clustering

**Silhouette Score:**
- **Rango**: -1 a +1
- **Interpretación**:
  - +1: Clusters perfectamente separados
  - 0: Clusters solapados
  - -1: Puntos asignados incorrectamente
- **Valor típico del modelo**: 0.3 - 0.6

**Inercia (WCSS):**
- **Definición**: Suma de distancias al cuadrado dentro de clusters
- **Objetivo**: Minimizar
- **Uso**: Método del codo para seleccionar K

**Coeficiente de Silhouette por Cluster:**
- Mide la calidad de cada cluster individualmente
- Identifica clusters mal definidos

#### G.2. Validación del Modelo

**Validación Cruzada:**
- No aplicable directamente a clustering no supervisado
- Se usa validación visual y métricas de calidad

**Validación Externa:**
- Comparación con conocimiento del dominio
- Verificación de que clusters tienen sentido operacional

**Validación Temporal:**
- Modelo se reentrena con nuevos datos periódicamente
- Permite adaptación a cambios en patrones

---

### H. Tecnologías Específicas de Machine Learning

#### H.1. Scikit-learn

**Versión**: ≥1.3.2

**Módulos Utilizados:**
- `sklearn.cluster.KMeans`: Algoritmo de clustering
- `sklearn.preprocessing.StandardScaler`: Normalización
- `sklearn.preprocessing.LabelEncoder`: Codificación de etiquetas
- `sklearn.metrics.silhouette_score`: Evaluación de clusters
- `sklearn.decomposition.PCA`: Reducción de dimensionalidad (visualización)

#### H.2. Pandas

**Versión**: 2.1.3

**Uso Principal:**
- Carga y manipulación de datos CSV
- Operaciones de agrupación y agregación
- Limpieza de datos (eliminación de duplicados, manejo de NaN)
- Transformación de fechas y tiempos

#### H.3. NumPy

**Versión**: 1.26.2

**Uso Principal:**
- Operaciones matemáticas en arrays
- Cálculos vectorizados para eficiencia
- Manipulación de arrays multidimensionales
- Operaciones estadísticas

#### H.4. Joblib

**Versión**: ≥1.3.2

**Uso Principal:**
- Serialización de modelos entrenados (pickle optimizado)
- Carga rápida de modelos en producción
- Persistencia de preprocesadores

---

### I. Arquitectura de Despliegue

#### I.1. Containerización con Docker

**Dockerfile:**
- Base: Python 3.11-slim
- Instalación de dependencias desde requirements.txt
- Copia de código, modelos y dataset
- Configuración de variables de entorno
- Entrypoint: script de inicio personalizado

**Ventajas:**
- Consistencia entre entornos
- Fácil despliegue
- Aislamiento de dependencias

#### I.2. Plataforma: Railway

**Características:**
- Despliegue automático desde Git
- Escalado automático
- Variables de entorno
- Logs en tiempo real
- SSL automático

**Configuración:**
- Puerto: Variable de entorno PORT
- Workers: 1 (Gunicorn)
- Timeout: 120 segundos

#### I.3. Servidor Web: Gunicorn

**Configuración:**
- Workers: 1 (para ahorrar memoria)
- Timeout: 120 segundos
- Logs: stdout/stderr
- Preload: Habilitado para mejor rendimiento

---

### J. Seguridad y Buenas Prácticas

#### J.1. Validación de Datos

- Validación de formato de archivos (solo CSV)
- Verificación de columnas requeridas
- Validación de tipos de datos
- Manejo de valores faltantes

#### J.2. Manejo de Errores

- Try-catch en operaciones críticas
- Mensajes de error descriptivos
- Logging de errores para debugging
- Fallbacks para operaciones no críticas

#### J.3. Backups Automáticos

- Backup del dataset antes de combinar datos nuevos
- Timestamp en nombres de backup
- Formato: `dataset.backup_YYYYMMDD_HHMMSS.csv`

---

### K. Limitaciones y Consideraciones

#### K.1. Limitaciones del Modelo

1. **Tamaño de Dataset**: Limitado a 8,000 filas para optimización de memoria
2. **Número de Clusters**: Fijo en 5 (determinado automáticamente)
3. **Características**: Solo 8 características utilizadas
4. **Temporalidad**: No considera tendencias temporales a largo plazo

#### K.2. Consideraciones de Uso

1. **Datos Nuevos**: Deben tener el mismo formato que datos de entrenamiento
2. **Reentrenamiento**: Necesario cuando se agregan datos significativos
3. **Interpretación**: Los clusters son descriptivos, no predictivos de eventos futuros
4. **Memoria**: Sistema optimizado para entornos con memoria limitada

#### K.3. Mejoras Futuras Posibles

1. **Más características**: Incluir más variables (tipo de avión, aerolínea, etc.)
2. **Clustering jerárquico**: Para análisis más detallado
3. **Análisis temporal**: Detectar tendencias a lo largo del tiempo
4. **Alertas automáticas**: Notificar cuando vuelos caen en clusters problemáticos
5. **Dashboard avanzado**: Más visualizaciones y análisis

---

### L. Referencias y Recursos

#### L.1. Documentación Técnica

- **Scikit-learn**: https://scikit-learn.org/stable/
- **Flask**: https://flask.palletsprojects.com/
- **Pandas**: https://pandas.pydata.org/
- **K-Means Algorithm**: https://scikit-learn.org/stable/modules/clustering.html#k-means

#### L.2. Conceptos de Machine Learning

- **Clustering**: Agrupación de datos similares
- **Aprendizaje No Supervisado**: Aprendizaje sin etiquetas
- **Normalización**: Escalado de características
- **Silhouette Score**: Métrica de calidad de clusters

#### L.3. Bibliografía Recomendada

1. "Hands-On Machine Learning" - Aurélien Géron
2. "Introduction to Machine Learning with Python" - Andreas Müller
3. "Pattern Recognition and Machine Learning" - Christopher Bishop

---

### M. Glosario Técnico

**Cluster**: Grupo de puntos de datos similares según sus características.

**Centroide**: Punto central de un cluster, calculado como el promedio de todos los puntos en el cluster.

**Feature (Característica)**: Variable de entrada utilizada por el modelo para hacer predicciones.

**Label Encoding**: Proceso de convertir datos categóricos (texto) a números.

**Normalización**: Proceso de escalar características para que tengan la misma escala.

**Silhouette Score**: Métrica que mide qué tan bien separados están los clusters.

**StandardScaler**: Preprocesador que normaliza datos a media 0 y desviación estándar 1.

**K-Means**: Algoritmo de clustering que divide datos en K grupos.

**Pickle**: Formato de serialización de Python para guardar objetos.

**API REST**: Interfaz de programación que permite comunicación entre frontend y backend.

**WSGI**: Interfaz estándar entre servidores web y aplicaciones Python.

---

**Última actualización:** Enero 2025  
**Versión del Sistema:** 1.0

