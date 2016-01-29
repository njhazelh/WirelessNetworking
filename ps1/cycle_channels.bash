#! /bin/bash

export PATH="$PATH:/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources"

function cycle() {
    local interface=$1
    local channel=$2
    echo "starting channel $channel"
    airport "$interface" sniff "$channel" >/dev/null 2>/dev/null &
    local pid=$!
    sleep 0.2 # 200ms
    echo "killing channel $channel"
    kill -9 "$pid" >/dev/null 2>/dev/null
    wait "$pid" 2>/dev/null
    rm /tmp/airportSniff*.cap
}

function main() {
    local interface=$1
    local c

    while true
    do
        for c in $(seq 1 13)
        do
            cycle "$interface" $c
        done
    done
}

main $1
