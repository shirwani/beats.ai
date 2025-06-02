import matplotlib.pyplot as plt
import numpy as np
from Cassandra import *

db = Cassandra()
cfg = read_from_json_file('config.json')
db_tablename = cfg['downloads']['db_tablename']
x_label = cfg['predict']['output']


def basic_analysis():
    feature_map = {
        "tempo":            "Tempo (BPM)",
        "energy":           "Energy Level",
        "danceability":     "Danceability",
        "complexity":       "Melodic Complexity",
        "loudness":         "Loudness (dB)",
        "speechiness":      "Speechiness",
        "valence":          "Valence (Happiness)",
        "time_signature":   "Time Signature",
        "key_mode":         "key_mode"
    }

    data1 = db.get_data_from_db(db_tablename, colname='genre',  colval='hip_hop_and_rap')
    data2 = db.get_data_from_db(db_tablename, colname='artist', colval='Gunna')

    features = list(feature_map.keys())
    fig, axes = plt.subplots(4, 2, figsize=(20, 10))
    for i, ax in enumerate(axes.flat):
        y_label = features[i]

        x1 = np.array(data1[x_label])
        y1 = np.array(data1[y_label])

        x2 = np.array(data2[x_label])
        y2 = np.array(data2[y_label])

        ax.scatter(x1,    y1,    color="blue", alpha=0.6, s=10)
        ax.scatter(x2,    y2,    color="red",  alpha=0.6, s=10)

        ax.set_xlabel(x_label)
        ax.set_ylabel(feature_map[y_label])
        ax.grid(True)
        ax.set_facecolor("gray")

        #ax.set_xscale('log')
        #ax.set_xlim(0, 10000000)

    fig.set_facecolor("gray")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    basic_analysis()
    db.shutdown()
