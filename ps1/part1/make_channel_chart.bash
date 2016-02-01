#! /bin/bash

function main() {
	local interface=$1

	echo "Generating channel chart..."
	tshark -i "$interface" \
		-X lua_script:record_beacons_tshark.lua \
		-a duration:5 \
		-Y "http" 2>/dev/null |
		./channel_chart.py
	echo "Chart generated"
}

main $@
