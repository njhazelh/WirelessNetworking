#! /usr/bin/env python3

import matplotlib
import sys
import collections

Beacon = collections.namedtuple("Beacon", "bssid channel dbm freq ssid")


def split_line(line):
    parts = line.split("\t")
    return Beacon(bssid=parts[0],
                  channel=parts[1],
                  dbm=parts[2],
                  freq=parts[3],
                  ssid=parts[4])


def read_lines():
    return (split_line(line) for line in sys.stdin.readlines())


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
    for n in info:
        print(n)


def save_chart(chart):
    pass


def main():
    beacons = read_lines()
    info = reduce_lines(beacons)
    chart = make_chart(info)
    save_chart(chart)


if __name__ == "__main__":
    main()
