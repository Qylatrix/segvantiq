import sys
import os

modules = [
    'streamlit',
    'pandas',
    'numpy',
    'plotly',
    'sklearn',
    'streamlit_lottie',
    'requests',
    'seaborn',
    'matplotlib',
    'joblib'
]

print(f"Python interpreter: {sys.executable}")
print(f"Python version: {sys.version}")
print("-" * 30)

failed = []
for mod in modules:
    try:
        __import__(mod)
        print(f"[OK] {mod}")
    except ImportError as e:
        print(f"[FAIL] {mod}: {e}")
        failed.append(mod)

print("-" * 30)
if not failed:
    print("All core modules imported successfully!")
else:
    print(f"Failed to import {len(failed)} modules: {', '.join(failed)}")

# Check local src imports
try:
    sys.path.append(os.getcwd())
    from src.preprocess import preprocess_pipeline
    from src.model import build_clustering_model
    print("[OK] Local src modules found")
except Exception as e:
    print(f"[FAIL] Local src modules: {e}")
