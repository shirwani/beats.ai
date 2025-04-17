from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from Cassandra import *

db = Cassandra()
cfg = read_from_json_file('config.json')
db_tablename = cfg['downloads']['db_tablename']
output  = cfg['prediction']['output']
colname = cfg['prediction']['colname']
colval  = cfg['prediction']['colval']

def batch_predict(data):
    # Load model and scaler once
    model_file = f"models/{output}_{colname}_{colval}"
    model = load_model(f"{model_file}.keras")
    scaler = joblib.load(f"{model_file}.pkl")
    print(f"{model_file}.keras")

    # Extract actuals and feature inputs
    df = pd.DataFrame(data)
    actuals = df[output].tolist()
    df_inputs = df.drop(columns=[output])

    # Reorder columns (important if model expects a specific order)
    feature_cols = scaler.feature_names_in_ if hasattr(scaler, 'feature_names_in_') else df_inputs.columns.tolist()
    df_inputs = df_inputs[feature_cols]

    # Scale and predict
    scaled_inputs = scaler.transform(df_inputs)
    predicted = model.predict(scaled_inputs).flatten()

    return actuals, predicted

if __name__ == '__main__':
    data = db.get_data_by_row_from_db(db_tablename, colname=colname, colval=colval)

    ya, yp = batch_predict(data)
    db.shutdown()

    x = list(range(1, len(ya) + 1))

    # Plot
    plt.scatter(x, ya, label='Actual', marker='o')
    plt.scatter(x, yp, label='Predicted', marker='x')
    plt.legend()
    plt.grid(True)
    plt.show()
