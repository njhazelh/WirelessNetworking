#! /bin/bash

function run() {
	local interface=$1
	local room=$2

	# create fingerprints dir if it doesn't exist
	[ -d fingerprints ] || mkdir fingerprints

	tshark -i "$interface" \
		-a duration:600 \
		-Y "http" \
		-X lua_script:record_beacons.lua |
		./parse_beacons.py > "fingerprints/$room"

	echo "Wifi fingerprint generated in file: fingerprints/$room"
}


function run_stdout() {
	local interface=$1

	tshark -i "$interface" \
		-Y "http" \
		-X lua_script:record_beacons.lua |
		./parse_beacons.py
}


function main() {
	local interface=$1
	local room=$2

	if [[ -z "$2" ]]; then
		run_stdout "$interface"
	else
		run "$interface" "$room"
	fi
}

main $@
