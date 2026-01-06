# 🔍 DIAGNÓSTICO COMPLETO PARA RAILWAY

## ✅ Cambios Realizados (Versión Simplificada)

He simplificado completamente la configuración:

1. ✅ **entrypoint.sh** - Script de inicio limpio y directo
2. ✅ **Dockerfile** - Simplificado, copia archivos específicos
3. ✅ **app.py** - Manejo de errores mejorado, fallback si template falla

## 📤 SUBIR CAMBIOS

```powershell
cd "D:\UNIVERSIDAD\CURSOS\APRENDIZAJE MAQUINA\PROYECTO FINAL"

git add .
git commit -m "Simplify deployment - fix Railway startup"
git push
```

## 🔍 VERIFICAR LOGS EN RAILWAY

**MUY IMPORTANTE**: Los logs te dirán exactamente qué está pasando.

1. Ve a Railway → Tu proyecto
2. Click en **"Deployments"** o **"Logs"**
3. Busca el despliegue más reciente
4. Click en **"View Logs"**

### Qué buscar en los logs:

✅ **Buenos signos:**
- "Starting application on port XXXX"
- "Python version: 3.11.x"
- "Booting worker"
- "Listening at: http://0.0.0.0:XXXX"

❌ **Malos signos:**
- "ModuleNotFoundError"
- "FileNotFoundError"
- "Permission denied"
- "Address already in use"
- Cualquier error en rojo

## 🧪 PROBAR ENDPOINTS

Una vez redesplegado, prueba en este orden:

### 1. Test básico (debería funcionar SIEMPRE)
```
https://tu-app.railway.app/test
```
**Esperado**: JSON con información del sistema

### 2. Health check
```
https://tu-app.railway.app/health
```
**Esperado**: JSON con status y estado del modelo

### 3. Página principal
```
https://tu-app.railway.app/
```
**Esperado**: Interfaz web o página de fallback

## 🐛 PROBLEMAS COMUNES Y SOLUCIONES

### Problema 1: "ModuleNotFoundError"
**Causa**: Falta una dependencia en requirements.txt
**Solución**: Verifica que todas las dependencias estén en requirements.txt

### Problema 2: "Template not found"
**Causa**: templates/index.html no está en Git
**Solución**: 
```bash
git add templates/index.html
git commit -m "Add template"
git push
```

### Problema 3: "Address already in use"
**Causa**: Conflicto de puerto
**Solución**: Ya está arreglado con ${PORT}

### Problema 4: La app inicia pero no responde
**Causa**: Gunicorn no está escuchando correctamente
**Solución**: Verifica los logs, busca "Listening at"

## 📋 CHECKLIST DE VERIFICACIÓN

Antes de desplegar, verifica:

- [ ] `app.py` existe y tiene todos los endpoints
- [ ] `templates/index.html` existe
- [ ] `requirements.txt` tiene todas las dependencias
- [ ] `Dockerfile` está correcto
- [ ] `entrypoint.sh` existe y es ejecutable
- [ ] Todos los archivos están en Git

Verificar archivos en Git:
```bash
git ls-files
```

## 🚀 SI AÚN NO FUNCIONA

### Opción 1: Usar modo de desarrollo (temporal)

Cambia temporalmente el Dockerfile para usar Flask directamente:

```dockerfile
CMD python app.py
```

Y en app.py, asegúrate de que el puerto se lea correctamente.

### Opción 2: Verificar estructura de archivos

Asegúrate de que la estructura sea:
```
.
├── app.py
├── train_model.py
├── requirements.txt
├── Dockerfile
├── entrypoint.sh
├── templates/
│   └── index.html
└── models/
    └── (vacío o con .pkl)
```

### Opción 3: Probar localmente con Docker

```bash
docker build -t test-app .
docker run -p 5000:5000 -e PORT=5000 test-app
```

Luego prueba: http://localhost:5000/test

## 📞 COMPARTIR INFORMACIÓN PARA AYUDA

Si necesitas ayuda, comparte:

1. **Logs completos** de Railway (últimas 50 líneas)
2. **Respuesta de** `/test` endpoint
3. **Estructura de archivos** (`git ls-files`)
4. **Versión de Python** (debería ser 3.11)

## ✅ VERSIÓN MÍNIMA FUNCIONAL

Si nada funciona, prueba esta versión mínima:

**app_minimal.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Despliega solo esto para verificar que Railway funciona, luego agrega el resto.

