#! /bin/env python3

from collections import defaultdict, namedtuple
import fileinput
from operator import itemgetter

Beacon = namedtuple("Beacon", "bssid channel dbm")


def split_line(line):
    parts = line.strip().split("\t")
    if len(parts) != 3 or "" in parts or "nil" in parts:
        return None
    return Beacon(bssid=parts[0],
                  channel=int(parts[1]),
                  dbm=int(parts[2]))


def print_states(states):
    ap_states = []
    for bssid, rssi in states.items():
        ap_states.append((bssid, rssi))

    sorted_states = sorted(ap_states, key=itemgetter(0))

    for s in sorted_states:
        print(s[0], s[1])


def main():
    states = defaultdict(int)
    for line in fileinput.input():
        b = split_line(line)
        if b is None:
            continue
        s = states[b.bssid]
        if s == 0:
            states[b.bssid] = b.dbm
        else:
            states[b.bssid] += b.dbm
            states[b.bssid] /= 2.0
        print_states(states)
        print("-fingerprint-")

if __name__ == "__main__":
    main()
