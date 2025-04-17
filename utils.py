import hashlib
import json
import csv
from functools import wraps
import os


def delete_file(file):
    try:
        os.remove(file)
    except Exception as e:
        print(e)

def hashify(text):
    """
    Generate MD5 hash from text
    """
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest()


def dump_to_json_file(data, file, indent=2):
    """
    Dump JSON input to file
    """
    with open(file, 'w') as f:
        json.dump(data, f, indent=indent)


def read_from_json_file(file):
    """
    Read and return JSON from .JSON file
    """
    with open(file, 'r') as f:
        return json.load(f)


def read_from_csv_file_with_header(file):
    """
    Read from csv file and return list() of dict(),
    where keys of doct() are column names from the header line
    """
    with open(file) as f:
        csv_reader = csv.reader(f)
        col_names = next(csv_reader)  # header
        data = list()
        for row in csv_reader:
            d = dict()
            for c in col_names:
                d[c] = row[col_names.index(c)]
            data.append(d)
    return data


def read_list_from_text_file(file):
    """
    Read the text file as a list of string
    """
    with open(file, "r") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    return lines

def fcn_logger(fcn):
    """
    Log function calls
    """
    @wraps(fcn)
    def wrapper(*args, **kwargs):
        print(f"->Calling '{fcn.__name__}'")
        result = fcn(*args, **kwargs)
        print(f"->Done '{fcn.__name__}'")
        return result
    return wrapper


def get_hat_data():
    data = dict()
    data['tempo'] = list()
    data['energy'] = list()
    data['danceability'] = list()
    data['complexity'] = list()
    data['speechiness'] = list()
    data['loudness'] = list()
    data['valence'] = list()
    data['time_signature'] = list()
    data['key'] = list()
    data['key_mode'] = list()
    data['views'] = list()
    data['likes'] = list()
    data['popularity'] = list()

    tracks = read_from_json_file('scratch/hackaz.json')

    for key in tracks:
        data['tempo'].append(tracks[key]['tempo'])
        data['energy'].append(tracks[key]['energy'])
        data['danceability'].append(tracks[key]['danceability'])
        data['complexity'].append(tracks[key]['complexity'])
        data['speechiness'].append(tracks[key]['speechiness'])
        data['loudness'].append(tracks[key]['loudness'])
        data['valence'].append(tracks[key]['valence'])
        data['time_signature'].append(tracks[key]['time_signature'])
        data['key'].append(tracks[key]['key'])
        data['key_mode'].append(tracks[key]['key_mode'])
        data['views'].append(tracks[key]['views'])
        data['likes'].append(tracks[key]['likes'])
        data['popularity'].append(tracks[key]['likes']/tracks[key]['views'])

    return data

