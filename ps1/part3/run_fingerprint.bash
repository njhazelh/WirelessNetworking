#! /bin/bash

function run() {
	local interface=$1
	local room=$2

	tshark -i "$interface" -a duration:10 -X lua_script:record_beacons.lua 2>/dev/null |
		grep -oE $'[abcdef1234567890:]*\t[[:digit:]]*\t-?[[:digit:]]*$' |
		./parse_beacons.py > "fingerprints/$room"

	echo "Wifi fingerprint generated in file: fingerprints/$room"
}

run "$1" "$2"
