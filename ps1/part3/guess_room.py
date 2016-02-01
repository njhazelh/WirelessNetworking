#! /usr/bin/env python3.4

import glob
from os.path import basename
import fileinput
from sklearn.linear_model import Perceptron
from sklearn.cross_validation import train_test_split
import subprocess as sp
import numpy as np
import sys
import argparse

"""
This script uses a Perceptron classifier to identify rooms by the strength of
neighboring access points.

Before running this script, make sure that you run
```
    ./run_fingerprint <interface> <room>
```
for each room you want to identify.  This will generate fingerprint files for
each room that you want to identify.  If you want to forget a room, just delete
the fingerprint file for that room from the fingerprints directory.
"""


def get_rooms():
    """
    Gets the list of fingerprint files in the fingerprints directory
    """
    files = glob.glob("fingerprints/*")
    return [basename(file) for file in files]


def get_access_points():
    """
    Run through all the fingerprint files and find the set of all access points
    seen.
    """
    access_points = set()
    with fileinput.input(files=glob.glob("fingerprints/*")) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 2:
                continue
            access_points.add(parts[0])
    return access_points


def index_access_points():
    """
    In order to train the model, we need to associate each access point with a
    variable index in the training data.  For example, if the training data
    were the matrix of rssi information with each row as a single datapoint:
    ```
        [[1 2 3]
         [4 5 6]]
    ```
    and we had access points A, B, and C, we might index the access points such
    that A had rssi of 1 and 4, B had 2 and 5, and C has 3 and 6.  This way,
    the model stays consistent with it's associatation of variables and access
    point rssi.
    """
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
    """
    Generate a single data point.  A datapoint is a list of access point signal
    strengths such that the strength of access point X is at index I, where
    I is the index assigned to it in index_access_points().

    :param access_points: A dict of bssid to ap rssi.
    :param ap_indexes: A dict of bssid to ap index.
    :returns: An array of access point strengths mapped to array indexes.
    """
    dp = [0] * len(ap_indexes)
    for ap, rssi in access_points:
        if ap not in ap_indexes:
            continue
        ap_index = ap_indexes[ap]
        dp[ap_index] = float(rssi)
    return dp


def generate_training_data(ap_indexes):
    """
    Read all the files in the fingerprints directory and generate a matrix of
    all the datapoints.

    :param ap_indexes: The indexes of accesspoints in the training data.
    :returns: A matrix of training data, and the rooms each row represents
    """
    data = []
    rooms = []
    access_points = []
    with fileinput.input(files=glob.glob("fingerprints/*")) as f:
        for line in f:
            line = line.strip()
            room = basename(fileinput.filename())
            if line == "-fingerprint-":
                datapoint = generate_datapoint(access_points, ap_indexes)
                data.append(datapoint)
                rooms.append(room)
                access_points = []
            else:
                parts = line.split()
                if len(parts) != 2:
                    print("malformed line:", line)
                    continue
                access_points.append(parts)
    return data, rooms


def train_model(data, rooms):
    """
    Train the Perceptron classifier on the data.

    :param data: An array of training data where each row is a list of access
        point rssi, and the rssi of an access point always has the same index.
    :param rooms: A list where the value at index i is the room that row i in
        the training data maps to.
    :returns: A trained Perceptron model.
    """
    model = Perceptron()
    data = np.array(data)
    # Split and randomize the locations of the data so we can compute the
    # accuracy and the model trains in balanced manner.
    x_train, x_test, y_train, y_test = train_test_split(data, rooms)

    # Check the accuracy of the model.
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Accuracy:", 1 - np.mean(y_pred == y_test))
    return model


def run_predictor(model, ap_indexes, interface):
    """
        Use the trained model to guess which room the computer is currently in.
        Runs in a stream that never ends.

        :param model: The trained model.
        :param ap_indexes: The access point indexes, so when we see an access
            point, we can map it to the right variable in our query to the
            model.
        :param interface: The name of a wireless interface that is in monitor
            mode.
        :returns: Never returns.  Runs in an infinite loop until you kill it.
    """
    access_points = []
    count = 0
    with sp.Popen(["./run_fingerprint.bash", interface],
                  stdout=sp.PIPE) as proc:
        while True:
            line = proc.stdout.readline().decode().strip()
            if line == "-fingerprint-":
                datapoint = generate_datapoint(access_points, ap_indexes)
                room = model.predict([datapoint])
                sys.stdout.write("%s %d\r" % (room[0], count))
                count += 1
                access_points = []
            else:
                parts = line.split()
                if len(parts) != 2:
                    print("malformed line:", line)
                    continue
                access_points.append(parts)


def main(args):
    """
        The entry point for the guesser.
    """

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
    data, rooms = generate_training_data(ap_indexes)

    # pass the data into Perceptron/NaiveBayes
    print("Training model")
    model = train_model(data, rooms)
    print("Finished training model")

    # run run_fingerprint and guess the correct room.
    run_predictor(model, ap_indexes, args.interface)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("interface",
                        help="A wireless interface in monitor mode")
    args = parser.parse_args()
    main(args)
