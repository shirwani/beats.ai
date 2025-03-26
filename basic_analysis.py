from cassandra.cluster import Cluster
import matplotlib.pyplot as plt
import numpy as np
from utils import *


cluster = Cluster(['127.0.0.1'])
session = cluster.connect('beats_ai')


def get_data_from_db(genre):
    query = "SELECT * FROM tracks WHERE genre = %s ALLOW FILTERING;"
    tracks = session.execute(query, (genre, ))
    data = dict()
    data['tempo']           = list()
    data['energy']          = list()
    data['danceability']    = list()
    data['complexity']      = list()
    data['loudness']        = list()
    data['valence']         = list()
    data['time_signature']  = list()
    data['key']             = list()
    data['key_mode']        = list()
    data['views']           = list()
    data['likes']           = list()
    data['popularity']      = list()

    for track in tracks:
        if track.key_mode is None:
            continue

        if track.views < 100000:
            continue

        data['tempo'].append(track.tempo)
        data['energy'].append(track.energy)
        data['danceability'].append(track.danceability)
        data['complexity'].append(track.complexity)
        data['loudness'].append(track.loudness)
        data['valence'].append(track.valence)
        data['time_signature'].append(track.time_signature)
        data['key'].append(track.key)
        data['key_mode'].append(track.key_mode)
        data['views'].append(track.views)
        data['likes'].append(track.likes)
        data['popularity'].append(track.likes/track.views)

    return data


def get_hat_data():
    data = dict()
    data['tempo'] = list()
    data['energy'] = list()
    data['danceability'] = list()
    data['complexity'] = list()
    data['loudness'] = list()
    data['valence'] = list()
    data['time_signature'] = list()
    data['key'] = list()
    data['key_mode'] = list()
    data['views'] = list()
    data['likes'] = list()
    data['popularity'] = list()

    tracks = read_from_json_file('hackaz.json')

    for key in tracks:
        data['tempo'].append(tracks[key]['tempo'])
        data['energy'].append(tracks[key]['energy'])
        data['danceability'].append(tracks[key]['danceability'])
        data['complexity'].append(tracks[key]['complexity'])
        data['loudness'].append(tracks[key]['loudness'])
        data['valence'].append(tracks[key]['valence'])
        data['time_signature'].append(tracks[key]['time_signature'])
        data['key'].append(tracks[key]['key'])
        data['views'].append(tracks[key]['views'])
        data['likes'].append(tracks[key]['likes'])
        data['popularity'].append(tracks[key]['likes']/tracks[key]['views'])
        data['key'].append(tracks[key]['key'])
        data['key_mode'].append(tracks[key]['key_mode'])

    return data


def basic_analysis():
    feature_map = {
        "tempo":            "Tempo (BPM)",
        "energy":           "Energy Level",
        "danceability":     "Danceability",
        "complexity":       "Melodic Complexity",
        "loudness":         "Loudness (dB)",
        "valence":          "Valence (Happiness)",
        "time_signature":   "Time Signature",
        "key_mode":          "key_mode"
    }

    data1 = get_data_from_db(genre="hip_hop_and_rap")
    data2 = get_data_from_db(genre="country")
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
