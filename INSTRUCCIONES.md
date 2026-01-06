# 📚 INSTRUCCIONES PASO A PASO

## 🎯 ¿Qué es este proyecto?

Una aplicación web que usa **aprendizaje no supervisado** (K-Means clustering) para agrupar vuelos similares. La aplicación está lista para desplegarse y tiene procesos automatizados de CI/CD.

---

## ✅ PASO 1: Preparar el Entorno

### 1.1 Instalar Python
- Asegúrate de tener Python 3.11 o superior
- Verifica: `python --version`

### 1.2 Instalar Dependencias
```bash
pip install -r requirements.txt
```

---

## ✅ PASO 2: Entrenar el Modelo

### 2.1 Verificar que tienes el dataset
- El archivo `DATA SET VUELOS - 70 000.xlsx` debe estar en la carpeta raíz

### 2.2 Ejecutar el entrenamiento
```bash
python train_model.py
```

**¿Qué hace este script?**
- Lee el archivo Excel
- Identifica columnas numéricas (duración, distancia, precio)
- Limpia los datos (elimina valores faltantes)
- Entrena un modelo K-Means con 5 clusters
- Guarda el modelo en `models/flight_cluster_model.pkl`

**⚠️ IMPORTANTE:** Si el script no encuentra las columnas esperadas, ajusta el código en `train_model.py` según las columnas reales de tu Excel.

---

## ✅ PASO 3: Probar la Aplicación Localmente

### 3.1 Ejecutar la aplicación
```bash
python app.py
```

### 3.2 Abrir en el navegador
- Ve a: `http://localhost:5000`
- Deberías ver una interfaz bonita para ingresar datos de vuelos

### 3.3 Probar una predicción
- Ingresa valores de ejemplo:
  - Duración: 2.5 horas
  - Distancia: 1500 km
  - Precio: 250
- Haz clic en "Predict Cluster"
- Deberías ver el cluster asignado

---

## ✅ PASO 4: Desplegar con Docker (Recomendado)

### 4.1 Construir la imagen
```bash
docker build -t flight-clustering-app .
```

### 4.2 Ejecutar el contenedor
```bash
docker run -p 5000:5000 flight-clustering-app
```

### 4.3 Verificar
- Abre: `http://localhost:5000`

---

## ✅ PASO 5: Desplegar en Producción

### Opción A: Heroku (Gratis)

1. **Instalar Heroku CLI**
   - Descarga desde: https://devcenter.heroku.com/articles/heroku-cli

2. **Crear archivo Procfile** (ya está creado si usas gunicorn)
   ```
   web: gunicorn app:app
   ```

3. **Iniciar sesión en Heroku**
   ```bash
   heroku login
   ```

4. **Crear aplicación**
   ```bash
   heroku create tu-app-nombre
   ```

5. **Desplegar**
   ```bash
   git push heroku main
   ```

### Opción B: Railway (Más fácil)

1. Ve a: https://railway.app
2. Conecta tu repositorio GitHub
3. Railway detectará automáticamente el Dockerfile
4. ¡Listo! Tu app estará en producción

### Opción C: Render

1. Ve a: https://render.com
2. Conecta tu repositorio
3. Selecciona "Web Service"
4. Render detectará el Dockerfile automáticamente

---

## ✅ PASO 6: Configurar CI/CD (GitHub Actions)

### 6.1 Subir código a GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin TU_REPOSITORIO_GITHUB
git push -u origin main
```

### 6.2 Verificar Pipeline
- Ve a tu repositorio en GitHub
- Click en "Actions"
- Deberías ver el pipeline ejecutándose automáticamente

**El pipeline hace:**
- ✅ Instala dependencias
- ✅ Ejecuta tests básicos
- ✅ Construye imagen Docker

---

## ✅ PASO 7: Probar Mantenimiento Continuo

### 7.1 Hacer un cambio pequeño
- Edita algún archivo (por ejemplo, `app.py`)
- Cambia un texto o color

### 7.2 Subir cambios
```bash
git add .
git commit -m "Test CI/CD"
git push
```

### 7.3 Verificar
- Ve a GitHub Actions
- Deberías ver el pipeline ejecutándose automáticamente
- Si todo está bien, el build será exitoso

---

## 📊 PARA LA PRESENTACIÓN

### 1. Funcionamiento de la aplicación (3 puntos)
- ✅ Muestra la app funcionando en inglés
- ✅ Explica cómo funciona el clustering
- ✅ Demuestra una predicción en vivo

### 2. Entrenamiento del modelo (3 puntos)
- ✅ Muestra el dataset
- ✅ Explica características usadas
- ✅ Muestra métricas (Silhouette Score)
- ✅ Explica hiperparámetros (n_clusters=5)

### 3. Despliegue (2 puntos)
- ✅ Muestra la app en producción (URL)
- ✅ Explica cómo se desplegó

### 4. Pipelines CI/CD (2 puntos)
- ✅ Muestra GitHub Actions funcionando
- ✅ Explica qué hace cada paso

### 5. Pruebas de funcionamiento (2 puntos)
- ✅ Muestra que el pipeline se ejecuta automáticamente
- ✅ Demuestra que detecta errores

### 6. Informe técnico (8 puntos)
- ✅ Documenta herramientas usadas
- ✅ Explica estructura del código
- ✅ Describe proceso de despliegue
- ✅ Documenta pipelines de CI/CD

---

## 🔧 AJUSTES NECESARIOS

### Si tu dataset tiene columnas diferentes:

1. Abre `train_model.py`
2. Busca la función `preprocess_data()`
3. Ajusta las columnas en `feature_cols` según tus datos reales
4. Ejemplo:
   ```python
   feature_cols = ['tiempo_vuelo', 'kilometros', 'tarifa']
   ```

### Si quieres cambiar el número de clusters:

1. Abre `train_model.py`
2. Busca `train_model(X, n_clusters=5)`
3. Cambia el número (ej: `n_clusters=7`)

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Model not trained yet"
- **Solución**: Ejecuta `python train_model.py` primero

### Error: "File not found"
- **Solución**: Asegúrate de que el Excel esté en la carpeta raíz

### Error: "No module named 'flask'"
- **Solución**: Ejecuta `pip install -r requirements.txt`

### La app no carga en el navegador
- **Solución**: Verifica que el puerto 5000 no esté ocupado

---

## 📝 PRÓXIMOS PASOS PARA MEJORAR

1. ✅ Estructura básica - **COMPLETADO**
2. ⏳ Ajustar según columnas reales del dataset
3. ⏳ Agregar más visualizaciones
4. ⏳ Implementar re-entrenamiento automático
5. ⏳ Agregar logging y monitoreo
6. ⏳ Mejorar interfaz con gráficos

---

## 📞 ¿NECESITAS AYUDA?

1. Revisa los archivos creados
2. Lee los comentarios en el código
3. Ejecuta paso a paso según estas instrucciones
4. Si algo falla, revisa la sección "Solución de Problemas"

¡Éxito con tu proyecto! 🚀

