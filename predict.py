from tensorflow.keras.models import load_model
import joblib  # for loading StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
from Cassandra import *

output  = 'popularity'
colname = 'artist'
colval  = "Kendrick Lamar"

db = Cassandra()
cfg = read_from_json_file('config.json')
db_tablename = cfg['youtube']['db_tablename']

def run_prediction(features):
    actual = features[output]

    model_file = f"models/{output}_{colname}_{colval}"
    model = load_model(f"{model_file}.keras")
    scaler = joblib.load(f"{model_file}.pkl")  # Must have saved it earlier with training
    print(f"{model_file}.keras")

    del features[output]

    feature_cols = list(features.keys())

    df_input = pd.DataFrame([features])[feature_cols]
    scaled_input = scaler.transform(df_input)

    # Predict
    predicted = model.predict(scaled_input)[0][0]

    print(f"📈 Actual    {output}: {actual}")
    print(f"📈 Predicted {output}: {predicted}")

    return [actual, predicted]


if __name__ == '__main__':
    data = db.get_data_by_row_from_db(db_tablename, colname='artist', colval='Eminem')
    ya = list()
    yp = list()
    x = list()
    count = 0

    for d in data:
        count += 1
        x.append(count)
        [a, p] = run_prediction(d)
        ya.append(a)
        yp.append(p)



    # Create plot
    plt.scatter(x, ya, label='Actual', marker='o')
    plt.scatter(x, yp, label='Predicted', marker='x')

    plt.legend()
    plt.grid(True)
    plt.show()