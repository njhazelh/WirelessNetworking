#! /usr/bin/env python3

import matplotlib.pyplot as plt
import sys
import collections
import numpy as np

Beacon = collections.namedtuple("Beacon", "bssid channel dbm freq ssid")


def split_line(line):
    parts = line.strip().split("\t")
    if len(parts) != 5 or "" in parts or "nil" in parts:
        return None
    return Beacon(bssid=parts[0],
                  channel=parts[1],
                  dbm=parts[2],
                  freq=parts[3],
                  ssid=parts[4])


def read_lines():
    beacons = []
    for line in sys.stdin.readlines():
        b = split_line(line)
        if b is None:
            continue
        beacons.append(b)
    return beacons


def reduce_lines(beacons):
    info = {}
    for b in beacons:
        bssid = b.bssid
        bssid_beacons = info.get(bssid) or {}
        bssid_beacons_channel = bssid_beacons.get(b.channel) or []
        bssid_beacons_channel.append(b)
        bssid_beacons[b.channel] = bssid_beacons_channel
        info[b.bssid] = bssid_beacons

    avg_beacons = []
    for ssid, network in info.items():
        for channel, beacons in network.items():
            dbms = [int(b.dbm) for b in beacons if b.dbm != "nil"]
            avg_dbm = sum(dbms) / len(dbms)
            avg_beacons.append(
                Beacon(beacons[0].bssid, beacons[0].channel, avg_dbm,
                       beacons[0].freq, beacons[0].ssid))

    return avg_beacons


def make_chart(info):
    info = sorted(info, key=lambda x: int(x.channel))
    data = np.array([(b.channel, b.dbm) for b in info])
    plt.figure(figsize=(15, 10), dpi=100)
    plt.title("2.4Ghz Access Points")
    plt.rc('font', family='arial', weight='normal', size=8)
    labels = [b.ssid for b in info]
    plt.subplots_adjust(bottom=0.1)
    plt.scatter(
        data[:, 0], data[:, 1], marker='o', cmap=plt.get_cmap('Spectral'))
    for label, x, y in zip(labels, data[:, 0], data[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(-5, -5),
                     textcoords='offset points', ha='right', va='bottom')
    plt.savefig("channels.png")


def main():
    beacons = read_lines()
    info = reduce_lines(beacons)
    chart = make_chart(info)


if __name__ == "__main__":
    main()
