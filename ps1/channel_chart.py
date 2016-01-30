#! /usr/bin/env python3

import matplotlib
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
    for n in info:
        print(n)
    data = np.array([b.channel for b in info])
    N = len(data)
    labels = ['point{0}'.format(i) for i in range(N)]
    plt.subplots_adjust(bottom = 0.1)
    plt.scatter(
        data[:, 0], data[:, 1], marker = 'o', c = data[:, 2], s = data[:, 3]*1500,
        cmap = plt.get_cmap('Spectral'))
    for label, x, y in zip(labels, data[:, 0], data[:, 1]):
        plt.annotate(
            label,
            xy = (x, y), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    plt.show()



def save_chart(chart):
    pass


def main():
    beacons = read_lines()
    info = reduce_lines(beacons)
    chart = make_chart(info)
    save_chart(chart)


if __name__ == "__main__":
    main()
