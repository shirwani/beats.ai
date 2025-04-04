import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import plot_model
import joblib

from cassandra.cluster import Cluster
from utils import *

metric     = 'popularity'
genre      = "country"
model_file = f"models/{metric}_{genre}"

def train_model():
    # Load dataset
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('beats_ai')

    data = get_data_from_db(session, genre)
    df = pd.DataFrame(data)

    # Prepare inputs and target
    X = df.drop(metric, axis=1)
    y = df[metric]

    # Normalize features
    feature_cols = list(data.keys())
    feature_cols.remove(metric) # that's our Y

    print(feature_cols)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)
    joblib.dump(scaler, f"{model_file}.pkl")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y, test_size=0.2, random_state=42)

    # Model
    model = keras.Sequential([
        keras.Input(shape=(len(feature_cols),)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64,  activation='relu'),
        layers.Dense(32,  activation='relu'),
        layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

    # Evaluate model
    loss, mae = model.evaluate(X_test, y_test)
    print(f"\nTest MAE: {mae:.5f} | Test MSE: {loss:.5f}")

    # Save model
    model.save(f"{model_file}.keras")


if __name__ == '__main__':
    train_model()
