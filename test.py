from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from Cassandra import *

db = Cassandra()
cfg = read_from_json_file('config.json')
db_tablename = cfg['downloads']['db_tablename']
output     = cfg['test']['output']
colname    = cfg['test']['colname']
colval     = cfg['test']['colval']

def actual_vs_predicted():
    data = db.get_data_by_row_from_db(db_tablename, colname=colname, colval=colval)

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

    x = list(range(1, len(actuals) + 1))

    # Plot

    plt.figure(figsize=(15, 5), facecolor='lightgray')
    plt.scatter(x, predicted, label='Predicted', marker='o', alpha=0.4, s=10, color='r')
    plt.scatter(x, actuals, label='Actual', marker='o', alpha=0.4, s=10, color='b')
    plt.legend()
    plt.grid(True)
    plt.title(f"{output} prediction for {colname} {colval} | model = {model_file}")
    plt.show()


if __name__ == '__main__':
    actual_vs_predicted()
    db.shutdown()
