# Troubleshooting - Railway Deployment

## Error: "Application failed to respond"

Este error significa que Railway no puede conectarse a tu aplicación. Aquí están las causas más comunes y soluciones:

### ✅ Solución 1: Verificar Logs en Railway

1. Ve a tu proyecto en Railway
2. Haz clic en "View Logs" o "Deploy Logs"
3. Busca errores relacionados con:
   - Gunicorn no iniciando
   - Errores de Python
   - Problemas con el puerto

### ✅ Solución 2: Verificar que la Aplicación Escuche en el Puerto Correcto

La aplicación debe escuchar en el puerto que Railway proporciona a través de la variable de entorno `PORT`.

**Verificado**: El código ya está configurado correctamente:
- `entrypoint.sh` usa `PORT=${PORT:-5000}`
- `app.py` usa `port = int(os.environ.get('PORT', 5000))`
- Gunicorn se ejecuta con `--bind 0.0.0.0:$PORT`

### ✅ Solución 3: El Script de Inicio Debe Ser Resiliente

**PROBLEMA ANTERIOR**: El `set -e` en `entrypoint.sh` hacía que el script se detuviera si el entrenamiento del modelo fallaba.

**SOLUCIONADO**: 
- Removí `set -e` para que el script continúe incluso si algo falla
- El entrenamiento del modelo ahora es opcional
- Gunicorn siempre se ejecuta al final, incluso si el modelo no se puede entrenar

### ✅ Solución 4: Verificar que Gunicorn Esté Instalado

Gunicorn está en `requirements.txt`, pero si hay problemas, el script ahora lo verifica e instala automáticamente.

### ✅ Solución 5: Verificar el Dataset

Si el dataset no está disponible:
- La aplicación **SÍ iniciará** (solucionado)
- El modelo no se entrenará automáticamente
- Puedes entrenarlo después desde la interfaz web

## Verificación Paso a Paso

### 1. Verificar que el Build Funcionó

En Railway, revisa los logs del build. Deberías ver:
```
✅ Requirements instalados
✅ Archivos copiados
✅ Dockerfile construido exitosamente
```

### 2. Verificar que la Aplicación Inició

En los logs de deploy, busca:
```
==========================================
Starting Flight Clustering Application
==========================================
Port: [número]
Starting Gunicorn server...
Listening on 0.0.0.0:[puerto]
```

### 3. Verificar Endpoints

Una vez desplegado, prueba estos endpoints:
- `https://tu-app.railway.app/health` - Debe responder con estado del sistema
- `https://tu-app.railway.app/test` - Debe responder con información básica
- `https://tu-app.railway.app/` - Debe mostrar la interfaz web

## Errores Comunes y Soluciones

### Error: "Module not found"
- Verifica que todas las dependencias estén en `requirements.txt`
- Revisa los logs del build para ver qué módulo falta

### Error: "Port already in use"
- Railway maneja esto automáticamente
- Asegúrate de usar la variable `PORT` de Railway

### Error: "Model not found"
- Esto es normal si el dataset no está disponible
- La aplicación iniciará de todas formas
- Entrena el modelo después desde la interfaz web

### Error: "Dataset file not found"
- La aplicación iniciará sin el dataset
- Sube el dataset después del despliegue
- O configura un volumen en Railway

## Comandos Útiles para Debugging

### Ver logs en tiempo real (Railway CLI)
```bash
railway logs
```

### Verificar estado del servicio
```bash
railway status
```

### Conectar al contenedor (si Railway lo permite)
```bash
railway shell
```

## Checklist Pre-Deploy

Antes de hacer deploy, verifica:

- [ ] `requirements.txt` tiene todas las dependencias
- [ ] `Dockerfile` está correctamente configurado
- [ ] `entrypoint.sh` tiene permisos de ejecución (`chmod +x`)
- [ ] `railway.json` está configurado correctamente
- [ ] El código no tiene errores de sintaxis
- [ ] Los templates HTML están en `templates/`
- [ ] Los scripts están en `scripts/`

## Después del Deploy

1. **Verifica los logs** - Deberías ver que gunicorn inició
2. **Prueba `/health`** - Debe responder con el estado
3. **Prueba `/test`** - Debe responder con información básica
4. **Accede a la interfaz web** - Debe cargar correctamente
5. **Si el modelo no existe** - Ve a "Mantenimiento" y entrénalo

## Si Nada Funciona

1. Revisa los logs completos en Railway
2. Verifica que el puerto esté correctamente configurado
3. Asegúrate de que gunicorn esté instalado
4. Verifica que no haya errores de sintaxis en Python
5. Contacta el soporte de Railway con los logs de error


