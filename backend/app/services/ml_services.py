import os

try:
    import joblib
except ImportError:
    joblib = None

MODEL_PATH = "model.pkl"

model = None

if joblib and os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ ML model loaded successfully")
    except Exception as e:
        print("❌ Failed to load ML model:", e)
else:
    print("⚠️ ML model not found, using dummy prediction")

def predict(features: dict):
    """
    features: dictionary of input features
    """
    if model:
        return model.predict([list(features.values())])[0]
    
    # Dummy fallback
    return "normal"