#! /bin/bash

function run() {
	local interface=$1
	local room=$2

	tshark -i "$interface" -X lua_script:record_beacons.lua 2>/dev/null | \
		grep -oE $'[abcdef1234567890:]*\t[[:digit:]]*\t-?[[:digit:]]*$' |
		./parse_beacons.py > "$room"
}

run "$1" "$2"
