#! /bin/env python3

from collections import defaultdict, namedtuple
import fileinput
from datetime import datetime, timedelta
import sys

Beacon = namedtuple("Beacon", "bssid dbm")


def split_line(line):
    parts = line.strip().split("\t")
    if len(parts) != 2 or "" in parts or "nil" in parts:
        # print("malformed line '%s'" % (line))
        return None
    return Beacon(bssid=parts[0], dbm=int(parts[1]))


def print_states(states):
    for bssid, rssi in states.items():
        sys.stdout.write("%s %d\n" % (bssid, rssi))
    sys.stdout.write("-fingerprint-\n")
    sys.stdout.flush()


def main():
    states = defaultdict(int)
    int_start = datetime.now()
    int_states = defaultdict(int)
    for line in fileinput.input():
        b = split_line(line)
        if b is None:
            continue
        s = int_states[b.bssid]
        if s == 0:
            int_states[b.bssid] = b.dbm
        else:
            int_states[b.bssid] = b.dbm * .8 + s * .2

        if int_start + timedelta(milliseconds=1200) < datetime.now():
            for key, rssi in int_states.items():
                states[key] = rssi
            for key, rssi in states.items():
                if key not in int_states:
                    states[key] = states[key] / 2.0
            states = {key: states[key] for key in states
                      if abs(states[key]) > 10}
            print_states(states)
            int_start = datetime.now()
            int_states = defaultdict(int)


if __name__ == "__main__":
    main()
