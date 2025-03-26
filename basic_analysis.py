from cassandra.cluster import Cluster
import matplotlib.pyplot as plt
import numpy as np
from utils import *


cluster = Cluster(['127.0.0.1'])
session = cluster.connect('beats_ai')


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
        "key_mode":          "key_mode"
    }

    data1 = get_data_from_db(session, genre="hip_hop_and_rap")
    data2 = get_data_from_db(session, genre="country")
    data_hat = get_hat_data()

    x_label = 'popularity'

    features = list(feature_map.keys())
    fig, axes = plt.subplots(4, 2, figsize=(8, 10))
    for i, ax in enumerate(axes.flat):
        y_label = features[i]

        x1 = np.array(data1[x_label])
        y1 = np.array(data1[y_label])

        x2 = np.array(data2[x_label])
        y2 = np.array(data2[y_label])

        x_hat = np.array(data_hat[x_label])
        y_hat = np.array(data_hat[y_label])

        print(len(x1), len(x2))

        ax.scatter(x1,    y1,    color="red",   alpha=0.6, s=10)
        ax.scatter(x2,    y2,    color="green", alpha=0.6, s=10)
        ax.scatter(x_hat, y_hat, color="blue",  alpha=0.6, s=10)

        #coeffs = np.polyfit(x, y, 2)  # Degree 1 for a straight line
        #best_fit_line = np.poly1d(coeffs)
        #y_fit = best_fit_line(x)
        #ax.plot(x, y_fit, color="blue", linestyle="--", label="Best-Fit Line")

        ax.set_xlabel(x_label)
        ax.set_ylabel(feature_map[y_label])
        ax.grid(True)
        ax.set_facecolor("gray")

        ax.set_xscale('log')

        #ax.set_xlim(0, 10000000)

    fig.set_facecolor("gray")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    basic_analysis()
    cluster.shutdown()
