from tensorflow.keras.models import load_model
import joblib  # for loading StandardScaler
import numpy as np
from utils import *

metric     = "popularity"
genre      = "hip_hop_and_rap"
track      = "amends"
file_path  = f"samples/{track}.mp3"
model_file = f"models/{metric}_{genre}"

def run_prediction():
    # Load model
    model = load_model(f"{model_file}.keras")

    # Load scaler used during training
    scaler = joblib.load(f"{model_file}.pkl")  # You must have saved it earlier
    print(scaler)

    features = get_features(track)
    print(features)

    # Convert to the correct input format for the model
    feature_array = np.array([list(features.values())])
    feature_array_scaled = scaler.transform(feature_array)

    # Predict
    predicted_ratio = model.predict(feature_array_scaled)[0][0]
    print(f"📈 Predicted likes/views ratio: {predicted_ratio:.5f}")

def get_features(track):
    tracks = read_from_json_file('hackaz.json')
    t = tracks[track]
    return t

if __name__ == '__main__':
    run_prediction()
