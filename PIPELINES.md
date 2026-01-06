# Pipelines de Mantenimiento e Integración Continua

Este documento describe los pipelines automatizados del sistema de clustering de vuelos.

## 🔄 Pipeline de Integración Continua (CI/CD)

### Configuración GitHub Actions

El pipeline está configurado en `.github/workflows/ci-cd.yml` y se ejecuta automáticamente cuando:

- Se hace push a las ramas `main` o `master`
- Se crea un Pull Request
- Se ejecuta manualmente desde GitHub Actions

### Etapas del Pipeline

1. **Test Stage**
   - Instala dependencias Python
   - Ejecuta health checks
   - Verifica existencia de archivos del modelo

2. **Train Model Stage** (solo en push a main/master)
   - Entrena el modelo automáticamente
   - Genera artefactos del modelo entrenado
   - Los artefactos se guardan por 7 días

3. **Deploy Stage** (solo en push a main/master)
   - Railway detecta automáticamente el push
   - Despliega la nueva versión
   - Ejecuta el entrypoint.sh que incluye:
     - Verificación del modelo
     - Health check
     - Inicio del servidor Gunicorn

## 📤 Pipeline de Procesamiento de Nueva Data

### Flujo Automatizado

Cuando subes nueva data a través de la interfaz web:

```
Nueva Data CSV
    ↓
Validación de Estructura
    ↓
Crear Backup del Dataset Actual
    ↓
Combinar con Dataset Principal
    ↓
Eliminar Duplicados
    ↓
Guardar Dataset Combinado
    ↓
Retrenar Modelo Automáticamente
    ↓
Modelo Actualizado Listo
```

### Uso desde la Interfaz Web

1. Ve a la pestaña **"Maintenance"**
2. Haz clic en el área de upload o arrastra un archivo CSV
3. El sistema automáticamente:
   - Valida que el CSV tenga las columnas requeridas
   - Crea un backup con timestamp del dataset anterior
   - Combina la nueva data con la existente
   - Retrena el modelo con los nuevos datos
   - Muestra el resultado del proceso

### Columnas Requeridas en el CSV

El CSV debe contener estas columnas:
- `Fecha`
- `ID_aerolinea`
- `Matricula`
- `Num_vuelo`
- `ID_Origgen_Seq`
- `Origen`
- `ID_Destino_Seq`
- `Destino`
- `Hora_salida`
- `Retraso_Salida`
- `Hora_llegada`
- `Retraso_llegada`
- `Retraso_Clima`

### Uso desde Línea de Comandos

```bash
# Procesar nueva data
python scripts/process_new_data.py --new-data nuevo_archivo.csv

# Retrenar modelo manualmente
python train_model.py
```

## 🔍 Health Check Pipeline

El sistema incluye health checks automáticos:

### En cada despliegue:
- Verifica existencia de archivos del modelo
- Valida que el modelo sea cargable
- Verifica disponibilidad del dataset
- Comprueba número de clusters

### Endpoint de Health Check

```bash
GET /health
```

Respuesta:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true,
  "n_clusters": 5,
  "data_available": true
}
```

## 🚀 Despliegue en Railway

### Configuración Automática

Railway detecta automáticamente:
- El Dockerfile
- El entrypoint.sh
- Las variables de entorno necesarias

### Variables de Entorno Recomendadas

- `PORT`: Puerto del servidor (Railway lo asigna automáticamente)
- `PYTHONUNBUFFERED=1`: Para logs en tiempo real

### Proceso de Despliegue

1. Railway detecta cambios en GitHub
2. Construye la imagen Docker
3. Ejecuta `entrypoint.sh`:
   ```bash
   # Verifica si el modelo existe
   # Si no existe, lo entrena
   # Ejecuta health check
   # Inicia Gunicorn
   ```
4. La aplicación queda disponible en la URL de Railway

## 📊 Monitoreo y Mantenimiento

### Logs

Los logs están disponibles en:
- Railway Dashboard → Logs
- GitHub Actions → Workflow runs

### Retrenamiento Manual

Si necesitas retrenar el modelo manualmente:

1. **Desde la interfaz web**: Botón "Retrain Model" en Maintenance
2. **Desde API**: `POST /api/retrain`
3. **Desde terminal**: `python train_model.py`

### Backup de Datos

Los backups se crean automáticamente con formato:
```
DATA SET VUELOS - 70 000.csv.backup_YYYYMMDD_HHMMSS
```

Los backups se guardan en el mismo directorio que el dataset principal.

## 🔐 Seguridad y Buenas Prácticas

1. **Validación de Datos**: Todos los CSVs son validados antes de procesar
2. **Backups Automáticos**: Se crean backups antes de modificar datos
3. **Timeouts**: Los procesos tienen timeouts para evitar bloqueos
4. **Error Handling**: Errores son capturados y reportados claramente
5. **Health Checks**: Verificación continua del estado del sistema

## 🐛 Troubleshooting

### El modelo no se entrena automáticamente

- Verifica que el dataset exista en Railway
- Revisa los logs en Railway Dashboard
- Ejecuta health check desde la interfaz web

### Error al subir nueva data

- Verifica que el CSV tenga todas las columnas requeridas
- Asegúrate de que el formato de fecha sea DD/MM/YYYY
- Revisa los logs en la respuesta del upload

### Pipeline de CI/CD no se ejecuta

- Verifica que el workflow esté en `.github/workflows/ci-cd.yml`
- Asegúrate de que Railway esté conectado al repositorio
- Revisa los permisos de GitHub Actions

## 📝 Notas Adicionales

- El modelo se entrena con K-Means usando número óptimo de clusters determinado automáticamente
- Los datos se normalizan usando StandardScaler antes del entrenamiento
- El sistema soporta hasta 70,000+ registros eficientemente
- Las visualizaciones usan PCA para reducir dimensionalidad a 2D

