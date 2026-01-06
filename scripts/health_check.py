"""
Health check script para verificar el estado del sistema
"""
import os
import sys
import joblib

def check_model_files():
    """Verificar que los archivos del modelo existan"""
    model_path = 'models/flight_cluster_model.pkl'
    scaler_path = 'models/scaler.pkl'
    
    checks = {
        'model_file': os.path.exists(model_path),
        'scaler_file': os.path.exists(scaler_path),
        'data_file': os.path.exists('DATA SET VUELOS - 10 000.csv')
    }
    
    if checks['model_file']:
        try:
            model = joblib.load(model_path)
            checks['model_valid'] = model is not None
            checks['n_clusters'] = model.n_clusters if hasattr(model, 'n_clusters') else 0
        except Exception as e:
            checks['model_valid'] = False
            checks['model_error'] = str(e)
    else:
        checks['model_valid'] = False
    
    return checks

def main():
    print("Running health check...")
    checks = check_model_files()
    
    all_ok = all([
        checks.get('model_file', False),
        checks.get('scaler_file', False),
        checks.get('model_valid', False),
        checks.get('data_file', False)
    ])
    
    if all_ok:
        print("✅ Health check passed!")
        print(f"  - Model file: OK")
        print(f"  - Scaler file: OK")
        print(f"  - Model valid: OK")
        print(f"  - Data file: OK")
        print(f"  - Number of clusters: {checks.get('n_clusters', 0)}")
        sys.exit(0)
    else:
        print("⚠️  Health check found issues:")
        for key, value in checks.items():
            if isinstance(value, bool) and not value:
                print(f"  - {key}: FAILED")
        sys.exit(1)

if __name__ == '__main__':
    main()
