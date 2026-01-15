import joblib
import numpy as np
from pathlib import Path

# -------------------------
# Paths to ML artifacts
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml_artifacts" / "model.pkl"
SCALER_PATH = BASE_DIR / "ml_artifacts" / "scaler.pkl"
ENCODER_PATH = BASE_DIR / "ml_artifacts" / "encoder.pkl"

# -------------------------
# Load artifacts
# -------------------------
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
encoder = joblib.load(ENCODER_PATH)  # if used for categorical features

# -------------------------
# Feature order (from training)
# -------------------------
FEATURE_ORDER = [
    'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max',
    'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std',
    'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
    'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean',
    'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean',
    'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
    'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags',
    'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length',
    'Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length',
    'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count',
    'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count',
    'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
    'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
    'Fwd Header Length.1', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk',
    'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk',
    'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', 'Subflow Fwd Bytes',
    'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
    'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward',
    'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean',
    'Idle Std', 'Idle Max', 'Idle Min'
]

# -------------------------
# Prediction function
# -------------------------
def predict(data: dict):
    """
    Input: JSON dict from /predict API
    Output: "attack" or "normal"
    """
    try:
        # 1️⃣ Extract values in correct order
        X = np.array([data[feature] for feature in FEATURE_ORDER]).reshape(1, -1)

        # 2️⃣ Encode categorical features (if any)
        # encoder.transform expects 2D array, apply only if needed
        # X_encoded = encoder.transform(X_categorical)
        # merge numeric + encoded features
        # Here assuming all features numeric, skip encoder step if unnecessary

        # 3️⃣ Scale
        X_scaled = scaler.transform(X)

        # 4️⃣ Predict
        pred = model.predict(X_scaled)[0]

        return "attack" if pred == 1 else "normal"

    except KeyError as e:
        raise ValueError(f"Missing feature in input JSON: {e}")