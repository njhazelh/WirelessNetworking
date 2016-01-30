#! /bin/bash

# Run using `sudo ./cycle_channels_linux.bash <interface>`

function cycle() {
    local interface=$1
    local channel=$2
    echo -en "\rrunning on channel $channel "
    iwconfig "$interface" channel "$channel" >/dev/null
    sleep 0.05 # 100ms
    wait "$pid" 2>/dev/null
}

function main() {
    local interface=$1
    local c

    if [ "$(id -u)" != "0" ]; then
        echo "This script must be run as root" 1>&2
        exit 1
    fi

    while true
    do
        for c in $(seq 1 13)
        do
            cycle "$interface" $c
        done
    done
}

main $1
