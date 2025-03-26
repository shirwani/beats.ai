from tensorflow.keras.models import load_model
import joblib  # for loading StandardScaler
import numpy as np
import pandas as pd
from utils import *

metric     = "popularity"
genre      = "country"
track      = "amends"
file_path  = f"samples/{track}.mp3"
model_file = f"models/{metric}_{genre}"

def run_prediction():
    # Load model
    model = load_model(f"{model_file}.keras")

    # Load scaler used during training
    scaler = joblib.load(f"{model_file}.pkl")  # Must have saved it earlier with training
    features = get_features()

    feature_cols = list(features.keys())

    print(feature_cols)

    # Convert to the correct input format for the model
    # Wrap in DataFrame
    df_input = pd.DataFrame([features])[feature_cols]
    scaled_input = scaler.transform(df_input)

    # Predict
    predicted_ratio = model.predict(scaled_input)[0][0]
    print(f"📈 Predicted popularity (likes/views ratio): {predicted_ratio:.5f}")

def get_features():
    tracks = read_from_json_file('hackaz.json')
    t = tracks[track]
    return t

if __name__ == '__main__':
    run_prediction()
