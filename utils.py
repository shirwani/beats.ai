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




