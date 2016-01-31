#! /bin/env python3

from collections import defaultdict, namedtuple
import fileinput
from operator import itemgetter
from datetime import datetime, timedelta
import sys

Beacon = namedtuple("Beacon", "bssid channel dbm")


def split_line(line):
    parts = line.strip().split("\t")
    if len(parts) != 3 or "" in parts or "nil" in parts:
        return None
    return Beacon(bssid=parts[0], channel=int(parts[1]), dbm=int(parts[2]))


def print_states(states):
    ap_states = []
    for bssid, rssi in states.items():
        ap_states.append((bssid, rssi))

    sorted_states = sorted(ap_states, key=itemgetter(0))

    for s in sorted_states:
        print(s[0], s[1])
    print("-fingerprint-")
    sys.stdout.flush()


def main():
    states = defaultdict(int)
    int_start = datetime.now()
    for line in fileinput.input():
        b = split_line(line)
        if b is None:
            continue
        states[b.bssid] = b.dbm
        if int_start + timedelta(milliseconds=100) < datetime.now():
            print_states(states)
            int_start = datetime.now()
            states = defaultdict(int)


if __name__ == "__main__":
    main()
