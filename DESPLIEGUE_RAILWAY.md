# 🚀 INSTRUCCIONES PARA SUBIR A GITHUB Y DESPLEGAR EN RAILWAY

## 📦 PASO 1: Preparar archivos para Git

### 1.1 Asegúrate de tener estos archivos en tu carpeta:
```
✅ app.py
✅ train_model.py
✅ requirements.txt
✅ Dockerfile
✅ Procfile
✅ templates/index.html
✅ README.md
✅ INSTRUCCIONES.md
✅ .gitignore
✅ railway.json (nuevo)
```

### 1.2 IMPORTANTE - Archivos que NO debes subir:
- ❌ `DATA SET VUELOS - 70 000.xlsx` (muy grande, no necesario en Git)
- ❌ `models/*.pkl` (se generarán automáticamente en Railway)
- ❌ `__pycache__/` (archivos temporales)

---

## 📤 PASO 2: Subir a GitHub

### 2.1 Abre PowerShell o Terminal en la carpeta del proyecto
```powershell
cd "D:\UNIVERSIDAD\CURSOS\APRENDIZAJE MAQUINA\PROYECTO FINAL"
```

### 2.2 Inicializar Git (si no lo has hecho)
```bash
git init
```

### 2.3 Agregar todos los archivos
```bash
git add .
```

### 2.4 Hacer commit
```bash
git commit -m "Initial commit - Flight Clustering App"
```

### 2.5 Conectar con tu repositorio de GitHub
```bash
git remote add origin https://github.com/Cristian072/DESPLIEGUE1.git
```

### 2.6 Subir a GitHub
```bash
git branch -M main
git push -u origin main
```

**Si te pide usuario y contraseña:**
- Usuario: tu usuario de GitHub
- Contraseña: usa un **Personal Access Token** (no tu contraseña normal)
  - Cómo crear token: https://github.com/settings/tokens
  - Permisos: repo (todos)

---

## 🚂 PASO 3: Desplegar en Railway

### 3.1 Crear cuenta en Railway
1. Ve a: https://railway.app
2. Click en "Login" → "Login with GitHub"
3. Autoriza Railway a acceder a tu GitHub

### 3.2 Crear nuevo proyecto
1. En Railway, click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona tu repositorio: **DESPLIEGUE1**
4. Railway detectará automáticamente el Dockerfile

### 3.3 Configurar variables de entorno (si es necesario)
- Railway detectará todo automáticamente
- No necesitas configurar nada adicional

### 3.4 Esperar el despliegue
- Railway comenzará a construir la imagen Docker
- Esto tomará 2-5 minutos
- Verás el progreso en tiempo real

### 3.5 Obtener la URL
1. Una vez desplegado, click en tu proyecto
2. Click en el servicio (service)
3. Ve a la pestaña **"Settings"**
4. Click en **"Generate Domain"**
5. Copia la URL (ejemplo: `tu-app.railway.app`)

---

## ⚠️ IMPORTANTE: Entrenar el modelo en Railway

Como el dataset no está en Git, tienes 2 opciones:

### Opción A: Subir el dataset a Railway (Recomendado)
1. En Railway, ve a tu proyecto
2. Click en **"Variables"**
3. Agrega el archivo Excel como variable de entorno o:
4. Usa el panel de archivos de Railway para subir el Excel

### Opción B: Entrenar localmente y subir modelos
1. Ejecuta localmente: `python train_model.py`
2. Esto creará `models/flight_cluster_model.pkl` y `models/scaler.pkl`
3. Actualiza `.gitignore` para incluir estos archivos:
   ```bash
   # Comentar esta línea en .gitignore:
   # models/*.pkl
   ```
4. Agrega los modelos a Git:
   ```bash
   git add models/*.pkl
   git commit -m "Add trained models"
   git push
   ```

---

## ✅ PASO 4: Verificar que funciona

### 4.1 Abre tu URL de Railway
- Ejemplo: `https://tu-app.railway.app`
- Deberías ver la interfaz de la aplicación

### 4.2 Probar una predicción
- Ingresa valores de ejemplo
- Click en "Predict Cluster"
- Debería funcionar si el modelo está entrenado

### 4.3 Si no funciona (modelo no entrenado)
- Ve a los logs de Railway
- Verás el error: "Model not trained yet"
- Necesitas entrenar el modelo (ver Opción A o B arriba)

---

## 🔄 PASO 5: Actualizaciones futuras

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

Railway detectará automáticamente los cambios y redesplegará la app.

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Permission denied"
- Verifica que tengas acceso al repositorio de GitHub
- Usa Personal Access Token en lugar de contraseña

### Error: "Model not found" en Railway
- Sube los archivos .pkl a Git (Opción B)
- O sube el Excel a Railway y entrena allí

### Error: "Port already in use"
- Railway maneja esto automáticamente
- No necesitas configurar puertos

### La app no carga
- Revisa los logs en Railway
- Verifica que el build fue exitoso

---

## 📝 RESUMEN RÁPIDO

```bash
# 1. Subir a GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/Cristian072/DESPLIEGUE1.git
git branch -M main
git push -u origin main

# 2. En Railway
# - Login con GitHub
# - New Project → Deploy from GitHub
# - Seleccionar DESPLIEGUE1
# - Esperar despliegue
# - Generar dominio
```

¡Listo! Tu app estará en producción 🎉

