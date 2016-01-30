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


# def reduce_lines(points):
#     info = {}
#     for p in points:
#         bssid = b.bssid
#         bssid_beacons = info.get(bssid) or {}
#         bssid_beacons_channel = bssid_beacons.get(b.channel) or []
#         bssid_beacons_channel.append(b)
#         bssid_beacons[b.channel] = bssid_beacons_channel
#         info[b.bssid] = bssid_beacons

#     avg_beacons = []
#     for ssid, network in info.items():
#         for channel, beacons in network.items():
#             dbms = [int(b.dbm) for b in beacons if b.dbm != "nil"]
#             avg_dbm = sum(dbms) / len(dbms)
#             avg_beacons.append(
#                 Beacon(beacons[0].bssid, beacons[0].channel, avg_dbm,
#                        beacons[0].freq, beacons[0].ssid))

#     return avg_beacons


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
