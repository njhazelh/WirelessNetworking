#! /usr/bin/env python3

import matplotlib.pyplot as plt
import sys
import collections
import math

Point = collections.namedtuple("Point", "channel dbm freq avg")
dBms = []


def split_line(line):
    parts = line.strip().split("\t")
    if len(parts) != 4 or "" in parts or "nil" in parts or parts[3] in dBms:
        print("csv formatting bad")
        return None
    dBms.append(parts[3])
    return Point(channel=parts[0],
                 dbm=parts[1],
                 freq=parts[2],
                 avg=parts[3])


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
    plt.scatter(*zip(*data))
    plt.savefig("averages_scatter.png")


def make_chart(points):
    data = [float(b.avg) for b in points]
    plt.figure(figsize=(15, 10), dpi=100)
    plt.title("Average packets per second")
    plt.xlabel("Average packets per second")
    plt.ylabel("Occurrences")
    plt.hist(data, 30)
    plt.savefig("averages_histogram.png")


def main():
    points = read_lines()
    make_chart(points)


if __name__ == "__main__":
    main()
