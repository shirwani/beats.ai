from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from audio_utils import *
from Cassandra import *
from pathlib import Path
from utils import *
import os


db = Cassandra()
cfg = read_from_json_file('config.json')
db_tablename = cfg['downloads']['db_tablename']
output     = cfg['predict']['output']
colname    = cfg['predict']['colname']
colval     = cfg['predict']['colval']

def run_prediction():
    # Load model and scaler only once
    model_file = f"models/{output}_{colname}_{colval}"
    model = load_model(f"{model_file}.keras")
    scaler = joblib.load(f"{model_file}.pkl")
    print(f"{model_file}.keras")

    feature_dicts = db.get_data_by_row_from_db(db_tablename, colname='artist', colval='Hackaz Beats')
    titles = list()
    for f in feature_dicts:
        titles.append(f['title'])
        f.pop('title', None)
        f.pop('popularity', None)

    feature_cols = list(feature_dicts[0].keys())  # assuming all feature dicts are consistent
    df_input = pd.DataFrame(feature_dicts)[feature_cols]

    # Scale features
    scaled_input = scaler.transform(df_input)

    # Predict all at once
    predictions = model.predict(scaled_input).flatten()

    # Display results
    for title, pred in zip(titles, predictions):
        print(f"📈 Predicted {output} for {title}: {pred: .4f}")

    plot_against_all_actual(titles, predictions)

def plot_against_all_actual(titles, predicted):

    plt.figure(figsize=(10, 5), facecolor='lightgray')

    imin =  np.argmin(predicted)
    imax =  np.argmax(predicted)

    pmin = predicted[imin]
    pmax = predicted[imax]

    mp3min = os.path.basename(titles[imin])
    mp3max = os.path.basename(titles[imax])


    # Predictions
    plt.axhline(y=pmax, color='g', linewidth=1, label=mp3max)
    plt.axhline(y=pmin, color='r', linewidth=1, label=mp3min)

    # Baseline training data
    data = db.get_data_by_row_from_db(db_tablename, colname=colname, colval=colval)
    df = pd.DataFrame(data)
    actuals = df[output].tolist()
    x = list(range(1, len(actuals) + 1))

    plt.scatter(x, actuals, label='Actual', marker='o', color='b', alpha=0.4, s=10)
    plt.grid(True)
    plt.title(f"{output} prediction with baseline {colname} -> {colval}")

    plt.legend()
    plt.show()


if __name__ == '__main__':
    run_prediction()
    db.shutdown()
