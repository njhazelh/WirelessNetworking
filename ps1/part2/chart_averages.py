#! /usr/bin/env python3

import matplotlib.pyplot as plt
import sys
import collections
import math

Point = collections.namedtuple("Point", "channel dbm freq avg")
# used to keep the amount of graphed data reasonable; the csv's can get very large
dBms = []

# pull out the relevant info from the lua script output
def split_line(line):
    parts = line.strip().split("\t")
    # alert and skip lines that got cut off (too few/incorrect parts) 
    # as well as skip extra stats from the same signal strength
    if len(parts) != 4 or "" in parts or "nil" in parts or parts[3] in dBms:
        print("csv formatting bad")
        return None
    dBms.append(parts[3])
    return Point(channel=parts[0],
                 dbm=parts[1],
                 freq=parts[2],
                 avg=parts[3])

# basic i/o to read in the csv
def read_lines():
    points = []
    for line in sys.stdin.readlines():
        b = split_line(line)
        if b is None:
            continue
        points.append(b)
    return points

# change call in main to output a scatter chart instead
def make_scatter_chart(points):
    data = [(b.dbm, b.avg) for b in points]
    plt.figure(figsize=(15, 10), dpi=100)
    plt.title("Average packets per second by RSSI")
    plt.xlabel("dBm")
    plt.ylabel("Average packets per second")
    # zip = [(x, y), (x, y) ...] to [(x, x, ...), (y, y, ...)]
    plt.scatter(*zip(*data))
    plt.savefig("averages_scatter.png")

# make a histogram 
def make_chart(points):
    # pull out the packet average and cast as a num
    data = [float(b.avg) for b in points]
    plt.figure(figsize=(15, 10), dpi=100)
    plt.title("Average packets per second")
    plt.xlabel("Average packets per second")
    plt.ylabel("Occurrences")
    # use 30 bins so the data isn't overwhelming
    plt.hist(data, 30)
    plt.savefig("averages_histogram.png")

# process the file and plot the data
def main():
    points = read_lines()
    make_chart(points)


if __name__ == "__main__":
    main()
