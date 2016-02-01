#! /bin/bash

# This function is used for generating a fingerprint of a room.
# It runs tshark for 10 minutes to generate datapoints from the lua script.
# These datapoints are written to the fingerprints directory within this
# folder.  If the folder doesn't exist, it should be created.
#
# -Y "http" is useful because it kills the output from tshark, so we can avoid
# using grep too much.
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


# This function is mostly used for debugging.
# -Y "http" is useful because it kills the output from tshark, so we can avoid
# using grep too much.
function run_stdout() {
	local interface=$1

	tshark -i "$interface" \
		-Y "http" \
		-X lua_script:record_beacons.lua |
		./parse_beacons.py
}

# The first argument of this script is the wireless interface to listen on.
# This interface should already be in monitor mode, and cycling through wifi
# channels. See scripts in the project root for guidance in setting this up.
#
# The second argument is the name of the room to fingerprint.  This argument
# is optional, but if it is ommited, the script will not generate a fingerprint
# file. Instead, it will write to stdout.
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
