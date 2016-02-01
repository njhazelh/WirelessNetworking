#! /bin/bash

function main() {
    local interface=$1

    if [ "$(id -u)" != "0" ]; then
        echo "This script must be run as root" 1>&2
        exit 1
    fi

    function cleanup() {
        ifconfig "$interface" down
        iwconfig "$interface" mode Managed
        ifup "$interface" >/dev/null
        echo -e "\rWireless interface $interface restarted"
        echo "Check 'iwconfig' if problems seen"
        exit 0
   }

    trap cleanup SIGINT SIGTERM

    ifdown "$interface"
    ifconfig "$interface" down
    iwconfig "$interface" mode Monitor
    ifconfig "$interface" up
    ./cycle_channels_linux.bash "$interface"
}

main "$1"
