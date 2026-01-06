# Configuración de Railway

## ⚠️ IMPORTANTE: El Dataset CSV

El archivo `DATA SET VUELOS - 70 000.csv` está en `.gitignore` (porque `*.csv` está ignorado), por lo que **NO se subirá a Git** y Railway no lo tendrá durante el build.

## Soluciones para Proporcionar el Dataset

### Opción 1: Quitar el CSV del .gitignore (Recomendado para archivos pequeños/medianos)

1. Edita `.gitignore` y agrega una excepción:
```gitignore
# Datos grandes (no subir a Git)
*.xlsx
*.csv
!DATA SET VUELOS - 70 000.csv  # Excepción para este archivo específico
```

2. Agrega el archivo a Git:
```bash
git add "DATA SET VUELOS - 70 000.csv"
git commit -m "Add dataset file"
git push
```

3. Descomenta la línea COPY en el Dockerfile:
```dockerfile
COPY ["DATA SET VUELOS - 70 000.csv", "./"]
```

### Opción 2: Usar Volumen en Railway (Recomendado para archivos grandes)

1. En Railway, ve a tu servicio
2. Agrega un volumen persistente
3. Monta el volumen en `/app`
4. Sube el archivo CSV al volumen usando Railway CLI o la interfaz web

### Opción 3: Descargar en Runtime

1. Sube el archivo CSV a un almacenamiento externo (Google Drive, Dropbox, S3, etc.)
2. En Railway, agrega una variable de entorno `DATASET_URL` con la URL del archivo
3. El script `scripts/download_dataset.sh` lo descargará automáticamente

### Opción 4: Subir Manualmente Después del Despliegue

1. Despliega la aplicación sin el dataset
2. Usa Railway CLI o la interfaz web para subir el archivo CSV
3. Reinicia el servicio para que entrene el modelo

## Problemas Comunes y Soluciones

### 1. Error al construir la imagen Docker

✅ **SOLUCIONADO**: El Dockerfile ya no intenta copiar el CSV durante el build. El build debería funcionar ahora.

### 2. Variables de Entorno en Railway

Railway automáticamente proporciona:
- `PORT`: Puerto donde la aplicación debe escuchar

No necesitas configurar variables adicionales a menos que uses servicios externos.

### 3. Verificar el Build

1. Ve a tu proyecto en Railway
2. Revisa los logs del build
3. Si hay errores, verifica:
   - Que todos los archivos necesarios estén en Git
   - Que el Dockerfile tenga la sintaxis correcta
   - Que el entrypoint.sh tenga permisos de ejecución

### 4. Después del Despliegue

Una vez desplegado:
1. El modelo se entrenará automáticamente si no existe (ver entrypoint.sh)
2. Puedes acceder a la aplicación en la URL proporcionada por Railway
3. Ve a `/health` para verificar el estado del sistema

## Estructura Recomendada para Railway

```
proyecto/
├── Dockerfile          # ✅ Configurado
├── railway.json        # ✅ Configurado
├── entrypoint.sh       # ✅ Configurado
├── app.py              # ✅ Aplicación Flask
├── train_model.py      # ✅ Script de entrenamiento
├── requirements.txt    # ✅ Dependencias
├── templates/         # ✅ Templates HTML
├── scripts/           # ✅ Scripts auxiliares
└── DATA SET VUELOS - 70 000.csv  # ⚠️ Debe estar en Git o como volumen
```

## Troubleshooting

### El build falla con error de archivo no encontrado
- Verifica que el archivo CSV esté en el repositorio Git
- O comenta la línea COPY en el Dockerfile y proporciona el archivo como volumen

### El modelo no se entrena
- Revisa los logs de Railway
- Verifica que el archivo CSV esté disponible en runtime
- El entrypoint.sh debería entrenar el modelo automáticamente si no existe

### La aplicación no inicia
- Verifica los logs en Railway
- Asegúrate de que el puerto esté configurado correctamente
- Verifica que gunicorn esté instalado en requirements.txt

