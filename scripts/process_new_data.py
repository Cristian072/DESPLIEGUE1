"""
Script para procesar nueva data y combinar con dataset existente
"""
import pandas as pd
import os
import sys
import argparse
from datetime import datetime

# Configurar codificación UTF-8 para evitar problemas en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def validate_data(df):
    """Validar que el DataFrame tenga las columnas requeridas"""
    required_columns = [
        'Fecha', 'ID_aerolinea', 'Matricula', 'Num_vuelo',
        'ID_Origgen_Seq', 'Origen', 'ID_Destino_Seq', 'Destino',
        'Hora_salida', 'Retraso_Salida', 'Hora_llegada',
        'Retraso_llegada', 'Retraso_Clima'
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"ERROR: Missing required columns: {missing}")
        return False
    
    return True

def process_new_data(new_data_path, main_data_path='DATA SET VUELOS - 10 000.csv'):
    """Procesar nueva data y combinar con dataset principal"""
    print(f"Processing new data from: {new_data_path}")
    
    # Cargar nueva data
    try:
        new_df = pd.read_csv(new_data_path)
        print(f"New data loaded: {new_df.shape[0]} rows, {new_df.shape[1]} columns")
    except Exception as e:
        print(f"ERROR loading new data: {e}")
        return False
    
    # Validar estructura
    if not validate_data(new_df):
        return False
    
    # Normalizar nombres de columnas (por si acaso)
    new_df.columns = new_df.columns.str.strip()
    
    # Cargar dataset principal
    if os.path.exists(main_data_path):
        try:
            main_df = pd.read_csv(main_data_path)
            print(f"Main dataset loaded: {main_df.shape[0]} rows")
            
            # Combinar datasets
            combined_df = pd.concat([main_df, new_df], ignore_index=True)
            print(f"Combined dataset: {combined_df.shape[0]} rows")
            
            # Eliminar duplicados si existen
            before_dedup = len(combined_df)
            combined_df = combined_df.drop_duplicates(
                subset=['Fecha', 'Num_vuelo', 'Origen', 'Destino', 'Hora_salida'],
                keep='last'
            )
            after_dedup = len(combined_df)
            if before_dedup != after_dedup:
                print(f"Removed {before_dedup - after_dedup} duplicate rows")
            
            # Crear backup del dataset original
            backup_path = f"{main_data_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            main_df.to_csv(backup_path, index=False)
            print(f"Backup created: {backup_path}")
            
            # Guardar dataset combinado
            combined_df.to_csv(main_data_path, index=False)
            print(f"Combined dataset saved to: {main_data_path}")
            
        except Exception as e:
            print(f"ERROR processing main dataset: {e}")
            return False
    else:
        # Si no existe el dataset principal, usar el nuevo como principal
        print(f"Main dataset not found. Using new data as main dataset.")
        new_df.to_csv(main_data_path, index=False)
        print(f"New dataset saved to: {main_data_path}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Process new flight data and merge with main dataset')
    parser.add_argument('--new-data', required=True, help='Path to new CSV file')
    parser.add_argument('--main-data', default='DATA SET VUELOS - 10 000.csv', 
                       help='Path to main dataset CSV file')
    
    args = parser.parse_args()
    
    success = process_new_data(args.new_data, args.main_data)
    
    if success:
        print("\n[SUCCESS] Data processing completed successfully!")
        print("You can now retrain the model using: python train_model.py")
        sys.exit(0)
    else:
        print("\n[ERROR] Data processing failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
