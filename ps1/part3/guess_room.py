#! /usr/bin/env python3

import glob
from os.path import basename
import fileinput


def get_rooms():
    files = glob.glob("fingerprints/*")
    return [basename(file) for file in files]


def get_access_points():
    access_points = set()
    with fileinput.input(files=glob.glob("fingerprints/*")) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 2:
                continue
            access_points.add(parts[0])
    return access_points


def index_access_points():
    # get the list of access points seen in all the files
    access_points = get_access_points()
    if len(access_points) == 0:
        raise RuntimeError("No access_points to work on")
    indexes = 0
    ap_indexes = {}
    for ap in access_points:
        ap_indexes[ap] = indexes
        indexes += 1
    return ap_indexes


def generate_datapoint(access_points, ap_indexes):
    dp = [0] * len(ap_indexes)
    for ap, rssi in access_points:
        ap_index = ap_indexes[ap]
        dp[ap_index] = rssi
    return dp


def generate_training_data(ap_indexes):
    data = []
    access_points = []
    with fileinput.input(files=glob.glob("fingerprints/*")) as f:
        for line in f:
            line = line.strip()
            room = basename(fileinput.filename())
            if line == "-fingerprint-":
                datapoint = generate_datapoint(access_points, ap_indexes)
                data.append((datapoint, room))
                access_points = []
            else:
                parts = line.split()
                if len(parts) != 2:
                    print("malformed line:", line)
                    continue
                access_points.append(parts)
    print(data)
    return data


def train_model(data):
    # each item in data is a ([rssi for each ap at ap_index], room_name)
    return None


def save_model(model):
    pass


def run_predictor(model, ap_indexes):
    pass


def main():
    # rooms are stored as the names of the files in the fingerprints directory
    rooms = get_rooms()

    if len(rooms) == 0:
        print("No room fingerprints to work on. Make fingerprints first.")
        exit(1)
    else:
        print("Found the following rooms:", rooms)

    # map access point bssids to incrementing integers from 0
    ap_indexes = None
    try:
        print("Indexing access_points")
        ap_indexes = index_access_points()
    except RuntimeError as e:
        print("Failed to index access_points:", e)
        exit(1)

    # generate a maxtrix where each row is the strength of the access points
    #    and access point X is located at position i in the previously
    #    generated map.
    print("Generating training data")
    data = generate_training_data(ap_indexes)

    # pass the data into Perceptron/NaiveBayes
    model = train_model(data)

    # save the model
    save_model(model)

    # run run_fingerprint and guess the correct room.
    run_predictor(model, ap_indexes)


if __name__ == "__main__":
    main()
